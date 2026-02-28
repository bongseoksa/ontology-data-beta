# Phase 9: 통합 의사결정 레이어 설계

---

## 1. 통합 레이어 개요

### 1.1 목적
다중 전문가(기술/경제/사업)의 분석 결과를 **통합**하고,
**충돌을 조정**하여 **최종 가격을 결정**하는 레이어

### 1.2 핵심 역할

| 역할 | 설명 |
|------|------|
| **결과 통합** | 각 전문가의 출력을 하나의 의사결정 컨텍스트로 통합 |
| **충돌 조정** | 전문가 간 상충되는 판단 조정 |
| **최종 결정** | 규칙 기반 + LLM 기반 최종 가격 결정 |
| **설명 생성** | 가격 산정 근거 설명문 생성 |

### 1.3 처리 흐름

```
┌─────────────────────────────────────────────────────────────────┐
│                      전문가 출력 수집                            │
├─────────────┬─────────────┬─────────────────────────────────────┤
│ 기술 전문가  │ 경제 전문가  │           사업 전문가              │
│             │             │                                     │
│ - 복잡도    │ - 원가      │ - 전략 가중치                       │
│ - 인력 구성 │ - 마진      │ - 경쟁 강도                         │
│ - 기간     │ - 리스크    │ - 할인 범위                          │
└──────┬──────┴──────┬──────┴─────────────┬───────────────────────┘
       │             │                    │
       └─────────────┴────────────────────┘
                     │
                     ▼
       ┌─────────────────────────────┐
       │      충돌 감지 및 조정       │
       └──────────────┬──────────────┘
                      │
                      ▼
       ┌─────────────────────────────┐
       │      최종 가격 계산          │
       │   (규칙 기반 엔진)           │
       └──────────────┬──────────────┘
                      │
                      ▼
       ┌─────────────────────────────┐
       │      설명문 생성             │
       │   (LLM 기반)                │
       └──────────────┬──────────────┘
                      │
                      ▼
       ┌─────────────────────────────┐
       │      최종 출력               │
       └─────────────────────────────┘
```

---

## 2. 입력 스키마

### 2.1 전문가 출력 통합 입력

```json
{
  "project_context": {
    "project_id": "string",
    "project_name": "string",
    "project_type": "string",
    "extracted_data": {...}
  },

  "technical_analysis": {
    "feature_complexity_score": {
      "value": "number (1-10)",
      "confidence": "number (0-1)"
    },
    "required_roles": [
      {
        "role": "string",
        "seniority": "JUNIOR | MID | SENIOR",
        "count": "number",
        "duration_months": "number"
      }
    ],
    "estimated_duration": {
      "optimistic": "number",
      "realistic": "number",
      "pessimistic": "number",
      "unit": "MONTH"
    },
    "technical_risks": ["string"],
    "reasoning": "string"
  },

  "economic_analysis": {
    "base_cost": {
      "labor_cost": "number",
      "infrastructure_cost": "number",
      "external_cost": "number",
      "overhead_cost": "number",
      "total": "number",
      "currency": "string"
    },
    "break_even_price": "number",
    "recommended_margin": {
      "min": "number",
      "recommended": "number",
      "max": "number"
    },
    "risk_premium": {
      "rate": "number",
      "factors": ["string"]
    },
    "reasoning": "string"
  },

  "business_analysis": {
    "strategic_weight": {
      "value": "number (0.8-1.2)",
      "factors": ["string"]
    },
    "competition_level": {
      "level": "LOW | MEDIUM | HIGH",
      "impact": "string"
    },
    "discount_range": {
      "min_discount": "number",
      "max_discount": "number",
      "recommended": "number"
    },
    "market_conditions": {
      "favorable": "boolean",
      "factors": ["string"]
    },
    "reasoning": "string"
  },

  "rag_references": {
    "similar_projects": [...],
    "pricing_benchmarks": [...],
    "market_data": [...]
  }
}
```

---

## 3. 충돌 감지 및 조정

### 3.1 충돌 유형 정의

