# Sequence Diagram: Ultra Semplificato - Email to Atto

📊 **SUPPLEMENTARY DIAGRAM - EXECUTIVE SUMMARY**: Versione estremamente semplificata della [sequenza canonica](01 CANONICAL - Generazione Atto Completo.md). Mostra solo 3 macro-blocchi (Email + AI + Sistema). Ideale per C-level executives e product demos veloce. **Nota**: Non include dettagli tecnici - consultare versione canonica per specifiche complete.

## Il Flusso in 3 Macro-Blocchi

Questo è il diagramma più essenziale: mostra solo le 3 macro-fasi del sistema con aggregazione di tutti i sottoprogetti.

```mermaid
sequenceDiagram
    autonumber
    participant U as Cittadino
    participant PEC as PEC Server
    participant OPS as Operatore PA
    
    box rgba(255, 215, 0, 0.3) 📧 BLOCCO EMAIL (SP01-SP02)
    participant EMAIL as Email Processing<br/>(Parse + Extract)
    end
    
    box rgba(135, 206, 250, 0.3) 🤖 BLOCCO AI (SP03-SP08)
    participant AI as AI Pipeline<br/>(Classify + Generate + Validate)
    end
    
    box rgba(144, 238, 144, 0.3) 🏛️ BLOCCO SISTEMA (SP09-SP11)
    participant SYS as System Layer<br/>(Workflow + Audit + Dashboard)
    end
    
    %% Fase 1: Ricezione Email
    Note over U,SYS: 📧 FASE 1: Ricezione Email PEC
    U->>PEC: Email + allegati
    PEC->>SYS: Notifica .eml
    SYS->>EMAIL: Processa email
    
    EMAIL->>EMAIL: Parse .eml<br/>Extract docs (OCR)<br/>NER data
    EMAIL-->>SYS: Metadata + Docs[]
    
    rect rgb(255, 235, 59, 0.3)
        SYS->>OPS: 🔄 HITL: Verifica allegati
        OPS-->>SYS: ✅ Conferma
    end
    
    %% Fase 2: AI Processing
    Note over U,SYS: 🤖 FASE 2: Elaborazione AI
    SYS->>AI: Avvia generazione
    
    AI->>AI: Classifica procedimento<br/>Recupera normativa<br/>Genera documento<br/>Valida conformità<br/>Quality check
    AI-->>SYS: Draft atto validato
    
    rect rgb(255, 235, 59, 0.3)
        SYS->>OPS: 🔄 HITL: Review + firma
        OPS-->>SYS: 🔐 Approvato e firmato
    end
    
    %% Fase 3: Finalizzazione
    Note over U,SYS: 🏛️ FASE 3: Pubblicazione
    SYS->>SYS: Protocollo<br/>Audit trail<br/>Archiviazione
    SYS->>U: 📧 Notifica PEC completamento
    
    Note over U,SYS: ✅ Tempo totale: ~44s (11s auto + 33s HITL)
```

## Le 3 Macro-Fasi nel Dettaglio

### 📧 BLOCCO EMAIL: Email Processing (SP01-SP02)
**Obiettivo**: Convertire email PEC in dati strutturati pronti per AI

| Step | Componente | Azione | Output |
|------|-----------|--------|--------|
| 1 | SP01 - EML Parser | Parse .eml, valida firma PEC | Metadata email + lista allegati |
| 2 | SP02 - Doc Extractor | OCR, classifica docs, NER | Documents[] con CF, indirizzi, importi |
| 3 | HITL #1 | Operatore verifica completezza | ✅ Conferma o richiede integrazioni |

**Tempo**: 3.3s automatico + 8s verifica = **11.3s**  
**Valore**: Elimina trascrizione manuale (da 20min a 11s)

---

### 🤖 BLOCCO AI: AI Pipeline (SP03-SP08)
**Obiettivo**: Generare atto amministrativo conforme

| Step | Componenti | Azione | Output |
|------|-----------|--------|--------|
| 1 | SP03 - Procedural | Classifica procedimento | Procedimento identificato (96% conf) |
| 2 | SP04 - Knowledge Base | RAG normativa | Contesto giuridico |
| 3 | SP05 - Template Engine | Genera con GPT-4/Groq | Draft documento |
| 4 | SP06 - Validator | Valida conformità | Score validazione (0-100) |
| 5 | SP07 - Content Classifier | Classifica tipo atto | Categoria documento |
| 6 | SP08 - Quality Checker | Controllo linguistico | Score qualità (0-100) |

