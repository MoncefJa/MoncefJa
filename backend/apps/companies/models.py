from django.conf import settings
from django.db import models


class Company(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="companies")
    name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=32, unique=True)
    vat_number = models.CharField(max_length=32)
    trade_register = models.CharField(max_length=32)
    address = models.TextField()
    vat_rate_default = models.DecimalField(max_digits=5, decimal_places=2, default=19)
    signature_certificate = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
