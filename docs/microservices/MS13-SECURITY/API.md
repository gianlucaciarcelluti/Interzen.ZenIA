# API - MS13-SECURITY

## API Keycloak (standard)
MS13-SECURITY espone le API standard di Keycloak:
- /auth/realms/zenia/protocol/openid-connect/token
- /auth/realms/zenia/protocol/openid-connect/userinfo
- /auth/realms/zenia/protocol/openid-connect/logout
- /auth/realms/zenia/account
- /auth/admin/realms/zenia/users
- /auth/admin/realms/zenia/roles

## Esempi di utilizzo

### 1. OAuth2 Token Request
```http
POST /auth/realms/zenia/protocol/openid-connect/token
Content-Type: application/x-www-form-urlencoded

grant_type=password&client_id=frontend&username=alice&password=secret
```
Risposta:
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "expires_in": 300,
  "token_type": "Bearer"
}
```

### 2. UserInfo
```http
GET /auth/realms/zenia/protocol/openid-connect/userinfo
Authorization: Bearer <access_token>
```
Risposta:
```json
{
  "sub": "user-id",
  "name": "Alice",
  "email": "alice@example.com",
  "roles": ["user", "admin"]
}
```

### 3. Admin API - Crea utente
```http
POST /auth/admin/realms/zenia/users
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "username": "bob",
  "email": "bob@example.com",
  "enabled": true,
  "credentials": [{"type": "password", "value": "secret"}]
}
```

## Sicurezza API
- Solo accesso autenticato (token)
- RBAC su endpoint admin
- TLS obbligatorio
- Audit log per operazioni critiche

---

**Vedi anche**: [README.md](./README.md) | [SPECIFICATION.md](./SPECIFICATION.md) | [DATABASE-SCHEMA.md](./DATABASE-SCHEMA.md) | [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
