from rest_framework import serializers
from .models import Customer, Channel, State, Parish, Zone, Location, Municipality

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'channel_name']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'estado_name']

class ParishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parish
        fields = ['id', 'parroquia_name']

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'zone_name']

class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        field = ['id', 'municipality_name']

class LocationSerializer(serializers.ModelSerializer):
    zone = ZoneSerializer(read_only=True)
    state = StateSerializer(read_only=True)
    parish = ParishSerializer(read_only=True)
    municipality = MunicipalitySerializer(read_only=True)

    class Meta:
        model = Location
        fields = ['id', 'lat', 'lon', 'zone', 'state', 'parish', 'municipality']

class CustomerSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer(read_only=True)
    state = StateSerializer(read_only=True)
    parish = ParishSerializer(read_only=True)
    municipality = MunicipalitySerializer(read_only=True)
    zone = ZoneSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    odoo_id = serializers.CharField(source='odoo_id')
    rif = serializers.CharField(source='rif')
    full_name = serializers.CharField(source='full_name')

    class Meta:
        model = Customer
        fields = [
            'odoo_id',
            'rif',
            'full_name',
            'channel',
            'state',
            'municipality',
            'parish',
            'zone',
            'location'
        ]
