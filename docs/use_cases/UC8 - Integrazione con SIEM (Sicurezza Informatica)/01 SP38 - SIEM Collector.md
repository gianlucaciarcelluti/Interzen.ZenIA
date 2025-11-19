# SP38 - SIEM Collector

## Descrizione Componente

Il **SP38 SIEM Collector** è il componente responsabile della raccolta, normalizzazione e aggregazione di eventi sicurezza da tutte le fonti nell'ecosistema amministrativo. Implementa una architettura distribuita e scalabile per gestire volumi elevati di log e eventi, fornendo una base solida per il rilevamento e la risposta alle minacce.

## Responsabilità

- **Log Collection**: Raccolta log da molteplici sorgenti eterogenee
- **Event Normalization**: Standardizzazione formato eventi per analisi
- **Data Enrichment**: Arricchimento eventi con context aggiuntivo
- **Real-time Streaming**: Streaming eventi per processing real-time
- **Data Quality**: Validazione e filtering qualità dati sicurezza

## Architettura Interna

```
┌─────────────────────────────────────────────────────────────┐
│                    COLLECTION LAYER                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Agent Collectors      API Collectors       File Collectors │ │
│  │  ┌─────────────────┐    ┌────────────────┐   ┌─────────┐ │ │
│  │  │  - Wazuh Agents  │    │  - REST APIs   │   │  - Log   │ │
│  │  │  - Filebeat      │    │  - Webhooks    │   │  - Files │ │
│  │  │  - Syslog        │    │  - Kafka       │   │  - DB    │ │
│  │  └─────────────────┘    └────────────────┘   └─────────┘ │ │
└─────────────────────────────────────────────────────────────┘
│                    PROCESSING LAYER                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Event Parser         Normalizer         Enricher       │ │
│  │  ┌─────────────────┐    ┌────────────────┐   ┌─────────┐ │ │
│  │  │  - Format Parse  │    │  - Schema Map │   │  - GeoIP │ │
│  │  │  - Field Extract │    │  - Time Norm  │   │  - Threat │ │
│  │  │  - Validation    │    │  - Dedup      │   │  - Asset │ │
│  │  └─────────────────┘    └────────────────┘   └─────────┘ │ │
└─────────────────────────────────────────────────────────────┘
│                    STREAMING LAYER                          │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Kafka Producer       Stream Processor    Queue Manager │ │
│  │  ┌─────────────────┐    ┌────────────────┐   ┌─────────┐ │ │
│  │  │  - Topic Routing │    │  - Filtering  │   │  - Buff  │ │
│  │  │  - Partitioning  │    │  - Aggregation│   │  - Retry │ │
│  │  │  - Compression   │    │  - Windowing  │   │  - DLQ   │ │
│  │  └─────────────────┘    └────────────────┘   └─────────┘ │ │
└─────────────────────────────────────────────────────────────┘
```

## Log Collection Engine

### Multi-Source Collection

Il motore di raccolta multi-sorgente gestisce l'acquisizione di log da fonti eterogenee:

**Source Diversity**:
- Raccolta da server, applicazioni, dispositivi di rete
- Supporto per protocolli standard (syslog, REST, file)
- Integrazione con sistemi cloud e on-premise
- Gestione di volumi elevati attraverso architettura distribuita

**Reliability Features**:
- Collection fault-tolerant con retry automatico
- Buffering per gestire interruzioni di connettività
- Deduplicazione per evitare duplicati
- Quality checks per validare integrità dei dati

### Agent-Based Collection

La raccolta basata su agenti fornisce monitoraggio profondo dei sistemi endpoint:

**Lightweight Agents**:
- Deployment semplice su tutti i sistemi target
- Monitoraggio real-time di file di log e eventi
- Configurazione centralizzata e aggiornamenti automatici
- Minimo impatto sulle performance del sistema host

**Security Integration**:
- Raccolta di eventi di sicurezza nativi del sistema
- Monitoraggio delle modifiche ai file critici
- Detection di comportamenti anomali
- Integrazione con sistemi di sicurezza esistenti

### API-Based Collection

La raccolta basata su API permette integrazione con servizi cloud e applicazioni:

**RESTful Integration**:
- Chiamate API standardizzate per raccolta dati
- Autenticazione sicura con OAuth e API keys
- Rate limiting e throttling per rispettare limiti API
- Error handling per API temporaneamente non disponibili

**Webhook Support**:
- Ricezione di eventi push da servizi esterni
- Validazione dell'autenticità dei webhook
- Processing asincrono per gestire burst di eventi
- Retry logic per garantire delivery affidabile

## Event Normalization

### Schema Mapping Engine

Il motore di mapping schema standardizza eventi da formati diversi:

**Format Standardization**:
- Conversione di eventi da formati proprietari a schema comune
- Mappatura intelligente di campi equivalenti
- Gestione di versioni multiple di schema
- Backward compatibility per evoluzione schema

