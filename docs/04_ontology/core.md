# Phase 4-1: Core Ontology 설계

---

## 1. Core Ontology 개요

### 1.1 설계 원칙
- **도메인 독립성**: 소프트웨어 산업 외 확장 가능한 범용 개념
- **최소 결합**: 각 개념 간 느슨한 결합
- **확장성**: 하위 온톨로지에서 특화 가능한 구조
- **재사용성**: 다른 시스템에서도 활용 가능

### 1.2 Core 개념 목록

| 개념 | 설명 | 역할 |
|------|------|------|
| **Project** | 수행 대상 프로젝트 | 중심 개념 |
| **Cost** | 비용/원가 | 가격 산정 기반 |
| **Revenue** | 수익/매출 | 가격 결정 결과 |
| **Contract** | 계약 | 비즈니스 컨텍스트 |
| **Resource** | 자원 (인력, 장비 등) | 비용 발생원 |
| **Risk** | 리스크 | 가격 조정 요소 |

---

## 2. 개념 정의 (Class Definitions)

### 2.1 Project

```yaml
Class: Project
  Description: 가격 산정 대상이 되는 프로젝트

  Properties:
    - projectId: String (PK)
    - projectName: String
    - projectType: ProjectType (enum)
    - status: ProjectStatus (enum)
    - startDate: Date
    - endDate: Date
    - description: String

  Relationships:
    - hasScope: Scope (1:1)
    - requiresResource: Resource (1:N)
    - producesCost: Cost (1:N)
    - generatesRevenue: Revenue (1:1)
    - boundByContract: Contract (1:1)
    - hasRisk: Risk (1:N)
```

### 2.2 Cost

```yaml
Class: Cost
  Description: 프로젝트 수행에 발생하는 모든 비용

  Properties:
    - costId: String (PK)
    - costType: CostType (enum)
    - amount: Decimal
    - currency: String
    - unit: CostUnit (enum)
    - calculatedAt: DateTime

  Subtypes:
    - DirectCost: 직접비
    - IndirectCost: 간접비
    - ExternalCost: 외부비용

  Relationships:
    - belongsToProject: Project (N:1)
    - consumesResource: Resource (N:N)
```

### 2.3 Revenue

```yaml
Class: Revenue
  Description: 프로젝트로 인해 발생하는 수익

  Properties:
    - revenueId: String (PK)
    - finalPrice: Decimal
    - currency: String
    - margin: Decimal (percentage)
    - calculatedAt: DateTime

  Relationships:
    - derivedFromProject: Project (1:1)
    - basedOnCost: Cost (1:N)
    - adjustedByRisk: Risk (1:N)
```

### 2.4 Contract

```yaml
Class: Contract
  Description: 프로젝트 수행의 법적/사업적 맥락

  Properties:
    - contractId: String (PK)
    - contractType: ContractType (enum)
    - clientName: String
    - contractValue: Decimal
    - paymentTerms: String
    - startDate: Date
    - endDate: Date

  Enums:
    ContractType:
      - PROJECT_BASED
      - BID_BASED
      - TIME_AND_MATERIAL
      - FIXED_PRICE

  Relationships:
    - governs: Project (1:N)
    - defines: PaymentSchedule (1:N)
```

### 2.5 Resource

```yaml
Class: Resource
  Description: 프로젝트에 투입되는 모든 자원

  Properties:
    - resourceId: String (PK)
    - resourceType: ResourceType (enum)
    - name: String
    - unitCost: Decimal
    - availability: Decimal (percentage)

  Subtypes:
    - HumanResource: 인적 자원
    - InfrastructureResource: 인프라 자원
    - ToolResource: 도구/라이선스

  Enums:
    ResourceType:
      - HUMAN
      - INFRASTRUCTURE
      - TOOL
      - EXTERNAL_SERVICE

  Relationships:
    - assignedToProject: Project (N:N)
    - generates: Cost (1:N)
```

### 2.6 Risk

```yaml
Class: Risk
  Description: 프로젝트 수행 시 발생 가능한 리스크

  Properties:
    - riskId: String (PK)
    - riskType: RiskType (enum)
    - description: String
    - probability: Decimal (0-1)
    - impact: ImpactLevel (enum)
    - premium: Decimal (percentage)

  Enums:
    RiskType:
      - TECHNICAL
      - BUSINESS
      - RESOURCE
      - SCHEDULE
      - SCOPE

    ImpactLevel:
      - LOW
      - MEDIUM
      - HIGH
      - CRITICAL

  Relationships:
    - affects: Project (N:N)
    - adjusts: Revenue (N:N)
```

---

## 3. 관계 정의 (Relationships)

### 3.1 관계 다이어그램

