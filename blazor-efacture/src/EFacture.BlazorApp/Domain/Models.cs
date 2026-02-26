namespace EFacture.BlazorApp;

public enum InvoiceType { B2B, B2C }
public enum InvoiceStatus { Draft, Submitted, Accepted, Rejected }

public record Company(
    Guid Id,
    string Name,
    string TaxId,
    string VatNumber,
    string TradeRegister,
    decimal DefaultVatRate,
    string Certificate
);

public record InvoiceLine(string Description, decimal Quantity, decimal UnitPrice, decimal VatRate)
{
    public decimal LineTotal => Quantity * UnitPrice * (1 + (VatRate / 100m));
}

public record Invoice(
    Guid Id,
    Guid CompanyId,
    string Number,
    InvoiceType Type,
    string CustomerName,
    string? CustomerTaxId,
    DateOnly IssueDate,
    decimal Subtotal,
    decimal VatAmount,
    decimal StampDuty,
    decimal Total,
    InvoiceStatus Status,
    List<InvoiceLine> Lines
);

public record Submission(
    Guid Id,
    Guid InvoiceId,
    string XmlPayload,
    string Signature,
    string QrPayload,
    string GovernmentReference,
    string Status,
    DateTimeOffset SentAt
);

public record AuditLog(Guid Id, string Action, string Target, DateTimeOffset Timestamp);
