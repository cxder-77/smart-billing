from django.urls import path
from .views import scan_add_to_cart

urlpatterns = [
    path('scan/', scan_add_to_cart),
]
