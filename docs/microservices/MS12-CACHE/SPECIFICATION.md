# SPECIFICATION - MS12-CACHE

## 1. Descrizione tecnica
MS12-CACHE implementa un cluster Redis distribuito per caching, session management, rate limiting e Pub/Sub. Utilizza Redis Cluster per scalabilità e Redis Sentinel per alta disponibilità.

## 2. Stack tecnologico
- Redis 7.x (Cluster mode)
- Redis Sentinel
- Kubernetes StatefulSet/Deployment
- Prometheus Redis Exporter
- Helm Chart opzionale

## 3. Configurazione
- **Cluster**: 3+ nodi Redis, 3+ Sentinel
- **Persistence**: AOF + RDB
- **Sicurezza**: Password, ACL, TLS
- **Configurazione**: via ConfigMap/Secret
- **Service**: ClusterIP per Redis, LoadBalancer/NodePort opzionale

## 4. Pattern di caching supportati
- Cache-aside (read-through/write-through)
- Expiry/TTL per chiavi
- Session store (token, JWT, OAuth2)
- Rate limiting buckets
- Pub/Sub canali interni

## 5. Policy di sicurezza
- Accesso limitato a namespace ZenIA
- ACL per microservizi
- Password rotate periodica
- TLS obbligatorio tra pod

## 6. Monitoraggio e logging
- Prometheus Redis Exporter
- Alert Grafana: memoria, replica, connessioni
- Log audit accessi e comandi critici

## 7. Performance
- Latenza < 1ms per operazione locale
- Throughput > 100k ops/sec (cluster)
- Failover < 5s (Sentinel)

---

**Vedi anche**: [README.md](./README.md) | [API.md](./API.md) | [DATABASE-SCHEMA.md](./DATABASE-SCHEMA.md) | [TROUBLESHOUTING.md](./TROUBLESHOUTING.md)
