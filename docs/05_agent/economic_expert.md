# Phase 5-4: Economic Expert (경제 전문가) 설계

---

## 1. 역할 정의

### 1.1 핵심 역할
기술 분석과 사업 분석 결과를 통합하여 **원가 계산, 마진 설정, 최종 가격 산정**을 수행

### 1.2 책임 영역

| 영역 | 설명 |
|------|------|
| **원가 계산** | 직접비, 간접비, 외부비용 상세 산출 |
| **마진 분석** | 목표 마진율 설정 및 손익분기점 계산 |
| **리스크 반영** | 리스크 프리미엄 산정 |
| **가격 결정** | 최종 가격 및 가격 범위 도출 |

---

## 2. 입력 스키마

### 2.1 필수 입력

```json
{
  "projectContext": {
    "projectId": "string",
    "projectType": "enum",
    "contractType": "enum"
  },

  "technicalAnalysis": {
    "teamComposition": [
      {
        "roleType": "enum",
        "skillLevel": "enum",
        "headcount": "number",
        "allocation": "percentage",
        "duration": "number"
      }
    ],
    "totalManMonth": "number",
    "estimatedDuration": "number",
    "complexityScore": "float",
    "adjustmentFactor": "float",
    "technicalRisks": [...]
  },

  "businessAnalysis": {
    "competitiveAdjustmentFactor": "float",
    "strategicWeight": "float",
    "negotiationRange": {...},
    "bidStrategy": "enum"
  },

  "costParameters": {
    "laborRates": {
      "source": "KOSA | CUSTOM",
      "rates": {...}
    },
    "overheadRate": "percentage",
    "technicalFeeRate": "percentage",
    "currency": "string"
  }
}
```

### 2.2 선택 입력

```json
{
  "infrastructureCosts": {
    "development": [...],
    "production": [...]
  },

  "toolCosts": [...],

  "externalCosts": [...],

  "constraints": {
    "budgetCeiling": "number",
    "minimumMargin": "percentage",
    "paymentTerms": "string"
  }
}
```

---

## 3. 출력 스키마

### 3.1 전체 출력 구조