| 충돌 유형 | 설명 | 예시 |
|----------|------|------|
| **기간-비용 불일치** | 기술 기간과 경제 비용의 상관관계 불일치 | 6개월 추정에 1년치 인건비 |
| **마진-전략 충돌** | 권장 마진과 전략 가중치 상충 | 고마진 권장 + 공격적 할인 필요 |
| **리스크 중복** | 복수 전문가가 동일 리스크 이중 반영 | 기술/경제 모두 동일 리스크 프리미엄 |
| **범위 초과** | 산출 값이 합리적 범위 초과 | 마진 50% 이상 |

### 3.2 충돌 감지 규칙

```python
CONFLICT_RULES = {
    "duration_cost_mismatch": {
        "condition": lambda data: (
            abs(calculate_implied_duration(data['economic_analysis']) -
                data['technical_analysis']['estimated_duration']['realistic'])
            > 2  # 2개월 이상 차이
        ),
        "severity": "HIGH",
        "resolution": "duration_reconciliation"
    },

    "margin_strategy_conflict": {
        "condition": lambda data: (
            data['economic_analysis']['recommended_margin']['recommended'] > 0.25 and
            data['business_analysis']['competition_level']['level'] == "HIGH"
        ),
        "severity": "MEDIUM",
        "resolution": "margin_adjustment"
    },

    "risk_duplication": {
        "condition": lambda data: (
            set(data['technical_analysis']['technical_risks']) &
            set(data['economic_analysis']['risk_premium']['factors'])
        ),
        "severity": "LOW",
        "resolution": "risk_deduplication"
    },

    "margin_out_of_range": {
        "condition": lambda data: (
            data['economic_analysis']['recommended_margin']['recommended'] > 0.4 or
            data['economic_analysis']['recommended_margin']['recommended'] < 0.05
        ),
        "severity": "HIGH",
        "resolution": "margin_normalization"
    }
}


def detect_conflicts(synthesis_input: dict) -> list:
    """
    충돌 감지 수행
    """
    conflicts = []

    for rule_name, rule in CONFLICT_RULES.items():
        if rule['condition'](synthesis_input):
            conflicts.append({
                "conflict_type": rule_name,
                "severity": rule['severity'],
                "resolution_strategy": rule['resolution']
            })

    return conflicts
```

### 3.3 충돌 조정 전략

```python
def resolve_conflicts(
    synthesis_input: dict,
    conflicts: list
) -> dict:
    """
    감지된 충돌 조정
    """
    adjusted_input = copy.deepcopy(synthesis_input)

    for conflict in conflicts:
        strategy = conflict['resolution_strategy']

        if strategy == "duration_reconciliation":
            adjusted_input = reconcile_duration(adjusted_input)

        elif strategy == "margin_adjustment":
            adjusted_input = adjust_margin_for_competition(adjusted_input)

        elif strategy == "risk_deduplication":
            adjusted_input = deduplicate_risks(adjusted_input)

        elif strategy == "margin_normalization":
            adjusted_input = normalize_margin(adjusted_input)

    return adjusted_input


def reconcile_duration(data: dict) -> dict:
    """
    기간-비용 불일치 조정
    """
    tech_duration = data['technical_analysis']['estimated_duration']['realistic']
    econ_implied = calculate_implied_duration(data['economic_analysis'])

    # 가중 평균 사용 (기술 전문가 70%, 경제 전문가 30%)
    reconciled_duration = tech_duration * 0.7 + econ_implied * 0.3

    # 비용 재계산
    data['economic_analysis']['base_cost'] = recalculate_cost(
        data['technical_analysis']['required_roles'],
        reconciled_duration
    )

    data['adjustments'] = data.get('adjustments', [])
    data['adjustments'].append({
        "type": "duration_reconciliation",
        "original_tech": tech_duration,
        "original_econ": econ_implied,
        "reconciled": reconciled_duration
    })

    return data


def adjust_margin_for_competition(data: dict) -> dict:
    """
    경쟁 상황에 따른 마진 조정
    """
    competition = data['business_analysis']['competition_level']['level']
    original_margin = data['economic_analysis']['recommended_margin']['recommended']

    adjustment_factor = {
        "LOW": 1.0,
        "MEDIUM": 0.85,
        "HIGH": 0.7
    }

    adjusted_margin = original_margin * adjustment_factor[competition]

    # 최소 마진 보장
    adjusted_margin = max(adjusted_margin, 0.08)

    data['economic_analysis']['recommended_margin']['adjusted'] = adjusted_margin
    data['adjustments'] = data.get('adjustments', [])
    data['adjustments'].append({
        "type": "margin_competition_adjustment",
        "original": original_margin,
        "adjusted": adjusted_margin,
        "reason": f"경쟁 강도 {competition}로 인한 조정"
    })

    return data
```

