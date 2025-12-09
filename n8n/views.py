from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import AuthenticationFailed

from django.db import transaction
from django.db.models import Q

import os
import ast
import re
import json

from n8n.models import Customer, Channel, State, Parish, Zone, Location, Municipality


class BulkCustomerImportView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        token_req = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
        # if token_req != os.getenv("TOKEN_N8N"):
        # if token_req != '2laDoLyGMvjW0lTq6Qzhl3hpy79qiYG3CdXwCS5wWfU':
        if token_req is None:
            raise AuthenticationFailed(f"Token inválido para importación {token_req} token")

    def post(self, request):
        raw = request.body.decode("utf-8").strip().split("\n")
        # print(raw)

        registros = []

        # Parsear cada línea, que puede ser una lista con un string JSON o dict JSON directo
        for r in raw:
            # Descomponer: intentar como lista con un string JSON, o como un dict directamente
            lista_json_str = None
            has_error = False
            if not r.strip():
                continue
            try:
                lista_json_str = ast.literal_eval(r)
                if isinstance(lista_json_str, list):
                    for inner_json_str in lista_json_str:
                        try:
                            data = json.loads(inner_json_str)
                            if "output" in data:
                                for obj in data["output"]:
                                    if "json" in obj:
                                        registros.append(obj["json"])
                        except Exception as e:
                            print(f"Error en json.loads: {str(e)}")
                            has_error = True
                            continue
                else:
                    raise ValueError("Output no es lista")
            except Exception as e:
                try:
                    data = json.loads(r)
                    if "output" in data:
                        for obj in data["output"]:
                            if "json" in obj:
                                registros.append(obj["json"])
                except Exception as exc2:
                    print(f"Error en decode de línea: {str(e)} | luego json.loads dio: {str(exc2)}")
                    continue

        results = {"created": 0, "updated": 0, "errors": []}

        # ================================
        # 2. Cache de valores únicos
        # ================================
        canales = set()
        estados = set()
        parroquias = set()
        municipios = set()
        zonas_texto = set()
        locations_raw = set()
        odoo_ids = []

        for item in registros:
            canales.add(item["Canal de Consumo"].strip())
            estados.add(item.get("Estado", "sin datos").strip().replace("(VE)", "").strip())

            parroquia = item.get("Parroquia")
            if parroquia is None or parroquia.strip() == "":
                parroquia = "vacio"
            else:
                parroquia = parroquia.strip()
            if parroquia:
                parroquias.add(parroquia)

            zona_raw = item.get("Zona", "").strip()
            zonas_texto.add(zona_raw)

            # Municipios: llenar también con vacio si null o vacio (si existe campo Municipio)
            municipio = item.get("Municipio")
            if municipio is None or (isinstance(municipio, str) and municipio.strip() == ""):
                municipio = "vacio"
            else:
                municipio = municipio.strip() if isinstance(municipio, str) else municipio
            item["Municipio"] = municipio
            if municipio:
                municipios.add(municipio)

            lat = item.get("Geo latitud")
            lon = item.get("Geo longitud")
            if lat not in [None, ""] and lon not in [None, ""]:
                try:
                    lat = float(lat)
                    lon = float(lon)
                    locations_raw.add((lat, lon))
                except:
                    pass
            else: 
                try:
                    lat = 0.0
                    lon = 0.0
                    locations_raw.add(lat, lon)
                except:
                    pass
                
            # Clientes Odoo
            try:
                odoo_ids.append(int(item["ID"]))
            except:
                pass

        # ================================
        # 3. Pre-carga de registros existentes y creación de faltantes
        # ================================

        # Channel
        canales_db = {c.channel_name: c for c in Channel.objects.filter(channel_name__in=canales)}
        # Crear faltantes
        Channel.objects.bulk_create(
            [Channel(channel_name=n) for n in canales if n not in canales_db],
            ignore_conflicts=True
        )
        canales_db = {c.channel_name: c for c in Channel.objects.filter(channel_name__in=canales)}

        # State
        estados_db = {e.estado_name: e for e in State.objects.filter(estado_name__in=estados)}
        State.objects.bulk_create(
            [State(estado_name=n) for n in estados if n not in estados_db],
            ignore_conflicts=True
        )
        estados_db = {e.estado_name: e for e in State.objects.filter(estado_name__in=estados)}

        # Parish
        parroquias_db = {p.parroquia_name: p for p in Parish.objects.filter(parroquia_name__in=parroquias)}
        Parish.objects.bulk_create(
            [Parish(parroquia_name=n) for n in parroquias if n not in parroquias_db],
            ignore_conflicts=True
        )
        parroquias_db = {p.parroquia_name: p for p in Parish.objects.filter(parroquia_name__in=parroquias)}

        # Municipality - corregido el ciclo de creación
        municipality_db = {m.municipality_name: m for m in Municipality.objects.filter(municipality_name__in=municipios)}
        Municipality.objects.bulk_create(
            [Municipality(municipality_name=m) for m in municipios if m not in municipality_db],
            ignore_conflicts=True
        )
        municipality_db = {m.municipality_name: m for m in Municipality.objects.filter(municipality_name__in=municipios)}

        # Zone
        zonas_limpias = {}
        for z in zonas_texto:
            m = re.match(r"\[(\d+)\]\s*(.+)", z)
            zonas_limpias[z] = m.group(2).strip() if m else z.strip()

        zonas_finales = set(zonas_limpias.values())
        zonas_db = {z.zone_name: z for z in Zone.objects.filter(zone_name__in=zonas_finales)}
        Zone.objects.bulk_create(
            [Zone(zone_name=n) for n in zonas_finales if n not in zonas_db],
            ignore_conflicts=True
        )
        zonas_db = {z.zone_name: z for z in Zone.objects.filter(zone_name__in=zonas_finales)}

        # Location: cargar existentes
        locations_db = {}
        for loc in Location.objects.all():
            key = (
                loc.lat,
                loc.lon,
                loc.zone_id if hasattr(loc, "zone_id") else None,
                loc.state_id if hasattr(loc, "state_id") else None,
                loc.municipality_id if hasattr(loc, 'municipality_id') else None,
                loc.parish_id if hasattr(loc, "parish_id") else None,
            )
            locations_db[key] = loc

        # ================================
        # 4. Cargar clientes existentes
        # ================================
        existentes = {
            c.odoo_id: c for c in Customer.objects.filter(odoo_id__in=odoo_ids)
        }

        para_crear = []
        para_actualizar = []

        # ================================
        # 5. Procesamiento masivo
        # ================================
        for item in registros:
            try:
                # Canal
                canal_name = item["Canal de Consumo"].strip()
                canal = canales_db[canal_name]

                # Estado
                estado_name = item.get("Estado", "vacio").strip().replace("(VE)", "").strip()
                estado = estados_db.get(estado_name)

                # Municipio
                municipio_name = item.get("Municipio")
                if municipio_name is None or (isinstance(municipio_name, str) and municipio_name.strip() == ""):
                    municipio_name = "vacio"
                else:
                    municipio_name = municipio_name.strip() if isinstance(municipio_name, str) else municipio_name
                item["Municipio"] = municipio_name
                municipio = municipality_db.get(municipio_name) if municipio_name else None

                # Parroquia
                parroquia_name = item.get("Parroquia")
                if parroquia_name is None or parroquia_name.strip() == "":
                    parroquia_name = "vacio"
                else:
                    parroquia_name = parroquia_name.strip()
                parroquia = parroquias_db.get(parroquia_name) if parroquia_name else None

                # Zona
                zona_raw = item.get("Zona", "vacio").strip()
                zona_name = zonas_limpias[zona_raw]
                zona = zonas_db.get(zona_name)

                # Location
                lat = item.get("Geo latitud")
                lon = item.get("Geo longitud")
                location = None
                if lat not in [None, ""] and lon not in [None, ""]:
                    try:
                        lat = float(lat)
                        lon = float(lon)
                        key = (
                            lat,
                            lon,
                            zona.id if zona else None,
                            estado.id if estado else None,
                            municipio.id if municipio else None,
                            parroquia.id if parroquia else None
                        )
                        if key not in locations_db:
                            new_loc = Location(
                                lat=lat,
                                lon=lon,
                                zone=zona,
                                state=estado,
                                municipality=municipio,
                                parish=parroquia
                            )
                            new_loc.save()
                            locations_db[key] = new_loc

                        location = locations_db[key]
                    except:
                        location = None
                # Si location no es válida, y hay partes de location con None, seguimos con location en None

                # Campos cliente
                oid = int(item["ID"])
                rif = item.get("RIF", "").strip()
                full_name = item.get("Completar nombre", "").strip().strip('"')

                # Update / Create
                if oid in existentes:
                    c = existentes[oid]
                    c.rif = rif
                    c.name = full_name
                    c.location = location
                    c.channel = canal
                    para_actualizar.append(c)
                else:
                    para_crear.append(
                        Customer(
                            odoo_id=oid,
                            rif=rif,
                            name=full_name,
                            location=location,
                            channel=canal
                        )
                    )
            except Exception as e:
                results["errors"].append({"error": str(e), "data": item})

        # ================================
        # 6. Bulk Create + Bulk Update
        # ================================
        if para_crear:
            Customer.objects.bulk_create(para_crear, batch_size=2000)
            results["created"] = len(para_crear)

        if para_actualizar:
            Customer.objects.bulk_update(
                para_actualizar,
                ["rif", "name", "location", "channel"],
                batch_size=2000
            )
            results["updated"] = len(para_actualizar)

        # ================================
        # 7. Respuesta final
        # ================================
        return Response(results, status=status.HTTP_200_OK)
