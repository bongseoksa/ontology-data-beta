# Phase 4-2: Project Ontology 설계

---

## 1. Project Ontology 개요

### 1.1 목적
Core Ontology의 `Project`를 소프트웨어 프로젝트 맥락으로 확장하여
프로젝트 구조, 범위, 일정, 인력 구성을 상세하게 모델링

### 1.2 Core → Project 확장 구조

```
Core:Project
    └── extends → SoftwareProject
                      ├── hasScope → Scope
                      ├── hasFeature → Feature
                      ├── hasTimeline → Timeline
                      ├── requiresRole → Role
                      ├── hasComplexity → Complexity
                      └── hasDependency → Dependency
```

---

## 2. SoftwareProject 확장

### 2.1 Class 정의

```yaml
Class: SoftwareProject
  Extends: Core:Project

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

SystemType:
  - ERP
  - CRM
  - SCM
  - ECOMMERCE
  - CMS
  - CUSTOM

SecurityLevel:
  - STANDARD
  - ENHANCED
  - HIGH_SECURITY
  - COMPLIANCE_REQUIRED

DataVolumeLevel:
  - SMALL      # < 1GB
  - MEDIUM     # 1GB ~ 100GB
  - LARGE      # 100GB ~ 1TB
  - VERY_LARGE # > 1TB
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
    - priority: Priority (enum)
    - fp: Integer                  # 기능점수
    - complexity: ComplexityLevel (enum)
    - status: FeatureStatus (enum)

  Relationships:
    - belongsToScope: Scope (N:1)
    - dependsOn: Feature (N:N)
    - requires: TechComponent (N:N)
    - assignedTo: Role (N:N)
```

### 4.2 FeatureType 분류

```yaml
FeatureType:
  # 데이터 기능
  - DATA_ENTRY           # 데이터 입력
  - DATA_DISPLAY         # 데이터 조회/표시
  - DATA_REPORT          # 리포트 생성

  # 프로세스 기능
  - WORKFLOW             # 업무 프로세스
  - CALCULATION          # 계산/연산
  - NOTIFICATION         # 알림/통지

  # 통합 기능
  - EXTERNAL_INTERFACE   # 외부 연동
  - BATCH_PROCESS        # 배치 처리
  - API_ENDPOINT         # API 제공

  # 보안/관리 기능
  - AUTHENTICATION       # 인증
  - AUTHORIZATION        # 권한 관리
  - AUDIT_LOG            # 감사 로그
```

### 4.3 ComplexityLevel

```yaml
ComplexityLevel:
  LOW:
    fpMultiplier: 0.8
    description: "표준 CRUD, 단순 로직"

  MEDIUM:
    fpMultiplier: 1.0
    description: "일반적인 비즈니스 로직"

  HIGH:
    fpMultiplier: 1.3
    description: "복잡한 로직, 다중 연동"

  VERY_HIGH:
    fpMultiplier: 1.6
    description: "고급 알고리즘, 실시간 처리"
```

---

## 5. Timeline (일정)

### 5.1 Class 정의

```yaml
Class: Timeline
  Description: 프로젝트 일정 및 마일스톤

  Properties:
    - timelineId: String (PK)
    - totalDuration: Duration
    - startDate: Date
    - endDate: Date

  Relationships:
    - belongsTo: SoftwareProject (1:1)
    - hasPhase: Phase (1:N)
    - hasMilestone: Milestone (1:N)
```

### 5.2 Phase (단계)

```yaml
Class: Phase
  Description: 프로젝트 수행 단계

  Properties:
    - phaseId: String (PK)
    - phaseName: String
    - phaseType: PhaseType (enum)
    - startDate: Date
    - endDate: Date
    - effortPercentage: Percentage
    - status: PhaseStatus (enum)

  Relationships:
    - belongsToTimeline: Timeline (N:1)
    - follows: Phase (1:1)
    - requiresRole: Role (N:N)
```

