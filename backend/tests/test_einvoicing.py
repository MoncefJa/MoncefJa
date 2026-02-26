from datetime import date

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.companies.models import Company
from apps.invoicing.models import Invoice, InvoiceLine


@pytest.mark.django_db
def test_invoice_submission_flow():
    user = get_user_model().objects.create_user(username="admin", password="pass1234", role="ADMIN")
    company = Company.objects.create(
        owner=user,
        name="ACME",
        tax_id="123",
        vat_number="TVA123",
        trade_register="RC123",
        address="Tunis",
    )
    invoice = Invoice.objects.create(
        company=company,
        number="FAC-2026-001",
        invoice_type="B2B",
        customer_name="Client Test",
        issue_date=date.today(),
        subtotal=100,
        vat_amount=19,
        stamp_duty=1,
        total=120,
    )
    InvoiceLine.objects.create(
        invoice=invoice,
        description="Service",
        quantity=1,
        unit_price=100,
        vat_rate=19,
        line_total=119,
    )

    client = APIClient()
    resp = client.post("/api/auth/token/", {"username": "admin", "password": "pass1234"}, format="json")
    token = resp.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    submit_resp = client.post(f"/api/submissions/submit/{invoice.id}/")
    assert submit_resp.status_code == 201
    assert submit_resp.data["status"] == "ACCEPTED"
