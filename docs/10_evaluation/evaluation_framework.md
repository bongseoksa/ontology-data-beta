# Phase 10: 검증 체계 설계

---

## 1. 검증 체계 개요

### 1.1 목적
시스템이 산출한 가격의 **정확성**, **신뢰성**, **일관성**을 검증하고,
지속적인 **개선 사이클**을 통해 시스템 품질을 향상

### 1.2 검증 범위

| 검증 영역 | 대상 | 방법 |
|----------|------|------|
| **정확성** | 산출 가격 vs 실제 계약 가격 | 오차율 분석 |
| **일관성** | 동일 입력에 대한 출력 변동 | 변동 계수 분석 |
| **완전성** | 필수 출력 항목 충족 | 체크리스트 검증 |
| **합리성** | 가격 범위의 적절성 | 벤치마크 비교 |

### 1.3 검증 흐름

```
┌─────────────────────────────────────────────────────────────────┐
│                      가격 산정 완료                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      자동 검증 (Real-time)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ 범위검증  │  │ 일관성   │  │ 완전성   │  │ 로직검증  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      결과 피드백 수집                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │ 계약체결  │  │ 사용자   │  │ 전문가   │                      │
│  │ 결과     │  │ 피드백   │  │ 리뷰     │                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      정확성 평가 (Batch)                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │ 오차분석  │  │ 트렌드   │  │ 편향분석  │                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      모델/규칙 개선                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 실시간 검증

### 2.1 범위 검증

```python
RANGE_VALIDATION_RULES = {
    "final_price": {
        "min": 1000000,      # 최소 100만원
        "max": 100000000000, # 최대 1000억원
        "relative_to_cost": {
            "min_ratio": 1.05,   # 원가 대비 최소 5% 이상
            "max_ratio": 5.0     # 원가 대비 최대 5배
        }
    },

    "margin_rate": {
        "min": 0.03,  # 최소 3%
        "max": 0.50,  # 최대 50%
        "warning_threshold": 0.35
    },

    "duration_months": {
        "min": 1,
        "max": 48,
        "warning_threshold": 24
    },

    "team_size": {
        "min": 1,
        "max": 100,
        "relative_to_duration": {
            "max_mm_ratio": 50  # 월당 최대 50MM
        }
    }
}


def validate_ranges(synthesis_result: dict) -> ValidationResult:
    """
    범위 검증 수행
    """
    errors = []
    warnings = []

    # 최종 가격 검증
    price = synthesis_result['final_price']['recommended']
    base_cost = synthesis_result['price_breakdown']['base_cost']

    if price < RANGE_VALIDATION_RULES['final_price']['min']:
        errors.append(ValidationError(
            field='final_price',
            message=f'최종 가격이 최소 기준 미달: {price:,}원',
            severity='ERROR'
        ))

    ratio = price / base_cost
    if ratio < RANGE_VALIDATION_RULES['final_price']['relative_to_cost']['min_ratio']:
        errors.append(ValidationError(
            field='final_price',
            message=f'가격이 원가보다 낮음 (비율: {ratio:.2f})',
            severity='ERROR'
        ))

    # 마진율 검증
    margin = synthesis_result['price_breakdown']['margin_amount'] / base_cost
    if margin > RANGE_VALIDATION_RULES['margin_rate']['warning_threshold']:
        warnings.append(ValidationWarning(
            field='margin_rate',
            message=f'마진율이 높음: {margin*100:.1f}%',
            suggestion='시장 경쟁력 검토 권장'
        ))

    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )
```

### 2.2 일관성 검증

```python
def validate_consistency(
    synthesis_result: dict,
    historical_cache: dict
) -> ValidationResult:
    """
    동일 조건에서의 일관성 검증
    """
    project_signature = create_project_signature(synthesis_result)

    if project_signature in historical_cache:
        historical = historical_cache[project_signature]

        # 가격 변동 계수 확인
        prices = historical['prices'] + [synthesis_result['final_price']['recommended']]
        cv = np.std(prices) / np.mean(prices)

        if cv > 0.15:  # 변동 계수 15% 초과
            return ValidationResult(
                is_valid=True,
                warnings=[ValidationWarning(
                    field='consistency',
                    message=f'유사 프로젝트 대비 가격 변동 큼 (CV: {cv:.2%})',
                    historical_range={
                        'min': min(historical['prices']),
                        'max': max(historical['prices']),
                        'mean': np.mean(historical['prices'])
                    }
                )]
            )

    return ValidationResult(is_valid=True)


