from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("invoicing", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="InvoiceSubmission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("xml_payload", models.TextField()),
                ("signature", models.TextField()),
                ("qr_code_data", models.TextField()),
                ("government_reference", models.CharField(blank=True, max_length=64)),
                ("status", models.CharField(default="PENDING", max_length=12)),
                ("response_message", models.TextField(blank=True)),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("invoice", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="submission", to="invoicing.invoice")),
            ],
        )
    ]
