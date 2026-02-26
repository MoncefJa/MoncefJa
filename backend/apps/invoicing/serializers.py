from rest_framework import serializers

from .models import Invoice, InvoiceLine


class InvoiceLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLine
        fields = ("id", "description", "quantity", "unit_price", "vat_rate", "line_total")


class InvoiceSerializer(serializers.ModelSerializer):
    lines = InvoiceLineSerializer(many=True)

    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ("status", "created_at")

    def create(self, validated_data):
        lines_data = validated_data.pop("lines", [])
        invoice = Invoice.objects.create(**validated_data)
        for line in lines_data:
            InvoiceLine.objects.create(invoice=invoice, **line)
        return invoice