def create_project_signature(result: dict) -> str:
    """
    프로젝트 특성 기반 시그니처 생성
    """
    components = [
        result['project_context']['project_type'],
        str(round(result['technical_analysis']['feature_complexity_score']['value'])),
        str(round(result['technical_analysis']['estimated_duration']['realistic'])),
        str(sum(r['count'] for r in result['technical_analysis']['required_roles']))
    ]
    return hashlib.md5('_'.join(components).encode()).hexdigest()[:16]
```

### 2.3 완전성 검증

```yaml
CompletenessChecklist:
  Required:
    - final_price.recommended
    - final_price.minimum
    - final_price.maximum
    - price_breakdown.base_cost
    - price_breakdown.margin_amount
    - confidence.overall
    - explanation.summary

  Recommended:
    - expert_summaries.technical
    - expert_summaries.economic
    - expert_summaries.business
    - risks[].risk
    - recommendations[]

  Optional:
    - conflicts_resolved[]
    - rag_references[]
```

```python
def validate_completeness(synthesis_result: dict) -> ValidationResult:
    """
    출력 완전성 검증
    """
    missing_required = []
    missing_recommended = []

    # 필수 항목 검증
    for field in COMPLETENESS_REQUIRED:
        if not get_nested_value(synthesis_result, field):
            missing_required.append(field)

    # 권장 항목 검증
    for field in COMPLETENESS_RECOMMENDED:
        if not get_nested_value(synthesis_result, field):
            missing_recommended.append(field)

    errors = [
        ValidationError(field=f, message=f'필수 항목 누락: {f}', severity='ERROR')
        for f in missing_required
    ]

    warnings = [
        ValidationWarning(field=f, message=f'권장 항목 누락: {f}')
        for f in missing_recommended
    ]

    return ValidationResult(
        is_valid=len(missing_required) == 0,
        errors=errors,
        warnings=warnings,
        completeness_score=calculate_completeness_score(
            len(missing_required),
            len(missing_recommended)
        )
    )
```

### 2.4 로직 검증

```python
LOGIC_VALIDATION_RULES = [
    {
        "name": "price_cost_relationship",
        "condition": lambda r: r['final_price']['recommended'] >= r['price_breakdown']['base_cost'],
        "error_message": "최종 가격이 원가보다 낮습니다"
    },
    {
        "name": "price_range_order",
        "condition": lambda r: (
            r['final_price']['minimum'] <=
            r['final_price']['recommended'] <=
            r['final_price']['maximum']
        ),
        "error_message": "가격 범위 순서가 잘못되었습니다"
    },
    {
        "name": "margin_calculation",
        "condition": lambda r: abs(
            r['price_breakdown']['margin_amount'] -
            (r['final_price']['recommended'] - r['price_breakdown']['base_cost'] -
             r['price_breakdown']['risk_premium_amount'])
        ) < r['final_price']['recommended'] * 0.01,  # 1% 허용 오차
        "error_message": "마진 계산이 일치하지 않습니다"
    },
    {
        "name": "confidence_range",
        "condition": lambda r: 0 <= r['confidence']['overall'] <= 1,
        "error_message": "신뢰도가 유효 범위를 벗어났습니다"
    }
]


def validate_logic(synthesis_result: dict) -> ValidationResult:
    """
    계산 로직 검증
    """
    errors = []

    for rule in LOGIC_VALIDATION_RULES:
        try:
            if not rule['condition'](synthesis_result):
                errors.append(ValidationError(
                    field=rule['name'],
                    message=rule['error_message'],
                    severity='ERROR'
                ))
        except (KeyError, TypeError) as e:
            errors.append(ValidationError(
                field=rule['name'],
                message=f'검증 실패: {str(e)}',
                severity='ERROR'
            ))

    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors
    )
