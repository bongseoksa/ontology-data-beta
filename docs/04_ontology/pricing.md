# Phase 4-4: Pricing Ontology 설계

---

## 1. Pricing Ontology 개요

### 1.1 목적
비용(Cost)에서 최종 가격(Price)으로 변환하는 과정에서 적용되는
마진 정책, 리스크 프리미엄, 경쟁 조정, 전략적 가중치를 모델링

### 1.2 Cost → Price 변환 흐름

```
BaseCost (원가)
    ↓ + MarginPolicy (마진 정책)
    ↓ + RiskPremium (리스크 프리미엄)
    ↓ × CompetitiveAdjustment (경쟁 조정)
    ↓ × StrategicWeight (전략 가중치)
    ↓
FinalPrice (최종 가격)
```

---

## 2. Pricing 기본 구조

### 2.1 Class 정의

```yaml
Class: Pricing
  Description: 가격 산정을 위한 종합 정책

  Properties:
    - pricingId: String (PK)
    - projectId: String (FK)
    - baseCost: Money
    - finalPrice: Money
    - calculatedAt: DateTime

  Relationships:
    - basedOn: SoftwareCost (1:1)
    - appliesMargin: MarginPolicy (1:1)
    - appliesRiskPremium: RiskPremium (1:1)
    - appliesCompetitiveAdjustment: CompetitiveAdjustment (1:1)
    - appliesStrategicWeight: StrategicWeight (1:1)
    - produces: Core:Revenue (1:1)
```

### 2.2 가격 계산 공식

```yaml
PricingFormula:
  # 기본 공식
  FinalPrice = BaseCost × (1 + MarginRate) × (1 + RiskPremiumRate) × CompetitiveAdjustmentFactor × StrategicWeightFactor

  # 세부 전개
  Components:
    BaseCost: TotalProjectCost (from Cost Ontology)
    MarginRate: 목표 마진율 (예: 15%)
    RiskPremiumRate: 리스크 프리미엄율 (예: 5%)
    CompetitiveAdjustmentFactor: 경쟁 조정 계수 (예: 0.95)
    StrategicWeightFactor: 전략 가중치 (예: 1.0)
```

---

## 3. MarginPolicy (마진 정책)

### 3.1 Class 정의

```yaml
Class: MarginPolicy
  Description: 프로젝트 마진 정책

  Properties:
    - marginPolicyId: String (PK)
    - marginType: MarginType (enum)
    - targetMarginRate: Percentage
    - minMarginRate: Percentage
    - maxMarginRate: Percentage
    - calculatedMargin: Money
    - justification: String

  Enums:
    MarginType:
      - FIXED_RATE          # 고정 마진율
      - TIERED              # 규모별 차등
      - VALUE_BASED         # 가치 기반
      - COMPETITIVE         # 경쟁 기반
```

### 3.2 마진율 기준

```yaml
MarginRateGuideline:
  # 프로젝트 유형별
  ByProjectType:
    SI_PROJECT:
      typical: "10-15%"
      range: [5, 20]

    CUSTOM_DEVELOPMENT:
      typical: "15-25%"
      range: [10, 35]

    SOLUTION_CUSTOMIZATION:
      typical: "20-30%"
      range: [15, 40]

    CONSULTING:
      typical: "25-40%"
      range: [20, 50]

  # 고객 유형별
  ByClientType:
    PUBLIC_SECTOR:
      typical: "10-15%"
      note: "법적 기준 적용"

    ENTERPRISE:
      typical: "15-20%"
      note: "협상 여지 있음"

    SMB:
      typical: "20-30%"
      note: "가격 민감도 낮음"

    STARTUP:
      typical: "25-35%"
      note: "가치 기반 가격"
```

### 3.3 마진 계산 예시

```json
{
  "marginPolicy": {
    "marginType": "TIERED",
    "baseCost": { "amount": 500000000, "currency": "KRW" },
    "rules": [
      { "threshold": 0, "rate": 20, "description": "기본 마진" },
      { "threshold": 300000000, "rate": 15, "description": "3억 초과" },
      { "threshold": 500000000, "rate": 12, "description": "5억 초과" }
    ],
    "appliedRate": 12,
    "calculatedMargin": { "amount": 60000000, "currency": "KRW" }
  }
}
```

