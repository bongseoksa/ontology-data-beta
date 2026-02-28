# Extension: Software Project

---

## 1. 개요

### 1.1 목적
Domain Ontology의 `Project`를 소프트웨어 프로젝트 맥락으로 확장하여
프로젝트 구조, 범위, 일정, 인력 구성을 상세하게 모델링

### 1.2 확장 구조

```
Domain:Project (domain.md)
    └── extends → SoftwareProject
                      ├── hasScope → Scope
                      ├── hasFeature → Feature
                      ├── hasTimeline → Timeline
                      ├── requiresRole → Role
                      ├── hasComplexity → Complexity
                      └── hasDependency → Dependency
```

---

## 2. SoftwareProject

### 2.1 Class 정의

```yaml
Class: SoftwareProject
  Extends: Domain:Project

  Properties:
    - applicationType: ApplicationType (enum)
    - systemType: SystemType (enum)
    - techStack: TechStack[]
    - targetUsers: Integer
    - dataVolume: DataVolumeLevel (enum)
    - integrationCount: Integer
    - securityLevel: SecurityLevel (enum)

  Relationships:
    - hasScope: Scope (1:1)
    - hasFeature: Feature (1:N)
    - hasTimeline: Timeline (1:1)
    - requiresRole: Role (1:N)
    - assessedComplexity: Complexity (1:1)
    - hasDependency: Dependency (1:N)
```

### 2.2 Enumeration

```yaml
ApplicationType:
  - WEB_APPLICATION
  - MOBILE_APPLICATION
  - DESKTOP_APPLICATION
  - API_PLATFORM
  - DATA_PLATFORM
  - AI_ML_SYSTEM
  - EMBEDDED_SYSTEM

SystemType:
  - ERP
  - CRM
  - SCM
  - ECOMMERCE
  - CMS
  - LMS
  - CUSTOM

SecurityLevel:
  - STANDARD
  - ENHANCED
  - HIGH_SECURITY
  - COMPLIANCE_REQUIRED    # ISMS, PCI-DSS 등

DataVolumeLevel:
  - SMALL          # < 1GB
  - MEDIUM         # 1GB ~ 100GB
  - LARGE          # 100GB ~ 1TB
  - VERY_LARGE     # > 1TB
```

---

## 3. Scope (범위)

### 3.1 Class 정의

```yaml
Class: Scope
  Description: 프로젝트의 전체 범위 정의

  Properties:
    - scopeId: String (PK)
    - totalFP: Integer            # 총 기능점수
    - moduleCount: Integer        # 모듈 수
    - screenCount: Integer        # 화면 수
    - reportCount: Integer        # 리포트 수
    - interfaceCount: Integer     # 인터페이스 수
    - batchCount: Integer         # 배치 프로그램 수

  Derived Properties:
    - estimatedLOC: Integer       # FP 기반 추정 LOC
    - sizeCategory: SizeCategory  # 규모 분류

  Relationships:
    - belongsTo: SoftwareProject (1:1)
    - contains: Feature (1:N)
    - defines: Deliverable (1:N)
```

### 3.2 SizeCategory 분류

```yaml
SizeCategory:
  SMALL:
    fpRange: [0, 300]
    typicalDuration: "2-4 months"
    typicalTeam: "3-5 members"

  MEDIUM:
    fpRange: [300, 1000]
    typicalDuration: "4-8 months"
    typicalTeam: "5-10 members"

  LARGE:
    fpRange: [1000, 3000]
    typicalDuration: "8-18 months"
    typicalTeam: "10-30 members"

  ENTERPRISE:
    fpRange: [3000, null]
    typicalDuration: "18+ months"
    typicalTeam: "30+ members"
```

---

## 4. Feature (기능)

### 4.1 Class 정의

```yaml
Class: Feature
  Description: 프로젝트의 개별 기능 단위

  Properties:
    - featureId: String (PK)
    - featureName: String
    - featureType: FeatureType (enum)
    - description: String
    - fp: Integer                 # 기능점수
    - complexity: ComplexityLevel (enum)
    - priority: Priority (enum)
    - status: FeatureStatus (enum)

  Enums:
    FeatureType:
      - CRUD                  # 기본 CRUD
      - WORKFLOW              # 업무 프로세스
      - REPORTING             # 리포팅/대시보드
      - INTEGRATION           # 외부 연동
      - BATCH                 # 배치 처리
      - SEARCH                # 검색 기능
      - NOTIFICATION          # 알림 기능
      - AUTH                  # 인증/권한

    ComplexityLevel:
      - LOW
      - MEDIUM
      - HIGH

    Priority:
      - MUST_HAVE
      - SHOULD_HAVE
      - COULD_HAVE
      - WONT_HAVE

    FeatureStatus:
      - PLANNED
      - IN_PROGRESS
      - COMPLETED
      - DEFERRED

  Relationships:
    - belongsTo: Scope (N:1)
    - dependsOn: Feature (N:N)
    - implementedInPhase: Phase (N:1)
```

---

## 5. Timeline (일정)

### 5.1 Class 정의