```

---

## 3. 피드백 수집

### 3.1 계약 결과 피드백

```python
@dataclass
class ContractFeedback:
    """계약 체결 결과 피드백"""
    project_id: str
    estimated_price: float
    contract_result: str  # WON | LOST | NEGOTIATED
    final_contract_price: Optional[float]
    negotiation_details: Optional[str]
    competitor_info: Optional[dict]
    feedback_date: datetime


def collect_contract_feedback(feedback: ContractFeedback) -> None:
    """
    계약 결과 피드백 수집 및 저장
    """
    feedback_record = {
        "project_id": feedback.project_id,
        "estimated_price": feedback.estimated_price,
        "contract_result": feedback.contract_result,
        "final_contract_price": feedback.final_contract_price,
        "price_difference": (
            feedback.final_contract_price - feedback.estimated_price
            if feedback.final_contract_price else None
        ),
        "error_rate": (
            (feedback.final_contract_price - feedback.estimated_price) / feedback.estimated_price
            if feedback.final_contract_price else None
        ),
        "feedback_date": feedback.feedback_date
    }

    store_feedback(feedback_record)
    update_accuracy_metrics(feedback_record)
```

### 3.2 사용자 피드백

```yaml
UserFeedbackSchema:
  fields:
    - name: overall_satisfaction
      type: rating
      range: [1, 5]
      required: true

    - name: price_reasonability
      type: rating
      range: [1, 5]
      required: true

    - name: explanation_clarity
      type: rating
      range: [1, 5]
      required: true

    - name: would_use_again
      type: boolean
      required: true

    - name: specific_feedback
      type: text
      required: false

    - name: improvement_suggestions
      type: text
      required: false
```

### 3.3 전문가 리뷰

```python
@dataclass
class ExpertReview:
    """내부 전문가 리뷰"""
    project_id: str
    reviewer_id: str
    reviewer_role: str  # TECHNICAL | ECONOMIC | BUSINESS

    # 평가 항목
    methodology_score: int  # 1-5
    accuracy_assessment: str  # ACCURATE | SLIGHTLY_OFF | SIGNIFICANTLY_OFF
    identified_issues: List[str]
    recommended_adjustments: List[dict]

    # 세부 평가
    technical_assessment: Optional[dict]
    economic_assessment: Optional[dict]
    business_assessment: Optional[dict]

    review_notes: str
    review_date: datetime
```

---

## 4. 정확성 평가

### 4.1 오차 메트릭

```python
class AccuracyMetrics:
    """정확성 평가 메트릭"""

    @staticmethod
    def mean_absolute_error(estimated: list, actual: list) -> float:
        """평균 절대 오차"""
        return np.mean(np.abs(np.array(estimated) - np.array(actual)))

    @staticmethod
    def mean_absolute_percentage_error(estimated: list, actual: list) -> float:
        """평균 절대 백분율 오차 (MAPE)"""
        return np.mean(
            np.abs((np.array(actual) - np.array(estimated)) / np.array(actual))
        ) * 100

    @staticmethod
    def symmetric_mape(estimated: list, actual: list) -> float:
        """대칭 MAPE"""
        return np.mean(
            np.abs(np.array(estimated) - np.array(actual)) /
            ((np.abs(np.array(estimated)) + np.abs(np.array(actual))) / 2)
        ) * 100

    @staticmethod
    def within_tolerance(estimated: list, actual: list, tolerance: float) -> float:
        """허용 오차 내 비율"""
        errors = np.abs((np.array(estimated) - np.array(actual)) / np.array(actual))
        return np.mean(errors <= tolerance) * 100

    @staticmethod
    def directional_accuracy(estimated: list, actual: list) -> dict:
        """방향성 정확도 (과대/과소 추정 비율)"""
        diff = np.array(estimated) - np.array(actual)
        return {
            "overestimate_rate": np.mean(diff > 0) * 100,
            "underestimate_rate": np.mean(diff < 0) * 100,
            "exact_rate": np.mean(diff == 0) * 100
        }
