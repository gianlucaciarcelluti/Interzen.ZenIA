# SP16 - Correspondence Classifier

## Panoramica

**SP16 - Correspondence Classifier** è il componente che classifica automaticamente il tipo di corrispondenza ricevuta (PEC, email, web form), distinguendo tra istanze, comunicazioni, richieste, notifiche, etc.

```mermaid
graph LR
    SP01[SP01<br/>EML Parser] -->|parsed_email| SP16[SP16<br/>Classifier]
    SP16 -->|classification| SP17[SP17<br/>Registry Suggester]
    SP16 -->|classification| SP10[SP10<br/>Dashboard]
    
    SP16 -.-> BERT[BERT<br/>Classifier]
    SP16 -.-> RULES[Rule<br/>Engine]
    SP16 -.-> CACHE[Redis<br/>Cache]
    SP16 -.-> DB[(PostgreSQL)]
    
    style SP16 fill:#ffd700
```

## Responsabilità

### Core Functions

1. **Correspondence Type Classification**
   - Istanza amministrativa
   - Comunicazione ufficiale
   - Richiesta informazioni
   - Notifica/avviso
   - Reclamo/segnalazione
   - Altro

2. **Channel Recognition**
   - PEC (Posta Elettronica Certificata)
   - Email ordinaria
   - Web form submission
   - API integration

3. **Priority Assessment**
   - Alta priorità (istanze, reclami)
   - Media priorità (comunicazioni)
   - Bassa priorità (notifiche)

4. **Language Detection**
   - Italiano ufficiale
   - Italiano regionale/dialettale
   - Altre lingue

## Architettura Tecnica

### Classification Pipeline

```mermaid
graph TD
    A[Parsed Email] --> B[Preprocessing]
    B --> C[Feature Extraction]
    C --> D[ML Classification]
    D --> E[Rule-based Validation]
    E --> F[Confidence Scoring]
    F --> G[Output Classification]
    
    style SP16 fill:#ffd700
```

### Tecnologie Utilizzate

| Componente | Tecnologia | Versione | Scopo |
|------------|------------|----------|--------|
| ML Model | BERT |  | Classificazione testo |
| Rule Engine | Drools | 8.0 | Validazione regole |
| Language Detection | langdetect | 1.0.9 | Rilevamento lingua |
| Cache | Redis | 7.2 | Cache risultati |
| Database | PostgreSQL | 15 | Training data |

### Esempi di Classificazione

#### Istanza Amministrativa
```
Input: "Con la presente si richiede autorizzazione per..."
Output: {type: "ISTANZA", priority: "HIGH", confidence: 0.96}
```

#### Comunicazione Ufficiale
```
Input: "Si comunica l'avvenuta pubblicazione..."
Output: {type: "COMUNICAZIONE", priority: "MEDIUM", confidence: 0.89}
```

### API Endpoints

```yaml
POST /api/v1/classify/correspondence
  - Input: {"email_text": "string", "metadata": {}}
  - Output: {"type": "string", "priority": "string", "confidence": 0.95}
```

### Configurazione

```yaml
sp16:
  model: 'bert-correspondence-classifier'
  threshold: 0.8
  categories:
    - istanza
    - comunicazione
    - richiesta
    - notifica
    - reclamo
  cache_ttl: 3600
```

### Performance Metrics

- **Accuracy**: >95% classificazione corretta
- **Precision**: >92% per categorie principali
- **Latency**: <2s per classificazione
- **Throughput**: 200 email/minuto

### Sicurezza

- **Data Sanitization**: Rimozione dati sensibili
- **Audit Logging**: Tracciamento classificazioni
- **Model Security**: Validazione input

### Evoluzione

1. **Multi-language**: Supporto multilingua
2. **Domain Adaptation**: Fine-tuning per ente specifico
3. **Real-time Learning**: Aggiornamento modello continuo</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC2 - Protocollo Informatico/01 SP16 - Correspondence Classifier.md