# MS04 - Validatore - API Reference

**Navigazione**: [← SPECIFICATION.md](SPECIFICATION.md) | [API](API.md) | [DATABASE-SCHEMA →](DATABASE-SCHEMA.md)

## Indice

1. [Panoramica API](#panoramica-api)
2. [Endpoint Validazione](#endpoint-validazione)
   - [POST /validate](#post-validate)
   - [POST /validate/async](#post-validateasync)
   - [GET /validation/{id}/status](#get-validationidstatus)
   - [GET /validation/{id}/report](#get-validationidreport)
3. [Endpoint Regole](#endpoint-regole)
   - [GET /rules](#get-rules)
   - [POST /rules](#post-rules)
   - [PUT /rules/{id}](#put-rulesid)
4. [Endpoint Certificati](#endpoint-certificati)
   - [GET /certificates/{id}](#get-certificatesid)
   - [POST /certificates/verify](#post-certificatesverify)
5. [Codici di Errore](#codici-di-errore)

---

## Panoramica API

MS04 espone un'API RESTful per la validazione completa dei documenti. Tutti gli endpoint utilizzano JSON per request/response e richiedono autenticazione tramite Bearer token.

**Base URL**: `http://localhost:8004/api/v1`

**Autenticazione**: `Authorization: Bearer {token}`

**Content-Type**: `application/json`

[↑ Torna al Indice](#indice)

---

## Endpoint Validazione

### POST /validate

Esegue validazione completa di un documento.

**Request Body**:
```json
{
  "document_id": "doc-2024-11-18-001",
  "document_type": "invoice",
  "validation_type": "full",
  "content": {
    "format": "pdf",
    "data": "base64-encoded-document-content",
    "size_bytes": 245760,
    "checksum": "a1b2c3d4e5f6...",
    "metadata": {
      "created_at": "2024-11-18T10:35:00Z",
      "author": "ms05_transformer",
      "version": "1.0"
    }
  },
  "rules": {
    "business_rules": ["rule_compliance", "rule_quality"],
    "compliance_rules": ["gdpr_compliance", "tax_validation"],
    "quality_rules": ["spelling_check", "format_validation"]
  },
  "options": {
    "fail_fast": false,
    "detailed_report": true,
    "notify_on_error": true,
    "generate_certificate": true
  }
}
```

**Response Success (200)**:
```json
{
  "validation_id": "val-2024-11-18-001",
  "document_id": "doc-2024-11-18-001",
  "status": "passed",
  "overall_score": 0.95,
  "validation_results": {
    "structural_validation": {
      "status": "passed",
      "score": 1.0,
      "checks_passed": 5,
      "checks_failed": 0
    },
    "business_validation": {
      "status": "passed",
      "score": 0.98,
      "rules_applied": 8,
      "rules_failed": 0
    },
    "compliance_validation": {
      "status": "passed",
      "score": 0.92,
      "gdpr_compliant": true,
      "tax_valid": true
    },
    "integrity_validation": {
      "status": "passed",
      "score": 1.0,
      "checksum_valid": true,
      "signature_valid": true
    },
    "quality_assessment": {
      "status": "warning",
      "score": 0.88,
      "spelling_errors": 1,
      "format_issues": 0
    }
  },
  "issues": [
    {
      "severity": "warning",
      "category": "quality",
      "code": "SPELLING_SUGGESTION",
      "message": "Spelling suggestion: 'recieved' should be 'received'",
      "location": {
        "page": 2,
        "line": 15,
        "position": 45
      },
      "suggestion": "received"
    }
  ],
  "certificates": [
    {
      "type": "validation_certificate",
      "certificate_id": "cert-val-2024-11-18-001",
      "issued_at": "2024-11-18T10:37:00Z",
      "valid_until": "2025-11-18T10:37:00Z",
      "download_url": "/certificates/cert-val-2024-11-18-001"
    }
  ],
  "processing_time_ms": 1250,
  "validated_at": "2024-11-18T10:37:00Z"
}
```

**Response Error (400)**:
```json
{
  "error": "VALIDATION_FAILED",
  "message": "Document validation failed with critical errors",
  "details": {
    "validation_id": "val-2024-11-18-001",
    "status": "failed",
    "critical_issues": [
      {
        "severity": "error",
        "category": "structural",
        "code": "SCHEMA_VIOLATION",
        "message": "Required field 'invoice_number' is missing",
        "location": "root.invoice"
      },
      {
        "severity": "error",
        "category": "compliance",
        "code": "TAX_VIOLATION",
        "message": "Tax calculation does not match expected value",
        "expected": 704.00,
        "actual": 700.00
      }
    ]
  }
}
```

[↑ Torna al Indice](#indice)

---

### POST /validate/async

Avvia validazione asincrona di un documento.

**Request Body**:
```json
{
  "document_id": "doc-2024-11-18-001",
  "document_type": "contract",
  "validation_type": "compliance_only",
  "content_url": "https://storage.example.com/documents/doc-2024-11-18-001.pdf",
  "callback_url": "https://client.example.com/validation/callback",
  "rules": {
    "compliance_rules": ["gdpr_compliance", "legal_validation"]
  }
}
```

**Response Success (202)**:
```json
{
  "validation_id": "val-2024-11-18-001",
  "status": "accepted",
  "estimated_completion": "2024-11-18T10:40:00Z",
  "queue_position": 2,
  "status_url": "/validation/val-2024-11-18-001/status",
  "report_url": "/validation/val-2024-11-18-001/report"
}
```

[↑ Torna al Indice](#indice)

---

### GET /validation/{id}/status

Recupera lo stato di una validazione asincrona.

**Path Parameters**:
- `id`: ID della validazione (string)

**Response Success (200)**:
```json
{
  "validation_id": "val-2024-11-18-001",
  "status": "completed",
  "progress": {
    "completed_steps": 5,
    "total_steps": 5,
    "percentage": 100
  },
  "result": {
    "overall_status": "passed",
    "score": 0.96
  },
  "completed_at": "2024-11-18T10:38:00Z",
  "processing_time_ms": 1800
}
```

**Response Processing (202)**:
```json
{
  "validation_id": "val-2024-11-18-001",
  "status": "processing",
  "progress": {
    "current_step": "compliance_validation",
    "completed_steps": 3,
    "total_steps": 5,
    "percentage": 60
  },
  "estimated_completion": "2024-11-18T10:39:00Z"
}
```

[↑ Torna al Indice](#indice)

---

### GET /validation/{id}/report

Recupera il report completo di validazione.

**Path Parameters**:
- `id`: ID della validazione (string)

**Query Parameters**:
- `format`: Formato report (json, pdf, xml)

**Response Success (200)**:
```json
{
  "validation_id": "val-2024-11-18-001",
  "document_id": "doc-2024-11-18-001",
  "status": "passed",
  "overall_score": 0.95,
  "validation_details": {
    "structural_validation": {
      "status": "passed",
      "score": 1.0,
      "details": {
        "schema_validated": true,
        "required_fields_present": true,
        "data_types_valid": true
      }
    },
    "business_validation": {
      "status": "passed",
      "score": 0.98,
      "applied_rules": [
        {
          "rule_id": "rule_amount_limit",
          "result": "passed",
          "condition": "amount <= 50000",
          "actual_value": 3200
        }
      ]
    },
    "compliance_validation": {
      "status": "passed",
      "score": 0.92,
      "checks": [
        {
          "check_type": "gdpr_compliance",
          "result": "passed",
          "details": "No personal data requiring consent detected"
        },
        {
          "check_type": "tax_validation",
          "result": "passed",
          "details": "Tax calculations verified against Italian tax rules"
        }
      ]
    },
    "integrity_validation": {
      "status": "passed",
      "score": 1.0,
      "checksum": {
        "algorithm": "SHA-256",
        "expected": "a1b2c3d4e5f6...",
        "actual": "a1b2c3d4e5f6...",
        "match": true
      },
      "digital_signature": {
        "present": true,
        "valid": true,
        "certificate_issuer": "CN=Validation Authority",
        "valid_from": "2024-01-01T00:00:00Z",
        "valid_to": "2025-01-01T00:00:00Z"
      }
    },
    "quality_assessment": {
      "status": "warning",
      "score": 0.88,
      "metrics": {
        "spelling_accuracy": 0.99,
        "grammar_score": 1.0,
        "format_compliance": 0.95,
        "completeness_score": 1.0
      },
      "issues": [
        {
          "type": "spelling",
          "severity": "minor",
          "text": "recieved",
          "suggestion": "received",
          "position": {
            "page": 2,
            "line": 15,
            "column": 45
          }
        }
      ]
    }
  },
  "recommendations": [
    {
      "type": "improvement",
      "category": "quality",
      "message": "Consider using automated spell checking before document generation",
      "impact": "medium"
    }
  ],
  "metadata": {
    "validation_started_at": "2024-11-18T10:36:00Z",
    "validation_completed_at": "2024-11-18T10:37:30Z",
    "processing_time_ms": 1250,
    "validator_version": "2.1.0",
    "rules_version": "1.5.2"
  }
}
```

[↑ Torna al Indice](#indice)

---

## Endpoint Regole

### GET /rules

Recupera la lista delle regole di validazione.

**Query Parameters**:
- `type`: Tipo regola (business, compliance, quality)
- `active`: Solo regole attive (true/false)

**Response Success (200)**:
```json
{
  "rules": [
    {
      "rule_id": "rule_compliance_check",
      "type": "business",
      "name": "Controllo Conformità Fatturazione",
      "description": "Verifica conformità base per fatture",
      "conditions": {
        "document_type": "invoice",
        "amount": {
          "operator": ">",
          "value": 100
        }
      },
      "actions": [
        {
          "action_type": "validate_field",
          "field": "tax_amount",
          "rule": "tax_calculation_correct"
        }
      ],
      "active": true,
      "priority": 10,
      "version": "2.1",
      "created_at": "2024-01-15T09:00:00Z"
    },
    {
      "rule_id": "rule_gdpr_compliance",
      "type": "compliance",
      "name": "Conformità GDPR",
      "description": "Verifica rispetto normative GDPR",
      "conditions": {
        "contains_personal_data": true
      },
      "actions": [
        {
          "action_type": "check_consent",
          "required": true
        },
        {
          "action_type": "validate_retention",
          "max_days": 2555
        }
      ],
      "active": true,
      "priority": 100,
      "version": "1.8"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 50
}
```

[↑ Torna al Indice](#indice)

---

### POST /rules

Crea una nuova regola di validazione.

**Request Body**:
```json
{
  "type": "quality",
  "name": "Controllo Qualità Documenti",
  "description": "Regola per valutazione qualità documenti",
  "conditions": {
    "document_type": "contract",
    "word_count": {
      "operator": ">",
      "value": 100
    }
  },
  "actions": [
    {
      "action_type": "spelling_check",
      "enabled": true
    },
    {
      "action_type": "grammar_check",
      "enabled": true
    },
    {
      "action_type": "readability_score",
      "minimum_score": 60
    }
  ],
  "priority": 5
}
```

**Response Success (201)**:
```json
{
  "rule_id": "rule_quality_check",
  "status": "created",
  "version": "1.0",
  "created_at": "2024-11-18T12:00:00Z"
}
```

[↑ Torna al Indice](#indice)

---

### PUT /rules/{id}

Aggiorna una regola esistente.

**Path Parameters**:
- `id`: ID della regola (string)

**Request Body**:
```json
{
  "active": false,
  "conditions": {
    "document_type": "invoice",
    "amount": {
      "operator": ">",
      "value": 500
    }
  },
  "priority": 15
}
```

**Response Success (200)**:
```json
{
  "rule_id": "rule_compliance_check",
  "status": "updated",
  "version": "2.2",
  "updated_at": "2024-11-18T12:30:00Z"
}
```

[↑ Torna al Indice](#indice)

---

## Endpoint Certificati

### GET /certificates/{id}

Recupera un certificato di validazione.

**Path Parameters**:
- `id`: ID del certificato (string)

**Query Parameters**:
- `format`: Formato certificato (json, pdf)

**Response Success (200)**:
```json
{
  "certificate_id": "cert-val-2024-11-18-001",
  "type": "validation_certificate",
  "document_id": "doc-2024-11-18-001",
  "validation_id": "val-2024-11-18-001",
  "status": "valid",
  "issued_at": "2024-11-18T10:37:00Z",
  "valid_until": "2025-11-18T10:37:00Z",
  "issuer": {
    "name": "ZenIA Validation Authority",
    "certificate": "CN=ZenIA Validator CA"
  },
  "subject": {
    "document_type": "invoice",
    "validation_score": 0.95,
    "validation_level": "full"
  },
  "validation_results": {
    "structural": "passed",
    "business": "passed",
    "compliance": "passed",
    "integrity": "passed",
    "quality": "warning"
  },
  "signature": {
    "algorithm": "SHA-256",
    "value": "signature-value-here"
  }
}
```

[↑ Torna al Indice](#indice)

---

### POST /certificates/verify

Verifica la validità di un certificato.

**Request Body**:
```json
{
  "certificate_id": "cert-val-2024-11-18-001",
  "certificate_data": "base64-encoded-certificate"
}
```

**Response Success (200)**:
```json
{
  "certificate_id": "cert-val-2024-11-18-001",
  "status": "valid",
  "verification_details": {
    "signature_valid": true,
    "certificate_chain_valid": true,
    "not_expired": true,
    "not_revoked": true,
    "issuer_trusted": true
  },
  "verified_at": "2024-11-18T14:00:00Z"
}
```

[↑ Torna al Indice](#indice)

---

## Codici di Errore

| Codice | Descrizione | HTTP Status |
|--------|-------------|-------------|
| `VALIDATION_FAILED` | Validazione fallita con errori critici | 400 |
| `DOCUMENT_NOT_FOUND` | Documento non trovato | 404 |
| `INVALID_DOCUMENT_FORMAT` | Formato documento non supportato | 400 |
| `SCHEMA_VALIDATION_ERROR` | Errore validazione schema | 400 |
| `RULE_EXECUTION_ERROR` | Errore esecuzione regola | 500 |
| `CERTIFICATE_EXPIRED` | Certificato scaduto | 400 |
| `AUTHENTICATION_FAILED` | Autenticazione fallita | 401 |
| `AUTHORIZATION_FAILED` | Autorizzazione negata | 403 |
| `RATE_LIMIT_EXCEEDED` | Limite richieste superato | 429 |

[↑ Torna al Indice](#indice)

---

**Navigazione**: [← SPECIFICATION.md](SPECIFICATION.md) | [API](API.md) | [DATABASE-SCHEMA →](DATABASE-SCHEMA.md)
