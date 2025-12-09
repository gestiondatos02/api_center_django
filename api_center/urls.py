
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("n8n/", include('n8n.urls')),
    # path("dispatch_lines", include('dispatch_lines.urls')),
    # path("odoo_budget", include('odoo_budget.urls')),
]
