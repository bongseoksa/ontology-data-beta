# 03. Relationship Diagrams

## 1) System Context

```mermaid
flowchart LR
  U[요구사항 문서/RFP] --> E[요구사항 추출기]
  E --> RS[req:RequirementSet]
  RS --> SZ[size:SizeEstimate]
  SZ --> CE[cost:CostEstimate]
  CE --> PP[price:PricingPolicy]
  CE --> QQ[quote:EstimateRange]
  RR[risk:RiskScore] --> QQ
  PP --> QQ
  QQ --> QV[quote:QuoteVersion]
  QV --> Q[quote:Quote]

  D1[단가표/가이드] --> PV[prov:Entity]
  D2[과거 실적 데이터] --> PV
  PV --> QV
```

## 2) Class Relationship

```mermaid
classDiagram
  class Project
  class RequirementSet
  class Requirement
  class SizeEstimate
  class CostEstimate
  class PricingPolicy
  class RiskScore
  class EstimateRange
  class Quote
  class QuoteVersion
  class Assumption
  class ProvenanceEntity

  RequirementSet "1" <-- "N" Requirement : belongsToSet
  Requirement "N" --> "N" SizeEstimate : drivesSize
  SizeEstimate "1" --> "N" CostEstimate : informsCost
  CostEstimate "N" --> "1" PricingPolicy : pricedBy
  RiskScore "1" --> "1" EstimateRange : adjustsRange
  Quote "1" --> "N" QuoteVersion : hasVersion
  QuoteVersion "N" --> "N" Assumption : usesAssumption
  QuoteVersion "N" --> "1" RequirementSet : derivedFromRequirementSet
  QuoteVersion "N" --> "N" ProvenanceEntity : prov:wasDerivedFrom
```

## 3) Estimate Generation Flow

```mermaid
sequenceDiagram
  participant User as Engineer
  participant API as Estimate API
  participant KG as Ontology Graph
  participant RULE as SHACL Validator
  participant ENG as Estimation Engine

  User->>API: 요구사항 입력/업로드
  API->>KG: RequirementSet 저장
  API->>RULE: 사전 검증 요청
  RULE-->>API: 검증 결과(OK/오류 목록)
  API->>ENG: size/cost/risk 계산 요청
  ENG->>KG: SizeEstimate, CostEstimate, RiskScore 저장
  ENG->>KG: EstimateRange, QuoteVersion 저장
  ENG->>KG: prov:wasDerivedFrom 링크 저장
  API-->>User: 견적값 + 신뢰구간 + 근거
```

## 4) Versioning Relationship

```mermaid
flowchart TB
  RC[cost:RateCard v2026.1] --> QV1[QuoteVersion 1]
  MP[price:MarginPolicy v3] --> QV1
  IN1[RequirementSet hash:A] --> QV1

  RC2[cost:RateCard v2026.2] --> QV2[QuoteVersion 2]
  MP2[price:MarginPolicy v4] --> QV2
  IN2[RequirementSet hash:B] --> QV2

  Q[quote:Quote Q-2026-001] --> QV1
  Q --> QV2
```

