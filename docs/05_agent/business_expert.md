# Phase 5-3: Business Expert (사업 전문가) 설계

---

## 1. 역할 정의

### 1.1 핵심 역할
시장 환경, 경쟁 상황, 고객 관계를 분석하여 **전략적 가격 조정 요소**를 도출

### 1.2 책임 영역

| 영역 | 설명 |
|------|------|
| **시장 분석** | 해당 산업/기술 시장의 현황 및 동향 파악 |
| **경쟁 분석** | 경쟁 강도 및 경쟁사 가격 수준 평가 |
| **전략 수립** | 가격 전략 및 협상 범위 제안 |
| **관계 평가** | 고객 관계 및 후속 사업 기회 분석 |

---

## 2. 입력 스키마

### 2.1 필수 입력

```json
{
  "projectContext": {
    "projectId": "string",
    "projectType": "enum",
    "contractType": "PROJECT_BASED | BID_BASED | TIME_MATERIAL"
  },

  "clientInfo": {
    "clientId": "string",
    "clientName": "string",
    "clientType": "PUBLIC | ENTERPRISE | SMB | STARTUP",
    "industry": "string",
    "relationship": "NEW | EXISTING | STRATEGIC_PARTNER",
    "previousProjects": "number"
  },

  "bidContext": {
    "bidType": "PUBLIC_LOWEST | PUBLIC_NEGOTIATION | PRIVATE_RFP | DIRECT",
    "expectedCompetitors": "number",
    "knownCompetitors": ["string"],
    "budgetRange": {
      "min": "number",
      "max": "number",
      "currency": "string"
    }
  },

  "technicalAnalysis": {
    "totalFP": "number",
    "sizeCategory": "enum",
    "complexityScore": "float",
    "totalManMonth": "number",
    "estimatedDuration": "number"
  }
}
```

### 2.2 선택 입력

```json
{
  "marketContext": {
    "currentTrends": ["string"],
    "demandLevel": "LOW | MEDIUM | HIGH",
    "supplyLevel": "LOW | MEDIUM | HIGH"
  },

  "historicalData": {
    "previousBids": [...],
    "winRate": "percentage",
    "averageMargin": "percentage"
  }
}
```

---

## 3. 출력 스키마

### 3.1 전체 출력 구조

```json
{
  "agentId": "business_expert",
  "analysisVersion": "1.0",
  "timestamp": "datetime",

  "marketAnalysis": {...},
  "competitiveAnalysis": {...},
  "strategicAssessment": {...},
  "pricingRecommendation": {...},

  "confidence": {
    "overall": "float (0-1)",
    "bySection": {...}
  },

  "rationale": {
    "summary": "string",
    "details": [...]
  }
}
```

### 3.2 Market Analysis (시장 분석)

```json
{
  "marketAnalysis": {
    "industryOverview": {
      "industry": "string",
      "marketSize": "string",
      "growthTrend": "DECLINING | STABLE | GROWING | BOOMING",
      "outlook": "string"
    },
    "demandSupplyGap": {
      "demandLevel": "LOW | MEDIUM | HIGH",
      "supplyLevel": "LOW | MEDIUM | HIGH",
      "gap": "OVERSUPPLY | BALANCED | UNDERSUPPLY",
      "priceImplication": "string"
    },
    "technologyTrends": [
      {
        "trend": "string",
        "relevance": "LOW | MEDIUM | HIGH",
        "impact": "string"
      }
    ],
    "seasonality": {
      "isSeasonalMarket": "boolean",
      "currentSeason": "PEAK | NORMAL | LOW",
      "recommendation": "string"
    }
  }
}
```

### 3.3 Competitive Analysis (경쟁 분석)

```json
{
  "competitiveAnalysis": {
    "competitionLevel": "MONOPOLY | LOW | MEDIUM | HIGH | INTENSE",
    "competitorCount": {
      "expected": "number",
      "known": ["string"]
    },
    "competitorProfile": [
      {
        "name": "string",
        "strengths": ["string"],
        "weaknesses": ["string"],
        "estimatedPriceRange": {
          "min": "number",
          "max": "number"
        },
        "winProbability": "percentage"
      }
    ],
    "ourPosition": {
      "strengths": ["string"],
      "weaknesses": ["string"],
      "differentiators": ["string"]
    },
    "competitiveAdjustmentFactor": "float (0.7-1.2)",
    "rationale": "string"
  }
}
```

### 3.4 Strategic Assessment (전략적 평가)

