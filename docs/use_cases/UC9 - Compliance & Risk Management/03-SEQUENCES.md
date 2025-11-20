# 01 Sequence diagrams

## Regulatory Change Management Process Flow

```mermaid
sequenceDiagram
    participant RS as Regulatory Sources
    participant SA as Source Aggregator
    participant CD as Change Detector
    participant IA as Impact Analyzer
    participant AP as Action Planner
    participant RM as Resource Manager
    participant TM as Task Manager
    participant SM as Stakeholder Manager
    participant CM as Compliance Monitor

    Note over RS,CM: Regulatory Change Detection & Analysis Phase

    RS->>SA: New regulatory content
    SA->>SA: Aggregate & validate sources
    SA->>CD: Process regulatory updates
    CD->>CD: Detect changes vs baseline
    CD->>IA: Detected changes

    Note over IA,AP: Impact Assessment & Planning Phase

    IA->>IA: Analyze business impact
    IA->>IA: Calculate costs & timeline
    IA->>IA: Assess implementation risks
    IA->>AP: Impact analysis results

    AP->>AP: Decompose into tasks
    AP->>RM: Request resource allocation
    RM->>AP: Resource availability
    AP->>AP: Create implementation plan
    AP->>TM: Schedule tasks
    AP->>SM: Notify stakeholders

    Note over TM,CM: Implementation & Monitoring Phase

    TM->>TM: Execute tasks in order
    TM->>CM: Update compliance status
    CM->>CM: Monitor progress vs plan
    CM->>SM: Report status to stakeholders

    SM->>SM: Communicate with stakeholders
    SM->>AP: Request plan adjustments if needed
    AP->>TM: Update task schedule
```

## Compliance Gap Analysis Flow

```mermaid
sequenceDiagram
    participant RC as Regulatory Change
    participant GA as Gap Analyzer
    participant CA as Current Assessment
    participant RA as Risk Assessor
    participant PA as Prioritizer
    participant RP as Remediation Planner
    participant VM as Validation Manager

    RC->>GA: New regulatory requirement
    GA->>CA: Assess current compliance state
    CA->>GA: Current state analysis

    GA->>GA: Identify compliance gaps
    GA->>RA: Gap analysis results
    RA->>RA: Assess gap risks
    RA->>PA: Risk assessment

    PA->>PA: Prioritize remediation actions
    PA->>RP: Prioritized gaps
    RP->>RP: Plan remediation activities
    RP->>VM: Remediation plan

    VM->>VM: Validate remediation approach
    VM->>RP: Validation feedback
    RP->>GA: Final remediation plan
```

## Automated Compliance Monitoring Flow

```mermaid
sequenceDiagram
    participant DS as Data Sources
    participant CM as Compliance Monitor
    participant RE as Rule Engine
    participant AA as Anomaly Analyzer
    participant AM as Alert Manager
    participant RM as Response Manager
    participant LM as Learning Module

    DS->>CM: Business activity data
    CM->>RE: Evaluate against compliance rules
    RE->>CM: Compliance status

    CM->>AA: Analyze for anomalies
    AA->>AA: Detect compliance deviations
    AA->>AM: Anomaly alerts

    AM->>AM: Assess alert severity
    AM->>RM: High-priority alerts
    RM->>RM: Determine response actions
    RM->>CM: Execute automated responses

    CM->>LM: Learning feedback
    LM->>LM: Update compliance models
    LM->>RE: Improved rules
    LM->>AA: Enhanced anomaly detection
```

## Risk Assessment & Mitigation Flow

```mermaid
sequenceDiagram
    participant RA as Risk Analyzer
    participant QM as Quantitative Model
    participant SM as Scenario Modeler
    participant SA as Stress Analyzer
    participant MA as Mitigation Assessor
    participant PA as Plan Activator
    participant EM as Escalation Manager

    RA->>QM: Risk factors & data
    QM->>QM: Calculate quantitative risk metrics
    QM->>RA: Quantitative risk scores

    RA->>SM: Risk scenarios
    SM->>SM: Model risk scenarios
    SM->>SA: Scenario stress tests
    SA->>SA: Analyze stress impacts
    SA->>SM: Stress test results
    SM->>RA: Scenario risk analysis

    RA->>MA: Combined risk assessment
    MA->>MA: Evaluate mitigation options
    MA->>PA: Recommended mitigations
    PA->>PA: Activate mitigation plans

    PA->>EM: Escalation if needed
    EM->>EM: Manage risk escalation
    EM->>RA: Escalation feedback
```

## Compliance Intelligence Learning Cycle