```

### 4.2 정확성 목표

| 메트릭 | 목표 | 최소 허용 |
|--------|------|----------|
| **MAPE** | < 10% | < 20% |
| **15% 내 적중률** | > 80% | > 60% |
| **25% 내 적중률** | > 95% | > 85% |
| **방향 균형** | 50:50 ± 10% | 50:50 ± 20% |

### 4.3 세그먼트별 분석

```python
def analyze_accuracy_by_segment(feedback_data: pd.DataFrame) -> dict:
    """
    세그먼트별 정확성 분석
    """
    segments = {
        "by_project_type": feedback_data.groupby('project_type'),
        "by_project_scale": feedback_data.groupby('project_scale'),
        "by_industry": feedback_data.groupby('industry'),
        "by_price_range": feedback_data.groupby(
            pd.cut(feedback_data['estimated_price'],
                   bins=[0, 50e6, 200e6, 500e6, np.inf],
                   labels=['소형', '중형', '대형', '초대형'])
        )
    }

    results = {}

    for segment_name, grouped in segments.items():
        segment_results = {}

        for name, group in grouped:
            estimated = group['estimated_price'].tolist()
            actual = group['final_contract_price'].dropna().tolist()

            if len(actual) >= 5:  # 최소 샘플 수
                segment_results[name] = {
                    "sample_size": len(actual),
                    "mape": AccuracyMetrics.mean_absolute_percentage_error(
                        estimated[:len(actual)], actual
                    ),
                    "within_15pct": AccuracyMetrics.within_tolerance(
                        estimated[:len(actual)], actual, 0.15
                    ),
                    "directional": AccuracyMetrics.directional_accuracy(
                        estimated[:len(actual)], actual
                    )
                }

        results[segment_name] = segment_results

    return results
```

### 4.4 트렌드 분석

```python
def analyze_accuracy_trend(
    feedback_data: pd.DataFrame,
    window: str = 'M'  # Monthly
) -> dict:
    """
    시간에 따른 정확성 트렌드 분석
    """
    feedback_data['period'] = feedback_data['feedback_date'].dt.to_period(window)

    trend_data = []

    for period, group in feedback_data.groupby('period'):
        estimated = group['estimated_price'].tolist()
        actual = group['final_contract_price'].dropna().tolist()

        if len(actual) >= 3:
            trend_data.append({
                "period": str(period),
                "sample_size": len(actual),
                "mape": AccuracyMetrics.mean_absolute_percentage_error(
                    estimated[:len(actual)], actual
                ),
                "avg_error": AccuracyMetrics.mean_absolute_error(
                    estimated[:len(actual)], actual
                )
            })

    return {
        "trend_data": trend_data,
        "improving": is_trend_improving(trend_data),
        "recent_performance": trend_data[-1] if trend_data else None
    }


def is_trend_improving(trend_data: list) -> bool:
    """트렌드 개선 여부 판단"""
    if len(trend_data) < 3:
        return None

    recent_mapes = [t['mape'] for t in trend_data[-3:]]
    return recent_mapes[-1] < np.mean(recent_mapes[:-1])
```

### 4.5 편향 분석

```python
def analyze_bias(feedback_data: pd.DataFrame) -> dict:
    """
    시스템 편향 분석
    """
    diff = feedback_data['estimated_price'] - feedback_data['final_contract_price']

    return {
        "systematic_bias": {
            "mean_bias": diff.mean(),
            "bias_direction": "과대추정" if diff.mean() > 0 else "과소추정",
            "bias_magnitude": abs(diff.mean()) / feedback_data['final_contract_price'].mean()
        },

        "conditional_bias": {
            "high_complexity_bias": analyze_conditional_bias(
                feedback_data[feedback_data['complexity_score'] > 7]
            ),
            "low_complexity_bias": analyze_conditional_bias(
                feedback_data[feedback_data['complexity_score'] <= 7]
            ),
            "large_project_bias": analyze_conditional_bias(
                feedback_data[feedback_data['estimated_price'] > 200e6]
            ),
            "small_project_bias": analyze_conditional_bias(
                feedback_data[feedback_data['estimated_price'] <= 200e6]
            )
        },

        "temporal_bias": analyze_temporal_bias(feedback_data)
    }
