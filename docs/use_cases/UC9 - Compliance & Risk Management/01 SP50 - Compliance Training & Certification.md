# SP50 - Compliance Training & Certification Platform

## Descrizione Componente

Il **SP50 Compliance Training & Certification Platform** gestisce la formazione e certificazione sulla conformità normativa. Fornisce percorsi di apprendimento personalizzati, verifica della comprensione e tracking dello stato di compliance del personale organizzato per ruoli e normative applicabili.

## Responsabilità

- **Training Content Management**: Gestione corsi, moduli, video, quiz
- **Personalized Learning Paths**: Percorsi formativi su misura per ruolo/normativa
- **Assessment & Certification**: Test di valutazione e certificazione
- **Compliance Tracking**: Monitoraggio dello stato di compliance per persona
- **Expiration Management**: Gestione scadenze certificazioni
- **Regulatory Updates**: Aggiornamenti automatici contenuti quando normativa cambia
- **Reporting & Analytics**: Dashboard compliance del personale

## Architettura Interna

```
┌─────────────────────────────────────────────────────────────┐
│            TRAINING MANAGEMENT LAYER                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Content Manager    Learning Path Engine    Assessment   ││
│  │ ┌──────────────┐    ┌──────────────────┐  ┌──────────┐ ││
│  │ │ - Courses    │    │ - Personalization│  │ - Quiz   │ ││
│  │ │ - Modules    │    │ - Progress Track │  │ - Exam   │ ││
│  │ │ - Media      │    │ - Recommendations│  │ - Certif.│ ││
│  │ │ - Meta       │    │ - Time Mgmt      │  │ - Badges │ ││
│  │ └──────────────┘    └──────────────────┘  └──────────┘ ││
└─────────────────────────────────────────────────────────────┘
│            GOVERNANCE & COMPLIANCE LAYER                    │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Expiration Tracker   Update Manager      Analytics      ││
│  │ ┌──────────────────┐ ┌────────────────┐  ┌──────────┐  ││
│  │ │ - Expiry Check   │ │ - Auto Update  │  │ - Status │  ││
│  │ │ - Notifications  │ │ - Publish      │  │ - Reports│  ││
│  │ │ - Reminders      │ │ - Version      │  │ - Trends │  ││
│  │ │ - Enforcement    │ │ - Compliance   │  │ - KPIs   │  ││
│  │ └──────────────────┘ └────────────────┘  └──────────┘  ││
└─────────────────────────────────────────────────────────────┘
│                    DATA LAYER                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ PostgreSQL        Elasticsearch      Redis              ││
│  │ ┌────────────────┐ ┌────────────────┐ ┌────────────┐   ││
│  │ │ - Courses      │ │ - Search       │ │ - Progress │   ││
│  │ │ - Enrollments  │ │ - Indexing     │ │ - Session  │   ││
│  │ │ - Assessments  │ │ - Analytics    │ │ - Certs    │   ││
│  │ │ - Certs        │ │ - Full Text    │ │ - Cache    │   ││
│  │ └────────────────┘ └────────────────┘ └────────────┘   ││
└─────────────────────────────────────────────────────────────┘
```

## Input/Output

### Input
- **Course Content**: Corsi, moduli, video, quiz da Learning Management System
- **User Profiles**: Dati utenti con ruoli, dipartimenti, normative applicabili
- **Regulatory Rules**: Regole quali-normative richiedono quale training
- **Assessment Templates**: Modelli per test e certificazioni
- **Compliance Calendar**: Calendario scadenze normative

### Output
- **Training Assignments**: Percorsi formativi assegnati personalmente
- **Assessment Results**: Risultati test e certificazioni
- **Compliance Certificates**: Certificati completamento
- **Compliance Reports**: Report stato compliance organizzazione
- **Expiration Alerts**: Notifiche scadenze prossime

## Dipendenze

### Upstream
```
SP42 (Policy Engine) → SP50
  Data: Policy requirements per ruolo/normativa
  Timing: On policy update
  SLA: Training path update < 1 hour

SP49 (Risk Registry) → SP50
  Data: Risk mitigation training requirements
  Timing: On risk assessment
  SLA: Training recommendation < 30 min
```

### Downstream
```
SP50 → SP10 (Dashboard)
  Data: Compliance training metrics, status
  Timing: Real-time
  SLA: < 500ms

SP50 → Compliance Reports
  Data: Certification proof, completion status
  Timing: On-demand / daily
  SLA: Report < 1 min
```

## Stack Tecnologico

| Componente | Tecnologia | Versione | Scopo |
|-----------|-----------|----------|-------|
| Language | Python | 3.11 | Core implementation |
| API | FastAPI | 0.104+ | REST endpoints |
| Frontend | React/Vue | Latest | Learning portal |
| Database | PostgreSQL | 15+ | Course, enrollments |
| Search | Elasticsearch | 8.10+ | Course search |
| Cache | Redis | 7.2+ | Session, caching |
| Video | Mux/Vimeo | API | Video hosting |
| Email | SendGrid | API | Notifications |
| PDF | ReportLab | Latest | Certificates |

## API Endpoints