### 5.3 표준 Phase 정의

```yaml
PhaseType:
  INITIATION:
    typicalEffort: "5-10%"
    keyRoles: [PM]
    deliverables: [ProjectCharter, KickoffPresentation]

  REQUIREMENTS:
    typicalEffort: "10-15%"
    keyRoles: [BA, Architect]
    deliverables: [SRS, UseCase]

  DESIGN:
    typicalEffort: "15-20%"
    keyRoles: [Architect, Designer, DBA]
    deliverables: [ArchitectureDoc, UIDesign, ERD]

  DEVELOPMENT:
    typicalEffort: "35-45%"
    keyRoles: [Developer, TechLead]
    deliverables: [SourceCode, UnitTest]

  TESTING:
    typicalEffort: "15-20%"
    keyRoles: [QA, Tester]
    deliverables: [TestReport, BugFixes]

  DEPLOYMENT:
    typicalEffort: "5-10%"
    keyRoles: [DevOps, PM]
    deliverables: [DeployedSystem, Documentation]
```

---

## 6. Role (역할)

### 6.1 Class 정의

```yaml
Class: Role
  Description: 프로젝트에 필요한 역할

  Properties:
    - roleId: String (PK)
    - roleName: String
    - roleType: RoleType (enum)
    - skillLevel: SkillLevel (enum)
    - headcount: Decimal           # 투입 인원 (0.5 등 가능)
    - duration: Duration           # 투입 기간
    - allocation: Percentage       # 투입률

  Derived Properties:
    - manMonth: Decimal            # headcount × duration × allocation

  Relationships:
    - assignedToProject: SoftwareProject (N:1)
    - performsPhase: Phase (N:N)
    - worksOnFeature: Feature (N:N)
    - maps: Core:Resource (1:1)
```

### 6.2 RoleType 및 SkillLevel

```yaml
RoleType:
  # 관리
  - PROJECT_MANAGER
  - SCRUM_MASTER
  - PRODUCT_OWNER

  # 기술
  - TECH_LEAD
  - ARCHITECT
  - BACKEND_DEVELOPER
  - FRONTEND_DEVELOPER
  - FULLSTACK_DEVELOPER
  - MOBILE_DEVELOPER
  - DBA
  - DEVOPS_ENGINEER

  # 품질
  - QA_ENGINEER
  - TESTER

  # 디자인
  - UI_DESIGNER
  - UX_DESIGNER

SkillLevel:
  JUNIOR:
    yearsOfExperience: [0, 3]
    techGrade: "초급"
    costMultiplier: 0.7

  MID:
    yearsOfExperience: [3, 7]
    techGrade: "중급"
    costMultiplier: 1.0

  SENIOR:
    yearsOfExperience: [7, 12]
    techGrade: "고급"
    costMultiplier: 1.3

  EXPERT:
    yearsOfExperience: [12, null]
    techGrade: "특급"
    costMultiplier: 1.6
```

---

## 7. Complexity (복잡도)

### 7.1 Class 정의

```yaml
Class: Complexity
  Description: 프로젝트 전체 복잡도 평가

  Properties:
    - complexityId: String (PK)
    - technicalComplexity: ComplexityScore
    - businessComplexity: ComplexityScore
    - organizationalComplexity: ComplexityScore
    - overallComplexity: ComplexityScore
    - adjustmentFactor: Decimal

  Relationships:
    - evaluates: SoftwareProject (1:1)
```

### 7.2 ComplexityScore 산정

