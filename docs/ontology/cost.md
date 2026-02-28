# Phase 4-3: Cost Ontology 설계

---

## 1. Cost Ontology 개요

### 1.1 목적
Core Ontology의 `Cost`를 소프트웨어 프로젝트 비용 구조로 확장하여
세부 비용 항목, 계산 로직, 비용 간 관계를 상세하게 모델링

### 1.2 Core → Cost 확장 구조

```
Core:Cost
    └── extends → SoftwareCost
                      ├── LaborCost (인건비)
                      ├── InfrastructureCost (인프라비)
                      ├── ToolCost (도구비)
                      ├── IndirectCost (간접비)
                      └── ExternalCost (외부비용)
```

---

## 2. SoftwareCost 기본 구조

### 2.1 Class 정의

```yaml
Class: SoftwareCost
  Extends: Core:Cost

  Properties:
    - costId: String (PK)
    - projectId: String (FK)
    - costCategory: CostCategory (enum)
    - amount: Money
    - calculationMethod: CalculationMethod (enum)
    - calculatedAt: DateTime
    - validFrom: Date
    - validTo: Date

  Derived Properties:
    - totalDirectCost: Money
    - totalIndirectCost: Money
    - totalCost: Money

  Relationships:
    - belongsTo: SoftwareProject (N:1)
    - hasComponent: CostComponent (1:N)
```

### 2.2 CostCategory

```yaml
CostCategory:
  DIRECT:
    - LABOR           # 인건비
    - INFRASTRUCTURE  # 인프라비
    - TOOL            # 도구/라이선스
    - EXTERNAL        # 외주/협력사

  INDIRECT:
    - OVERHEAD        # 제경비
    - MANAGEMENT      # 일반관리비
    - TECHNICAL_FEE   # 기술료

  CONTINGENCY:
    - RISK_RESERVE    # 리스크 예비비
    - BUFFER          # 버퍼
```

---

## 3. LaborCost (인건비)

### 3.1 Class 정의

```yaml
Class: LaborCost
  Extends: SoftwareCost

  Properties:
    - laborCostId: String (PK)

  Relationships:
    - hasAllocation: LaborAllocation (1:N)

  Calculation:
    totalLaborCost = SUM(LaborAllocation.cost)
```

### 3.2 LaborAllocation (인력 투입)

```yaml
Class: LaborAllocation
  Description: 개별 인력 투입 및 비용

  Properties:
    - allocationId: String (PK)
    - roleType: RoleType (enum)
    - skillLevel: SkillLevel (enum)
    - headcount: Decimal
    - duration: Duration
    - allocation: Percentage      # 투입률
    - unitCost: Money             # 월 노임단가
    - cost: Money                 # 계산된 비용

  Calculation:
    manMonth = headcount × duration(months) × (allocation / 100)
    cost = manMonth × unitCost
```

### 3.3 노임단가 참조 테이블

```yaml
LaborUnitCost:
  Description: 기술자 등급별 노임단가

  Properties:
    - grade: TechGrade (enum)
    - monthlyRate: Money
    - dailyRate: Money
    - effectiveYear: Integer

  Reference:
    source: "KOSA SW기술자 평균임금"
    updateCycle: "Annual (September)"

TechGrade:
  EXPERT:       # 특급
    monthlyRate: 12000000
    dailyRate: 550000

  SENIOR:       # 고급
    monthlyRate: 10000000
    dailyRate: 450000

  MID:          # 중급
    monthlyRate: 8000000
    dailyRate: 360000

  JUNIOR:       # 초급
    monthlyRate: 5500000
    dailyRate: 250000
```

### 3.4 인건비 계산 예시

```json
{
  "laborCost": {
    "allocations": [
      {
        "roleType": "PROJECT_MANAGER",
        "skillLevel": "SENIOR",
        "headcount": 1,
        "duration": { "value": 6, "unit": "MONTH" },
        "allocation": 100,
        "unitCost": { "amount": 10000000, "currency": "KRW" },
        "manMonth": 6.0,
        "cost": { "amount": 60000000, "currency": "KRW" }
      },
      {
        "roleType": "BACKEND_DEVELOPER",
        "skillLevel": "MID",
        "headcount": 3,
        "duration": { "value": 5, "unit": "MONTH" },
        "allocation": 100,
        "unitCost": { "amount": 8000000, "currency": "KRW" },
        "manMonth": 15.0,
        "cost": { "amount": 120000000, "currency": "KRW" }
      }
    ],
    "totalLaborCost": { "amount": 180000000, "currency": "KRW" }
  }
}
```

---

## 4. InfrastructureCost (인프라비)

### 4.1 Class 정의

