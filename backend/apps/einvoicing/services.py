import base64
import hashlib
import uuid
import xml.etree.ElementTree as ET

from apps.invoicing.models import Invoice


def generate_invoice_xml(invoice: Invoice) -> str:
    root = ET.Element("EInvoice")
    ET.SubElement(root, "InvoiceNumber").text = invoice.number
    ET.SubElement(root, "Type").text = invoice.invoice_type
    ET.SubElement(root, "IssueDate").text = str(invoice.issue_date)
    ET.SubElement(root, "CustomerName").text = invoice.customer_name
    ET.SubElement(root, "TaxTotal").text = str(invoice.vat_amount)
    ET.SubElement(root, "StampDuty").text = str(invoice.stamp_duty)
    ET.SubElement(root, "Total").text = str(invoice.total)

    lines_el = ET.SubElement(root, "Lines")
    for line in invoice.lines.all():
        line_el = ET.SubElement(lines_el, "Line")
        ET.SubElement(line_el, "Description").text = line.description
        ET.SubElement(line_el, "Quantity").text = str(line.quantity)
        ET.SubElement(line_el, "UnitPrice").text = str(line.unit_price)
        ET.SubElement(line_el, "VATRate").text = str(line.vat_rate)
        ET.SubElement(line_el, "LineTotal").text = str(line.line_total)

    return ET.tostring(root, encoding="unicode")


def sign_invoice_xml(xml_payload: str, certificate_text: str) -> str:
    raw = f"{xml_payload}:{certificate_text or 'mock-cert'}".encode()
    digest = hashlib.sha256(raw).digest()
    return base64.b64encode(digest).decode()


def generate_qr_data(invoice: Invoice, signature: str) -> str:
    token = f"{invoice.number}|{invoice.total}|{signature[:16]}"
    return base64.b64encode(token.encode()).decode()


def mock_send_to_government(_payload: str) -> tuple[str, str]:
    reference = f"TN-{uuid.uuid4().hex[:12].upper()}"
    return "ACCEPTED", reference