---

## 4. 최종 가격 계산

### 4.1 계산 공식

```
최종 가격 = 기본 원가 × (1 + 조정 마진) × (1 + 리스크 프리미엄) × 전략 가중치
```

### 4.2 계산 엔진

```python
def calculate_final_price(adjusted_input: dict) -> dict:
    """
    최종 가격 계산
    """
    economic = adjusted_input['economic_analysis']
    business = adjusted_input['business_analysis']

    # 1. 기본 원가
    base_cost = economic['base_cost']['total']

    # 2. 조정된 마진 (충돌 조정 반영)
    margin = economic['recommended_margin'].get(
        'adjusted',
        economic['recommended_margin']['recommended']
    )

    # 3. 리스크 프리미엄
    risk_premium = economic['risk_premium']['rate']

    # 4. 전략 가중치
    strategic_weight = business['strategic_weight']['value']

    # 5. 최종 가격 계산
    price_before_strategy = base_cost * (1 + margin) * (1 + risk_premium)
    final_price = price_before_strategy * strategic_weight

    # 6. 가격 범위 산출
    discount = business['discount_range']
    price_range = {
        "minimum": final_price * (1 - discount['max_discount']),
        "recommended": final_price,
        "maximum": final_price * (1 + 0.1)  # 10% 상향 여지
    }

    return {
        "calculation": {
            "base_cost": base_cost,
            "margin_rate": margin,
            "risk_premium_rate": risk_premium,
            "strategic_weight": strategic_weight,
            "price_before_strategy": price_before_strategy,
            "final_price": final_price
        },
        "price_range": price_range,
        "currency": economic['base_cost']['currency'],
        "confidence": calculate_price_confidence(adjusted_input)
    }


def calculate_price_confidence(data: dict) -> float:
    """
    가격 산정 신뢰도 계산
    """
    factors = []

    # 기술 분석 신뢰도
    factors.append(
        data['technical_analysis']['feature_complexity_score']['confidence']
    )

    # 충돌 조정 여부 (충돌 많을수록 신뢰도 하락)
    adjustment_count = len(data.get('adjustments', []))
    adjustment_factor = max(0.5, 1 - (adjustment_count * 0.1))
    factors.append(adjustment_factor)

    # RAG 참조 품질
    rag_quality = assess_rag_quality(data.get('rag_references', {}))
    factors.append(rag_quality)

    return round(sum(factors) / len(factors), 2)
```

---

## 5. 설명 생성

### 5.1 설명 생성 프롬프트

