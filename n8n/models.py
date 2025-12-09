from django.db import models

class Zone(models.Model):
    zone_name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'mapa_clientes_zone'

    def __str__(self):
        return self.zone_name

class State(models.Model):
    estado_name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'mapa_clientes_state'

    def __str__(self):
        return self.estado_name

class Parish(models.Model):
    parroquia_name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'mapa_clientes_parish'

    def __str__(self):
        return self.parroquia_name
    
class Municipality(models.Model):
    municipality_name = models.CharField(max_length=255, unique=True)
    
    class Meta:
        db_table = 'mapa_clientes_municipality'
        
    def __str__(self):
        return self.municipality_name

class Location(models.Model):
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, db_column='zone_id'
    )
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, db_column='state_id'
    )
    parish = models.ForeignKey(
        Parish, on_delete=models.CASCADE, db_column='parish_id'
    )
    municipality = models.ForeignKey(
        Municipality, on_delete = models.CASCADE, db_column='municipality_id'
    )

    class Meta:
        db_table = 'mapa_clientes_location'

    def __str__(self):
        return f"{self.lat}, {self.lon}"

class Channel(models.Model):
    channel_name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'mapa_clientes_channels'

    def __str__(self):
        return self.channel_name

class Customer(models.Model):
    odoo_id = models.IntegerField(unique=True)
    rif = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, db_column='location_id'
    )
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, db_column='channel_id'
    )

    class Meta:
        db_table = 'mapa_clientes_customers'

    def __str__(self):
        return self.name