```mermaid
sequenceDiagram
    participant CI as Compliance Intelligence
    participant DA as Data Aggregator
    participant ML as Machine Learning Engine
    participant PM as Pattern Miner
    participant RM as Recommendation Engine
    participant VM as Validation Module
    participant KM as Knowledge Manager

    CI->>DA: Collect compliance data
    DA->>DA: Aggregate historical & real-time data
    DA->>ML: Training datasets

    ML->>ML: Train compliance models
    ML->>PM: Trained models
    PM->>PM: Mine compliance patterns
    PM->>RM: Discovered patterns

    RM->>RM: Generate intelligence recommendations
    RM->>VM: Recommendations for validation
    VM->>VM: Validate recommendation accuracy
    VM->>KM: Validated intelligence

    KM->>KM: Update knowledge base
    KM->>CI: Enhanced compliance intelligence
    CI->>ML: Feedback for model improvement
```

## Regulatory Change Impact Propagation

```mermaid
sequenceDiagram
    participant RC as Regulatory Change
    participant IA as Impact Analyzer
    participant BA as Business Area A
    participant BB as Business Area B
    participant BC as Business Area C
    participant DM as Dependency Mapper
    participant CA as Cascade Analyzer
    participant RA as Risk Aggregator

    RC->>IA: Regulatory change details
    IA->>BA: Direct impact assessment
    IA->>BB: Direct impact assessment
    IA->>BC: Direct impact assessment

    BA->>DM: Affected dependencies
    BB->>DM: Affected dependencies
    BC->>DM: Affected dependencies

    DM->>CA: Dependency network
    CA->>CA: Analyze impact cascade
    CA->>RA: Cascading impacts

    RA->>RA: Aggregate total risk exposure
    RA->>IA: Comprehensive impact analysis
    IA->>RC: Final impact assessment
```

## Implementation Progress Tracking

```mermaid
sequenceDiagram
    participant IP as Implementation Plan
    participant TM as Task Monitor
    participant PM as Progress Manager
    participant QA as Quality Assessor
    participant RM as Risk Monitor
    participant CM as Change Manager
    participant SM as Status Manager

    IP->>TM: Task execution schedule
    TM->>PM: Task status updates
    PM->>PM: Calculate overall progress

    PM->>QA: Progress quality checks
    QA->>QA: Assess implementation quality
    QA->>PM: Quality metrics

    PM->>RM: Progress risk assessment
    RM->>RM: Monitor implementation risks
    RM->>CM: Risk mitigation if needed

    CM->>CM: Manage plan changes
    CM->>IP: Updated implementation plan
    IP->>TM: Revised task schedule

    PM->>SM: Consolidated status
    SM->>SM: Generate status reports
    SM->>IP: Progress feedback
```

## Stakeholder Communication Flow

```mermaid
sequenceDiagram
    participant RC as Regulatory Change
    participant SC as Stakeholder Classifier
    participant CM as Communication Manager
    participant TM as Template Manager
    participant SM as Stakeholder Manager
    participant FM as Feedback Manager
    participant RM as Relationship Manager

    RC->>SC: Change details & impact
    SC->>SC: Classify stakeholders by interest
    SC->>CM: Stakeholder classification

    CM->>TM: Request communication templates
    TM->>CM: Customized templates
    CM->>SM: Stakeholder communication plan

    SM->>SM: Execute communication plan
    SM->>FM: Collect stakeholder feedback
    FM->>FM: Analyze feedback sentiment

    FM->>RM: Feedback insights
    RM->>RM: Update stakeholder relationships
    RM->>CM: Communication effectiveness

    CM->>SC: Feedback for stakeholder classification
    SC->>RC: Stakeholder impact assessment
```

## Audit Trail & Compliance Reporting

```mermaid
sequenceDiagram
    participant AT as Audit Trail
    participant CR as Compliance Reporter
    participant DR as Data Retriever
    participant VA as Validation Agent
    participant FM as Format Manager
    participant DM as Distribution Manager
    participant AM as Archive Manager

    AT->>CR: Compliance events & activities
    CR->>DR: Request compliance data
    DR->>DR: Retrieve relevant data
    DR->>VA: Data for validation

    VA->>VA: Validate data accuracy
    VA->>CR: Validated compliance data
    CR->>CR: Generate compliance reports

    CR->>FM: Request report formatting
    FM->>FM: Format reports per requirements
    FM->>DM: Formatted reports

    DM->>DM: Distribute to stakeholders
    DM->>AM: Archive reports
    AM->>AM: Store in compliance archive

    AM->>AT: Archive confirmation
    AT->>CR: Audit trail update
```</content>
<parameter name="filePath">/Users/giangio/Documents/GitHub/Interzen/Interzen.POC/ZenIA/docs/use_cases/UC9 - Compliance & Risk Management/01 Sequence diagrams.md