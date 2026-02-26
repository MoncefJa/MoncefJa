using EFacture.BlazorApp.Data;
using EFacture.BlazorApp.Security;
using EFacture.BlazorApp.Services;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorComponents().AddInteractiveServerComponents();
builder.Services.AddSingleton<InMemoryStore>();
builder.Services.AddScoped<EInvoiceService>();
builder.Services.AddScoped<JwtTokenService>();

var jwtKey = builder.Configuration["Jwt:Key"] ?? "dev-ultra-secret-key-change-me";
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = false,
            ValidateAudience = false,
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtKey))
        };
    });

builder.Services.AddAuthorization();

var app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();

app.MapRazorComponents<App>().AddInteractiveServerRenderMode();

app.MapPost("/api/auth/token", (LoginRequest req, JwtTokenService jwt) =>
{
    var role = req.Username == "admin" ? "Admin" : "User";
    return Results.Ok(new { access_token = jwt.Generate(req.Username, role) });
});

app.MapGet("/api/companies", (InMemoryStore store) => Results.Ok(store.Companies));
app.MapPost("/api/companies", (Company company, InMemoryStore store) =>
{
    store.Companies.Add(company with { Id = Guid.NewGuid() });
    return Results.Created($"/api/companies/{company.Id}", company);
});

app.MapGet("/api/invoices", (InMemoryStore store) => Results.Ok(store.Invoices));
app.MapPost("/api/invoices", (Invoice invoice, InMemoryStore store) =>
{
    store.Invoices.Add(invoice with { Id = Guid.NewGuid(), Status = InvoiceStatus.Draft });
    return Results.Created($"/api/invoices/{invoice.Id}", invoice);
});

app.MapPost("/api/invoices/{id:guid}/submit", (Guid id, InMemoryStore store, EInvoiceService service) =>
{
    var invoice = store.Invoices.FirstOrDefault(x => x.Id == id);
    if (invoice is null) return Results.NotFound();

    var submission = service.Submit(invoice);
    store.Submissions.Add(submission);
    store.AuditLogs.Add(new AuditLog(Guid.NewGuid(), "INVOICE_SUBMITTED", $"Invoice:{invoice.Number}", DateTimeOffset.UtcNow));

    var status = submission.Status == "ACCEPTED" ? InvoiceStatus.Accepted : InvoiceStatus.Rejected;
    store.ReplaceInvoice(invoice with { Status = status });

    return Results.Ok(submission);
});

app.MapGet("/api/submissions", (InMemoryStore store) => Results.Ok(store.Submissions));
app.MapPost("/api/mock-government/receive", () => Results.Ok(new { status = "ACCEPTED", reference = $"MOCK-{Guid.NewGuid():N}" }));

app.Run();

public record LoginRequest(string Username, string Password);
