from django.urls import path
from .views import verify_qr

urlpatterns = [
    path("verify/", verify_qr),
]
