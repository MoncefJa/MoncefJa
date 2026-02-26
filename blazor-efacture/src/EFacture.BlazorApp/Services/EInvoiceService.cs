using System.Security.Cryptography;
using System.Text;
using System.Xml.Linq;

namespace EFacture.BlazorApp.Services;

public class EInvoiceService
{
    public Submission Submit(Invoice invoice)
    {
        var xml = GenerateXml(invoice);
        var signature = Sign(xml, "mock-cert");
        var qr = GenerateQr(invoice, signature);
        var govRef = $"TN-{Guid.NewGuid():N}"[..15].ToUpperInvariant();

        return new Submission(
            Guid.NewGuid(),
            invoice.Id,
            xml,
            signature,
            qr,
            govRef,
            "ACCEPTED",
            DateTimeOffset.UtcNow
        );
    }

    public string GenerateXml(Invoice invoice)
    {
        var doc = new XDocument(
            new XElement("EInvoice",
                new XElement("InvoiceNumber", invoice.Number),
                new XElement("Type", invoice.Type.ToString()),
                new XElement("IssueDate", invoice.IssueDate.ToString("yyyy-MM-dd")),
                new XElement("CustomerName", invoice.CustomerName),
                new XElement("TaxTotal", invoice.VatAmount),
                new XElement("StampDuty", invoice.StampDuty),
                new XElement("Total", invoice.Total),
                new XElement("Lines",
                    invoice.Lines.Select(l => new XElement("Line",
                        new XElement("Description", l.Description),
                        new XElement("Quantity", l.Quantity),
                        new XElement("UnitPrice", l.UnitPrice),
                        new XElement("VatRate", l.VatRate),
                        new XElement("LineTotal", l.LineTotal)
                    ))
                )
            )
        );

        return doc.ToString(SaveOptions.DisableFormatting);
    }

    public string Sign(string xmlPayload, string certificate)
    {
        var bytes = Encoding.UTF8.GetBytes($"{xmlPayload}:{certificate}");
        var hash = SHA256.HashData(bytes);
        return Convert.ToBase64String(hash);
    }

    public string GenerateQr(Invoice invoice, string signature)
    {
        var content = $"{invoice.Number}|{invoice.Total}|{signature[..16]}";
        return Convert.ToBase64String(Encoding.UTF8.GetBytes(content));
    }
}