```yaml
ComplexityScore:
  Properties:
    - score: Decimal (1.0 ~ 3.0)
    - factors: ComplexityFactor[]

ComplexityFactor:
  # Technical Factors
  - CONCURRENT_USERS:
      low: "<100"
      medium: "100-1000"
      high: ">1000"

  - DATA_VOLUME:
      low: "<1GB"
      medium: "1-100GB"
      high: ">100GB"

  - INTEGRATION_COUNT:
      low: "1-2"
      medium: "3-5"
      high: ">5"

  - REALTIME_REQUIREMENT:
      low: "None"
      medium: "Partial"
      high: "Full"

  # Business Factors
  - PROCESS_COUNT:
      low: "<5"
      medium: "5-15"
      high: ">15"

  - USER_TYPES:
      low: "1-2"
      medium: "3-5"
      high: ">5"

  - REGULATORY_COMPLIANCE:
      low: "None"
      medium: "Some"
      high: "Strict"
```

---

## 8. Dependency (의존성)

### 8.1 Class 정의

```yaml
Class: Dependency
  Description: 프로젝트 내/외부 의존성

  Properties:
    - dependencyId: String (PK)
    - dependencyType: DependencyType (enum)
    - description: String
    - isBlocking: Boolean
    - riskLevel: RiskLevel (enum)

  Relationships:
    - belongsTo: SoftwareProject (N:1)
    - affects: Feature (N:N)
```

### 8.2 DependencyType

```yaml
DependencyType:
  # 내부 의존성
  - FEATURE_DEPENDENCY     # 기능 간 의존
  - DATA_DEPENDENCY        # 데이터 의존
  - RESOURCE_DEPENDENCY    # 인력/장비 의존

  # 외부 의존성
  - EXTERNAL_SYSTEM        # 외부 시스템 연동
  - THIRD_PARTY_SERVICE    # 서드파티 서비스
  - VENDOR_DEPENDENCY      # 벤더 의존
  - REGULATORY_DEPENDENCY  # 규제/승인 의존
```

---

## 9. 관계 다이어그램

```
┌─────────────────────────────────────────────────────────────────┐
│                     SoftwareProject                              │
│                           │                                      │
│     ┌─────────────────────┼─────────────────────┐               │
│     │                     │                     │               │
│     ▼                     ▼                     ▼               │
│ ┌─────────┐         ┌──────────┐         ┌────────────┐        │
│ │  Scope  │         │ Timeline │         │ Complexity │        │
│ │         │         │          │         │            │        │
│ └────┬────┘         └────┬─────┘         └────────────┘        │
│      │                   │                                      │
│      ▼                   ▼                                      │
│ ┌─────────┐         ┌─────────┐                                │
│ │ Feature │         │  Phase  │◄────────┐                      │
│ │         │         │         │         │                      │
│ └────┬────┘         └────┬────┘         │                      │
│      │                   │              │                      │
│      └───────────────────┼──────────────┘                      │
│                          │                                      │
│                          ▼                                      │
│                    ┌──────────┐         ┌────────────┐         │
│                    │   Role   │────────►│ Dependency │         │
│                    │          │         │            │         │
│                    └──────────┘         └────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. JSON 스키마 예시

```json
{
  "@type": "SoftwareProject",
  "@id": "PRJ-2024-001",
  "projectName": "고객관리시스템 구축",
  "applicationType": "WEB_APPLICATION",
  "systemType": "CRM",

  "scope": {
    "totalFP": 650,
    "moduleCount": 8,
    "screenCount": 45,
    "sizeCategory": "MEDIUM"
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
    { "roleType": "PROJECT_MANAGER", "headcount": 1, "skillLevel": "SENIOR" },
    { "roleType": "BACKEND_DEVELOPER", "headcount": 3, "skillLevel": "MID" },
    { "roleType": "FRONTEND_DEVELOPER", "headcount": 2, "skillLevel": "MID" },
    { "roleType": "QA_ENGINEER", "headcount": 1, "skillLevel": "MID" }
  ],

  "complexity": {
    "technicalComplexity": 1.5,
    "businessComplexity": 1.3,
    "overallComplexity": 1.4,
    "adjustmentFactor": 1.1
  }
}
```

---

## 문서 정보

- **작성일**: 2026-02-25
- **상태**: Phase 4-2 완료
- **다음 문서**: cost.md (Cost Ontology)