```yaml
Class: Timeline
  Description: 프로젝트 전체 일정 계획

  Properties:
    - timelineId: String (PK)
    - totalDuration: Duration
    - startDate: Date
    - endDate: Date

  Relationships:
    - belongsTo: SoftwareProject (1:1)
    - hasPhase: Phase (1:N, ordered)
    - hasMilestone: Milestone (1:N)
```

### 5.2 Phase (단계)

```yaml
Class: Phase
  Description: 프로젝트 수행 단계

  Properties:
    - phaseId: String (PK)
    - phaseType: PhaseType (enum)
    - order: Integer
    - duration: Duration
    - effortPercentage: Percentage
    - startDate: Date
    - endDate: Date
    - status: PhaseStatus (enum)

  Enums:
    PhaseType:
      - INITIATION            # 착수 (5%)
      - REQUIREMENTS          # 요구분석 (15%)
      - DESIGN                # 설계 (20%)
      - DEVELOPMENT           # 개발 (40%)
      - TESTING               # 테스트 (15%)
      - DEPLOYMENT            # 배포/이행 (5%)

    PhaseStatus:
      - NOT_STARTED
      - IN_PROGRESS
      - COMPLETED
      - DELAYED

  Relationships:
    - belongsTo: Timeline (N:1)
    - hasFeature: Feature (1:N)
    - requires: Role (1:N)
```

### 5.3 Milestone (마일스톤)

```yaml
Class: Milestone
  Description: 프로젝트 주요 이정표

  Properties:
    - milestoneId: String (PK)
    - name: String
    - targetDate: Date
    - actualDate: Date (nullable)
    - deliverables: String[]
    - status: MilestoneStatus (enum)
    - paymentPercentage: Percentage (nullable)

  Enums:
    MilestoneStatus:
      - UPCOMING
      - DUE
      - ACHIEVED
      - MISSED

  Relationships:
    - belongsTo: Timeline (N:1)
    - completesPhase: Phase (N:1)
```

---

## 6. Role (역할)

### 6.1 Class 정의

```yaml
Class: Role
  Description: 프로젝트에 필요한 역할 및 인력 구성

  Properties:
    - roleId: String (PK)
    - roleType: RoleType (enum)
    - skillLevel: SkillLevel (enum)
    - headcount: Decimal
    - duration: Duration
    - allocation: Percentage       # 투입률
    - manMonth: Decimal            # 계산된 M/M

  Enums:
    RoleType:
      - PROJECT_MANAGER
      - BUSINESS_ANALYST
      - ARCHITECT
      - BACKEND_DEVELOPER
      - FRONTEND_DEVELOPER
      - MOBILE_DEVELOPER
      - DEVOPS_ENGINEER
      - QA_ENGINEER
      - UI_UX_DESIGNER
      - DATA_ENGINEER
      - ML_ENGINEER
      - DBA
      - SECURITY_ENGINEER

    SkillLevel:
      - JUNIOR:
          yearRange: [0, 3]
          costMultiplier: 0.7
      - MID:
          yearRange: [3, 7]
          costMultiplier: 1.0
      - SENIOR:
          yearRange: [7, 12]
          costMultiplier: 1.3
      - EXPERT:
          yearRange: [12, null]
          costMultiplier: 1.6

  Calculation:
    manMonth = headcount × duration(months) × (allocation / 100)

  Relationships:
    - assignedTo: SoftwareProject (N:1)
    - participatesIn: Phase (N:N)
    - mapsTo: Core:Resource (N:1)
```

---

## 7. Complexity (복잡도)

### 7.1 Class 정의

```yaml
Class: Complexity
  Description: 프로젝트 복잡도 평가

  Properties:
    - complexityId: String (PK)
    - technicalComplexity: ComplexityScore
    - businessComplexity: ComplexityScore
    - organizationalComplexity: ComplexityScore
    - overallComplexity: ComplexityLevel (enum)
    - complexityFactors: ComplexityFactor[]

  Embedded:
    ComplexityScore:
      score: Decimal (1-5)
      factors: String[]
      notes: String

  Enums:
    ComplexityLevel:
      - LOW           # 1.0 - 1.5
      - MEDIUM        # 1.5 - 2.5
      - HIGH          # 2.5 - 3.5
      - VERY_HIGH     # 3.5 - 5.0

  Relationships:
    - evaluates: SoftwareProject (1:1)
```

### 7.2 ComplexityFactor

```yaml
ComplexityFactor:
  TECHNICAL:
    - NEW_TECHNOLOGY:
        description: "신기술 도입 여부"
        weight: 15%
    - INTEGRATION_COMPLEXITY:
        description: "연동 복잡도"
        weight: 15%
    - PERFORMANCE_REQUIREMENT:
        description: "성능 요구사항 수준"
        weight: 10%
    - SECURITY_REQUIREMENT:
        description: "보안 요구사항 수준"
        weight: 10%

  BUSINESS:
    - REQUIREMENT_CLARITY:
        description: "요구사항 명확성"
        weight: 15%
    - BUSINESS_RULE_COMPLEXITY:
        description: "비즈니스 규칙 복잡도"
        weight: 10%
    - DATA_COMPLEXITY:
        description: "데이터 구조 복잡도"
        weight: 10%

  ORGANIZATIONAL:
    - STAKEHOLDER_COUNT:
        description: "이해관계자 수"
        weight: 5%
    - COMMUNICATION_COMPLEXITY:
        description: "의사소통 복잡도"
        weight: 5%
    - DEPENDENCY_MANAGEMENT:
        description: "의존성 관리 복잡도"
        weight: 5%
```

