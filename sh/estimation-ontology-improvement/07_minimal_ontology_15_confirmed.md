# 07. Minimal Ontology 15 (Confirmed)

- 확정일: 2026-03-01
- 목적: 견적 AI 운영에 필요한 최소 클래스 집합 고정
- 원칙: "작게 시작하고, 강하게 검증"

## 1) 확정 클래스 15

1. `base:Project`
2. `req:RequirementSet`
3. `req:Requirement`
4. `base:Assumption`
5. `base:Constraint`
6. `size:SizeEstimate`
7. `cost:CostEstimate`
8. `cost:LaborCost`
9. `cost:RateCard`
10. `risk:RiskItem`
11. `risk:RiskScore`
12. `price:PricingPolicy`
13. `quote:Quote`
14. `quote:QuoteVersion`
15. `quote:EstimateRange`

## 2) 필수 관계 (확정)

1. `req:Requirement -> req:belongsToSet -> req:RequirementSet`
2. `req:Requirement -> req:drivesSize -> size:SizeEstimate`
3. `size:SizeEstimate -> size:informsCost -> cost:CostEstimate`
4. `cost:CostEstimate -> price:pricedBy -> price:PricingPolicy`
5. `risk:RiskItem -> risk:aggregatedInto -> risk:RiskScore`
6. `risk:RiskScore -> risk:adjustsRange -> quote:EstimateRange`
7. `quote:Quote -> quote:hasVersion -> quote:QuoteVersion`
8. `quote:QuoteVersion -> quote:derivedFromRequirementSet -> req:RequirementSet`
9. `quote:QuoteVersion -> quote:usesAssumption -> base:Assumption`
10. `quote:QuoteVersion -> prov:wasDerivedFrom -> prov:Entity`
11. `cost:LaborCost -> cost:usesRateCard -> cost:RateCard`
12. `base:Project -> quote:hasQuote -> quote:Quote`

## 3) 필수 속성 (Hard Requirement)

- `req:Requirement`: `req:statement`, `req:testability`
- `cost:LaborCost`: `cost:rateYear`, `cost:rateSource`, `cost:pointCost`
- `quote:QuoteVersion`: `quote:versionNo`, `quote:generatedAt`
- `quote:EstimateRange`: `quote:min`, `quote:p50`, `quote:p80`, `quote:max`

## 4) 필수 검증 규칙 (Hard Rule)

1. `QuoteVersion`는 `prov:wasDerivedFrom` 1개 이상
2. `EstimateRange`는 `min <= p50 <= p80 <= max`
3. `LaborCost`는 `RateCard` 미연결 시 invalid
4. `Requirement`는 `statement` 또는 `testability` 누락 시 invalid

## 5) 적용 범위

- 포함: 요구사항 입력 기반 견적 생성/갱신/설명
- 제외: 상세 WBS, 인사/조직 전체 모델링, 고급 계약 도메인

## 6) 확장 정책

- 확장은 "클래스 추가"보다 "속성/규칙 강화"를 우선
- 신규 클래스는 아래 조건 모두 만족 시에만 추가
- 기존 15개로 표현 불가
- 운영 에러의 20% 이상이 해당 누락에서 발생
- 검증 규칙으로 해결 불가

