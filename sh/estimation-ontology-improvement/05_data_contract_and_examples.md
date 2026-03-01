# 05. Data Contract and Examples

## 1) Inbound Contract (요구사항 입력)

필수 필드:

- `projectId`
- `requirementSetId`
- `requirements[]`
- `requirements[].statement`
- `requirements[].priority`
- `requirements[].testability`

권장 필드:

- `requirements[].stability`
- `requirements[].qualityType`
- `constraints[]`
- `assumptions[]`

## 2) Outbound Contract (견적 결과)

필수 필드:

- `quoteId`
- `quoteVersion`
- `estimateRange.min`
- `estimateRange.p50`
- `estimateRange.p80`
- `estimateRange.max`
- `confidence`
- `evidence[]`

권장 필드:

- `riskSummary`
- `policySummary`
- `assumptionDigest`

## 3) JSON-LD Shape (개념)

```json
{
  "@context": "../schemas/context.json",
  "@type": "quote:QuoteVersion",
  "quote:versionNo": 3,
  "quote:generatedAt": "2026-03-01T10:30:00Z",
  "quote:derivedFromRequirementSet": "req:REQSET-2026-0007",
  "quote:usesAssumption": ["base:ASM-01", "base:ASM-02"],
  "prov:wasDerivedFrom": [
    "https://www.sw.or.kr/site/sw/ex/board/View.do?cbIdx=304&bcIdx=64717",
    "https://www.sw.or.kr/site/sw/ex/board/View.do?cbIdx=276&bcIdx=63607"
  ]
}
```

## 4) 운영 체크리스트

- 입력 요구사항 누락 시 견적 생성 차단
- 근거 URI가 비어 있으면 배포 차단
- 산정 결과는 버전 고정 후 수정 불가(신규 버전 생성)