---

## 4. RiskPremium (리스크 프리미엄)

### 4.1 Class 정의

```yaml
Class: RiskPremium
  Description: 프로젝트 리스크에 대한 가격 프리미엄

  Properties:
    - riskPremiumId: String (PK)
    - overallRiskLevel: RiskLevel (enum)
    - premiumRate: Percentage
    - premiumAmount: Money
    - riskFactors: RiskFactor[]

  Relationships:
    - evaluates: Core:Risk (N:N)

  Calculation:
    premiumRate = SUM(RiskFactor.weight × RiskFactor.score)
    premiumAmount = BaseCost × (premiumRate / 100)
```

### 4.2 RiskFactor (리스크 요소)

```yaml
Class: RiskFactor
  Properties:
    - factorId: String (PK)
    - factorType: RiskFactorType (enum)
    - score: Decimal (1-5)
    - weight: Percentage
    - premiumContribution: Percentage

RiskFactorType:
  # 기술 리스크
  TECHNICAL:
    - NEW_TECHNOLOGY:
        description: "신기술 도입 여부"
        lowScore: "검증된 기술"
        highScore: "미검증 최신 기술"
        weight: 15%

    - INTEGRATION_COMPLEXITY:
        description: "연동 복잡도"
        lowScore: "단순 연동"
        highScore: "다수 레거시 연동"
        weight: 15%

    - PERFORMANCE_REQUIREMENT:
        description: "성능 요구 수준"
        lowScore: "일반적 요구"
        highScore: "극한 성능 요구"
        weight: 10%

  # 비즈니스 리스크
  BUSINESS:
    - REQUIREMENT_CLARITY:
        description: "요구사항 명확도"
        lowScore: "상세 명세 있음"
        highScore: "모호한 요구사항"
        weight: 20%

    - CLIENT_EXPERIENCE:
        description: "고객 IT 경험"
        lowScore: "IT 이해도 높음"
        highScore: "IT 이해도 낮음"
        weight: 10%

    - SCOPE_CHANGE_LIKELIHOOD:
        description: "범위 변경 가능성"
        lowScore: "변경 가능성 낮음"
        highScore: "변경 가능성 높음"
        weight: 15%

  # 자원 리스크
  RESOURCE:
    - TEAM_AVAILABILITY:
        description: "인력 확보 용이성"
        lowScore: "인력 확보 용이"
        highScore: "인력 확보 어려움"
        weight: 10%

    - SKILL_GAP:
        description: "기술 역량 갭"
        lowScore: "충분한 역량"
        highScore: "역량 부족"
        weight: 5%
```

### 4.3 리스크 프리미엄 계산

```yaml
RiskPremiumCalculation:
  # 리스크 점수 산정
  riskScore = SUM(factor.score × factor.weight) / SUM(factor.weight)

  # 점수 → 프리미엄율 매핑
  PremiumRateMapping:
    - scoreRange: [1.0, 1.5]
      premiumRate: 0-3%
      level: LOW

    - scoreRange: [1.5, 2.5]
      premiumRate: 3-8%
      level: MEDIUM

    - scoreRange: [2.5, 3.5]
      premiumRate: 8-15%
      level: HIGH

    - scoreRange: [3.5, 5.0]
      premiumRate: 15-30%
      level: CRITICAL
```

### 4.4 리스크 프리미엄 예시

```json
{
  "riskPremium": {
    "riskFactors": [
      { "factorType": "NEW_TECHNOLOGY", "score": 3, "weight": 15 },
      { "factorType": "REQUIREMENT_CLARITY", "score": 4, "weight": 20 },
      { "factorType": "INTEGRATION_COMPLEXITY", "score": 2, "weight": 15 }
    ],
    "overallRiskScore": 3.1,
    "overallRiskLevel": "HIGH",
    "premiumRate": 12,
    "baseCost": { "amount": 500000000, "currency": "KRW" },
    "premiumAmount": { "amount": 60000000, "currency": "KRW" }
  }
}
```

---

## 5. CompetitiveAdjustment (경쟁 조정)

### 5.1 Class 정의

