# API Reference - MS05-TRANSFORMER

## Panoramica API

L'API REST di MS05-TRANSFORMER fornisce endpoint per la trasformazione sincrona e asincrona di documenti, oltre a funzionalità di monitoraggio e gestione.

**Base URL**: `http://ms05-transformer:8005/api/v1`

**Autenticazione**: Bearer Token (JWT)

## Endpoint Trasformazione

### POST /transform

Trasformazione sincrona di documenti.

**Parametri Header**:
```
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data
```

**Parametri Form**:
- `document` (file): Documento da trasformare (max 10MB)
- `target_format` (string): Formato destinazione (PDF, DOCX, XML, JSON)
- `options` (string, JSON): Opzioni di trasformazione

**Esempio Richiesta**:
```bash
curl -X POST "http://ms05-transformer:8005/api/v1/transform" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -F "document=@document.pdf" \
  -F "target_format=DOCX" \
  -F 'options={"compression": "HIGH", "preserve_metadata": true}'
```

**Risposta Successo (200)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "COMPLETED",
  "result": {
    "document_id": "550e8400-e29b-41d4-a716-446655440001",
    "original_format": "PDF",
    "target_format": "DOCX",
    "file_size": 245760,
    "processing_time": 12.5,
    "download_url": "http://ms05-transformer:8005/api/v1/download/550e8400-e29b-41d4-a716-446655440001"
  },
  "metadata": {
    "created_at": "2025-11-18T10:30:00Z",
    "processed_by": "transformer-v2.1.0"
  }
}
```

**Risposta Errore (422)**:
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Formato di destinazione non supportato",
  "details": {
    "supported_formats": ["PDF", "DOCX", "XML", "JSON"],
    "requested_format": "TXT"
  },
  "timestamp": "2025-11-18T10:30:05Z"
}
```

### POST /transform/async

Trasformazione asincrona di documenti.

**Parametri**: Identici a `/transform`

**Risposta Successo (202)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440002",
  "status": "QUEUED",
  "estimated_completion": "2025-11-18T10:31:00Z",
  "queue_position": 3,
  "monitoring_url": "http://ms05-transformer:8005/api/v1/status/550e8400-e29b-41d4-a716-446655440002"
}
```

### GET /status/{job_id}

Verifica stato trasformazione asincrona.

**Parametri Path**:
- `job_id` (string): ID del job di trasformazione

**Risposta (200)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440002",
  "status": "PROCESSING",
  "progress": {
    "percentage": 65,
    "current_step": "Converting PDF to DOCX",
    "estimated_completion": "2025-11-18T10:30:45Z"
  },
  "result": null,
  "created_at": "2025-11-18T10:29:00Z",
  "updated_at": "2025-11-18T10:30:15Z"
}
```

**Risposta Completata (200)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440002",
  "status": "COMPLETED",
  "progress": {
    "percentage": 100,
    "current_step": "Transformation completed",
    "estimated_completion": "2025-11-18T10:30:30Z"
  },
  "result": {
    "document_id": "550e8400-e29b-41d4-a716-446655440003",
    "original_format": "PDF",
    "target_format": "DOCX",
    "file_size": 245760,
    "processing_time": 28.7,
    "download_url": "http://ms05-transformer:8005/api/v1/download/550e8400-e29b-41d4-a716-446655440003"
  },
  "created_at": "2025-11-18T10:29:00Z",
  "updated_at": "2025-11-18T10:30:30Z"
}
```

### GET /download/{document_id}

Download documento trasformato.

**Parametri Path**:
- `document_id` (string): ID del documento trasformato

**Risposta**: File binario del documento trasformato

## Endpoint Gestione

### GET /formats

Elenco formati supportati.

**Risposta (200)**:
```json
{
  "supported_formats": [
    {
      "format": "PDF",
      "description": "Portable Document Format",
      "input_supported": true,
      "output_supported": true,
      "max_size": "10MB"
    },
    {
      "format": "DOCX",
      "description": "Microsoft Word Document",
      "input_supported": true,
      "output_supported": true,
      "max_size": "10MB"
    },
    {
      "format": "XML",
      "description": "Extensible Markup Language",
      "input_supported": true,
      "output_supported": true,
      "max_size": "5MB"
    },
    {
      "format": "JSON",
      "description": "JavaScript Object Notation",
      "input_supported": true,
      "output_supported": true,
      "max_size": "2MB"
    }
  ],
  "conversion_matrix": {
    "PDF_to_DOCX": "supported",
    "DOCX_to_PDF": "supported",
    "XML_to_JSON": "supported",
    "JSON_to_XML": "supported"
  }
}
```

### GET /health

Verifica stato del servizio.

**Risposta (200)**:
```json
{
  "status": "healthy",
  "version": "2.1.0",
  "uptime": "7d 4h 23m",
  "services": {
    "database": "connected",
    "redis": "connected",
    "storage": "available"
  },
  "metrics": {
    "active_jobs": 12,
    "queue_depth": 45,
    "success_rate": 0.967
  },
  "timestamp": "2025-11-18T10:30:00Z"
}
```

### GET /metrics

Metriche dettagliate del servizio.

**Risposta (200)**:
```json
{
  "performance": {
    "requests_per_minute": 45.2,
    "average_response_time": 2.3,
    "error_rate": 0.023,
    "throughput_mbps": 12.5
  },
  "transformations": {
    "total_processed": 15420,
    "success_rate": 0.967,
    "average_processing_time": 15.7,
    "format_distribution": {
      "PDF_to_DOCX": 0.45,
      "DOCX_to_PDF": 0.32,
      "XML_to_JSON": 0.15,
      "JSON_to_XML": 0.08
    }
  },
  "system": {
    "cpu_usage": 0.67,
    "memory_usage": 0.78,
    "disk_usage": 0.45,
    "network_io": 1024000
  },
  "timestamp": "2025-11-18T10:30:00Z"
}
```

## Endpoint Amministrazione

### POST /admin/purge/{days}

Pulizia documenti più vecchi di N giorni.

**Parametri Path**:
- `days` (integer): Giorni di retention

**Risposta (200)**:
```json
{
  "purged_documents": 1250,
  "freed_space_mb": 2450,
  "timestamp": "2025-11-18T10:30:00Z"
}
```

### POST /admin/retry/{job_id}

Retry manuale di un job fallito.

**Risposta (200)**:
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440004",
  "status": "REQUEUED",
  "retry_count": 1,
  "max_retries": 3,
  "timestamp": "2025-11-18T10:30:00Z"
}
```

## Codici di Stato HTTP

- **200**: Successo
- **202**: Accepted (elaborazione asincrona avviata)
- **400**: Bad Request (parametri invalidi)
- **401**: Unauthorized (token mancante/invalido)
- **403**: Forbidden (permessi insufficienti)
- **404**: Not Found (risorsa non esistente)
- **413**: Payload Too Large
- **422**: Unprocessable Entity (validazione fallita)
- **429**: Too Many Requests (rate limit superato)
- **500**: Internal Server Error
- **503**: Service Unavailable (manutenzione/sovraccarico)

## Rate Limiting

- **Authenticated requests**: 100/minuto per client
- **Anonymous requests**: 10/minuto per IP
- **Burst limit**: 20 richieste simultanee

## Versioning API

L'API utilizza versioning nell'URL path (`/api/v1/`).
Versioni future manterranno retrocompatibilità per 12 mesi.
