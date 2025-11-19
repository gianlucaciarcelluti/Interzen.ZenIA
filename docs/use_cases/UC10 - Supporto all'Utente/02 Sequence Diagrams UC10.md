# 02 Sequence Diagrams UC10

## Support Request Flow

```mermaid
sequenceDiagram
    participant U as User
    participant SP as Self-Service Portal
    participant VA as Virtual Assistant
    participant KB as Knowledge Base
    participant HD as Help Desk
    participant AG as Agent
    participant FB as Feedback System

    U->>SP: Access portal
    SP->>U: Display dashboard

    U->>SP: Search for help
    SP->>KB: Query knowledge base
    KB-->>SP: Return results
    SP->>U: Display search results

    U->>VA: Start chat
    VA->>U: Greeting & context gathering

    U->>VA: Describe issue
    VA->>VA: Intent recognition
    VA->>KB: Check for solutions
    KB-->>VA: Return relevant articles

    alt Solution found
        VA->>U: Provide solution
        U->>VA: Confirm resolution
        VA->>FB: Request feedback
        U->>FB: Rate experience
    else No solution
        VA->>HD: Create ticket
        HD->>AG: Assign to agent
        AG->>U: Contact for resolution
        AG->>U: Resolve issue
        AG->>FB: Request feedback
        U->>FB: Provide feedback
    end
```

## Ticket Resolution Flow

```mermaid
sequenceDiagram
    participant U as User
    participant HD as Help Desk System
    participant RT as Routing Engine
    participant AG as Agent
    participant KB as Knowledge Base
    participant SA as Support Analytics
    participant FB as Feedback System

    U->>HD: Submit ticket
    HD->>RT: Route ticket
    RT->>RT: Analyze priority & category
    RT->>HD: Assign to queue

    HD->>AG: Notify agent
    AG->>HD: Accept ticket
    AG->>KB: Research solution
    KB-->>AG: Provide knowledge

    AG->>U: Contact user
    U->>AG: Provide details
    AG->>AG: Work on resolution

    AG->>HD: Update ticket status
    HD->>SA: Record metrics

    AG->>U: Deliver solution
    U->>AG: Confirm resolution

    AG->>HD: Close ticket
    HD->>FB: Trigger feedback survey
    FB->>U: Send survey
    U->>FB: Complete survey

    FB->>SA: Send feedback data
    SA->>SA: Update analytics
```

## Knowledge Base Management Flow

```mermaid
sequenceDiagram
    participant AU as Author/Content Creator
    participant KB as Knowledge Base
    participant RV as Review System
    participant AP as Approval Workflow
    participant PB as Publishing System
    participant SR as Search Engine
    participant US as Users

    AU->>KB: Create new article
    KB->>AU: Article template

    AU->>KB: Submit draft
    KB->>RV: Send for review
    RV->>RV: Automated checks
    RV->>AP: Route for approval

    AP->>AP: Approval workflow
    AP->>PB: Approve for publishing

    PB->>KB: Publish article
    KB->>SR: Update search index
    SR->>SR: Re-index content

    US->>SR: Search knowledge
    SR->>US: Return results
    US->>KB: Access article

    KB->>KB: Track usage metrics
    KB->>AU: Send usage analytics
```

## Virtual Assistant Interaction Flow

```mermaid
sequenceDiagram
    participant U as User
    participant VA as Virtual Assistant
    participant NLP as NLP Engine
    participant DM as Dialog Manager
    participant KB as Knowledge Base
    participant WF as Workflow Engine
    participant HD as Help Desk

    U->>VA: Send message
    VA->>NLP: Process text
    NLP->>NLP: Tokenize & analyze
    NLP-->>VA: Intent & entities

    VA->>DM: Get next action
    DM->>DM: Update context
    DM-->>VA: Response strategy

    alt Knowledge query
        VA->>KB: Search knowledge
        KB-->>VA: Return articles
        VA->>U: Provide information
    else Workflow start
        VA->>WF: Initiate workflow
        WF-->>VA: First step
        VA->>U: Request information
    else Escalation needed
        VA->>HD: Create ticket
        HD-->>VA: Ticket created
        VA->>U: Confirm ticket creation
    end

    VA->>VA: Update conversation state
    VA->>U: Send response
```

## Self-Service Portal Flow