```json
{
  "strategicAssessment": {
    "clientValue": {
      "currentValue": "LOW | MEDIUM | HIGH",
      "potentialValue": "LOW | MEDIUM | HIGH",
      "factors": ["string"]
    },
    "relationshipFactor": {
      "relationshipType": "NEW | EXISTING | STRATEGIC",
      "trustLevel": "LOW | MEDIUM | HIGH",
      "historyQuality": "POOR | NEUTRAL | GOOD | EXCELLENT",
      "adjustmentFactor": "float (0.85-1.0)"
    },
    "followOnOpportunity": {
      "likelihood": "LOW | MEDIUM | HIGH",
      "estimatedValue": "number",
      "timeline": "string",
      "adjustmentFactor": "float (0.85-1.0)"
    },
    "referenceValue": {
      "referenceQuality": "LOW | MEDIUM | HIGH",
      "marketingValue": "string",
      "adjustmentFactor": "float (0.9-1.0)"
    },
    "overallStrategicWeight": "float (0.75-1.1)",
    "strategicRationale": "string"
  }
}
```

### 3.5 Pricing Recommendation (가격 권고)

```json
{
  "pricingRecommendation": {
    "bidStrategy": "PREMIUM | MARKET_RATE | COMPETITIVE | AGGRESSIVE | PENETRATION",
    "pricePositioning": {
      "vsMarket": "ABOVE | AT | BELOW",
      "percentage": "float"
    },
    "negotiationRange": {
      "ceiling": "percentage from base",
      "target": "percentage from base",
      "floor": "percentage from base",
      "rationale": "string"
    },
    "discountAuthority": {
      "maxDiscount": "percentage",
      "conditions": ["string"]
    },
    "valueProposition": {
      "keyMessages": ["string"],
      "differentiators": ["string"],
      "risksToHighlight": ["string"]
    },
    "winProbabilityEstimate": {
      "atCeiling": "percentage",
      "atTarget": "percentage",
      "atFloor": "percentage"
    }
  }
}
```

---

## 4. 분석 로직

### 4.1 경쟁 강도 평가 로직

```yaml
CompetitionLevelAssessment:
  Factors:
    competitorCount:
      weight: 30%
      scoring:
        0: MONOPOLY
        1-2: LOW
        3-5: MEDIUM
        6-10: HIGH
        ">10": INTENSE

    bidType:
      weight: 25%
      scoring:
        DIRECT: -1 (경쟁 낮춤)
        PRIVATE_RFP: 0
        PUBLIC_NEGOTIATION: +1
        PUBLIC_LOWEST: +2

    priceTransparency:
      weight: 20%
      scoring:
        OPAQUE: -1
        PARTIALLY_VISIBLE: 0
        FULLY_TRANSPARENT: +1

    switchingCost:
      weight: 15%
      scoring:
        HIGH: -1
        MEDIUM: 0
        LOW: +1

    incumbentAdvantage:
      weight: 10%
      scoring:
        STRONG: -1
        WEAK: 0
        NONE: +1

  CompetitiveAdjustmentMapping:
    MONOPOLY: 1.0 - 1.2
    LOW: 0.95 - 1.1
    MEDIUM: 0.90 - 1.0
    HIGH: 0.85 - 0.95
    INTENSE: 0.75 - 0.90
```

### 4.2 전략 가중치 계산 로직

```yaml
StrategicWeightCalculation:
  Components:
    RelationshipFactor:
      NEW_CLIENT: 1.0
      EXISTING_CLIENT: 0.95
      STRATEGIC_PARTNER: 0.90
      weight: 30%

    FollowOnFactor:
      UNLIKELY: 1.0
      POSSIBLE: 0.95
      LIKELY: 0.90
      weight: 30%

    ReferenceFactor:
      LOW_VALUE: 1.0
      MEDIUM_VALUE: 0.95
      HIGH_VALUE: 0.90
      weight: 20%

    MarketEntryFactor:
      EXISTING_MARKET: 1.0
      NEW_SEGMENT: 0.95
      NEW_MARKET: 0.85
      weight: 20%

  Calculation:
    strategicWeight =
      (RelationshipFactor × 0.3) +
      (FollowOnFactor × 0.3) +
      (ReferenceFactor × 0.2) +
      (MarketEntryFactor × 0.2)

  Constraints:
    minimum: 0.75
    maximum: 1.1
```

### 4.3 협상 범위 결정 로직

