# TROUBLESHOUTING - MS12-CACHE

## 1. Redis non raggiungibile
- Verifica pod e service:
  ```bash
  kubectl get pods -l app=ms12-cache
  kubectl get svc ms12-cache
  ```
- Controlla i log:
  ```bash
  kubectl logs -l app=ms12-cache
  ```
- Test connessione da un pod:
  ```bash
  kubectl exec -it <pod> -- redis-cli -h ms12-cache -a <password> ping
  ```

## 2. Failover non funziona
- Verifica stato Sentinel:
  ```bash
  kubectl get pods -l app=ms12-cache-sentinel
  kubectl logs -l app=ms12-cache-sentinel
  ```
- Controlla configurazione quorum e monitor

## 3. Performance bassa
- Verifica metriche Prometheus (latency, ops/sec)
- Controlla saturazione CPU/memoria
- Verifica slowlog Redis

## 4. Errori di autenticazione
- Controlla Secret e password
- Verifica ACL e permessi

## 5. Alert monitoraggio
- Consulta dashboard Grafana
- Verifica alert su memoria, replica, connessioni

---

**Vedi anche**: [README.md](./README.md) | [SPECIFICATION.md](./SPECIFICATION.md) | [API.md](./API.md) | [DATABASE-SCHEMA.md](./DATABASE-SCHEMA.md)