from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

class VerificationLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField()
    scanned_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.order.order_id} - {self.is_valid}"
