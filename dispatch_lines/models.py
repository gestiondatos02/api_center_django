from email.policy import default
from django import dispatch
from django.db import models

class Companies(models.Model):
    name = models.CharField(("Nombre"), max_length=200, default="not company")#empresa
    rif = models.CharField(("Rif"), max_length=50, null=False)#rif empresa

class Branches(models.Model):
    name = models.CharField(("Nombre de sucursal"), max_length=100, default="not branch") #sucursal

class States(models.Model):
    name = models.CharField(("Nombre de estado"), max_length=50, default="not state") #eestado geografico

class Zones(models.Model):
    name = models.CharField(("Nombre de zona"), max_length=100, default="not zone") #zona geografica
    
class CustomerType(models.Model):
    name = models.CharField(("Tipo de cliente"), max_length=200, default="not customer_type") #tipo de cliente

class SalesChannel(models.Model):
    name = models.CharField(("Canal de consumo"), max_length=50, default="not sales channel") #canal de consumo
    
class Sellers(models.Model):
    seller_code = models.CharField(("Codigo de vendedor"), max_length=50, null=False) #codigo vendedro
    seller_name = models.CharField(("Nombre de vendedor"), max_length=100, default="not seller name") #nombre dvendedor 
    supervisor_name = models.CharField(("Nombre de supervisor"), max_length=100, default= "not supervisor name") #supervisor
 
class Location(models.Model):
    zone = models.ForeignKey("Zones", on_delete=models.CASCADE, null=True, blank=True) #tabla many to many de estado y zona#####################3
    state = models.ForeignKey("States", on_delete=models.CASCADE, null=True, blank=True)
   
class Customer(models.Model):
    customer_id = models.IntegerField(("ID de cliente"), null=False) #id cliente
    customer_rif = models.CharField(("Rif cliente"), max_length=50) #rif cliente
    customer_name = models.CharField(("Nombre de vendedor"), max_length=100) #nombre de cliente
    customer_type = models.ForeignKey("CustomerType", on_delete=models.CASCADE, null=True, blank=True) #fk de tipo de cliente
    customer_location = models.ForeignKey("Location", on_delete=models.CASCADE, null=True, blank=True) #fk de many to many de estado y zona
    customer_channel = models.ForeignKey("SalesChannel", on_delete=models.CASCADE, null=True, blank=True)

class Brands(models.Model):
    brand_name = models.CharField(("Marca principal"), max_length=50) #marca
    secondary_name = models.CharField(("Marca secundaria"), max_length = 50) #marca 2
    third_name = models.CharField(("Marca tercera"), max_length=50, default="not third name") #marca 1
    
class Lines(models.Model):
    line_name = models.CharField(("Linea principal"), max_length=50)
    secondary_name = models.CharField(("Linea secundaria"), max_length=50) #linea 3
    
class MeasurementLines(models.Model):
    name = models.CharField(("Linea de presentacion"), max_length=50) # 0 aparece con el nombre 0

class Measurements(models.Model):
    name = models.CharField(("Medidas de presentacion"), max_length=100) # medidas de presentacion
    
class Articles(models.Model):
    sku = models.CharField(("Sku"),max_length=100, default="not sku")
    article_name = models.CharField(("Nombre de articulo"), max_length=100, default="not article name")
    brand = models.ForeignKey("Brands", on_delete=models.CASCADE, null=True, blank=True) #fk de marca
    line = models.ForeignKey("Lines", on_delete=models.CASCADE, null=True, blank=True) #fk
    measurement_line = models.ForeignKey("MeasurementLines", on_delete=models.CASCADE, null=True, blank=True) #fk
    measurements = models.ForeignKey("Measurements", on_delete=models.CASCADE, null=True, blank=True) #fk
    
    
class Orders(models.Model):
    article = models.ForeignKey("Articles", on_delete=models.CASCADE, null=True, blank=True) #articulo
    order_number = models.CharField(("Nro de pedido"), max_length = 50) #numero de pedido
    order_date = models.CharField(("Fecha de la orden"), max_length=50) #fecha de pedido
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, null=True, blank=True)
    seller = models.ForeignKey("Sellers", on_delete=models.CASCADE, null=True, blank=True)
    
class Dispatches(models.Model):
    dispatch_number = models.CharField("Despacho", max_length=50) #despacho
    consolidation_date = models.CharField("Fecha consolidacion de carga", max_length=50) #fecha consolidacion de carga

class DocumentType(models.Model):
    name = models.CharField(("Tipo de documento"), max_length=200, default="not document type") #tpo de documento
    
class DocumentStatus(models.Model):
    name = models.CharField(("Estado del documento"), max_length=100, default="not state name") #estatus de documento    
    
class Documents(models.Model):
    document_type = models.ForeignKey("DocumentType", on_delete=models.CASCADE, null=True, blank=True) #fk
    document_number = models.CharField(("Nro documento"), max_length=70) #numero de documento
    document_date = models.CharField(("Fecha dcmto"), max_length=50) #fecha de documento
    document_status = models.ForeignKey("DocumentStatus", on_delete=models.CASCADE, null=True, blank=True) #fk
    control_number = models.CharField(("Nro de control"), max_length=70) #nummero de control
    document_detail = models.ForeignKey("DocumentsDetail", on_delete=models.CASCADE, null=True, blank=True) #fk    
    
class DocumentsDetail(models.Model):
    dispatch = models.ForeignKey("Dispatches", on_delete=models.CASCADE, null=True, blank=True) #fk
    order = models.ForeignKey("Orders", on_delete=models.CASCADE, null=True, blank=True) #fk
    company = models.ForeignKey("Companies", on_delete=models.CASCADE, null=True, blank=True) #fk
    branch = models.ForeignKey("Branches", on_delete=models.CASCADE, null=True, blank=True) #fk
    quantity_sacks = models.IntegerField()
    quantity_packages = models.IntegerField()
    weigth = models.FloatField()
    anulated_weigth = models.FloatField()
    total_weigth = models.FloatField()
    detal_price = models.FloatField()
    sku_amount = models.FloatField()
    discount_percentage = models.FloatField()
    discount = models.FloatField()
    total_tax = models.FloatField()
    net_total = models.FloatField()
    discount_percentage = models.FloatField()
    discount_dollars = models.FloatField()
    total_dcto = models.FloatField()
    quantity_sacks_secondary = models.IntegerField()
    boxes = models.FloatField()
    activation = models.IntegerField()
    NC_concept = models.CharField()
    rif_doc = models.CharField()