**Tempo**: ~8s automatico + 17s review = **25s**  
**Valore**: Automatizza generazione mantenendo qualità PA

---

### 🏛️ BLOCCO SISTEMA: System Layer (SP09-SP11)
**Obiettivo**: Orchestrare, auditare, pubblicare

| Componente | Ruolo | Tecnologie |
|-----------|-------|------------|
| SP09 - Workflow Engine | Orchestrazione flusso, gestione HITL | Apache NiFi, Event Bus |
| SP10 - Dashboard | Visualizzazione metriche, interfaccia review | React, WebSocket, D3.js |
| SP11 - Security & Audit | Tracciabilità, firma digitale, compliance | JWT, Blockchain, HSM |

**Tempo**: 8s protocollo/audit  
**Valore**: Compliance GDPR/AgID, tracciabilità certificata

---

## Il Flusso in 1 Immagine

```
📧 EMAIL PEC (Cittadino)
    ↓
┌─────────────────────────────────────────┐
│ SP01: Parse .eml (0.8s)                 │
│ SP02: Extract docs + OCR (2.5s)         │
└─────────────────────────────────────────┘
    ↓
🔄 HITL #1: Verifica Documenti (8s)
    ↓
┌─────────────────────────────────────────┐
│ SP03: Classifica Procedimento (0.5s)    │
│ SP04: Recupera Normativa (1.2s)         │
│ SP05: Genera Atto (2.3s)                │
│ SP06: Valida Conformità (0.8s)          │
│ SP08: Quality Check (0.3s)              │
└─────────────────────────────────────────┘
    ↓
🔄 HITL #2-4: Review + Firma (25s)
    ↓
┌─────────────────────────────────────────┐
│ SP11: Protocollo + Audit (2s)           │
└─────────────────────────────────────────┘
    ↓
📧 NOTIFICA PEC (Cittadino)

⏱️ TOTALE: ~44s (19s AI + 25s umano)
```

## Metriche Chiave per Stakeholder

### Per il Cittadino
- ⏱️ **Tempo risposta**: da 30 giorni a 1 giorno
- 📊 **Tracciabilità**: Real-time su dashboard pubblica
- ✅ **Correttezza**: 97% validazione automatica

### Per l'Operatore PA
- 🚀 **Produttività**: da 20 a 80+ pratiche/giorno
- ⌨️ **Lavoro manuale**: -95% (da 20min a 33s)
- 🎯 **Focus**: Solo review critica, no trascrizione

### Per il Manager PA
- 💰 **Costi**: -60% per pratica
- ⚖️ **Compliance**: 100% tracciato (GDPR/AgID)
- 📈 **SLA**: 95% pratiche <24h

## Confronto: Prima vs Dopo

| Aspetto | PRIMA (Manuale) | DOPO (SP01-SP11) | Miglioramento |
|---------|-----------------|------------------|---------------|
| **Input** | Upload manuale docs | Email PEC diretta | Integrazione nativa |
| **Estrazione dati** | Trascrizione manuale (20min) | OCR + NER (3.3s) | **360x più veloce** |
| **Classificazione** | Esperienza operatore | AI + KB (0.5s) | Oggettivo e ripetibile |
| **Generazione** | Copia/incolla template | GPT-4 contestuale (2.3s) | Personalizzazione automatica |
| **Validazione** | Checklist manuale | AI multi-layer (1.1s) | 97% accuratezza |
| **Errori** | 12-15% (trascrizione) | <3% | **-80% errori** |
| **Pratiche/giorno** | 20 | 80+ | **4x throughput** |
| **Tempo totale** | 20min + 30gg iter | 44s + 1gg iter | **-97% tempo elaborazione** |

## Architettura dei 3 Blocchi