---

## 8. Dependency (의존성)

### 8.1 Class 정의

```yaml
Class: Dependency
  Description: 프로젝트 내외부 의존성

  Properties:
    - dependencyId: String (PK)
    - dependencyType: DependencyType (enum)
    - source: String
    - target: String
    - impact: ImpactLevel (enum)
    - status: DependencyStatus (enum)
    - description: String

  Enums:
    DependencyType:
      - FEATURE_DEPENDENCY      # 기능 간 의존
      - DATA_DEPENDENCY         # 데이터 의존
      - RESOURCE_DEPENDENCY     # 인력/자원 의존
      - EXTERNAL_DEPENDENCY     # 외부 시스템 의존
      - TECHNOLOGY_DEPENDENCY   # 기술 스택 의존
      - TIMELINE_DEPENDENCY     # 일정 의존
      - CONTRACT_DEPENDENCY     # 계약/법적 의존
      - THIRD_PARTY_DEPENDENCY  # 써드파티 의존

    DependencyStatus:
      - IDENTIFIED
      - RESOLVED
      - BLOCKED
      - MITIGATED

  Relationships:
    - affects: SoftwareProject (N:1)
```

---

## 9. 관계 다이어그램

```
┌────────────────────────────────────────────────────────────────┐
│                     SoftwareProject                             │
│  (extends Domain:Project)                                       │
│                                                                 │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐           │
│  │   Scope    │    │  Timeline  │    │ Complexity │           │
│  │            │    │            │    │            │           │
│  │ - totalFP  │    │ - phases   │    │ - factors  │           │
│  │ - modules  │    │ - milestones│   │ - scores   │           │
│  └─────┬──────┘    └─────┬──────┘    └────────────┘           │
│        │                 │                                      │
│        │ contains        │ hasPhase                            │
│        ▼                 ▼                                      │
│  ┌────────────┐    ┌────────────┐                              │
│  │  Feature   │◄───│   Phase    │                              │
│  │            │    │            │                              │
│  │ - fp       │    │ - effort % │                              │
│  │ - priority │    │ - duration │                              │
│  └────────────┘    └─────┬──────┘                              │
│                          │                                      │
│                          │ requires                             │
│                          ▼                                      │
│                    ┌────────────┐    ┌────────────┐            │
│                    │    Role    │───►│ Dependency │            │
│                    │            │    │            │            │
│                    │ - M/M      │    │ - type     │            │
│                    │ - level    │    │ - impact   │            │
│                    └────────────┘    └────────────┘            │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 10. JSON 예시

```json
{
  "softwareProject": {
    "activityId": "PRJ-2026-001",
    "activityName": "고객관리시스템 구축",
    "activityType": "PROJECT",
    "applicationType": "WEB_APPLICATION",
    "systemType": "CRM",
    "securityLevel": "ENHANCED",
    "dataVolume": "MEDIUM",

    "scope": {
      "totalFP": 850,
      "sizeCategory": "MEDIUM",
      "moduleCount": 8,
      "screenCount": 45,
      "reportCount": 12,
      "interfaceCount": 5
    },

    "timeline": {
      "totalDuration": { "value": 6, "unit": "MONTH" },
      "phases": [
        { "phaseType": "REQUIREMENTS", "effortPercentage": 15 },
        { "phaseType": "DESIGN", "effortPercentage": 20 },
        { "phaseType": "DEVELOPMENT", "effortPercentage": 40 },
        { "phaseType": "TESTING", "effortPercentage": 20 },
        { "phaseType": "DEPLOYMENT", "effortPercentage": 5 }
      ]
    },

    "roles": [
      { "roleType": "PROJECT_MANAGER", "skillLevel": "SENIOR", "headcount": 1, "manMonth": 6 },
      { "roleType": "BACKEND_DEVELOPER", "skillLevel": "MID", "headcount": 3, "manMonth": 15 },
      { "roleType": "FRONTEND_DEVELOPER", "skillLevel": "MID", "headcount": 2, "manMonth": 10 },
      { "roleType": "QA_ENGINEER", "skillLevel": "MID", "headcount": 1, "manMonth": 3 }
    ],

    "complexity": {
      "technicalComplexity": 2.5,
      "businessComplexity": 3.0,
      "organizationalComplexity": 2.0,
      "overallComplexity": "MEDIUM"
    }
  }
}
```

---

## 문서 정보

- **작성일**: 2026-02-27
- **버전**: 1.0
- **의존 문서**: core.md, cost.md, pricing.md