```python
def generate_explanation(
    synthesis_input: dict,
    price_result: dict,
    conflicts: list
) -> str:
    """
    LLM 기반 가격 산정 설명 생성
    """
    prompt = f"""
당신은 프로젝트 가격 산정 결과를 설명하는 전문가입니다.

## 프로젝트 정보
- 프로젝트명: {synthesis_input['project_context']['project_name']}
- 프로젝트 유형: {synthesis_input['project_context']['project_type']}

## 기술 분석 요약
- 복잡도 점수: {synthesis_input['technical_analysis']['feature_complexity_score']['value']}/10
- 예상 기간: {synthesis_input['technical_analysis']['estimated_duration']['realistic']}개월
- 필요 인력: {sum(r['count'] for r in synthesis_input['technical_analysis']['required_roles'])}명

## 경제 분석 요약
- 기본 원가: {price_result['calculation']['base_cost']:,.0f}원
- 적용 마진: {price_result['calculation']['margin_rate'] * 100:.1f}%
- 리스크 프리미엄: {price_result['calculation']['risk_premium_rate'] * 100:.1f}%

## 사업 분석 요약
- 전략 가중치: {price_result['calculation']['strategic_weight']}
- 경쟁 강도: {synthesis_input['business_analysis']['competition_level']['level']}

## 조정 사항
{format_adjustments(synthesis_input.get('adjustments', []))}

## 최종 가격
- 권장 가격: {price_result['calculation']['final_price']:,.0f}원
- 가격 범위: {price_result['price_range']['minimum']:,.0f}원 ~ {price_result['price_range']['maximum']:,.0f}원
- 신뢰도: {price_result['confidence'] * 100:.0f}%

위 정보를 바탕으로 고객에게 전달할 가격 산정 근거 설명문을 작성해주세요.

설명문 작성 원칙:
1. 비전문가도 이해할 수 있는 용어 사용
2. 가격의 합리성을 논리적으로 설명
3. 주요 가격 구성 요소 명시
4. 불확실성/리스크 요소 투명하게 설명
5. 300-500자 분량
"""

    return llm.generate(prompt)
```

### 5.2 설명 구조

```json
{
  "explanation": {
    "summary": "한 줄 요약",
    "price_breakdown": {
      "cost_explanation": "원가 구성 설명",
      "margin_explanation": "마진 설정 이유",
      "adjustment_explanation": "조정 사항 설명"
    },
    "confidence_explanation": "신뢰도 설명",
    "recommendations": ["권장 사항"],
    "caveats": ["주의 사항"]
  }
}
```

---

## 6. 출력 스키마

### 6.1 최종 출력

```json
{
  "synthesis_result": {
    "project_id": "string",
    "timestamp": "datetime",

    "final_price": {
      "recommended": "number",
      "minimum": "number",
      "maximum": "number",
      "currency": "string"
    },

    "price_breakdown": {
      "base_cost": "number",
      "margin_amount": "number",
      "risk_premium_amount": "number",
      "strategic_adjustment": "number"
    },

    "confidence": {
      "overall": "number (0-1)",
      "factors": {
        "technical_confidence": "number",
        "data_quality": "number",
        "conflict_adjustment": "number"
      }
    },

    "conflicts_resolved": [
      {
        "type": "string",
        "original_value": "any",
        "adjusted_value": "any",
        "reason": "string"
      }
    ],

    "explanation": {
      "summary": "string",
      "detailed": "string",
      "for_customer": "string"
    },

    "expert_summaries": {
      "technical": "string",
      "economic": "string",
      "business": "string"
    },

    "recommendations": [
      {
        "category": "string",
        "recommendation": "string",
        "impact": "string"
      }
    ],

    "risks": [
      {
        "risk": "string",
        "probability": "LOW | MEDIUM | HIGH",
        "impact": "string",
        "mitigation": "string"
      }
    ]
  },

  "metadata": {
    "processing_time_ms": "number",
    "llm_calls": "number",
    "rag_retrievals": "number",
    "version": "string"
  }
}
```

---

## 7. 의사결정 트레이스

### 7.1 트레이스 구조

```python
class DecisionTrace:
    """
    의사결정 과정 추적
    """
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.steps = []

    def add_step(
        self,
        step_type: str,
        input_data: dict,
        output_data: dict,
        reasoning: str
    ):
        self.steps.append({
            "timestamp": datetime.now().isoformat(),
            "step_type": step_type,
            "input_summary": summarize_data(input_data),
            "output_summary": summarize_data(output_data),
            "reasoning": reasoning
        })

    def export(self) -> dict:
        return {
            "project_id": self.project_id,
            "total_steps": len(self.steps),
            "steps": self.steps,
            "decision_path": self.get_decision_path()
        }

    def get_decision_path(self) -> str:
        return " → ".join([s['step_type'] for s in self.steps])
```

