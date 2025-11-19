# DATABASE-SCHEMA - MS15-CONFIG

## Modello Dati Principale (PostgreSQL)

### Tabella: `configurations`

| Campo        | Tipo         | Note                        |
|--------------|--------------|-----------------------------|
| id           | SERIAL       | PK                          |
| service      | VARCHAR      | Nome microservizio          |
| version      | INT          | Versione config             |
| config       | JSONB        | Configurazione              |
| note         | TEXT         | Note modifica               |
| updated_at   | TIMESTAMP    | Data modifica               |
| updated_by   | VARCHAR      | Utente                      |

### Tabella: `config_audit`

| Campo        | Tipo         | Note                        |
|--------------|--------------|-----------------------------|
| id           | SERIAL       | PK                          |
| config_id    | INT          | FK -> configurations.id     |
| action       | VARCHAR      | update, rollback            |
| user         | VARCHAR      | Utente                      |
| timestamp    | TIMESTAMP    | Data evento                 |
| details      | JSONB        | Dettagli evento             |

## Retention & Backup
- Retention default: 24 mesi
- Backup: dump periodici

## Altre Tabelle
- `config_events` (notifiche push)
