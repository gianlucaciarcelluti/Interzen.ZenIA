# DATABASE-SCHEMA - MS16-REGISTRY

## Modello Dati Principale (PostgreSQL)

### Tabella: `services`

| Campo        | Tipo         | Note                        |
|--------------|--------------|-----------------------------|
| id           | SERIAL       | PK                          |
| name         | VARCHAR      | Nome servizio               |
| address      | VARCHAR      | IP/hostname                 |
| port         | INT          | Porta                       |
| tags         | TEXT[]       | Tag servizio                |
| health_url   | VARCHAR      | Endpoint health             |
| status       | VARCHAR      | healthy/unhealthy           |
| registered_at| TIMESTAMP    | Data registrazione          |
| updated_at   | TIMESTAMP    | Ultima modifica             |

### Tabella: `service_audit`

| Campo        | Tipo         | Note                        |
|--------------|--------------|-----------------------------|
| id           | SERIAL       | PK                          |
| service_id   | INT          | FK -> services.id           |
| action       | VARCHAR      | register, deregister, check |
| user         | VARCHAR      | Utente                      |
| timestamp    | TIMESTAMP    | Data evento                 |
| details      | JSONB        | Dettagli evento             |

## Retention & Backup
- Retention default: 12 mesi
- Backup: dump periodici

## Altre Tabelle
- `service_events` (notifiche push)