```yaml
Class: CompetitiveAdjustment
  Description: 경쟁 환경에 따른 가격 조정

  Properties:
    - adjustmentId: String (PK)
    - competitionLevel: CompetitionLevel (enum)
    - adjustmentFactor: Decimal (0.7 ~ 1.2)
    - marketPosition: MarketPosition (enum)
    - bidStrategy: BidStrategy (enum)
    - justification: String

  Enums:
    CompetitionLevel:
      - MONOPOLY          # 독점 (경쟁 없음)
      - LOW               # 낮음 (1-2 경쟁사)
      - MEDIUM            # 보통 (3-5 경쟁사)
      - HIGH              # 높음 (6+ 경쟁사)
      - INTENSE           # 치열 (가격 전쟁)

    MarketPosition:
      - LEADER            # 시장 선도자
      - CHALLENGER        # 도전자
      - FOLLOWER          # 추종자
      - NICHE             # 틈새 시장

    BidStrategy:
      - PREMIUM           # 프리미엄 가격 (1.1~1.2)
      - MARKET_RATE       # 시장 가격 (1.0)
      - COMPETITIVE       # 경쟁 가격 (0.9~1.0)
      - AGGRESSIVE        # 공격적 가격 (0.8~0.9)
      - PENETRATION       # 시장 침투 (0.7~0.8)
```

### 5.2 경쟁 조정 계수 가이드

```yaml
CompetitiveAdjustmentGuide:
  # 경쟁 수준별
  ByCompetitionLevel:
    MONOPOLY:
      factor: [1.0, 1.2]
      recommendation: "가치 기반 가격 가능"

    LOW:
      factor: [0.95, 1.1]
      recommendation: "프리미엄 가격 유지 가능"

    MEDIUM:
      factor: [0.90, 1.0]
      recommendation: "시장 가격 수준"

    HIGH:
      factor: [0.85, 0.95]
      recommendation: "경쟁적 가격 필요"

    INTENSE:
      factor: [0.75, 0.90]
      recommendation: "가격 경쟁 불가피"

  # 입찰 유형별
  ByBidType:
    PUBLIC_LOWEST_PRICE:
      factor: [0.80, 0.90]
      note: "최저가 낙찰"

    PUBLIC_NEGOTIATION:
      factor: [0.90, 0.95]
      note: "협상에 의한 계약"

    PRIVATE_RFP:
      factor: [0.90, 1.05]
      note: "기술/가격 종합 평가"

    PRIVATE_DIRECT:
      factor: [1.0, 1.1]
      note: "수의 계약"
```

---

## 6. StrategicWeight (전략 가중치)

### 6.1 Class 정의

```yaml
Class: StrategicWeight
  Description: 전략적 고려사항에 따른 가격 조정

  Properties:
    - weightId: String (PK)
    - overallWeight: Decimal (0.8 ~ 1.3)
    - strategicFactors: StrategicFactor[]
    - justification: String

  Calculation:
    overallWeight = PRODUCT(factor.weight) or AVERAGE(factor.weight)
```

### 6.2 StrategicFactor (전략 요소)

```yaml
StrategicFactor:
  # 관계 요소
  RELATIONSHIP:
    - CLIENT_RELATIONSHIP:
        description: "기존 고객 관계"
        newClient: 1.0
        existingClient: 0.95
        strategicPartner: 0.90

    - REFERENCE_VALUE:
        description: "레퍼런스 가치"
        lowValue: 1.0
        highValue: 0.90
        note: "전략적 레퍼런스인 경우 할인"

  # 사업 요소
  BUSINESS:
    - FOLLOW_ON_OPPORTUNITY:
        description: "후속 사업 가능성"
        unlikely: 1.0
        possible: 0.95
        likely: 0.90
        note: "후속 사업 기대 시 할인"

    - MARKET_ENTRY:
        description: "신규 시장 진입"
        existingMarket: 1.0
        newMarket: 0.85
        note: "신규 시장 진입 시 공격적 가격"

  # 브랜드 요소
  BRAND:
    - PORTFOLIO_FIT:
        description: "포트폴리오 적합성"
        low: 1.0
        high: 0.95

    - INNOVATION_VALUE:
        description: "혁신 프로젝트 가치"
        standard: 1.0
        innovative: 0.90
        note: "기술 시연 목적 프로젝트"
```

### 6.3 전략 가중치 예시

