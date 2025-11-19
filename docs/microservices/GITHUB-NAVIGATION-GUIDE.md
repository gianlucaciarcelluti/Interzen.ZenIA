# GitHub Navigation Guide - Migliorare Anchor Links

**Navigazione**: [← BREADCRUMB-NAVIGATION.md](BREADCRUMB-NAVIGATION.md) | [GITHUB-NAVIGATION-GUIDE](GITHUB-NAVIGATION-GUIDE.md)

## Indice

1. [Il Problema con Anchor su GitHub](#il-problema-con-anchor-su-github)
2. [Tabella di Contenuti Manuale](#tabella-di-contenuti-toc-manuale)
3. [Anchor Rules - Esempi Pratici](#anchor-rules---esempi-pratici)
4. [Pattern TOC per Microservizi](#pattern-toc-per-microservizi)
5. [Testing Anchor Links](#testing-anchor-links)
6. [Advanced: Anchor con Sottosezioni](#advanced-anchor-con-sottosezioni)
7. [Implementazione Rapida](#implementazione-rapida)
8. [Template Completo](#template-completo---specmd)
9. [Pro Tips](#pro-tips)
10. [Link Rapidi di Riferimento](#link-rapidi-di-riferimento)

---

## 🎯 Il Problema con Anchor su GitHub

Quando scrivi documenti Markdown su GitHub, gli anchor link hanno un comportamento specifico:

**❌ Non funziona:**
```markdown
[Link a sezione](#My Section)
```

**✅ Funziona:**
```markdown
[Link a sezione](#my-section)
```

**Regole GitHub Anchor:**
- Tutti i caratteri MINUSCOLI
- Spazi → trattini `-`
- Niente simboli speciali `()[]{}@#$%&`
- Niente emoji (vengono ignorati)
- Numero e punti rimangono

[↑ Torna al Indice](#indice)

---

## 📋 Tabella di Contenuti (TOC) Manuale

GitHub **non genera automaticamente** il TOC, quindi lo facciamo manualmente:

### Template TOC Standard

```markdown
# Documento Lungo

## Indice

1. [Sezione 1](#sezione-1)
2. [Sezione 2](#sezione-2)
3. [Sezione 3](#sezione-3)
4. [Sezione 4](#sezione-4)

---

## Sezione 1

Contenuto sezione 1...

---

## Sezione 2

Contenuto sezione 2...

---

## Sezione 3

Contenuto sezione 3...

---

## Sezione 4

Contenuto sezione 4...

---

[Torna al Indice](#indice)
```

[↑ Torna al Indice](#indice)

---

## 🔗 Anchor Rules - Esempi Pratici

### Heading → Anchor Mapping

| Heading | Anchor |
|---------|--------|
| `## Getting Started` | `#getting-started` |
| `## Setup Local Environment` | `#setup-local-environment` |
| `## API Endpoints` | `#api-endpoints` |
| `## Troubleshooting Common Issues` | `#troubleshooting-common-issues` |
| `## MS01-CLASSIFIER Setup` | `#ms01-classifier-setup` |
| `## v1.0 Release Notes` | `#v10-release-notes` |
| `## Why 2-3 weeks?` | `#why-2-3-weeks` |

### ❌ Errori Comuni

| Heading | ❌ SBAGLIATO | ✅ CORRETTO |
|---------|------------|-----------|
| `## Getting Started` | `#Getting-Started` | `#getting-started` |
| `## Setup Local` | `#Setup Local` | `#setup-local` |
| `## API v2.0` | `#API-v2.0` | `#api-v20` |
| `## Why?` | `#Why?` | `#why` |
| `## (Optional)` | `#(Optional)` | `#optional` |

[↑ Torna al Indice](#indice)

---

## 📐 Pattern TOC per Microservizi

### Per README.md (breve)

```markdown
# MS01-CLASSIFIER - README

**Navigazione**: [← MS-ARCHITECTURE-MASTER](../MS-ARCHITECTURE-MASTER.md) | [Next: SPECIFICATION →](SPECIFICATION.md)

## Quick Links

- [Cosa fa](#cosa-fa)
- [Setup rapido](#setup-rapido)
- [Primi test](#primi-test)
- [Prossimo passo](#prossimo-passo)

---

## Cosa Fa

[contenuto...]

---

## Setup Rapido

[contenuto...]

---

## Primi Test

[contenuto...]

---

## Prossimo Passo

[contenuto...]

---

**Navigazione**: [← MS-ARCHITECTURE-MASTER](../MS-ARCHITECTURE-MASTER.md) | [Next: SPECIFICATION →](SPECIFICATION.md)
```

### Per SPECIFICATION.md (lungo)

```markdown
# MS01-CLASSIFIER - SPECIFICATION

**Navigazione**: [← README.md](README.md) | [SPECIFICATION](SPECIFICATION.md) | [Next: API →](API.md)

## Indice

1. [Overview](#overview)
2. [Architettura](#architettura)
3. [Componenti](#componenti)
4. [Sequence Diagrams](#sequence-diagrams)
5. [Data Model](#data-model)
6. [Performance SLA](#performance-sla)
7. [Troubleshooting](#troubleshooting)

---

## Overview

[contenuto...]

[Torna al Indice](#indice)

---

## Architettura

[contenuto...]

[Torna al Indice](#indice)

---

## Componenti

[contenuto...]

[Torna al Indice](#indice)

---

## Sequence Diagrams

[contenuto...]

[Torna al Indice](#indice)

---

## Data Model

[contenuto...]

[Torna al Indice](#indice)

---

## Performance SLA

[contenuto...]

[Torna al Indice](#indice)

---

## Troubleshooting

[contenuto...]

[Torna al Indice](#indice)

---

**Navigazione**: [← README.md](README.md) | [SPECIFICATION](SPECIFICATION.md) | [Next: API →](API.md)
```

[↑ Torna al Indice](#indice)

---

## ✅ Testing Anchor Links

### Come Verificare su GitHub

1. **Apri il file su GitHub**
2. **Clicca su un heading** → GitHub genera il TOC automatico nel visualization
3. **Copia il link** che appare nell'URL
4. **Usa quel link** nei tuoi anchor

Esempio:
- Heading: `## Getting Started`
- URL diventa: `https://github.com/user/repo/blob/main/file.md#getting-started`
- Usa in anchor: `[Go to Getting Started](#getting-started)`

### Manual Test Checklist

- [ ] Ho creato un Indice/TOC
- [ ] Ogni link nel TOC inizia con `#`
- [ ] Testo anchor = heading ma MINUSCOLO
- [ ] Spazi sono sostituiti con `-`
- [ ] Niente simboli speciali
- [ ] Ho aggiunto "Torna al Indice" dopo sezioni lunghe
- [ ] Ho testato cliccando i link su GitHub

[↑ Torna al Indice](#indice)

---

## 🎨 Advanced: Anchor con Sottosezioni

Quando hai sezioni annidate:

```markdown
## Section 1

Contenuto...

### Sottosezione 1.1

Contenuto...

### Sottosezione 1.2

Contenuto...

## Section 2

Contenuto...
```

**Anchor per sottosezioni:**
- `## Section 1` → `#section-1`
- `### Sottosezione 1.1` → `#sottosezione-11`
- `### Sottosezione 1.2` → `#sottosezione-12`
- `## Section 2` → `#section-2`

**TOC con sottosezioni:**

```markdown
## Indice

1. [Section 1](#section-1)
   - [Sottosezione 1.1](#sottosezione-11)
   - [Sottosezione 1.2](#sottosezione-12)
2. [Section 2](#section-2)
```

[↑ Torna al Indice](#indice)

---

## 🚀 Implementazione Rapida

### Step 1: Aggiungi TOC all'inizio

Dopo il titolo, metti l'indice:

```markdown
# My Document

## Indice

- [Sezione A](#sezione-a)
- [Sezione B](#sezione-b)
- [Sezione C](#sezione-c)

---
```

### Step 2: Usa heading consistenti

```markdown
## Sezione A
Contenuto...

## Sezione B
Contenuto...

## Sezione C
Contenuto...
```

### Step 3: Aggiungi "Back to TOC"

Dopo sezioni lunghe:

```markdown
## Sezione A

Contenuto lungo...

[↑ Torna al Indice](#indice)

---

## Sezione B
```

### Step 4: Testa su GitHub

1. Vai al repo su GitHub
2. Apri il file
3. Clicca su un heading
4. Verifica che il link funziona

[↑ Torna al Indice](#indice)

---

## 📝 Template Completo - SPEC.md

```markdown
# MS01-CLASSIFIER - SPECIFICATION

**Navigazione**: [← README.md](README.md) | [SPECIFICATION](SPECIFICATION.md) | [API →](API.md)

## Indice

1. [Overview](#overview)
2. [Architettura](#architettura)
3. [Sequence Diagrams](#sequence-diagrams)
4. [Performance](#performance)

---

## Overview

Descrizione generale...

[↑ Torna al Indice](#indice)

---

## Architettura

Dettagli architettura...

### Componenti

Descrizione componenti...

### ER Diagram

Diagrama...

[↑ Torna al Indice](#indice)

---

## Sequence Diagrams

Sequence diagrams...

### Happy Path

Diagram...

### Error Scenario

Diagram...

[↑ Torna al Indice](#indice)

---

## Performance

SLA details...

[↑ Torna al Indice](#indice)

---

**Navigazione**: [← README.md](README.md) | [SPECIFICATION](SPECIFICATION.md) | [API →](API.md)
```

[↑ Torna al Indice](#indice)

---

## 💡 Pro Tips

1. **Minuscoli sempre** - GitHub è strict con minuscoli/maiuscoli
2. **Niente emojis negli anchor** - Emoji non funzionano negli anchor
3. **Usa underscore per parole** - `#getting_started` vs `#getting-started` (dipende da GitHub)
4. **Test subito** - Non aspettare il merge, testa in preview
5. **Consistent spacing** - Un'unica forma di anchor per il progetto

[↑ Torna al Indice](#indice)

---

## 🔗 Link Rapidi di Riferimento

- [GitHub: Creating and highlighting code blocks](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#links)
- [Markdown: Creating internal links](https://www.markdownguide.org/extended-syntax/#linking-to-heading-ids)

---

**Creato**: 2024-11-18
**Status**: Guida di riferimento
**Uso**: Copia i pattern nei tuoi documenti per migliorare navigazione

[↑ Torna al Indice](#indice)

---

**Navigazione**: [← BREADCRUMB-NAVIGATION.md](BREADCRUMB-NAVIGATION.md) | [GITHUB-NAVIGATION-GUIDE](GITHUB-NAVIGATION-GUIDE.md)