```json
{
  "agentId": "economic_expert",
  "analysisVersion": "1.0",
  "timestamp": "datetime",

  "costBreakdown": {...},
  "marginAnalysis": {...},
  "riskPremiumAnalysis": {...},
  "finalPricing": {...},
  "financialMetrics": {...},

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

### 3.2 Cost Breakdown (비용 상세)

```json
{
  "costBreakdown": {
    "directCost": {
      "laborCost": {
        "details": [
          {
            "roleType": "enum",
            "skillLevel": "enum",
            "techGrade": "특급 | 고급 | 중급 | 초급",
            "headcount": "number",
            "manMonth": "number",
            "unitCost": "number",
            "totalCost": "number"
          }
        ],
        "total": "number"
      },
      "infrastructureCost": {
        "development": "number",
        "staging": "number",
        "total": "number"
      },
      "toolCost": {
        "details": [...],
        "total": "number"
      },
      "externalCost": {
        "outsourcing": "number",
        "consulting": "number",
        "other": "number",
        "total": "number"
      },
      "totalDirectCost": "number"
    },

    "indirectCost": {
      "overhead": {
        "rate": "percentage",
        "base": "number",
        "amount": "number"
      },
      "technicalFee": {
        "rate": "percentage",
        "base": "number",
        "amount": "number"
      },
      "managementFee": {
        "rate": "percentage",
        "base": "number",
        "amount": "number"
      },
      "totalIndirectCost": "number"
    },

    "contingency": {
      "rate": "percentage",
      "amount": "number"
    },

    "totalBaseCost": "number"
  }
}
```

### 3.3 Margin Analysis (마진 분석)

```json
{
  "marginAnalysis": {
    "targetMargin": {
      "rate": "percentage",
      "amount": "number",
      "rationale": "string"
    },
    "marginRange": {
      "minimum": {
        "rate": "percentage",
        "amount": "number"
      },
      "target": {
        "rate": "percentage",
        "amount": "number"
      },
      "maximum": {
        "rate": "percentage",
        "amount": "number"
      }
    },
    "marginFactors": [
      {
        "factor": "string",
        "impact": "percentage",
        "rationale": "string"
      }
    ]
  }
}
```

### 3.4 Risk Premium Analysis (리스크 프리미엄)

```json
{
  "riskPremiumAnalysis": {
    "overallRiskLevel": "LOW | MEDIUM | HIGH | CRITICAL",
    "riskScore": "float (1-5)",
    "premiumRate": "percentage",
    "premiumAmount": "number",
    "riskFactors": [
      {
        "category": "TECHNICAL | BUSINESS | RESOURCE | SCHEDULE",
        "factor": "string",
        "score": "number (1-5)",
        "weight": "percentage",
        "contribution": "percentage",
        "mitigation": "string"
      }
    ],
    "rationale": "string"
  }
}
```

### 3.5 Final Pricing (최종 가격)

```json
{
  "finalPricing": {
    "calculationSteps": [
      {
        "step": "number",
        "description": "string",
        "formula": "string",
        "value": "number"
      }
    ],
    "priceRange": {
      "minimum": {
        "value": "number",
        "marginRate": "percentage",
        "description": "손익분기점 + 최소마진"
      },
      "target": {
        "value": "number",
        "marginRate": "percentage",
        "description": "권장 가격"
      },
      "maximum": {
        "value": "number",
        "marginRate": "percentage",
        "description": "시장 수용 최대가"
      }
    },
    "recommendedPrice": "number",
    "effectiveMarginRate": "percentage",
    "currency": "string"
  }
}
```

### 3.6 Financial Metrics (재무 지표)

```json
{
  "financialMetrics": {
    "breakEvenPoint": {
      "price": "number",
      "marginAtBreakEven": "0%"
    },
    "grossProfitMargin": "percentage",
    "operatingMargin": "percentage",
    "returnOnProject": "percentage",
    "cashFlowAnalysis": {
      "initialInvestment": "number",
      "paybackPeriod": "string",
      "paymentSchedule": [
        {
          "milestone": "string",
          "percentage": "number",
          "amount": "number"
        }
      ]
    },
    "sensitivityAnalysis": {
      "priceChange": {
        "5%_increase": {
          "newMargin": "percentage",
          "winProbabilityImpact": "string"
        },
        "5%_decrease": {
          "newMargin": "percentage",
          "winProbabilityImpact": "string"
        }
      },
      "costChange": {
        "10%_increase": {
          "newMargin": "percentage",
          "recommendation": "string"
        }
      }
    }
  }
}
```

---

## 4. 분석 로직

### 4.1 인건비 계산 로직

```yaml
LaborCostCalculation:
  # 역할 → 기술자 등급 매핑
  RoleToGradeMapping:
    PROJECT_MANAGER:
      default: "고급"
      ifSenior: "특급"
    TECH_LEAD:
      default: "고급"
    ARCHITECT:
      default: "특급"
    SENIOR_DEVELOPER:
      default: "고급"
    MID_DEVELOPER:
      default: "중급"
    JUNIOR_DEVELOPER:
      default: "초급"
    QA_ENGINEER:
      default: "중급"
    DEVOPS:
      default: "중급"

  # 노임단가 (2024년 KOSA 기준 예시)
  LaborRates_2024:
    특급:
      monthly: 12000000
      daily: 550000
    고급:
      monthly: 10000000
      daily: 450000
    중급:
      monthly: 8000000
      daily: 360000
    초급:
      monthly: 5500000
      daily: 250000

  # 계산
  ForEachRole:
    manMonth = headcount × duration × (allocation / 100)
    laborCost = manMonth × monthlyRate

  TotalLaborCost = SUM(laborCost)
```

### 4.2 간접비 계산 로직

```yaml
IndirectCostCalculation:
  # 공공사업 기준
  PublicProjectRates:
    overhead:
      base: "직접인건비"
      rate: "110%"  # 110-120%
      description: "제경비"

    technicalFee:
      base: "직접인건비 + 제경비"
      rate: "25%"   # 20-40%
      description: "기술료"

  # 민간사업 기준 (간소화)
  PrivateProjectRates:
    indirectRate:
      base: "직접비"
      rate: "30-50%"
      description: "간접비 일괄"

  Calculation:
    overhead = DirectLaborCost × OverheadRate
    technicalFee = (DirectLaborCost + overhead) × TechnicalFeeRate
    totalIndirect = overhead + technicalFee
