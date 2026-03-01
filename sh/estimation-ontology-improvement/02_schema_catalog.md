# 02. Schema Catalog

## 1) Namespace

- `base:` 공통 엔티티
- `req:` 요구사항
- `size:` 기능규모
- `cost:` 원가
- `risk:` 리스크/불확실성
- `price:` 가격정책
- `quote:` 견적 결과
- `prov:` 근거 추적 (W3C PROV-O)

## 2) Core Class Catalog

| Module | Class | Purpose | Key Properties |
|---|---|---|---|
| base | `base:Project` | 견적 대상 프로젝트 식별 | `projectId`, `name`, `domain`, `clientType` |
| base | `base:Assumption` | 계산 가정 관리 | `text`, `impact`, `owner`, `validFrom` |
| base | `base:Constraint` | 일정/예산/정책 제약 | `constraintType`, `severity`, `description` |
| req | `req:RequirementSet` | 입력 요구사항 묶음(스냅샷) | `setId`, `sourceType`, `createdAt`, `completenessScore` |
| req | `req:Requirement` | 개별 요구사항 | `reqId`, `statement`, `priority`, `stability`, `testability` |
| req | `req:NonFunctionalRequirement` | NFR (성능/보안/가용성 등) | `qualityType`, `targetMetric`, `targetValue` |
| size | `size:SizeEstimate` | 기능규모 추정 상위 | `sizeId`, `method`, `sizeValue`, `unit` |
| size | `size:FunctionPointEstimate` | FP 추정 | `ifpugVersion`, `uFP`, `vaf`, `fp` |
| size | `size:COSMICEstimate` | COSMIC 추정 | `entryCount`, `exitCount`, `readCount`, `writeCount`, `cfp` |
| cost | `cost:CostEstimate` | 비용 추정 상위 | `costId`, `currency`, `pointCost`, `costYear` |
| cost | `cost:LaborCost` | 인건비 세부 | `manMonth`, `gradeMix`, `rateYear`, `rateSource` |
| cost | `cost:RateCard` | 단가표 버전 | `rateCardId`, `provider`, `effectiveFrom`, `effectiveTo` |
| risk | `risk:RiskItem` | 리스크 항목 | `riskType`, `score`, `weight`, `mitigationPlan` |
| risk | `risk:RiskScore` | 집계 점수 | `weightedScore`, `level`, `confidence` |
| risk | `risk:UncertaintyDistribution` | 불확실성 분포 | `distributionType`, `parametersJson` |
| price | `price:PricingPolicy` | 가격 정책 상위 | `policyId`, `policyType`, `validFrom`, `validTo` |
| price | `price:MarginPolicy` | 마진 정책 | `targetMarginRate`, `minRate`, `maxRate` |
| quote | `quote:EstimateScenario` | 시나리오(낙관/기준/보수) | `scenarioType`, `description`, `selected` |
| quote | `quote:Quote` | 견적 식별자(업무 단위) | `quoteId`, `status`, `ownerTeam` |
| quote | `quote:QuoteVersion` | 실행 시점 견적 버전 | `versionNo`, `generatedAt`, `modelVersion`, `qualityGateResult` |
| quote | `quote:EstimateRange` | 범위 견적 결과 | `min`, `p50`, `p80`, `max`, `pointEstimate` |

## 3) Object Property Catalog

| Property | Domain -> Range | Cardinality | 설명 |
|---|---|---|---|
| `req:belongsToSet` | `req:Requirement` -> `req:RequirementSet` | N:1 | 요구사항이 속한 입력 스냅샷 |
| `req:drivesSize` | `req:Requirement` -> `size:SizeEstimate` | N:N | 요구사항이 규모를 유도 |
| `size:informsCost` | `size:SizeEstimate` -> `cost:CostEstimate` | 1:N | 규모에서 비용으로 전이 |
| `price:pricedBy` | `cost:CostEstimate` -> `price:PricingPolicy` | N:1 | 비용에 적용된 정책 |
| `risk:adjustsRange` | `risk:RiskScore` -> `quote:EstimateRange` | 1:1 | 리스크가 범위를 보정 |
| `quote:hasVersion` | `quote:Quote` -> `quote:QuoteVersion` | 1:N | 견적 버전 히스토리 |
| `quote:usesAssumption` | `quote:QuoteVersion` -> `base:Assumption` | N:N | 버전에 사용된 가정 |
| `quote:derivedFromRequirementSet` | `quote:QuoteVersion` -> `req:RequirementSet` | N:1 | 버전의 입력 근거 |
| `prov:wasDerivedFrom` | `quote:QuoteVersion` -> `prov:Entity` | N:N | 문서/데이터/모델 출처 링크 |

## 4) Data Property Rules (요약)

- `quote:EstimateRange`:
  - 필수: `min`, `p50`, `p80`, `max`
  - 제약: `min <= p50 <= p80 <= max`

- `cost:LaborCost`:
  - 필수: `manMonth`, `rateYear`, `rateSource`

- `req:Requirement`:
  - 필수: `statement`, `priority`, `testability`

## 5) Versioning 규약

- 정책/단가/모델은 모두 기간 속성 필수
- 권장 필드: `validFrom`, `validTo`, `sourceURI`, `sourceVersion`
- 재현성을 위해 `quote:QuoteVersion`에 아래 필드 저장
  - `modelVersion`
  - `rateCardVersion`
  - `policyVersion`
  - `inputSnapshotHash`