**Field Extraction**:
- Parsing avanzato per estrazione campi strutturati
- Regular expressions per pattern recognition
- Template-based extraction per formati noti
- Validation rules per garantire completezza dati

## Data Enrichment

### Context Enrichment Engine

Il motore di arricchimento contesto aggiunge informazioni utili per l'analisi:

**Geographic Enrichment**:
- Risoluzione IP addresses a informazioni geografiche
- Identificazione di paesi, città, coordinate
- Timezone detection per analisi temporali
- ASN information per network classification

**Asset Context**:
- Correlazione eventi con inventario asset
- Informazioni sui sistemi e proprietari
- Classificazione per criticità e funzione
- Integration con CMDB per completezza contesto

**Threat Intelligence**:
- Enrichment con feed di threat intelligence
- IOC matching per identificazione minacce note
- Reputation scoring per indirizzi IP e domini
- Behavioral analysis per detection avanzata

## Streaming & Queue Management

### Kafka Integration

L'integrazione Kafka garantisce streaming affidabile di eventi ad alto volume:

**Topic Management**:
- Organizzazione eventi per categorie e priorità
- Partitioning per distribuzione load bilanciata
- Retention policies per gestione spazio
- Topic naming conventions per discoverability

**Producer Configuration**:
- Batching per ottimizzare throughput
- Compression per ridurre bandwidth
- Acknowledgment levels per garantire delivery
- Error handling per producer failures

## Quality Assurance

### Event Validation

La validazione degli eventi garantisce qualità e affidabilità dei dati:

**Schema Validation**:
- Convalida contro schema JSON definito
- Type checking per campi obbligatori
- Range validation per valori numerici
- Format validation per date e indirizzi

**Data Quality Checks**:
- Detection di valori null o mancanti
- Sanity checks per valori fuori range
- Duplicate detection e filtering
- Correlation validation per eventi correlati

## Monitoring & Statistics

### Collection Metrics

Le metriche di raccolta forniscono insight sulla salute e performance del sistema:

**Volume Metrics**:
- Numero di eventi raccolti per unità di tempo
- Breakdown per sorgente e tipo di evento
- Trend analysis per identificare variazioni
- Capacity planning basato su volumi storici

**Quality Metrics**:
- Percentuale di eventi validati con successo
- Tasso di duplicati e eventi scartati
- Latenza media dalla generazione alla raccolta
- Error rates per sorgente e tipo di errore

## Configurazione

### Collection Configuration
```yaml
collection:
  sources:
    - type: agent
      name: wazuh_agents
      config:
        manager_ip: "10.0.0.10"
        manager_port: 1514
        agent_groups: ["web", "database", "application"]

    - type: api
      name: cloudtrail_api
      config:
        url: "https://cloudtrail.amazonaws.com"
        auth_type: "aws_iam"
        collection_interval: 300
        pagination: true

    - type: file
      name: application_logs
      config:
        paths: ["/var/log/application/*.log"]
        format: "json"
        rotation: "daily"

  normalization:
    timestamp_formats:
      - "%Y-%m-%d %H:%M:%S"
      - "%Y-%m-%dT%H:%M:%S.%fZ"
      - "%b %d %H:%M:%S"

    field_mappings:
      source_ip: ["client_ip", "src_ip", "source"]
      destination_ip: ["server_ip", "dst_ip", "destination"]
      username: ["user", "login", "account"]

  enrichment:
    geoip:
      enabled: true
      database_path: "/opt/geoip/GeoLite2-City.mmdb"

    asset_lookup:
      enabled: true
      cache_ttl: 3600

    threat_intel:
      enabled: true
      feeds:
        - "alienvault_otx"
        - "abuseipdb"
```

## Testing

### Collection Testing

## Performance Optimization

### Buffering & Batching

## Disaster Recovery

### Collection Recovery
- **Event Buffering**: Buffer eventi durante outage
- **Checkpointing**: Salvataggio stato raccolta periodico
- **Replay Capability**: Ri-elaborazione eventi da checkpoint
- **Failover**: Automatic failover tra collector instances

### Recovery Procedures
1. **Restart Collection**: Resume da ultimo checkpoint
2. **Buffer Replay**: Ri-elabora eventi bufferizzati
3. **Gap Detection**: Identifica e recupera eventi mancanti
4. **State Synchronization**: Sync stato tra instances

## Roadmap

### Version 1.0 (Current)
- Basic log collection da agenti
- Event normalization semplice
- Kafka streaming foundation
- Real-time dashboards

### Version 2.0 (Next)
- Advanced enrichment con threat intel
- API collection completo
- Schema evolution management
- Performance optimization

### Version 3.0 (Future)
- AI-powered event correlation
- Predictive event normalization
- Autonomous collection scaling
- Edge collection capabilities</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC8 - Integrazione con SIEM (Sicurezza Informatica)/01 SP38 - SIEM Collector.md