```

### 4.3 리스크 프리미엄 계산 로직

```yaml
RiskPremiumCalculation:
  # 리스크 점수 산정
  RiskFactors:
    TECHNICAL:
      - NEW_TECHNOLOGY: {weight: 15%}
      - INTEGRATION_COMPLEXITY: {weight: 15%}
      - PERFORMANCE_REQUIREMENT: {weight: 10%}

    BUSINESS:
      - REQUIREMENT_CLARITY: {weight: 20%}
      - CLIENT_EXPERIENCE: {weight: 10%}
      - SCOPE_CHANGE_LIKELIHOOD: {weight: 15%}

    RESOURCE:
      - TEAM_AVAILABILITY: {weight: 10%}
      - SKILL_GAP: {weight: 5%}

  # 점수 → 프리미엄율 매핑
  ScoreToPremiumMapping:
    - range: [1.0, 1.5]
      premiumRate: "0-3%"
      level: LOW

    - range: [1.5, 2.5]
      premiumRate: "3-8%"
      level: MEDIUM

    - range: [2.5, 3.5]
      premiumRate: "8-15%"
      level: HIGH

    - range: [3.5, 5.0]
      premiumRate: "15-30%"
      level: CRITICAL

  Calculation:
    riskScore = SUM(factor.score × factor.weight)
    premiumRate = MapToRate(riskScore)
    premiumAmount = BaseCost × premiumRate
```

### 4.4 최종 가격 계산 로직

```yaml
FinalPriceCalculation:
  Steps:
    1_BaseCost:
      formula: "DirectCost + IndirectCost + Contingency"
      description: "총 원가"

    2_MarginedPrice:
      formula: "BaseCost × (1 + MarginRate)"
      description: "마진 적용"

    3_RiskAdjusted:
      formula: "MarginedPrice × (1 + RiskPremiumRate)"
      description: "리스크 반영"

    4_CompetitiveAdjusted:
      formula: "RiskAdjusted × CompetitiveAdjustmentFactor"
      description: "경쟁 조정"

    5_StrategicAdjusted:
      formula: "CompetitiveAdjusted × StrategicWeight"
      description: "전략 가중치"

  FinalPrice: "Step 5 결과"

  EffectiveMargin:
    formula: "(FinalPrice - BaseCost) / BaseCost × 100"
```

---

## 5. RAG 활용 전략

### 5.1 RAG 쿼리 시나리오

| 시나리오 | 쿼리 예시 | 활용 목적 |
|----------|----------|----------|
| 노임단가 | "2024년 KOSA SW기술자 노임단가" | 인건비 기준 |
| 마진율 벤치마크 | "중형 SI 프로젝트 평균 마진율" | 마진 설정 |
| 간접비율 | "공공 SW사업 제경비율 기준" | 간접비 산정 |
| 유사 사례 | "500FP CRM 프로젝트 계약 금액" | 가격 검증 |

### 5.2 RAG 쿼리 템플릿

```json
{
  "queryTemplates": {
    "LABOR_RATE": {
      "query": "{year}년 SW기술자 {grade}등급 노임단가",
      "filters": {
        "docType": "OFFICIAL_RATE",
        "source": "KOSA"
      }
    },
    "MARGIN_BENCHMARK": {
      "query": "{projectType} {sizeCategory} 프로젝트 마진율",
      "filters": {
        "industry": "{industry}",
        "recency": "3years"
      }
    },
    "SIMILAR_PROJECT": {
      "query": "{fpRange}FP {systemType} 프로젝트 계약 사례",
      "filters": {
        "projectSize": "{sizeCategory}",
        "clientType": "{clientType}"
      }
    }
  }
}
```

---

## 6. LLM 프롬프트 설계

### 6.1 시스템 프롬프트

```
당신은 소프트웨어 프로젝트의 경제/재무 전문가입니다.

역할:
- 프로젝트 원가를 정확하게 계산합니다
- 적절한 마진과 리스크 프리미엄을 산정합니다
- 최종 가격과 가격 범위를 도출합니다
- 재무적 타당성을 검증합니다

원칙:
1. 정확한 계산: 모든 비용 항목을 누락 없이 계산
2. 보수적 마진: 최소 마진 보장 원칙
3. 리스크 반영: 식별된 리스크를 가격에 반영
4. 검증 가능: 모든 계산 과정 추적 가능

