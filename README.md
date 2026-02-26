# SaaS e-Facturation Tunisie (MVP)

Application SaaS d'e-facturation conforme (MVP) pour PME/TPE/freelances/cabinets comptables.

## Stack
- Backend: Django + DRF + JWT
- Frontend: React + TypeScript (Vite)
- DB: PostgreSQL
- Conteneurs: Docker Compose

## Démarrage
```bash
docker compose up --build
```
- API: http://localhost:8000/api/
- Frontend: http://localhost:5173

## Endpoints principaux
- `POST /api/auth/token/`
- `GET/POST /api/companies/`
- `GET/POST /api/invoices/`
- `POST /api/submissions/submit/{invoice_id}/`
- `POST /api/mock-government/receive/`

## Parcours MVP
1. Créer un utilisateur admin Django.
2. Créer une société (données fiscales + certificat mock).
3. Créer une facture B2B/B2C avec lignes.
4. Soumettre la facture via endpoint submission.
5. Récupérer le statut, la référence, l'XML et la signature.

## Conformité et sécurité (MVP)
- Auth JWT + rôles.
- Filtrage multi-tenant par utilisateur propriétaire.
- Journal d'audit des soumissions.
- Archivage de payload XML/signature/retour gouvernemental.
- Rétention légale configurable via `LEGAL_ARCHIVE_RETENTION_YEARS`.

## Documentation architecture
- Voir `docs/architecture.md`.
