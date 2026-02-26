from django.db import models

from apps.invoicing.models import Invoice


class InvoiceSubmission(models.Model):
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name="submission")
    xml_payload = models.TextField()
    signature = models.TextField()
    qr_code_data = models.TextField()
    government_reference = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=12, default="PENDING")
    response_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