```yaml
Class: InfrastructureCost
  Extends: SoftwareCost

  Properties:
    - infraCostId: String (PK)
    - environment: Environment (enum)

  Relationships:
    - hasComponent: InfraComponent (1:N)

  Calculation:
    totalInfraCost = SUM(InfraComponent.cost)
```

### 4.2 InfraComponent

```yaml
Class: InfraComponent
  Description: 개별 인프라 구성 요소 비용

  Properties:
    - componentId: String (PK)
    - componentType: InfraType (enum)
    - provider: String
    - specification: String
    - quantity: Integer
    - unitCost: Money
    - duration: Duration
    - cost: Money

  Calculation:
    cost = unitCost × quantity × duration(months)

InfraType:
  - COMPUTE          # 서버/VM
  - STORAGE          # 스토리지
  - DATABASE         # 데이터베이스
  - NETWORK          # 네트워크
  - CDN              # CDN
  - CONTAINER        # 컨테이너/쿠버네티스
  - SERVERLESS       # 서버리스
  - SECURITY         # 보안 (WAF, 방화벽 등)

Environment:
  - DEVELOPMENT      # 개발 환경
  - STAGING          # 스테이징 환경
  - PRODUCTION       # 운영 환경 (초기 구축만)
```

### 4.3 인프라비 계산 예시

```json
{
  "infrastructureCost": {
    "environment": "DEVELOPMENT",
    "components": [
      {
        "componentType": "COMPUTE",
        "provider": "AWS",
        "specification": "t3.medium × 2",
        "unitCost": { "amount": 150000, "currency": "KRW" },
        "duration": { "value": 6, "unit": "MONTH" },
        "cost": { "amount": 900000, "currency": "KRW" }
      },
      {
        "componentType": "DATABASE",
        "provider": "AWS RDS",
        "specification": "db.t3.medium",
        "unitCost": { "amount": 200000, "currency": "KRW" },
        "duration": { "value": 6, "unit": "MONTH" },
        "cost": { "amount": 1200000, "currency": "KRW" }
      }
    ],
    "totalInfraCost": { "amount": 2100000, "currency": "KRW" }
  }
}
```

---

## 5. ToolCost (도구/라이선스비)

### 5.1 Class 정의

```yaml
Class: ToolCost
  Extends: SoftwareCost

  Properties:
    - toolCostId: String (PK)

  Relationships:
    - hasTool: ToolLicense (1:N)

  Calculation:
    totalToolCost = SUM(ToolLicense.cost)
```

### 5.2 ToolLicense

```yaml
Class: ToolLicense
  Description: 개발 도구 및 라이선스 비용

  Properties:
    - licenseId: String (PK)
    - toolName: String
    - toolCategory: ToolCategory (enum)
    - licenseType: LicenseType (enum)
    - userCount: Integer
    - unitCost: Money
    - duration: Duration
    - cost: Money

  Calculation:
    cost = unitCost × userCount × duration(months)

ToolCategory:
  - IDE                # 개발 IDE
  - VERSION_CONTROL    # 버전 관리
  - CI_CD              # CI/CD 도구
  - PROJECT_MANAGEMENT # 프로젝트 관리
  - COLLABORATION      # 협업 도구
  - TESTING            # 테스트 도구
  - MONITORING         # 모니터링
  - DESIGN             # 디자인 도구

LicenseType:
  - SUBSCRIPTION       # 구독형
  - PERPETUAL          # 영구 라이선스
  - OPEN_SOURCE        # 오픈소스 (무료)
  - ENTERPRISE         # 기업용
```

---

## 6. IndirectCost (간접비)

### 6.1 Class 정의

```yaml
Class: IndirectCost
  Extends: SoftwareCost

  Properties:
    - indirectCostId: String (PK)
    - costType: IndirectCostType (enum)
    - rateBase: RateBase (enum)
    - rate: Percentage
    - baseAmount: Money
    - cost: Money

  Calculation:
    cost = baseAmount × (rate / 100)

IndirectCostType:
  - OVERHEAD           # 제경비 (사무실, 관리비 등)
  - MANAGEMENT_FEE     # 일반관리비
  - TECHNICAL_FEE      # 기술료

RateBase:
  - DIRECT_LABOR       # 직접인건비 기준
  - TOTAL_DIRECT       # 직접비 합계 기준
  - LABOR_PLUS_OVERHEAD # 인건비+제경비 기준
```

### 6.2 공공사업 간접비 기준

```yaml
PublicProjectIndirectCost:
  Description: SW사업 대가산정 가이드 기준

  Rates:
    OVERHEAD:
      rateBase: DIRECT_LABOR
      rate: 110-120%
      description: "임차료, 관리비, 복리후생비 등"

    TECHNICAL_FEE:
      rateBase: LABOR_PLUS_OVERHEAD
      rate: 20-40%
      description: "기술 개발에 대한 이윤"
```