출력 형식:
JSON 형식으로 출력하며, 지정된 스키마를 엄격히 따릅니다.
모든 금액은 원화(KRW) 단위로 표시합니다.
```

### 6.2 사용자 프롬프트 템플릿

```
## 프로젝트 정보
{projectContext}

## 기술 분석 결과 (Technical Expert)
{technicalAnalysis}

## 사업 분석 결과 (Business Expert)
{businessAnalysis}

## 비용 파라미터
{costParameters}

## 참조 데이터 (RAG)
{ragContext}

## 분석 요청
위 정보를 바탕으로 다음을 계산해주세요:
1. 상세 비용 내역 (직접비, 간접비, 예비비)
2. 마진 분석 (목표 마진, 마진 범위)
3. 리스크 프리미엄 산정
4. 최종 가격 및 가격 범위
5. 재무 지표 (손익분기점, 수익률 등)

계산 결과는 지정된 JSON 스키마로 출력해주세요.
```

---

## 7. 검증 규칙

### 7.1 계산 검증

```yaml
CalculationValidation:
  CostBreakdown:
    - "totalDirectCost = laborCost + infraCost + toolCost + externalCost"
    - "totalIndirectCost = overhead + technicalFee + managementFee"
    - "totalBaseCost = totalDirectCost + totalIndirectCost + contingency"

  FinalPrice:
    - "recommendedPrice >= totalBaseCost (손실 방지)"
    - "effectiveMarginRate >= minimumMargin (최소마진 보장)"
    - "minimum <= target <= maximum (가격 범위 일관성)"

  FinancialMetrics:
    - "breakEvenPoint = totalBaseCost"
    - "grossProfitMargin = (FinalPrice - totalBaseCost) / FinalPrice"
```

### 7.2 비즈니스 규칙 검증

```yaml
BusinessRuleValidation:
  - rule: "최소 마진 보장"
    check: "effectiveMarginRate >= 5%"
    severity: ERROR
    action: "가격 상향 필요"

  - rule: "시장 가격 범위"
    check: "recommendedPrice within marketRange ± 20%"
    severity: WARNING
    action: "가격 재검토 권고"

  - rule: "예산 준수"
    check: "recommendedPrice <= budgetCeiling"
    severity: WARNING
    action: "범위 조정 또는 스코프 협의"
```

### 7.3 데이터 일관성 검증

```yaml
ConsistencyChecks:
  - check: "인건비 vs M/M"
    rule: "totalLaborCost / totalManMonth가 적정 단가 범위 내"
    range: [5000000, 15000000]
    severity: ERROR

  - check: "간접비율 적정성"
    rule: "totalIndirectCost / totalDirectCost가 0.5-1.5 범위 내"
    severity: WARNING

  - check: "전체 비용 vs FP"
    rule: "totalBaseCost / totalFP가 50-100만원 범위 내"
    severity: WARNING
```

---

## 8. 출력 예시

```json
{
  "agentId": "economic_expert",
  "timestamp": "2024-03-15T14:30:00Z",

  "costBreakdown": {
    "directCost": {
      "laborCost": {
        "details": [
          {"roleType": "PM", "grade": "고급", "manMonth": 6, "unitCost": 10000000, "totalCost": 60000000},
          {"roleType": "BACKEND", "grade": "중급", "manMonth": 15, "unitCost": 8000000, "totalCost": 120000000}
        ],
        "total": 200000000
      },
      "infrastructureCost": {"total": 5000000},
      "toolCost": {"total": 3000000},
      "externalCost": {"total": 10000000},
      "totalDirectCost": 218000000
    },
    "indirectCost": {
      "overhead": {"rate": 110, "amount": 220000000},
      "technicalFee": {"rate": 25, "amount": 105000000},
      "totalIndirectCost": 325000000
    },
    "contingency": {"rate": 5, "amount": 27150000},
    "totalBaseCost": 570150000
  },

  "finalPricing": {
    "recommendedPrice": 655000000,
    "priceRange": {
      "minimum": 599000000,
      "target": 655000000,
      "maximum": 720000000
    },
    "effectiveMarginRate": 14.9
  },

  "confidence": {"overall": 0.85}
}
```

---

## 문서 정보

- **작성일**: 2026-02-25
- **상태**: Phase 5-4 완료
- **다음 단계**: Phase 6 - 계산 엔진 설계
