# 04. Validation and Reasoning

## 1) Validation Strategy

검증은 두 단계로 운영합니다.

1. 사전 검증 (Pre-check)
- 입력 누락, 형식 오류, 정책 적용 가능성 확인

2. 사후 검증 (Post-check)
- 계산 결과 논리 일관성, 범위/신뢰도 유효성 확인

## 2) Hard Validation Rules (견적 차단)

- `QuoteVersion`는 `prov:wasDerivedFrom` 최소 1개 필수
- `EstimateRange`는 `min/p50/p80/max` 모두 필수
- `EstimateRange` 순서 제약: `min <= p50 <= p80 <= max`
- `LaborCost`는 `rateYear`, `rateSource`, `manMonth` 필수
- `Requirement`는 `statement`와 `testability` 필수

## 3) Soft Validation Rules (경고)

- NFR이 있는데 대응 `RiskItem`이 없으면 경고
- `completenessScore < 0.7`이면 신뢰도 하향 경고
- 공공사업인데 정책 근거 URI가 없으면 경고

## 4) SHACL 적용 범위

- NodeShape
  - `quote:QuoteVersion`
  - `quote:EstimateRange`
  - `cost:LaborCost`
  - `req:Requirement`

- PropertyShape
  - datatype 검증
  - 최소/최대 cardinality
  - 값 범위(숫자 비교)

## 5) Reasoning Rules (운영 규칙)

- Rule R1: `RiskScore.level = HIGH` 이고 `Requirement.stability = LOW`면 `scenarioType = CONSERVATIVE` 권고
- Rule R2: 공공 클라이언트 + 보안 NFR 존재 시 `security contingency` 자동 가중
- Rule R3: 요구사항 변경 이벤트가 발생하면 `QuoteVersion` 신규 생성 강제

## 6) Error Handling Contract

- 에러는 코드 + 메시지 + 조치 가이드로 반환

예시:
- `QV_001`: QuoteVersion에 provenance 누락
- `ER_002`: EstimateRange 순서 위반
- `LC_003`: labor rate source 누락
- `RQ_004`: testability 미정의

