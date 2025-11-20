# SPECIFICATION - MS13-SECURITY

## 1. Descrizione tecnica
MS13-SECURITY implementa un Identity Provider centralizzato (Keycloak) per autenticazione, autorizzazione e gestione identità. Supporta OAuth2, OIDC, SAML, RBAC, MFA e policy di sicurezza avanzate.

## 2. Stack tecnologico
- Keycloak 23.x (HA)
- PostgreSQL 15.x (StatefulSet)
- Redis 7.x (sessioni)
- Kubernetes Deployment/StatefulSet
- Prometheus Keycloak Exporter

## 3. Configurazione
- **Keycloak**: 2+ pod, TLS, realm ZenIA
- **Database**: PostgreSQL, persistence
- **Sessioni**: Redis, persistence
- **Sicurezza**: TLS, password policy, brute force
- **Configurazione**: ConfigMap/Secret
- **Service**: ClusterIP, Ingress per Keycloak

## 4. Policy di autenticazione
- OAuth2 (Authorization Code, Client Credentials, Implicit, PKCE)
- OpenID Connect (ID Token, UserInfo)
- SAML 2.0
- MFA (OTP, WebAuthn)
- Password rotation, brute force detection

## 5. Policy di autorizzazione
- RBAC: ruoli, gruppi, permessi
- Policy per microservizio, scope, claim
- Mapping ruoli/attributi

## 6. Monitoraggio e logging
- Prometheus Keycloak Exporter
- Alert Grafana: login, errori, brute force
- Audit log: accessi, modifiche utenti, policy

## Gestione Errori

### Scenari di Errore Comuni

1. **Timeout Query**
   - Descrizione: Query supera tempo limite di esecuzione
   - Causa: Query complessa o dati voluminosi
   - Mitigation: Implementare timeout configurabile e fallback

2. **Connessione Database**
   - Descrizione: Perdita connessione ai servizi dipendenti
   - Causa: Servizio non disponibile o problemi rete
   - Mitigation: Retry logic con exponential backoff

3. **Validazione Dati**
   - Descrizione: Input non valido o formato errato
   - Causa: Client fornisce dati non conformi
   - Mitigation: Validazione input e error messages chiari

### Error Codes

| Code | Status | Descrizione | Azione |
|------|--------|-------------|--------|
| 400 | Bad Request | Input non valido | Correggi parametri request |
| 408 | Timeout | Operazione timeout | Riprova con parametri ridotti |
| 500 | Internal Error | Errore interno | Contatta supporto |
| 503 | Service Unavailable | Servizio non disponibile | Riprova più tardi |

### Recovery Procedures

- **Automatic Retry**: Sistema riprova automaticamente con backoff esponenziale
- **Graceful Degradation**: Fallback a cache o risultati parziali se disponibili
- **Error Logging**: Tutti gli errori registrati per analisi e monitoring
- **Alerting**: Notifiche su errori critici ai team di supporto

## 7. Performance
- Latenza < 100ms autenticazione
- Throughput > 1000 login/min
- Failover < 10s (Keycloak HA)

---

**Vedi anche**: [README.md](./README.md) | [API.md](./API.md) | [DATABASE-SCHEMA.md](./DATABASE-SCHEMA.md) | [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