```

---

## 5. 개선 사이클

### 5.1 개선 트리거

```python
IMPROVEMENT_TRIGGERS = {
    "accuracy_degradation": {
        "condition": lambda metrics: metrics['mape'] > 15,
        "action": "PARAMETER_TUNING",
        "priority": "HIGH"
    },

    "systematic_bias": {
        "condition": lambda metrics: abs(metrics['mean_bias']) > 0.1,
        "action": "BIAS_CORRECTION",
        "priority": "HIGH"
    },

    "segment_underperformance": {
        "condition": lambda metrics: any(
            seg['mape'] > 25 for seg in metrics['segments'].values()
        ),
        "action": "SEGMENT_SPECIFIC_TUNING",
        "priority": "MEDIUM"
    },

    "low_confidence_correlation": {
        "condition": lambda metrics: metrics['confidence_accuracy_corr'] < 0.5,
        "action": "CONFIDENCE_MODEL_UPDATE",
        "priority": "MEDIUM"
    },

    "user_satisfaction_drop": {
        "condition": lambda metrics: metrics['satisfaction'] < 3.5,
        "action": "UX_REVIEW",
        "priority": "MEDIUM"
    }
}


def check_improvement_triggers(metrics: dict) -> list:
    """
    개선 필요 여부 판단
    """
    triggered = []

    for trigger_name, trigger in IMPROVEMENT_TRIGGERS.items():
        if trigger['condition'](metrics):
            triggered.append({
                "trigger": trigger_name,
                "action": trigger['action'],
                "priority": trigger['priority']
            })

    return sorted(triggered, key=lambda x: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[x['priority']])
```

### 5.2 개선 액션

```python
IMPROVEMENT_ACTIONS = {
    "PARAMETER_TUNING": {
        "description": "계산 파라미터 조정",
        "steps": [
            "오차 패턴 분석",
            "파라미터 민감도 분석",
            "조정 범위 결정",
            "A/B 테스트 설계",
            "배포 및 모니터링"
        ],
        "automated": True
    },

    "BIAS_CORRECTION": {
        "description": "시스템 편향 보정",
        "steps": [
            "편향 원인 분석",
            "보정 계수 산출",
            "보정 로직 적용",
            "검증",
            "배포"
        ],
        "automated": True
    },

    "SEGMENT_SPECIFIC_TUNING": {
        "description": "특정 세그먼트 튜닝",
        "steps": [
            "세그먼트 특성 분석",
            "세그먼트별 파라미터 조정",
            "RAG 데이터 보강",
            "테스트",
            "배포"
        ],
        "automated": False
    },

    "CONFIDENCE_MODEL_UPDATE": {
        "description": "신뢰도 모델 업데이트",
        "steps": [
            "신뢰도-정확도 상관 분석",
            "신뢰도 계산 로직 개선",
            "검증",
            "배포"
        ],
        "automated": True
    },

    "RAG_DATA_UPDATE": {
        "description": "RAG 지식베이스 업데이트",
        "steps": [
            "피드백 데이터 분석",
            "신규 프로젝트 사례 추가",
            "단가 정보 갱신",
            "임베딩 재생성"
        ],
        "automated": True
    }
}
```

### 5.3 자동 파라미터 튜닝

```python
def auto_parameter_tuning(
    feedback_data: pd.DataFrame,
    current_params: dict
) -> dict:
    """
    피드백 기반 자동 파라미터 튜닝
    """
    # 1. 오차 분석
    errors = feedback_data['estimated_price'] - feedback_data['final_contract_price']
    error_rates = errors / feedback_data['final_contract_price']

    # 2. 세그먼트별 오차 패턴
    segment_errors = analyze_error_patterns(feedback_data, error_rates)

    # 3. 파라미터 조정 계산
    adjustments = {}

    # 마진 조정
    if segment_errors['overall']['mean_error_rate'] > 0.05:
        # 과대추정 경향 → 마진 하향
        adjustments['default_margin_multiplier'] = 0.95
    elif segment_errors['overall']['mean_error_rate'] < -0.05:
        # 과소추정 경향 → 마진 상향
        adjustments['default_margin_multiplier'] = 1.05

    # 복잡도 가중치 조정
    if segment_errors['by_complexity']['high']['mean_error_rate'] > 0.1:
        adjustments['complexity_weight_high'] = current_params['complexity_weight_high'] * 0.9

    # 4. 새 파라미터 생성
    new_params = {**current_params}
    for key, value in adjustments.items():
        if key in new_params:
            new_params[key] = new_params[key] * value
        else:
            new_params[key] = value

    return {
        "previous_params": current_params,
        "adjustments": adjustments,
        "new_params": new_params,
        "expected_improvement": estimate_improvement(adjustments)
    }
