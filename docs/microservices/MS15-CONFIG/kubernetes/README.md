# MS15-CONFIG - Deployment Kubernetes

> **Manifest Kubernetes per Configurazione centralizzata**

[![PostgreSQL](https://img.shields.io/badge/postgresql-%23336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=flat&logo=kubernetes&logoColor=white)](https://kubernetes.io)

## 🎯 Overview Deployment

Questa directory contiene i manifest Kubernetes per il deployment di **MS15-CONFIG** (API, PostgreSQL, Redis, Exporter) in ambiente containerizzato.

### Componenti Deployati

| Componente         | Tipo         | Replica | Descrizione                |
|--------------------|--------------|---------|----------------------------|
| Config API         | Deployment   | 2+      | API REST per config        |
| PostgreSQL         | StatefulSet  | 1       | Storage config/versioning  |
| Redis              | StatefulSet  | 1       | Cache/eventi               |
| ConfigMap          | ConfigMap    | -       | Configurazione API         |
| Secret             | Secret       | -       | Password, TLS, JWT         |
| Service            | ClusterIP    | -       | Accesso API/DB/Redis       |
| Prometheus Exporter| Deployment   | 1       | Metriche monitoring        |

## 🚀 Quick Start

### Prerequisiti
- Kubernetes 1.24+
- kubectl configurato
- Namespace `zenia` creato

### Deployment

```bash
# 1. Crea namespace
kubectl create namespace zenia

# 2. Applica configurazioni base
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml

# 3. Deploy PostgreSQL
kubectl apply -f postgresql-statefulset.yaml
kubectl wait --for=condition=ready pod -l app=ms15-config-db --timeout=300s

# 4. Deploy Redis
kubectl apply -f redis-statefulset.yaml
kubectl wait --for=condition=ready pod -l app=ms15-config-redis --timeout=300s

# 5. Deploy Config API
kubectl apply -f config-api-deployment.yaml
kubectl wait --for=condition=ready pod -l app=ms15-config-api --timeout=300s

# 6. Deploy Exporter
kubectl apply -f config-exporter.yaml

# 7. Verifica deployment
kubectl get pods -n zenia
kubectl get svc -n zenia
```

### Verifica Installazione

```bash
# Test API
kubectl port-forward svc/ms15-config-api 8080:8080
curl http://localhost:8080/api/config/MS11-API-GATEWAY

# Test DB
kubectl exec -it <pod> -- psql -h ms15-config-db -U config -d config

# Test Redis
kubectl exec -it <pod> -- redis-cli -h ms15-config-redis -a <password> ping

# Metriche Prometheus
kubectl port-forward svc/ms15-config-exporter 8081:8081
curl http://localhost:8081/metrics
```

## 📁 Struttura Manifest

```
kubernetes/
├── README.md
├── configmap.yaml
├── secrets.yaml
├── config-api-deployment.yaml
├── postgresql-statefulset.yaml
├── redis-statefulset.yaml
├── config-exporter.yaml
├── service.yaml
├── network-policies.yaml
├── hpa.yaml
├── pdb.yaml
├── monitoring/
│   ├── service-monitor.yaml
│   └── prometheus-rules.yaml
```

## 🔧 Configurazioni

### Environment Variables

```yaml
# config-api-deployment.yaml
env:
  - name: JWT_SECRET
    valueFrom:
      secretKeyRef:
        name: ms15-config-secrets
        key: jwt-secret
  - name: DB_URL
    value: postgresql://config:$(DB_PASSWORD)@ms15-config-db:5432/config
  - name: REDIS_URL
    value: redis://:$(REDIS_PASSWORD)@ms15-config-redis:6379/0
  - name: CONFIG_RETENTION_DAYS
    value: "730"
```

### ConfigMap API

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ms15-config-config
  namespace: zenia
data:
  app.conf: |
    ...
```

### Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ms15-config-secrets
  namespace: zenia
type: Opaque
data:
  jwt-secret: c2VjdXJlX2p3dF9rZXk=  # secure_jwt_key (base64)
  db-user: Y29uZmln  # config (base64)
  db-password: c2VjdXJlX2RiX3B3  # secure_db_pw (base64)
  redis-password: c2VjdXJlX3JlZGlzX3B3  # secure_redis_pw (base64)
  tls-cert: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0t  # Certificato (base64)
  tls-key: LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0t  # Chiave privata (base64)
```

## 🏗️ Architettura Deployment

```mermaid
graph TB
    subgraph "Kubernetes Cluster"
        API1[Config API Pod 1]
        API2[Config API Pod 2]
        DB[PostgreSQL]
        REDIS[Redis]
        EXPORTER[Config Exporter]
    end
    API1-->|Replica|API2
    API1-->|DB|DB
    API2-->|DB|DB
    API1-->|Cache/Eventi|REDIS
    API2-->|Cache/Eventi|REDIS
    EXPORTER-->|Metrics|API1
    EXPORTER-->|Metrics|API2
```

## 🔒 Sicurezza

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ms15-config-netpol
  namespace: zenia
spec:
  podSelector:
    matchLabels:
      app: ms15-config-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: zenia
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to: []
    ports:
    - protocol: TCP
      port: 5432
    - protocol: TCP
      port: 6379
    - protocol: TCP
      port: 53
```

## 📊 Monitoraggio

### Service Monitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ms15-config-api-monitor
  namespace: zenia
spec:
  selector:
    matchLabels:
      app: ms15-config-exporter
  endpoints:
  - port: metrics
    path: /metrics
    interval: 30s
    scrapeTimeout: 10s
```

### Prometheus Rules

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: ms15-config-api-alerts
  namespace: zenia
spec:
  groups:
  - name: ms15-config-api
    rules:
    - alert: ConfigApiDown
      expr: up{job="ms15-config-api"} == 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Config API is down"
        description: "Config API non raggiungibile da oltre 5 minuti."
    - alert: ConfigUpdateErrors
      expr: increase(config_update_error_total[5m]) > 5
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Errori update config"
        description: "Errori update config > 5 in 5m."
```

## 🔄 Aggiornamenti e Rollback

### Rolling Update

```bash
kubectl rollout restart deployment/ms15-config-api
```

### Backup e Restore

- Dump automatico PostgreSQL
- Restore tramite volume mount

## 🐛 Troubleshooting

Vedi [TROUBLESHOUTING.md](../TROUBLESHOUTING.md)

---

**Documentazione correlata**: [README.md](../README.md) | [SPECIFICATION.md](../SPECIFICATION.md) | [API.md](../API.md)
