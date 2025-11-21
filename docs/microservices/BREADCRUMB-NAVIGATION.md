# Breadcrumb Navigation - Navigazione tra Documenti

Questo file fornisce link di navigazione da aggiungere in testa/fondo a ogni documento per facilitare la navigazione.

---

## 📍 Pattern Breadcrumb

Ogni documento ha questa struttura:

```markdown
**Navigazione**: [← Parent Doc](../path/to/parent.md) | [Document Title](link) | [Next Doc](path/to/next.md) →
```

Oppure per documenti nello stesso livello:

```markdown
**Back**: [← MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md)
**Home**: [📚 README](../README.md)
```

---

## 🗂️ Breadcrumb per Ogni Documento

### Livello Root: /docs/microservices/

#### MS-ARCHITECTURE-MASTER.md
```markdown
**Navigazione**: [← README](../README.md) | [MS-ARCHITECTURE-MASTER](MS-ARCHITECTURE-MASTER.md) | [DEVELOPER-WORKFLOW](DEVELOPER-WORKFLOW.md) →
```

#### DEVELOPER-WORKFLOW.md
```markdown
**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](MS-ARCHITECTURE-MASTER.md) | [DEVELOPER-WORKFLOW](DEVELOPER-WORKFLOW.md) | [DEVELOPMENT-GUIDE](../DEVELOPMENT-GUIDE.md) →
```

### Livello MS01: /docs/microservices/MS01-CLASSIFIER/

#### MS01-CLASSIFIER/README.md
```markdown
**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](../MS-ARCHITECTURE-MASTER.md) | [README](README.md) | [SPECIFICATION →](SPECIFICATION.md)
```

#### MS01-CLASSIFIER/SPECIFICATION.md
```markdown
**Navigazione**: [← README.md](README.md) | [SPECIFICATION](SPECIFICATION.md) | [API →](API.md)
```

#### MS01-CLASSIFIER/API.md
```markdown
**Navigazione**: [← SPECIFICATION.md](SPECIFICATION.md) | [API](API.md) | [DATABASE-SCHEMA →](DATABASE-SCHEMA.md)
```

#### MS01-CLASSIFIER/DATABASE-SCHEMA.md
```markdown
**Navigazione**: [← API.md](API.md) | [DATABASE-SCHEMA](DATABASE-SCHEMA.md) | [TROUBLESHOOTING →](TROUBLESHOOTING.md)
```

#### MS01-CLASSIFIER/TROUBLESHOOTING.md
```markdown
**Navigazione**: [← DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [TROUBLESHOOTING](TROUBLESHOOTING.md) | [Back to MS →](../MS-ARCHITECTURE-MASTER.md#ms01--classifier)
```

---

## 🔄 Navigation Loop Pattern

```
docs/
├── README.md
├── ARCHITECTURE-OVERVIEW.md
├── DEVELOPMENT-GUIDE.md
├── COMPLIANCE-MATRIX.md
│
└── microservices/
    ├── MS-ARCHITECTURE-MASTER.md ⭐ Entry Point
    ├── DEVELOPER-WORKFLOW.md
    ├── BREADCRUMB-NAVIGATION.md (questo file)
    │
    └── MS01-CLASSIFIER/
        ├── README.md (5 min)
        ├── SPECIFICATION.md (30 min)
        ├── API.md (reference)
        ├── DATABASE-SCHEMA.md (reference)
        ├── TROUBLESHOOTING.md
        ├── docker-compose.yml
        ├── kubernetes/
        └── examples/
```

**Navigation Flow:**
1. Start: README.md → microservices/MS-ARCHITECTURE-MASTER.md
2. Learn: DEVELOPER-WORKFLOW.md
3. Pick MS: MS01-CLASSIFIER/README.md
4. Read sequence: README → SPECIFICATION → API → DATABASE-SCHEMA → TROUBLESHOOTING
5. Back to start: ← MS-ARCHITECTURE-MASTER.md

---

## 📋 Breadcrumb Templates (Copy-Paste)

### Template 1: Sequential (README → SPEC → API → DB → TROUBLESHOOTING)