**GET /api/v1/training/courses**
```
Response:
{
  "courses": [
    {
      "id": "course_123",
      "title": "GDPR Compliance Basics",
      "description": "...",
      "duration_hours": 2.5,
      "level": "beginner",
      "target_roles": ["manager", "analyst"],
      "regulatory_standard": "GDPR",
      "modules": 5,
      "enrollment_count": 234
    }
  ]
}
```

**POST /api/v1/training/enroll**

Request:
```json
{
  "user_id": "user_456",
  "course_id": "course_123",
  "due_date": "2025-12-31",
  "mandatory": true
}
```

Response:
```json
{
  "enrollment_id": "enr_789",
  "progress": 0,
  "status": "in_progress",
  "deadline": "2025-12-31"
}
```

**POST /api/v1/training/assessment/submit**

Request:
```json
{
  "user_id": "user_456",
  "assessment_id": "assess_111",
  "answers": [{"question_id": "q1", "answer": "b"}],
  "submission_time": 1500
}
```

Response:
```json
{
  "assessment_id": "assess_111",
  "score": 92,
  "passed": true,
  "certificate_issued": true,
  "certificate_id": "cert_222",
  "valid_until": "2026-12-31"
}
```

**GET /api/v1/training/compliance-status**
```
Response:
{
  "user_id": "user_456",
  "overall_compliance": 87,
  "courses_required": 12,
  "courses_completed": 10,
  "certifications": [
    {
      "name": "GDPR",
      "status": "certified",
      "valid_until": "2025-12-31",
      "days_until_expiry": 44
    }
  ],
  "overdue_trainings": [
    {
      "course_name": "Data Protection Advanced",
      "due_date": "2025-11-10",
      "days_overdue": 7
    }
  ]
}
```

## Database Schema

```sql
CREATE TABLE training_courses (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255),
  description TEXT,
  duration_minutes INT,
  content_type VARCHAR(50),  -- video, interactive, text, quiz
  regulatory_standard VARCHAR(100),  -- GDPR, CAD, eIDAS
  target_roles JSONB,
  modules JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ,
  INDEX idx_regulatory_standard (regulatory_standard)
);

CREATE TABLE user_enrollments (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255),
  course_id INT REFERENCES training_courses(id),
  enrolled_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  due_date DATE,
  status VARCHAR(20),  -- in_progress, completed, overdue, failed
  progress_percentage INT,
  completion_proof JSONB,
  INDEX idx_user_id (user_id),
  INDEX idx_status (status),
  INDEX idx_due_date (due_date)
);

CREATE TABLE assessments (
  id SERIAL PRIMARY KEY,
  course_id INT REFERENCES training_courses(id),
  assessment_type VARCHAR(50),  -- quiz, exam, practical
  questions JSONB,
  passing_score INT,
  certification_validity_days INT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE assessment_results (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255),
  assessment_id INT REFERENCES assessments(id),
  score INT,
  passed BOOLEAN,
  certificate_id VARCHAR(255),
  submitted_at TIMESTAMPTZ DEFAULT NOW(),
  valid_until DATE,
  INDEX idx_user_id (user_id),
  INDEX idx_certificate_id (certificate_id)
);

CREATE TABLE compliance_certificates (
  id SERIAL PRIMARY KEY,
  certificate_id VARCHAR(255) UNIQUE,
  user_id VARCHAR(255),
  course_id INT,
  assessment_id INT,
  issued_at TIMESTAMPTZ DEFAULT NOW(),
  valid_until DATE,
  content BYTEA,  -- PDF certificate
  INDEX idx_user_id (user_id),
  INDEX idx_valid_until (valid_until)
);
```

## Performance & KPIs

| Metrica | Target |
|---------|--------|
| **Course Load Time** | < 2 sec |
| **Assessment Response** | < 500ms |
| **Certificate Generation** | < 10 sec |
| **Report Generation** | < 30 sec |
| **Compliance Coverage** | > 95% of staff |
| **Average Completion Time** | Per course defined |
| **Assessment Pass Rate** | > 80% |

## Security & Compliance

- **Data Protection**: GDPR-compliant data handling
- **Access Control**: Role-based access to courses/certifications
- **Audit Trail**: Complete logging of all training activities
- **Certificate Authenticity**: Digital signatures on certificates
- **Platform Security**: SOC 2 Type II compliance

## Testing Strategy

- **Unit**: Course management, assessment logic (> 85% coverage)
- **Integration**: Enrollment → assessment → certification pipeline
- **E2E**: Full user learning journey (login → course → exam → cert)
- **Load**: Support 10,000+ concurrent learners
- **Compliance**: Validate certificate validity and audit trail

## Implementazione Timeline

1. **Phase 1**: Basic course management + enrollment
2. **Phase 2**: Assessment engine + certification
3. **Phase 3**: Compliance tracking & reporting
4. **Phase 4**: AI-powered personalization + recommendations

---

**Associato a**: UC9 - Compliance & Risk Management
**MS Primario**: MS12 Generic User Interface
**MS Supporto**: MS06 Knowledge Base, MS10 Analytics
**Status**: In Design
**Created**: 2025-11-17
