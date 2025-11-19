# MS16-REGISTRY - Deployment Kubernetes

> **Manifest Kubernetes per Registry e Service Discovery**

[![PostgreSQL](https://img.shields.io/badge/postgresql-%23336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=flat&logo=kubernetes&logoColor=white)](https://kubernetes.io)

## 🎯 Overview Deployment

Questa directory contiene i manifest Kubernetes per il deployment di **MS16-REGISTRY** (API, PostgreSQL, Redis, Exporter) in ambiente containerizzato.

### Componenti Deployati

| Componente         | Tipo         | Replica | Descrizione                |
|--------------------|--------------|---------|----------------------------|
| Registry API       | Deployment   | 2+      | API REST/gRPC registry     |
| PostgreSQL         | StatefulSet  | 1       | Storage servizi            |
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
kubectl wait --for=condition=ready pod -l app=ms16-registry-db --timeout=300s

# 4. Deploy Redis
kubectl apply -f redis-statefulset.yaml
kubectl wait --for=condition=ready pod -l app=ms16-registry-redis --timeout=300s

# 5. Deploy Registry API
kubectl apply -f registry-api-deployment.yaml
kubectl wait --for=condition=ready pod -l app=ms16-registry-api --timeout=300s

# 6. Deploy Exporter
kubectl apply -f registry-exporter.yaml

# 7. Verifica deployment
kubectl get pods -n zenia
kubectl get svc -n zenia
```

### Verifica Installazione

```bash
# Test API
kubectl port-forward svc/ms16-registry-api 8080:8080
curl http://localhost:8080/api/registry/services

# Test DB
kubectl exec -it <pod> -- psql -h ms16-registry-db -U registry -d registry

# Test Redis
kubectl exec -it <pod> -- redis-cli -h ms16-registry-redis -a <password> ping

# Metriche Prometheus
kubectl port-forward svc/ms16-registry-exporter 8081:8081
curl http://localhost:8081/metrics
```

## 📁 Struttura Manifest

```
kubernetes/
├── README.md
├── configmap.yaml
├── secrets.yaml
├── registry-api-deployment.yaml
├── postgresql-statefulset.yaml
├── redis-statefulset.yaml
├── registry-exporter.yaml
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
# registry-api-deployment.yaml
env:
  - name: JWT_SECRET
    valueFrom:
      secretKeyRef:
        name: ms16-registry-secrets
        key: jwt-secret
  - name: DB_URL
    value: postgresql://registry:$(DB_PASSWORD)@ms16-registry-db:5432/registry
  - name: REDIS_URL
    value: redis://:$(REDIS_PASSWORD)@ms16-registry-redis:6379/0
  - name: SERVICE_RETENTION_DAYS
    value: "365"
```

### ConfigMap API

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ms16-registry-config
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
  name: ms16-registry-secrets
  namespace: zenia
type: Opaque
data:
  jwt-secret: c2VjdXJlX2p3dF9rZXk=  # secure_jwt_key (base64)
  db-user: cmVnaXN0cnk=  # registry (base64)
  db-password: c2VjdXJlX2RiX3B3  # secure_db_pw (base64)
  redis-password: c2VjdXJlX3JlZGlzX3B3  # secure_redis_pw (base64)
  tls-cert: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0t  # Certificato (base64)
  tls-key: LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0t  # Chiave privata (base64)
```

## 🏗️ Architettura Deployment

```mermaid
graph TB
    subgraph "Kubernetes Cluster"
        API1[Registry API Pod 1]
        API2[Registry API Pod 2]
        DB[PostgreSQL]
        REDIS[Redis]
        EXPORTER[Registry Exporter]
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
  name: ms16-registry-netpol
  namespace: zenia
spec:
  podSelector:
    matchLabels:
      app: ms16-registry-api
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
  name: ms16-registry-api-monitor
  namespace: zenia
spec:
  selector:
    matchLabels:
      app: ms16-registry-exporter
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
  name: ms16-registry-api-alerts
  namespace: zenia
spec:
  groups:
  - name: ms16-registry-api
    rules:
    - alert: RegistryApiDown
      expr: up{job="ms16-registry-api"} == 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Registry API is down"
        description: "Registry API non raggiungibile da oltre 5 minuti."
    - alert: RegistryHealthErrors
      expr: increase(registry_health_error_total[5m]) > 5
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Errori health check"
        description: "Errori health check > 5 in 5m."
```

## 🔄 Aggiornamenti e Rollback

### Rolling Update

```bash
kubectl rollout restart deployment/ms16-registry-api
```

### Backup e Restore

- Dump automatico PostgreSQL
- Restore tramite volume mount

## 🐛 Troubleshooting

Vedi [TROUBLESHOUTING.md](../TROUBLESHOUTING.md)

---

**Documentazione correlata**: [README.md](../README.md) | [SPECIFICATION.md](../SPECIFICATION.md) | [API.md](../API.md)
