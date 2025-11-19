# Configurazioni Kubernetes per MS08-MONITOR

Questa directory contiene le configurazioni Kubernetes per il deployment di MS08-MONITOR in ambiente di produzione.

## File Inclusi

- `deployment.yaml`: Deployment principale del servizio monitor
- `service.yaml`: Service per esposizione API
- `configmap.yaml`: Configurazioni applicative
- `secret.yaml`: Secrets per credenziali
- `network-policy.yaml`: Policy di rete
- `hpa.yaml`: Horizontal Pod Autoscaler
- `pdb.yaml`: Pod Disruption Budget
- `service-monitor.yaml`: ServiceMonitor per Prometheus
- `ingress.yaml`: Ingress per accesso esterno