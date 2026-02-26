# EFacture Tunisie SaaS — Version Blazor

Ce dossier contient un **second projet séparé** basé sur **Blazor Server (.NET 8)** pour répondre à votre demande.

## Stack
- Frontend + Backend: ASP.NET Core Blazor Server
- Auth: JWT + API Key interne (mock)
- DB: PostgreSQL (EF Core prévu)
- API: REST minimal APIs
- Conteneurs: Docker

## Lancer (en environnement .NET)
```bash
cd blazor-efacture/src/EFacture.BlazorApp
dotnet restore
dotnet run
```

## Fonctionnalités MVP incluses
- Multi-tenant logique via `CompanyId`.
- Rôles `Admin`, `Accountant`, `User`.
- Factures B2B/B2C avec TVA + timbre.
- Génération XML e-facture.
- Signature électronique mock (SHA256 + Base64).
- QR payload.
- Soumission vers API gouvernementale mock.
- Journal d'audit.
- Archivage (en mémoire pour MVP, stockage DB à brancher).

## Endpoints
- `POST /api/auth/token`
- `GET /api/companies`
- `POST /api/companies`
- `GET /api/invoices`
- `POST /api/invoices`
- `POST /api/invoices/{id}/submit`
- `GET /api/submissions`
- `POST /api/mock-government/receive`

## Notes
- Ce projet est prêt pour extension vers EF Core + PostgreSQL réel.
- L'intégration officielle API État + certificat réel est mockée dans cette version.