```
                    ┌─────────────┐
                    │   Contract  │
                    │             │
                    └──────┬──────┘
                           │ governs
                           ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Resource  │◄───│   Project   │───►│    Risk     │
│             │    │             │    │             │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       │ generates        │ produces         │ adjusts
       ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Cost     │───►│   Revenue   │◄───│   (Risk)    │
│             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 3.2 관계 상세 정의

| 관계명 | 소스 | 타겟 | 카디널리티 | 설명 |
|--------|------|------|:----------:|------|
| governs | Contract | Project | 1:N | 계약이 프로젝트를 규정 |
| requiresResource | Project | Resource | 1:N | 프로젝트가 자원을 필요로 함 |
| produces | Project | Cost | 1:N | 프로젝트가 비용을 발생시킴 |
| generates | Resource | Cost | 1:N | 자원 사용이 비용을 발생시킴 |
| hasRisk | Project | Risk | 1:N | 프로젝트가 리스크를 가짐 |
| basedOn | Revenue | Cost | 1:N | 수익이 비용을 기반으로 함 |
| adjustedBy | Revenue | Risk | 1:N | 수익이 리스크로 조정됨 |

---

## 4. Enumeration 정의

### 4.1 Project 관련

```yaml
ProjectType:
  - NEW_DEVELOPMENT      # 신규 개발
  - ENHANCEMENT          # 기능 개선
  - MIGRATION            # 마이그레이션
  - INTEGRATION          # 시스템 통합
  - MAINTENANCE          # 유지보수

ProjectStatus:
  - PLANNING             # 기획 중
  - IN_PROGRESS          # 진행 중
  - COMPLETED            # 완료
  - ON_HOLD              # 보류
  - CANCELLED            # 취소
```

### 4.2 Cost 관련

```yaml
CostType:
  - LABOR                # 인건비
  - INFRASTRUCTURE       # 인프라비
  - TOOL                 # 도구비
  - EXTERNAL             # 외주비
  - OVERHEAD             # 간접비
  - CONTINGENCY          # 예비비

CostUnit:
  - MONTHLY              # 월 단위
  - DAILY                # 일 단위
  - HOURLY               # 시간 단위
  - FIXED                # 고정 금액
  - PER_UNIT             # 단위당
```

### 4.3 Resource 관련

```yaml
ResourceType:
  - HUMAN                # 인적 자원
  - INFRASTRUCTURE       # 인프라
  - TOOL                 # 도구/라이선스
  - EXTERNAL_SERVICE     # 외부 서비스

ResourceAvailability:
  - FULL_TIME            # 100%
  - PART_TIME            # 50%
  - ON_DEMAND            # 필요 시
```

---

## 5. 확장 포인트 (Extension Points)

### 5.1 Domain-Specific 확장

```
Core Ontology
├── Project
│   └── [Extension] → SoftwareProject (Phase 4-2)
├── Cost
│   └── [Extension] → SoftwareCost (Phase 4-3)
├── Resource
│   └── [Extension] → Developer, QA, PM...
└── Risk
    └── [Extension] → TechnicalRisk, BusinessRisk...
```

### 5.2 Industry-Specific 확장 (향후)

```
Core Ontology
├── [소프트웨어] SoftwareProject, SoftwareCost...
├── [제조업] ManufacturingProject, ProductionCost...
└── [서비스업] ServiceProject, ServiceCost...
```

---

## 6. 데이터 타입 정의

### 6.1 기본 타입

| 타입 | 설명 | 예시 |
|------|------|------|
| String | 문자열 | "프로젝트A" |
| Decimal | 소수점 숫자 | 1500000.00 |
| Integer | 정수 | 10 |
| Date | 날짜 | 2024-01-15 |
| DateTime | 날짜시간 | 2024-01-15T09:00:00 |
| Boolean | 참/거짓 | true |

### 6.2 복합 타입

```yaml
Money:
  amount: Decimal
  currency: String (ISO 4217)

Duration:
  value: Integer
  unit: DurationUnit (DAY, WEEK, MONTH)

Percentage:
  value: Decimal (0-100)
```

---

## 7. 제약 조건 (Constraints)

### 7.1 무결성 제약

```
[Project]
- startDate <= endDate
- projectId는 고유해야 함

[Cost]
- amount >= 0
- Cost는 반드시 Project에 속해야 함

[Revenue]
- finalPrice >= totalCost (손실 프로젝트 제외)
- margin은 -100 ~ 100 범위

[Resource]
- unitCost >= 0
- availability는 0 ~ 100 범위
```

### 7.2 비즈니스 규칙

```
[Rule 1] 프로젝트 총 비용 = SUM(관련 Cost)
[Rule 2] 최종 가격 = 총 비용 × (1 + margin) × (1 + riskPremium)
[Rule 3] 계약 금액 >= 최종 가격 (협상 후)
```

---

## 8. JSON-LD 표현 예시

```json
{
  "@context": {
    "onto": "http://pricing-ontology.example.com/core#",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@type": "onto:Project",
  "@id": "onto:project/PRJ-2024-001",
  "onto:projectName": "고객관리시스템 구축",
  "onto:projectType": "onto:NEW_DEVELOPMENT",
  "onto:startDate": {
    "@type": "xsd:date",
    "@value": "2024-03-01"
  },
  "onto:requiresResource": [
    { "@id": "onto:resource/RES-001" },
    { "@id": "onto:resource/RES-002" }
  ],
  "onto:hasRisk": [
    { "@id": "onto:risk/RISK-001" }
  ]
}
```

---

## 문서 정보

- **작성일**: 2026-02-25
- **상태**: Phase 4-1 완료
- **다음 문서**: project.md (Project Ontology)