```mermaid
sequenceDiagram
    participant U as User
    participant SP as Self-Service Portal
    participant SC as Service Catalog
    participant WF as Workflow Engine
    participant KB as Knowledge Base
    participant FB as Feedback System

    U->>SP: Login to portal
    SP->>SP: Load user preferences
    SP->>U: Display personalized dashboard

    U->>SC: Browse services
    SC->>SC: Filter & search
    SC-->>U: Display service catalog

    U->>SC: Select service
    SC->>WF: Check prerequisites
    WF-->>SC: Prerequisites met

    SC->>WF: Start guided workflow
    WF->>U: First step form
    U->>WF: Submit form data

    loop Workflow steps
        WF->>WF: Process step
        WF->>U: Next step or completion
    end

    WF->>U: Workflow completed
    WF->>FB: Trigger satisfaction survey
    FB->>U: Send survey

    U->>FB: Complete survey
    FB->>SP: Update user experience
```

## Training Platform Flow

```mermaid
sequenceDiagram
    participant U as User
    participant TP as Training Platform
    participant UP as User Profiling
    participant LP as Learning Path Engine
    participant CM as Course Management
    participant AS as Assessment Engine
    participant CE as Certification Engine

    U->>TP: Access training portal
    TP->>UP: Assess user profile
    UP->>UP: Analyze skills & preferences
    UP-->>TP: User profile

    TP->>LP: Generate learning path
    LP->>LP: Match courses to profile
    LP-->>TP: Recommended path

    U->>CM: Enroll in course
    CM->>CM: Check prerequisites
    CM-->>U: Enrollment confirmed

    U->>CM: Start learning module
    CM->>CM: Track progress
    U->>CM: Complete module

    CM->>AS: Trigger assessment
    AS->>U: Present questions
    U->>AS: Submit answers

    AS->>AS: Grade assessment
    AS-->>U: Results & feedback

    alt Assessment passed
        CM->>CE: Issue certificate
        CE-->>U: Digital certificate
    else Assessment failed
        CM->>U: Remediation path
    end
```

## Support Analytics Flow

```mermaid
sequenceDiagram
    participant SY as Support Systems
    participant RA as Real-Time Analytics
    participant PA as Predictive Analytics
    participant BI as Business Intelligence
    participant DB as Dashboard
    participant RP as Report Engine
    participant MG as Management

    SY->>RA: Generate events
    RA->>RA: Process in real-time
    RA->>RA: Update metrics

    RA->>PA: Feed historical data
    PA->>PA: Train models
    PA->>PA: Generate predictions

    DB->>BI: Request dashboard data
    BI->>RA: Get real-time metrics
    BI->>PA: Get predictions
    BI-->>DB: Compiled dashboard

    MG->>RP: Request report
    RP->>BI: Gather data
    RP->>RP: Generate report
    RP-->>MG: Deliver report

    RA->>RA: Detect anomalies
    RA->>SY: Trigger alerts
```

## Feedback Management Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FC as Feedback Collection
    participant SA as Sentiment Analysis
    participant FP as Feedback Processing
    participant AM as Action Management
    participant HD as Help Desk
    participant KB as Knowledge Base

    U->>FC: Provide feedback
    FC->>FC: Collect via multiple channels
    FC->>SA: Send for analysis

    SA->>SA: Analyze sentiment & intent
    SA-->>FC: Analysis results

    FC->>FP: Process feedback
    FP->>FP: Categorize & prioritize
    FP->>AM: Determine actions

    AM->>AM: Route actions
    AM->>HD: Create tickets (if needed)
    AM->>KB: Update knowledge (if needed)
    AM->>U: Send responses (if needed)

    FP->>FP: Track action completion
    FP->>FC: Update feedback status
```

## Integration Flow UC10 Components

```mermaid
sequenceDiagram
    participant U as User
    participant SP as Self-Service Portal
    participant VA as Virtual Assistant
    participant HD as Help Desk
    participant KB as Knowledge Base
    participant TP as Training Platform
    participant SA as Support Analytics
    participant FB as Feedback Management

    U->>SP: Access support
    SP->>VA: Route to assistant
    VA->>KB: Query knowledge
    KB-->>VA: Return solutions

    VA->>HD: Escalate if needed
    HD->>HD: Process ticket
    HD->>TP: Recommend training

    HD->>SA: Send metrics
    SA->>SA: Analyze performance

    HD->>FB: Collect feedback
    FB->>FB: Process & analyze
    FB->>KB: Update knowledge base
    FB->>HD: Trigger improvements

    SA->>SP: Update portal content
    SA->>VA: Improve responses
    SA->>HD: Optimize routing
```</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC10 - Supporto all'Utente/02 Sequence Diagrams UC10.md