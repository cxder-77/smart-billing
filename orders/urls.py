from django.urls import path
from .views import create_order, generate_master_qr

urlpatterns = [
    path("create/", create_order),
    path("qr/<uuid:order_id>/", generate_master_qr),
]