```json
{
  "strategicWeight": {
    "factors": [
      {
        "type": "CLIENT_RELATIONSHIP",
        "value": "existingClient",
        "weight": 0.95
      },
      {
        "type": "FOLLOW_ON_OPPORTUNITY",
        "value": "likely",
        "weight": 0.90
      },
      {
        "type": "REFERENCE_VALUE",
        "value": "highValue",
        "weight": 0.90
      }
    ],
    "overallWeight": 0.77,
    "adjustedWeight": 0.85,
    "justification": "전략적 고객 - 후속 사업 및 레퍼런스 기대"
  }
}
```

---

## 7. 최종 가격 산정

### 7.1 전체 계산 흐름

```yaml
FinalPriceCalculation:
  Step1_BaseCost:
    input: Cost Ontology
    output: BaseCost (총 원가)

  Step2_ApplyMargin:
    formula: BaseCost × (1 + MarginRate)
    output: MarginedPrice

  Step3_ApplyRiskPremium:
    formula: MarginedPrice × (1 + RiskPremiumRate)
    output: RiskAdjustedPrice

  Step4_ApplyCompetitiveAdjustment:
    formula: RiskAdjustedPrice × CompetitiveAdjustmentFactor
    output: CompetitivePrice

  Step5_ApplyStrategicWeight:
    formula: CompetitivePrice × StrategicWeightFactor
    output: FinalPrice
```

### 7.2 가격 범위 산정

```yaml
PriceRange:
  # 최소 가격 (손익분기점)
  minimumPrice: BaseCost

  # 목표 가격
  targetPrice: FinalPrice (calculated)

  # 최대 가격 (시장 수용 가능)
  maximumPrice: BaseCost × MaxMarginFactor × MaxRiskPremium

  # 협상 범위
  negotiationRange:
    floor: minimumPrice × 1.05  # 최소 5% 마진
    target: targetPrice
    ceiling: maximumPrice
```

### 7.3 최종 가격 JSON 예시

```json
{
  "pricing": {
    "projectId": "PRJ-2024-001",

    "baseCost": { "amount": 500000000, "currency": "KRW" },

    "marginPolicy": {
      "type": "FIXED_RATE",
      "rate": 15,
      "amount": { "amount": 75000000, "currency": "KRW" }
    },

    "riskPremium": {
      "level": "MEDIUM",
      "rate": 8,
      "amount": { "amount": 46000000, "currency": "KRW" }
    },

    "competitiveAdjustment": {
      "level": "MEDIUM",
      "factor": 0.95
    },

    "strategicWeight": {
      "factors": ["existingClient", "followOnOpportunity"],
      "factor": 0.92
    },

    "calculation": {
      "step1_baseCost": 500000000,
      "step2_afterMargin": 575000000,
      "step3_afterRisk": 621000000,
      "step4_afterCompetitive": 589950000,
      "step5_finalPrice": 542754000
    },

    "priceRange": {
      "minimum": 500000000,
      "target": 542754000,
      "maximum": 700000000,
      "negotiationFloor": 525000000
    },

    "finalPrice": { "amount": 542754000, "currency": "KRW" },

    "effectiveMarginRate": 8.55
  }
}
```

---

## 8. 관계 다이어그램

```
┌────────────────────────────────────────────────────────────────┐
│                         Pricing                                 │
│                            │                                    │
│     ┌──────────────────────┼──────────────────────┐            │
│     │                      │                      │            │
│     ▼                      ▼                      ▼            │
│ ┌─────────┐          ┌──────────┐          ┌──────────┐       │
│ │ Margin  │          │   Risk   │          │Competitive│       │
│ │ Policy  │          │ Premium  │          │Adjustment │       │
│ └─────────┘          └──────────┘          └──────────┘       │
│                                                   │            │
│                            ┌──────────────────────┘            │
│                            ▼                                   │
│                      ┌──────────┐                              │
│                      │Strategic │                              │
│                      │ Weight   │                              │
│                      └────┬─────┘                              │
│                           │                                    │
│                           ▼                                    │
│                    ┌────────────┐                              │
│                    │Final Price │                              │
│                    └────────────┘                              │
└────────────────────────────────────────────────────────────────┘
```

---

## 문서 정보

- **작성일**: 2026-02-25
- **상태**: Phase 4-4 완료
- **다음 단계**: Phase 5 - Multi-Agent 구조 설계
