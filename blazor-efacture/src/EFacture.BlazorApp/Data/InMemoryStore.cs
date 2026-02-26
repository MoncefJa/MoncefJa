namespace EFacture.BlazorApp.Data;

public class InMemoryStore
{
    public List<Company> Companies { get; } =
    [
        new(Guid.NewGuid(), "Demo SARL", "1234567A", "TVA123", "RC999", 19m, "mock-cert")
    ];

    public List<Invoice> Invoices { get; } =
    [
        new(
            Guid.NewGuid(),
            Guid.Empty,
            "FAC-2026-001",
            InvoiceType.B2B,
            "Client Test",
            "TAX-CLIENT",
            DateOnly.FromDateTime(DateTime.Today),
            100m,
            19m,
            1m,
            120m,
            InvoiceStatus.Draft,
            [new InvoiceLine("Service", 1, 100, 19)]
        )
    ];

    public List<Submission> Submissions { get; } = [];
    public List<AuditLog> AuditLogs { get; } = [];

    public void ReplaceInvoice(Invoice updated)
    {
        var idx = Invoices.FindIndex(i => i.Id == updated.Id);
        if (idx >= 0) Invoices[idx] = updated;
    }
}
