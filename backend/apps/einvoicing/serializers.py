from rest_framework import serializers

from .models import InvoiceSubmission


class InvoiceSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceSubmission
        fields = "__all__"
        read_only_fields = ("sent_at", "updated_at")