```

---

## 6. 보고서 생성

### 6.1 정기 보고서 구조

```yaml
EvaluationReport:
  metadata:
    report_period: "date_range"
    generated_at: "datetime"
    total_evaluations: "number"

  accuracy_summary:
    overall_mape: "percentage"
    within_15pct_rate: "percentage"
    within_25pct_rate: "percentage"
    trend: "IMPROVING | STABLE | DECLINING"

  segment_performance:
    by_project_type: [...]
    by_scale: [...]
    by_industry: [...]

  bias_analysis:
    systematic_bias: {...}
    segment_specific_bias: {...}

  user_feedback:
    satisfaction_score: "number"
    top_issues: [...]
    improvement_requests: [...]

  improvements_made:
    - action: "string"
      impact: "string"
      date: "date"

  recommendations:
    - priority: "HIGH | MEDIUM | LOW"
      recommendation: "string"
      expected_impact: "string"
```

### 6.2 대시보드 메트릭

```python
DASHBOARD_METRICS = {
    "real_time": {
        "today_evaluations": {"type": "counter"},
        "avg_confidence": {"type": "gauge"},
        "validation_pass_rate": {"type": "gauge"}
    },

    "daily": {
        "mape": {"type": "time_series"},
        "within_tolerance_rate": {"type": "time_series"},
        "user_satisfaction": {"type": "time_series"}
    },

    "weekly": {
        "accuracy_by_segment": {"type": "heatmap"},
        "bias_trend": {"type": "line_chart"},
        "improvement_impact": {"type": "bar_chart"}
    },

    "monthly": {
        "comprehensive_accuracy": {"type": "report"},
        "segment_deep_dive": {"type": "report"},
        "improvement_roadmap": {"type": "report"}
    }
}
```

---

## 7. 품질 게이트

### 7.1 배포 전 검증

```python
QUALITY_GATES = {
    "pre_deployment": {
        "minimum_test_coverage": 0.8,
        "validation_pass_rate": 0.95,
        "regression_test_pass": True,
        "performance_degradation_max": 0.1
    },

    "post_deployment": {
        "monitoring_period_hours": 24,
        "error_rate_threshold": 0.01,
        "accuracy_degradation_threshold": 0.05,
        "rollback_trigger": {
            "error_rate": 0.05,
            "accuracy_drop": 0.1
        }
    }
}


def check_quality_gates(
    gate_type: str,
    metrics: dict
) -> QualityGateResult:
    """
    품질 게이트 통과 여부 확인
    """
    gate = QUALITY_GATES[gate_type]
    passed = True
    failures = []

    for criterion, threshold in gate.items():
        if isinstance(threshold, dict):
            continue

        actual_value = metrics.get(criterion)
        if actual_value is None:
            failures.append(f"{criterion}: 값 없음")
            passed = False
        elif isinstance(threshold, bool):
            if actual_value != threshold:
                failures.append(f"{criterion}: 기대값 {threshold}, 실제값 {actual_value}")
                passed = False
        else:
            if actual_value < threshold:
                failures.append(f"{criterion}: 기준 {threshold}, 실제값 {actual_value}")
                passed = False

    return QualityGateResult(
        passed=passed,
        gate_type=gate_type,
        failures=failures
    )
```

---

## 문서 정보

- **작성일**: 2026-02-26
- **상태**: Phase 10 완료
- **다음 단계**: Phase 11 - 최종 프로젝트 아키텍처
