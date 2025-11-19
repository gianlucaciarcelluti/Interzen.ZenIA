# TROUBLESHOOTING - MS13-SECURITY

## 1. Keycloak non raggiungibile
- Verifica pod e service:
  ```bash
  kubectl get pods -l app=ms13-security
  kubectl get svc ms13-security
  ```
- Controlla i log:
  ```bash
  kubectl logs -l app=ms13-security
  ```
- Test connessione da un pod:
  ```bash
  kubectl exec -it <pod> -- curl -k https://ms13-security:8443/auth/realms/zenia
  ```

## 2. Login falliti o errori OAuth2
- Verifica configurazione client/realm
- Controlla log Keycloak
- Verifica policy password, brute force

## 3. Performance bassa
- Verifica metriche Prometheus (login/sec, errori)
- Controlla saturazione CPU/memoria
- Verifica slowlog DB

## 4. Errori di autenticazione
- Controlla Secret e password
- Verifica mapping ruoli/utenti

## 5. Alert monitoraggio
- Consulta dashboard Grafana
- Verifica alert su login, errori, brute force

---

**Vedi anche**: [README.md](./README.md) | [SPECIFICATION.md](./SPECIFICATION.md) | [API.md](./API.md) | [DATABASE-SCHEMA.md](./DATABASE-SCHEMA.md)