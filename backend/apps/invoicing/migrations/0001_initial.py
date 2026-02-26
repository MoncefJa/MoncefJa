from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("companies", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.CharField(max_length=30)),
                ("invoice_type", models.CharField(choices=[("B2B", "B2B"), ("B2C", "B2C")], max_length=5)),
                ("customer_name", models.CharField(max_length=255)),
                ("customer_tax_id", models.CharField(blank=True, max_length=64)),
                ("issue_date", models.DateField()),
                ("due_date", models.DateField(blank=True, null=True)),
                ("subtotal", models.DecimalField(decimal_places=3, max_digits=12)),
                ("vat_amount", models.DecimalField(decimal_places=3, max_digits=12)),
                ("stamp_duty", models.DecimalField(decimal_places=3, default=1.0, max_digits=12)),
                ("total", models.DecimalField(decimal_places=3, max_digits=12)),
                ("status", models.CharField(choices=[("DRAFT", "Brouillon"), ("SUBMITTED", "Soumise"), ("ACCEPTED", "Acceptée"), ("REJECTED", "Rejetée")], default="DRAFT", max_length=12)),
                ("is_recurring", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="invoices", to="companies.company")),
            ],
            options={"unique_together": {("company", "number")}},
        ),
        migrations.CreateModel(
            name="InvoiceLine",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.CharField(max_length=255)),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=10)),
                ("unit_price", models.DecimalField(decimal_places=3, max_digits=10)),
                ("vat_rate", models.DecimalField(decimal_places=2, max_digits=5)),
                ("line_total", models.DecimalField(decimal_places=3, max_digits=12)),
                ("invoice", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lines", to="invoicing.invoice")),
            ],
        ),
    ]