```markdown
**Navigazione**: [← MS-ARCHITECTURE-MASTER.md](../MS-ARCHITECTURE-MASTER.md) | [README](README.md) | [SPECIFICATION →](SPECIFICATION.md)
**Navigazione**: [← README.md](README.md) | [SPECIFICATION](SPECIFICATION.md) | [API →](API.md)
**Navigazione**: [← SPECIFICATION.md](SPECIFICATION.md) | [API](API.md) | [DATABASE-SCHEMA →](DATABASE-SCHEMA.md)
**Navigazione**: [← API.md](API.md) | [DATABASE-SCHEMA](DATABASE-SCHEMA.md) | [TROUBLESHOOTING →](TROUBLESHOOTING.md)
**Navigazione**: [← DATABASE-SCHEMA.md](DATABASE-SCHEMA.md) | [TROUBLESHOOTING](TROUBLESHOOTING.md) | [Indietro →](../MS-ARCHITECTURE-MASTER.md)
```

### Template 2: Home Always Visible

```markdown
[🏠 Home](../MS-ARCHITECTURE-MASTER.md) > [MS01](../MS-ARCHITECTURE-MASTER.md#ms01) > [README](README.md)
```

### Template 3: Quick Links

```markdown
**Salta a**: [API](API.md) | [Examples](examples/) | [Setup](docker-compose.yml) | [Deploy](kubernetes/)
```

---

## 💡 Pro Tips for GitHub Navigation

1. **Use GitHub's breadcrumb** - GitHub mostra il path dei file
2. **Pin questo file** - BREADCRUMB-NAVIGATION.md in ogni MS folder
3. **Consistent naming** - Sempre stesso ordine: README → SPECIFICATION → API → DB → TROUBLESHOOTING
4. **Emoji per chiarezza**:
   - 📘 = README/intro
   - 🔧 = SPECIFICATION/technical
   - 🔌 = API
   - 💾 = DATABASE
   - 🐛 = TROUBLESHOOTING
   - ← = Previous
   - → = Next
   - 🏠 = Home

---

## 🔗 Anchor Navigation (GitHub-Compatible)

GitHub genera automaticamente anchor da heading:

```markdown
## My Section

# Referenziare la sezione:
[Vai a My Section](#my-section)
```

**Esempi pratici:**
```markdown
[Torna a Microservizi Disponibili](MS-ARCHITECTURE-MASTER.md#microservizi-disponibili)
[Vedi Pattern Dati](MS-ARCHITECTURE-MASTER.md#pattern-dati)
[Workflow Operativo](DEVELOPER-WORKFLOW.md#il-tuo-workflow-in-70-minuti)
```

---

## 📌 Breadcrumb Position

Mettere breadcrumb in **due posti**:

### Top of File (Subito dopo titolo)
```markdown
# Document Title

**Navigazione**: [← Previous](previous.md) | [This Doc](current.md) | [Next →](next.md)

---

## Contenuto del documento...
```

### Bottom of File (Prima di EOF)
```markdown
...

---

**Navigazione**: [← Previous](previous.md) | [This Doc](current.md) | [Next →](next.md)
```

---

## ✅ Checklist di Implementazione

Per ogni MSxx folder:

- [ ] README.md ha breadcrumb a top e bottom
- [ ] SPECIFICATION.md ha breadcrumb a top e bottom
- [ ] API.md ha breadcrumb a top e bottom
- [ ] DATABASE-SCHEMA.md ha breadcrumb a top e bottom
- [ ] TROUBLESHOOTING.md ha breadcrumb a top e bottom
- [ ] Tutti i link sono relativi (../../ per salire di livello)
- [ ] Testato su GitHub che i link funzionano
- [ ] Uso lo stesso pattern per tutti i MS (MS01-MS16)

---

## 🚀 Come Implementare

1. **Copia il template** che corrisponde al tuo documento
2. **Sostituisci i nomi** con i tuoi (es: MS02 al posto di MS01)
3. **Aggiungi in top e bottom** di ogni documento
4. **Verifica i link** funzionino su GitHub

Esempio per MS02-ANALYZER/API.md:

```markdown
# MS02-ANALYZER API Reference

**Navigazione**: [← SPECIFICATION.md](SPECIFICATION.md) | [API](API.md) | [DATABASE-SCHEMA →](DATABASE-SCHEMA.md)

## Endpoints

[contenuto del file...]

---

**Navigazione**: [← SPECIFICATION.md](SPECIFICATION.md) | [API](API.md) | [DATABASE-SCHEMA →](DATABASE-SCHEMA.md)
```

---

**Creato**: 2024-11-18
**Status**: Template di riferimento
**Uso**: Copia-incolla i pattern in ogni documento
