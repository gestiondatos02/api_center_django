from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from odoo_budgets.serializers import BranchesSerializer
from .models import Companies, Branches, States, Zones, CustomerType, SalesChannel, Sellers, Location, Customer, Brands, Lines, MeasurementLines, Measurements, Articles, Orders, Dispatches, DocumentType, DocumentStatus, Documents, DocumentsDetail

class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = ['id', 'name', 'rif']
        
class BrancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branches
        fields = ['id', 'name']
        
class StatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = ['id', 'name']
        
class ZonesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zones
        fields = ['id', 'name']
        
class CustomerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerType
        fields = ['id', 'name']
        
class SalesChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesChannel
        fields = ['id', 'name']
        
class SellersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sellers
        fields = ['id', 'seller_code', 'seller_name', 'supervisor_name']
        
class LocationSerializer(serializers.ModelSerializer):
    zone = ZonesSerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    
    class Meta:
        model = Location
        fields = ['id', 'zone', 'state']
        
class CustomerSerializer(serializers.ModelSerializer):
    customer_type = CustomerTypeSerializer(read_only=True)
    customer_location = LocationSerializer(read_only = True)
    customer_channel = SalesChannelSerializer(read_only = True)
    
    class Meta:
        models = Customer
        fields = ['id', 'customer_id', 'customer_rif', 'customer_name', 'customer_type', 'customer_location', 'customer_channel']
        
class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ['id', 'brand_name', 'secondary_name', 'third_name']
        
class LinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lines
        fields = ['id', 'line_name', 'secondary_name']
        
class MeasurementLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementLines
        fields = ['id', 'name']
        
class MeasurementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurements
        fields = ['id', 'name']
        
class ArticlesSerializer(serializers.ModelSerializer):
    brand = BrandsSerializer(read_only = True)
    line = LinesSerializer(read_only = True)
    measurement_line = MeasurementLinesSerializer(read_only = True)
    measurement = MeasurementsSerializer(read_only = True)
    
    class Meta:
        model = Articles
        fields = ['id', 'sku', 'article_name', 'brand', 'line', 'measurement_line', 'measurements']
        
class OrdersSerializer(serializers.ModelSerializer):
    article = ArticlesSerializer(read_only = True)
    customer = CustomerSerializer(read_only = True)
    seller = SellersSerializer(read_only = True)
    
    class Meta:
        model = Orders
        fields = ['id', 'article', 'order_number', 'order_date', 'customer', 'seller']
        
class DispatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatches
        fields = ['id', 'dispatch_number', 'consolidation_date']
        
class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name']
        
class DocumentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentStatus
        fields = ['id', 'name']
        
class DocumentsDetailSerializer(serializers.ModelSerializer):
    dispatch = DispatchesSerializer(read_only=True)
    order = OrdersSerializer(read_only=True)
    company = CompaniesSerializer(read_only = True)
    branch = BranchesSerializer(read_only=True)
    
    class Meta:
        model = DocumentsDetail
        fields = ['id', 'dispatch', 'order', 'company', 'branch', 'quantity_sacks', 'quantity_packages', 'weigth', 'anulated_weigth', 'total_weigth', 'detal_price', 'sku_amount', 'discount_percentage', 'discount', 'total_tax', 'net_total', 'discount_percentage', 'discount_dollars', 'total_dcto', 'quantity_sacks_secondary', 'boxes', 'activation', 'NC_concept', 'rif_doc']

class DocumentsSerializer(serializers.ModelSerializer):
    document_type = DocumentTypeSerializer(read_only = True)
    document_status = DocumentStatusSerializer(read_only=True)
    document_detail = DocumentsDetailSerializer(read_only = True)
    
    class Meta:
        model = Documents
        fields = ['id', 'document_type', 'document_number', 'document_date', 'document_status', 'control_number', 'document_detail']