```yaml
NegotiationRangeLogic:
  BaseRange:
    PUBLIC_LOWEST:
      ceiling: "+5%"
      target: "0%"
      floor: "-10%"

    PUBLIC_NEGOTIATION:
      ceiling: "+10%"
      target: "+5%"
      floor: "-5%"

    PRIVATE_RFP:
      ceiling: "+15%"
      target: "+10%"
      floor: "0%"

    DIRECT:
      ceiling: "+20%"
      target: "+15%"
      floor: "+5%"

  Adjustments:
    strongRelationship: "+5% to all"
    weakCompetition: "+5% to ceiling"
    urgentTimeline: "+10% to floor"
    budgetConstrained: "-5% to all"
```

---

## 5. RAG 활용 전략

### 5.1 RAG 쿼리 시나리오

| 시나리오 | 쿼리 예시 | 활용 목적 |
|----------|----------|----------|
| 시장 동향 | "2024년 금융권 SI 시장 전망" | 시장 분석 근거 |
| 경쟁 가격 | "공공 CRM 구축 낙찰 사례" | 경쟁 가격 참조 |
| 협상 사례 | "대기업 IT 계약 협상 범위" | 협상 범위 설정 |
| 고객 분석 | "○○기업 IT 투자 현황" | 고객 가치 평가 |

### 5.2 RAG 쿼리 템플릿

```json
{
  "queryTemplates": {
    "MARKET_TREND": {
      "query": "{year}년 {industry} {techArea} 시장 동향",
      "filters": {
        "docType": ["REPORT", "ANALYSIS"],
        "recency": "2years"
      }
    },
    "COMPETITOR_PRICE": {
      "query": "{clientType} {projectType} 낙찰 사례 가격",
      "filters": {
        "industry": "{industry}",
        "projectSize": "{sizeCategory}"
      }
    },
    "NEGOTIATION_CASE": {
      "query": "{clientType} {contractType} 계약 협상 사례",
      "filters": {
        "outcome": "SUCCESS"
      }
    }
  }
}
```

---

## 6. LLM 프롬프트 설계

### 6.1 시스템 프롬프트

```
당신은 소프트웨어 사업의 전략 전문가입니다.

역할:
- 시장 환경과 경쟁 상황을 분석합니다
- 고객 관계와 전략적 가치를 평가합니다
- 적절한 가격 전략과 협상 범위를 제안합니다
- 수주 확률을 추정합니다

원칙:
1. 시장 현실 반영: 실제 시장 데이터 기반 분석
2. 전략적 사고: 단기 이익과 장기 관계 균형
3. 리스크 인식: 가격 결정의 리스크 명시
4. 근거 제시: 모든 권고에 구체적 근거 제시

출력 형식:
JSON 형식으로 출력하며, 지정된 스키마를 엄격히 따릅니다.
```

### 6.2 사용자 프롬프트 템플릿

```
## 프로젝트 정보
{projectContext}

## 고객 정보
{clientInfo}

## 입찰 컨텍스트
{bidContext}

## 기술 분석 결과 (Technical Expert)
{technicalAnalysis}

## 참조 데이터 (RAG)
{ragContext}

## 분석 요청
위 정보를 바탕으로 다음을 분석해주세요:
1. 시장 현황 및 동향 분석
2. 경쟁 환경 및 경쟁사 분석
3. 전략적 가치 평가 (고객 관계, 후속 사업, 레퍼런스)
4. 가격 전략 및 협상 범위 권고
5. 수주 확률 추정

분석 결과는 지정된 JSON 스키마로 출력해주세요.
```

---

## 7. 검증 규칙

### 7.1 출력 검증

```yaml
ValidationRules:
  CompetitiveAnalysis:
    - "competitiveAdjustmentFactor가 0.7-1.2 범위 내"
    - "competitionLevel과 adjustmentFactor 일관성"

  StrategicAssessment:
    - "모든 adjustmentFactor가 0.75-1.1 범위 내"
    - "overallStrategicWeight 계산 정확성"

  PricingRecommendation:
    - "floor <= target <= ceiling"
    - "winProbability가 ceiling에서 가장 낮고 floor에서 가장 높음"
    - "bidStrategy와 pricePositioning 일관성"
```

### 7.2 논리적 일관성 검증

```yaml
ConsistencyChecks:
  - check: "경쟁 강도 vs 가격 전략"
    rule: "HIGH 경쟁일 때 PREMIUM 전략이면 경고"
    severity: WARNING

  - check: "고객 관계 vs 할인 수준"
    rule: "NEW 고객에게 과도한 할인은 경고"
    severity: WARNING

  - check: "예산 vs 추천 가격"
    rule: "추천 가격이 예산 범위 밖이면 경고"
    severity: ERROR
```

---

## 문서 정보

- **작성일**: 2026-02-25
- **상태**: Phase 5-3 완료
- **다음 문서**: economic_expert.md
