# DATABASE-SCHEMA - MS13-SECURITY

## PostgreSQL Structure

### 1. Tabelle principali
- `user_entity`: utenti
- `role_entity`: ruoli
- `user_role_mapping`: mapping utenti-ruoli
- `group_entity`: gruppi
- `user_group_membership`: mapping utenti-gruppi
- `credential`: credenziali
- `federated_identity`: identità federate
- `event_entity`: eventi/audit

### 2. Esempi di struttura
```sql
-- Utente
SELECT * FROM user_entity WHERE username = 'alice';

-- Ruoli
SELECT * FROM role_entity WHERE name = 'admin';

-- Mapping utenti-ruoli
SELECT * FROM user_role_mapping WHERE user_id = '...' AND role_id = '...';

-- Eventi di login
SELECT * FROM event_entity WHERE type = 'LOGIN';
```

### 3. Policy di retention
- Audit log: 1 anno
- Sessioni: 1h-24h
- Password: rotazione ogni 90 giorni

### 4. Sicurezza dati
- Password hashate (bcrypt/argon2)
- TLS obbligatorio
- Audit log per accessi e modifiche

---

**Vedi anche**: [README.md](./README.md) | [SPECIFICATION.md](./SPECIFICATION.md) | [API.md](./API.md) | [TROUBLESHOUTING.md](./TROUBLESHOUTING.md)
