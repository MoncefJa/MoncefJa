from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from apps.companies.models import Company
from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    filterset_fields = ["status", "company"]

    def get_queryset(self):
        return Invoice.objects.filter(company__owner=self.request.user).prefetch_related("lines")

    def perform_create(self, serializer):
        company: Company = serializer.validated_data["company"]
        if company.owner_id != self.request.user.id:
            raise PermissionDenied("Company does not belong to user")
        serializer.save()
