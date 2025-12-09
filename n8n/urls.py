from django.urls import path
from .views import BulkCustomerImportView

urlpatterns = [
    path("n8n/create/", BulkCustomerImportView.as_view(), name="n8n-create")
]