```mermaid
graph TB
    subgraph "📧 EMAIL PROCESSING"
        PEC[PEC Server] --> SP01[SP01<br/>EML Parser]
        SP01 --> SP02[SP02<br/>Doc Extractor]
        SP02 --> HITL1[HITL #1<br/>Verifica]
    end
    
    subgraph "🤖 AI PIPELINE"
        HITL1 --> SP03[SP03<br/>Procedural]
        SP03 --> SP04[SP04<br/>Knowledge Base]
        SP04 --> SP05[SP05<br/>Template]
        SP05 --> SP06[SP06<br/>Validator]
        SP06 --> SP08[SP08<br/>Quality]
        SP08 --> HITL2[HITL #2-4<br/>Review + Firma]
    end
    
    subgraph "🏛️ SYSTEM LAYER"
        HITL2 --> SP11[SP11<br/>Security & Audit]
        SP11 --> Protocol[Protocollo]
        Protocol --> Notify[Notifica PEC]
        
        SP09[SP09 Workflow] -.orchestrates.-> SP01
        SP09 -.orchestrates.-> SP03
        SP09 -.orchestrates.-> SP11
        
        SP10[SP10 Dashboard] -.monitors.-> SP09
    end
    
    style SP01 fill:#ffd700
    style SP02 fill:#ffd700
    style SP03 fill:#87ceeb
    style SP04 fill:#87ceeb
    style SP05 fill:#87ceeb
    style SP06 fill:#87ceeb
    style SP08 fill:#87ceeb
    style SP09 fill:#98fb98
    style SP10 fill:#98fb98
    style SP11 fill:#98fb98
    style HITL1 fill:#ffe4b5
    style HITL2 fill:#ffe4b5
```

## Deployment e Scaling Strategy

### Blocco Email (SP01-SP02)
- **SP01**: 2-4 replicas (light parsing)
- **SP02**: 6-12 replicas (OCR intensivo, GPU-ready)
- **Priorità**: Alta (gateway del sistema)

### Blocco AI (SP03-SP08)
- **SP03**: 4-6 replicas (classificazione frequente)
- **SP04**: 2-3 replicas (caching normativa)
- **SP05**: 3-5 replicas (GPT-4 con rate limiting)
- **SP06/SP08**: 2 replicas (validazione lightweight)
- **Priorità**: Critica (core business)

### Blocco Sistema (SP09-SP11)
- **SP09**: 2 replicas (orchestrator stateful)
- **SP10**: 3-5 replicas (frontend scaling)
- **SP11**: 2 replicas (audit write-heavy)
- **Priorità**: Media (supporto)

## Decision Tree: Quale Blocco Scala?

```mermaid
flowchart TD
    Start{Problema<br/>Performance?}
    
    Start -->|Lentezza upload| EmailBlock[Scala SP01-SP02]
    Start -->|Generazione lenta| AIBlock[Scala SP03-SP08]
    Start -->|Dashboard lag| SysBlock[Scala SP10]
    Start -->|Audit overflow| SysBlock2[Scala SP11]
    
    EmailBlock --> CheckOCR{OCR<br/>bottleneck?}
    CheckOCR -->|Sì| ScaleSP02[+GPU + replicas SP02]
    CheckOCR -->|No| ScaleSP01[+replicas SP01]
    
    AIBlock --> CheckPhase{Quale<br/>fase?}
    CheckPhase -->|Classificazione| ScaleSP03[+replicas SP03]
    CheckPhase -->|RAG| ScaleSP04[+cache + sharding SP04]
    CheckPhase -->|Generazione| ScaleSP05[+rate limit GPT-4]
    
    SysBlock --> ScaleSP10[+replicas SP10 + CDN]
    SysBlock2 --> ScaleSP11[+DB sharding SP11]
    
    style Start fill:#ffd700
    style EmailBlock fill:#ffb6c1
    style AIBlock fill:#87ceeb
    style SysBlock fill:#98fb98
    style SysBlock2 fill:#98fb98
```

## ROI per Blocco

| Blocco | Investimento | Risparmio Annuo | ROI | Priorità |
|--------|-------------|-----------------|-----|----------|
| **EMAIL (SP01-SP02)** | 15K€ (dev OCR) | 120K€ (no trascrizione) | **800%** | 🔴 Critica |
| **AI (SP03-SP08)** | 45K€ (licenze AI) | 200K€ (automazione) | **444%** | 🔴 Critica |
| **SYSTEM (SP09-SP11)** | 30K€ (infra) | 80K€ (audit compliance) | **267%** | 🟡 Alta |
| **TOTALE** | 90K€ | 400K€ | **444%** | 12 mesi payback |

---

## Conclusione: Perché 3 Blocchi?

1. **📧 EMAIL**: Risolve il problema dell'input eterogeneo (PEC nativa)
2. **🤖 AI**: Applica intelligenza al dominio PA (normativa + linguaggio)
3. **🏛️ SYSTEM**: Garantisce compliance e governance (AgID/GDPR)

**Il valore**: Trasformare la PA da "ufficio protocollo" a **"piattaforma digitale intelligente"** in grado di processare 80+ email PEC al giorno con qualità certificata e tracciabilità completa.

**Prossimi step**:
1. Pilota SP01-SP02 su 50 email reali
2. A/B test SP03-SP05 vs generazione manuale
3. Audit SP11 per certificazione AgID