### 7.2 추적 포인트

| 단계 | 추적 내용 |
|------|----------|
| **전문가 분석** | 각 전문가 입력/출력/추론 |
| **RAG 검색** | 검색 쿼리, 결과, 선택 근거 |
| **충돌 감지** | 감지된 충돌, 심각도 |
| **충돌 조정** | 조정 전/후 값, 조정 이유 |
| **가격 계산** | 계산 단계별 중간값 |
| **설명 생성** | 생성된 설명, 프롬프트 |

---

## 8. 에러 처리

### 8.1 에러 유형

| 에러 | 설명 | 처리 |
|------|------|------|
| **전문가 출력 누락** | 일부 전문가 결과 없음 | 기본값 사용 + 경고 |
| **계산 범위 초과** | 비정상적 계산 결과 | 범위 클램핑 + 경고 |
| **충돌 조정 실패** | 조정 불가능한 충돌 | 수동 검토 요청 |
| **신뢰도 미달** | 신뢰도 < 0.5 | 추가 검토 권고 |

### 8.2 폴백 전략

```python
def synthesis_with_fallback(synthesis_input: dict) -> dict:
    """
    폴백 전략이 포함된 통합 처리
    """
    try:
        # 정상 처리
        conflicts = detect_conflicts(synthesis_input)
        adjusted = resolve_conflicts(synthesis_input, conflicts)
        price_result = calculate_final_price(adjusted)
        explanation = generate_explanation(adjusted, price_result, conflicts)

        return {
            "status": "SUCCESS",
            "result": {
                "price": price_result,
                "explanation": explanation,
                "conflicts": conflicts
            }
        }

    except ExpertOutputMissing as e:
        # 기본값으로 대체
        synthesis_input = fill_missing_expert_output(synthesis_input, e.missing)
        return synthesis_with_fallback(synthesis_input)

    except CalculationOutOfRange as e:
        # 범위 클램핑
        return {
            "status": "WARNING",
            "result": clamp_calculation(e.result),
            "warnings": [f"계산 결과가 범위를 벗어남: {e.field}"]
        }

    except ConflictUnresolvable as e:
        # 수동 검토 요청
        return {
            "status": "MANUAL_REVIEW_REQUIRED",
            "partial_result": e.partial_result,
            "unresolved_conflicts": e.conflicts,
            "message": "자동 조정이 불가능한 충돌이 감지되었습니다."
        }
```

---

## 9. 성능 최적화

### 9.1 병렬 처리

```python
async def parallel_synthesis(synthesis_input: dict) -> dict:
    """
    병렬 처리로 성능 최적화
    """
    # 병렬 실행 가능한 작업
    tasks = [
        detect_conflicts_async(synthesis_input),
        prepare_explanation_context_async(synthesis_input),
        validate_input_async(synthesis_input)
    ]

    results = await asyncio.gather(*tasks)

    conflicts, explanation_ctx, validation = results

    # 순차 실행 필요한 작업
    adjusted = resolve_conflicts(synthesis_input, conflicts)
    price_result = calculate_final_price(adjusted)
    explanation = generate_explanation(adjusted, price_result, conflicts)

    return compile_result(price_result, explanation, conflicts)
```

### 9.2 캐싱 전략

```python
CACHE_CONFIG = {
    "conflict_rules": {
        "ttl": 3600,  # 1시간
        "key_pattern": "conflict_rules_v{version}"
    },
    "calculation_templates": {
        "ttl": 86400,  # 24시간
        "key_pattern": "calc_template_{project_type}"
    },
    "explanation_templates": {
        "ttl": 3600,
        "key_pattern": "explanation_{template_type}"
    }
}
```

---

## 문서 정보

- **작성일**: 2026-02-26
- **상태**: Phase 9 완료
- **다음 단계**: Phase 10 - 검증 체계
