# Esempi d'Uso - MS13-SECURITY

Questa directory contiene esempi di payload, configurazioni e comandi per l'utilizzo di MS13-SECURITY (Keycloak).

## 1. Richiesta Token OAuth2
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

## 2. UserInfo
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

## 3. Admin API - Crea utente
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
