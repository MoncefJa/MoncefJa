from django.db import models

from apps.companies.models import Company


class Invoice(models.Model):
    class InvoiceType(models.TextChoices):
        B2B = "B2B", "B2B"
        B2C = "B2C", "B2C"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Brouillon"
        SUBMITTED = "SUBMITTED", "Soumise"
        ACCEPTED = "ACCEPTED", "Acceptée"
        REJECTED = "REJECTED", "Rejetée"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="invoices")
    number = models.CharField(max_length=30)
    invoice_type = models.CharField(max_length=5, choices=InvoiceType.choices)
    customer_name = models.CharField(max_length=255)
    customer_tax_id = models.CharField(max_length=64, blank=True)
    issue_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=3)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=3)
    stamp_duty = models.DecimalField(max_digits=12, decimal_places=3, default=1.000)
    total = models.DecimalField(max_digits=12, decimal_places=3)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT)
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("company", "number")


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="lines")
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=3)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=3)
