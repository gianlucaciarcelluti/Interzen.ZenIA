# DATABASE-SCHEMA - MS14-AUDIT

## Modello Dati Principale (Elasticsearch)

### Indice: `zenia-audit-logs-*`

```json
{
  "timestamp": "2025-11-19T10:15:00Z",
  "user": "utente1",
  "ip": "192.168.1.10",
  "action": "LOGIN",
  "resource": "MS11-API-GATEWAY",
  "outcome": "SUCCESS",
  "details": {"browser": "Chrome"},
  "signature": "SHA256:...",
  "ingest_id": "uuid"
}
```

- **timestamp**: Data/ora evento
- **user**: Utente coinvolto
- **ip**: Indirizzo IP sorgente
- **action**: Azione (LOGIN, LOGOUT, CREATE, UPDATE, DELETE, ...)
- **resource**: Risorsa coinvolta
- **outcome**: SUCCESS/FAILURE
- **details**: Info aggiuntive (browser, device, ...)
- **signature**: Firma digitale evento
- **ingest_id**: UUID ingestione

## Retention & Replica
- Retention default: 12 mesi
- Replica: 2+ (cluster Elasticsearch)
- Backup: snapshot periodici

## Altri Indici
- `zenia-audit-alerts-*` (eventi critici)
- `zenia-audit-export-*` (esportazioni)