### 6.3 간접비 계산 예시

```json
{
  "indirectCost": {
    "directLaborCost": { "amount": 200000000, "currency": "KRW" },
    "components": [
      {
        "costType": "OVERHEAD",
        "rate": 110,
        "baseAmount": { "amount": 200000000, "currency": "KRW" },
        "cost": { "amount": 220000000, "currency": "KRW" }
      },
      {
        "costType": "TECHNICAL_FEE",
        "rate": 25,
        "baseAmount": { "amount": 420000000, "currency": "KRW" },
        "cost": { "amount": 105000000, "currency": "KRW" }
      }
    ],
    "totalIndirectCost": { "amount": 325000000, "currency": "KRW" }
  }
}
```

---

## 7. ExternalCost (외부비용)

### 7.1 Class 정의

```yaml
Class: ExternalCost
  Extends: SoftwareCost

  Properties:
    - externalCostId: String (PK)

  Relationships:
    - hasExpense: ExternalExpense (1:N)

  Calculation:
    totalExternalCost = SUM(ExternalExpense.cost)
```

### 7.2 ExternalExpense

```yaml
Class: ExternalExpense
  Description: 외주/협력사 및 기타 외부 비용

  Properties:
    - expenseId: String (PK)
    - expenseType: ExternalExpenseType (enum)
    - vendorName: String
    - description: String
    - cost: Money

ExternalExpenseType:
  - OUTSOURCING        # 외주 개발
  - CONSULTING         # 컨설팅
  - DESIGN_SERVICE     # 디자인 서비스
  - TRANSLATION        # 번역/현지화
  - AUDIT              # 감리
  - CERTIFICATION      # 인증
  - TRAINING           # 교육
  - TRAVEL             # 출장
```

---

## 8. 비용 집계 구조

### 8.1 비용 계층 구조

```
TotalProjectCost
├── DirectCost
│   ├── LaborCost
│   ├── InfrastructureCost
│   ├── ToolCost
│   └── ExternalCost
│
├── IndirectCost
│   ├── Overhead
│   ├── ManagementFee
│   └── TechnicalFee
│
└── Contingency
    └── RiskReserve
```

### 8.2 비용 계산 공식

```yaml
CostFormula:
  # 직접비
  DirectCost:
    formula: LaborCost + InfrastructureCost + ToolCost + ExternalCost

  # 간접비 (공공사업 기준)
  IndirectCost:
    Overhead: DirectLaborCost × OverheadRate
    TechnicalFee: (DirectLaborCost + Overhead) × TechnicalFeeRate
    formula: Overhead + TechnicalFee

  # 직접경비 (인프라, 도구, 외부비용)
  DirectExpense:
    formula: InfrastructureCost + ToolCost + ExternalCost

  # 총 비용
  TotalCost:
    formula: DirectCost + IndirectCost

  # 또는 (공공사업 방식)
  TotalCostPublic:
    formula: (DirectLaborCost + Overhead + TechnicalFee) + DirectExpense
```

### 8.3 비용 집계 JSON 예시

```json
{
  "projectCost": {
    "projectId": "PRJ-2024-001",

    "directCost": {
      "laborCost": 200000000,
      "infrastructureCost": 5000000,
      "toolCost": 3000000,
      "externalCost": 20000000,
      "total": 228000000
    },

    "indirectCost": {
      "overhead": 220000000,
      "technicalFee": 105000000,
      "total": 325000000
    },

    "contingency": {
      "riskReserve": 27650000,
      "rate": 5
    },

    "totalCost": {
      "beforeContingency": 553000000,
      "afterContingency": 580650000
    }
  }
}
```

---

## 9. 관계 다이어그램

```
┌──────────────────────────────────────────────────────────────┐
│                      SoftwareCost                             │
│                           │                                   │
│     ┌─────────────────────┼─────────────────────┐            │
│     │                     │                     │            │
│     ▼                     ▼                     ▼            │
│ ┌─────────┐         ┌──────────┐         ┌──────────┐       │
│ │ Direct  │         │ Indirect │         │Contingency│       │
│ │  Cost   │         │   Cost   │         │          │       │
│ └────┬────┘         └────┬─────┘         └──────────┘       │
│      │                   │                                   │
│      ▼                   ▼                                   │
│ ┌─────────┐         ┌──────────┐                            │
│ │ Labor   │         │ Overhead │                            │
│ │ Infra   │         │ Tech Fee │                            │
│ │ Tool    │         │ Mgmt Fee │                            │
│ │External │         └──────────┘                            │
│ └─────────┘                                                  │
└──────────────────────────────────────────────────────────────┘
```

---

## 문서 정보

- **작성일**: 2026-02-25
- **상태**: Phase 4-3 완료
- **다음 문서**: pricing.md (Pricing Ontology)
