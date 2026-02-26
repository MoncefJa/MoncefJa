from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("tax_id", models.CharField(max_length=32, unique=True)),
                ("vat_number", models.CharField(max_length=32)),
                ("trade_register", models.CharField(max_length=32)),
                ("address", models.TextField()),
                ("vat_rate_default", models.DecimalField(decimal_places=2, default=19, max_digits=5)),
                ("signature_certificate", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="companies", to=settings.AUTH_USER_MODEL)),
            ],
        )
    ]
