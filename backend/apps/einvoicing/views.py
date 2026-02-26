from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit.models import AuditLog
from apps.invoicing.models import Invoice

from .models import InvoiceSubmission
from .serializers import InvoiceSubmissionSerializer
from .services import generate_invoice_xml, generate_qr_data, mock_send_to_government, sign_invoice_xml


class InvoiceSubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InvoiceSubmissionSerializer

    def get_queryset(self):
        return InvoiceSubmission.objects.filter(invoice__company__owner=self.request.user)

    @action(detail=False, methods=["post"], url_path="submit/(?P<invoice_id>[^/.]+)")
    def submit(self, request, invoice_id=None):
        invoice = Invoice.objects.get(id=invoice_id, company__owner=request.user)
        xml_payload = generate_invoice_xml(invoice)
        signature = sign_invoice_xml(xml_payload, invoice.company.signature_certificate)
        qr_data = generate_qr_data(invoice, signature)
        gov_status, gov_ref = mock_send_to_government(xml_payload)

        submission, _ = InvoiceSubmission.objects.update_or_create(
            invoice=invoice,
            defaults={
                "xml_payload": xml_payload,
                "signature": signature,
                "qr_code_data": qr_data,
                "status": gov_status,
                "government_reference": gov_ref,
                "response_message": "Processed by mock API",
            },
        )
        invoice.status = gov_status
        invoice.save(update_fields=["status"])

        AuditLog.objects.create(
            user=request.user,
            action="INVOICE_SUBMITTED",
            target=f"Invoice#{invoice.id}",
            metadata={"government_reference": gov_ref, "status": gov_status},
        )

        return Response(self.get_serializer(submission).data, status=status.HTTP_201_CREATED)


class MockGovernmentAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({"status": "ACCEPTED", "reference": "MOCK-STATE-123"})
