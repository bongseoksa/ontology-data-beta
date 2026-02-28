# Phase 6-2: 가격 산정 엔진 설계

---

## 1. 가격 산정 엔진 개요

### 1.1 목적
원가(Base Cost)에 마진, 리스크, 경쟁/전략 요소를 반영하여 **최종 가격(Final Price)**을 산정

### 1.2 가격 산정 흐름

```
원가 (Base Cost)
    │
    ├── × (1 + 마진율)
    │       ↓
    │   마진 적용 가격 (Margined Price)
    │
    ├── × (1 + 리스크 프리미엄율)
    │       ↓
    │   리스크 조정 가격 (Risk-Adjusted Price)
    │
    ├── × 경쟁 조정 계수
    │       ↓
    │   경쟁 조정 가격 (Competitive Price)
    │
    └── × 전략 가중치
            ↓
        최종 가격 (Final Price)
```

---

## 2. 마진 적용 (Margin Application)

### 2.1 기본 공식

```
마진 적용 가격 = 원가 × (1 + 마진율)
```

### 2.2 마진율 결정 로직

```python
def determine_margin_rate(
    project_type,
    client_type,
    contract_type,
    project_size,
    custom_margin=None
):
    """
    마진율 결정 함수

    기본 마진율을 프로젝트/고객/계약 유형에 따라 조정
    """
    # 기본 마진율 (프로젝트 유형별)
    base_margin = {
        'SI_PROJECT': 0.12,         # 12%
        'CUSTOM_DEVELOPMENT': 0.18,  # 18%
        'SOLUTION_CUSTOMIZATION': 0.22,  # 22%
        'CONSULTING': 0.30          # 30%
    }

    # 고객 유형별 조정
    client_adjustment = {
        'PUBLIC': -0.03,            # 공공: -3%
        'ENTERPRISE': 0.00,         # 대기업: 0%
        'SMB': 0.03,               # 중소기업: +3%
        'STARTUP': 0.05            # 스타트업: +5%
    }

    # 계약 유형별 조정
    contract_adjustment = {
        'BID_BASED': -0.02,        # 입찰: -2%
        'PROJECT_BASED': 0.00,     # 프로젝트: 0%
        'TIME_MATERIAL': 0.02,     # T&M: +2%
        'DIRECT': 0.03             # 수의계약: +3%
    }

    # 규모별 조정 (대규모일수록 마진율 감소)
    size_adjustment = {
        'SMALL': 0.03,             # 소형: +3%
        'MEDIUM': 0.00,            # 중형: 0%
        'LARGE': -0.02,            # 대형: -2%
        'ENTERPRISE': -0.05        # 초대형: -5%
    }

    if custom_margin is not None:
        return custom_margin

    base = base_margin.get(project_type, 0.15)
    adjustment = (
        client_adjustment.get(client_type, 0) +
        contract_adjustment.get(contract_type, 0) +
        size_adjustment.get(project_size, 0)
    )

    # 최종 마진율 (최소 5%, 최대 40%)
    final_margin = max(0.05, min(0.40, base + adjustment))

    return final_margin
```

### 2.3 마진 계산 함수

```python
def apply_margin(base_cost, margin_rate):
    """
    마진 적용 함수
    """
    margin_amount = base_cost * margin_rate
    margined_price = base_cost + margin_amount

    return {
        'base_cost': base_cost,
        'margin_rate': margin_rate * 100,
        'margin_amount': margin_amount,
        'margined_price': margined_price
    }
```

### 2.4 마진율 가이드라인

| 프로젝트 유형 | 기본 마진 | 범위 |
|-------------|:--------:|:----:|
| SI 프로젝트 | 12% | 8-18% |
| 커스텀 개발 | 18% | 12-25% |
| 솔루션 커스터마이징 | 22% | 15-30% |
| 컨설팅 | 30% | 20-40% |

---

## 3. 리스크 프리미엄 적용 (Risk Premium)

### 3.1 기본 공식

```
리스크 조정 가격 = 마진 적용 가격 × (1 + 리스크 프리미엄율)
```

### 3.2 리스크 프리미엄 계산 로직

```python
def calculate_risk_premium(risk_factors, base_price):
    """
    리스크 프리미엄 계산 함수

    Parameters:
    - risk_factors: 리스크 요소별 점수 (1-5)
    - base_price: 마진 적용 후 가격

    Returns:
    - risk_premium_result: 리스크 프리미엄 상세
    """
    # 리스크 요소별 가중치
    factor_weights = {
        # 기술 리스크 (40%)
        'NEW_TECHNOLOGY': 0.15,
        'INTEGRATION_COMPLEXITY': 0.15,
        'PERFORMANCE_REQUIREMENT': 0.10,

        # 비즈니스 리스크 (40%)
        'REQUIREMENT_CLARITY': 0.20,
        'SCOPE_CHANGE_LIKELIHOOD': 0.15,
        'CLIENT_EXPERIENCE': 0.05,

        # 자원 리스크 (20%)
        'TEAM_AVAILABILITY': 0.12,
        'SKILL_GAP': 0.08
    }

    # 가중 평균 리스크 점수 계산
    weighted_sum = 0
    total_weight = 0

    factor_details = []
    for factor, weight in factor_weights.items():
        score = risk_factors.get(factor, 2.5)  # 기본값: 중간
        weighted_sum += score * weight
        total_weight += weight

        factor_details.append({
            'factor': factor,
            'score': score,
            'weight': weight * 100,
            'contribution': score * weight
        })

    risk_score = weighted_sum / total_weight if total_weight > 0 else 2.5

    # 리스크 점수 → 프리미엄율 매핑
    if risk_score <= 1.5:
        premium_rate = 0.02  # 2%
        risk_level = 'LOW'
    elif risk_score <= 2.5:
        premium_rate = 0.05  # 5%
        risk_level = 'MEDIUM'
    elif risk_score <= 3.5:
        premium_rate = 0.10  # 10%
        risk_level = 'HIGH'
    else:
        premium_rate = 0.20  # 20%
        risk_level = 'CRITICAL'

    premium_amount = base_price * premium_rate
    adjusted_price = base_price + premium_amount

    return {
        'risk_factors': factor_details,
        'risk_score': round(risk_score, 2),
        'risk_level': risk_level,
        'premium_rate': premium_rate * 100,
        'premium_amount': premium_amount,
        'risk_adjusted_price': adjusted_price
    }
```

### 3.3 리스크 수준별 프리미엄율

| 리스크 수준 | 점수 범위 | 프리미엄율 |
|:----------:|:--------:|:---------:|
| LOW | 1.0 - 1.5 | 0 - 3% |
| MEDIUM | 1.5 - 2.5 | 3 - 8% |
| HIGH | 2.5 - 3.5 | 8 - 15% |
| CRITICAL | 3.5 - 5.0 | 15 - 30% |

---

## 4. 경쟁 조정 적용 (Competitive Adjustment)

### 4.1 기본 공식

```
경쟁 조정 가격 = 리스크 조정 가격 × 경쟁 조정 계수
```

### 4.2 경쟁 조정 계수 결정 로직

```python
def determine_competitive_adjustment(
    competition_level,
    bid_type,
    market_position,
    incumbent_advantage
):
    """
    경쟁 조정 계수 결정 함수

    Returns:
    - adjustment_factor: 경쟁 조정 계수 (0.7 ~ 1.2)
    """
    # 경쟁 강도별 기본 계수
    competition_base = {
        'MONOPOLY': 1.10,      # 독점
        'LOW': 1.03,           # 낮은 경쟁
        'MEDIUM': 0.98,        # 보통 경쟁
        'HIGH': 0.92,          # 높은 경쟁
        'INTENSE': 0.85        # 치열한 경쟁
    }

    # 입찰 유형별 조정
    bid_adjustment = {
        'PUBLIC_LOWEST': -0.05,    # 최저가 낙찰
        'PUBLIC_NEGOTIATION': 0.00, # 협상 계약
        'PRIVATE_RFP': 0.02,       # 민간 RFP
        'DIRECT': 0.05            # 수의계약
    }

    # 시장 지위별 조정
    position_adjustment = {
        'LEADER': 0.03,           # 시장 선도자
        'CHALLENGER': 0.00,       # 도전자
        'FOLLOWER': -0.02,        # 추종자
        'NICHE': 0.02             # 틈새
    }

    # 기존 관계 이점
    incumbent_adjustment = 0.03 if incumbent_advantage else 0.00

    base = competition_base.get(competition_level, 0.95)
    total_adjustment = (
        bid_adjustment.get(bid_type, 0) +
        position_adjustment.get(market_position, 0) +
        incumbent_adjustment
    )

    # 최종 계수 (0.75 ~ 1.20 범위)
    final_factor = max(0.75, min(1.20, base + total_adjustment))

    return final_factor
```

### 4.3 경쟁 조정 적용 함수

```python
def apply_competitive_adjustment(
    risk_adjusted_price,
    competitive_factor
):
    """
    경쟁 조정 적용 함수
    """
    adjustment_amount = risk_adjusted_price * (competitive_factor - 1)
    competitive_price = risk_adjusted_price * competitive_factor

    return {
        'risk_adjusted_price': risk_adjusted_price,
        'competitive_factor': competitive_factor,
        'adjustment_amount': adjustment_amount,
        'competitive_price': competitive_price
    }
```

---

## 5. 전략 가중치 적용 (Strategic Weight)

### 5.1 기본 공식

```
최종 가격 = 경쟁 조정 가격 × 전략 가중치
```

### 5.2 전략 가중치 계산 로직

```python
def calculate_strategic_weight(strategic_factors):
    """
    전략 가중치 계산 함수

    Parameters:
    - strategic_factors: 전략적 요소 딕셔너리

    Returns:
    - strategic_weight: 전략 가중치 (0.75 ~ 1.10)
    """
    # 관계 요소
    relationship_weights = {
        'NEW': 1.00,
        'EXISTING': 0.97,
        'STRATEGIC_PARTNER': 0.93
    }

    # 후속 사업 기회
    follow_on_weights = {
        'UNLIKELY': 1.00,
        'POSSIBLE': 0.97,
        'LIKELY': 0.92
    }

    # 레퍼런스 가치
    reference_weights = {
        'LOW': 1.00,
        'MEDIUM': 0.97,
        'HIGH': 0.93
    }

    # 시장 진입
    market_entry_weights = {
        'EXISTING_MARKET': 1.00,
        'NEW_SEGMENT': 0.96,
        'NEW_MARKET': 0.90
    }

    # 가중 평균 계산
    relationship = relationship_weights.get(
        strategic_factors.get('relationship', 'NEW'), 1.00
    )
    follow_on = follow_on_weights.get(
        strategic_factors.get('follow_on', 'UNLIKELY'), 1.00
    )
    reference = reference_weights.get(
        strategic_factors.get('reference_value', 'LOW'), 1.00
    )
    market = market_entry_weights.get(
        strategic_factors.get('market_entry', 'EXISTING_MARKET'), 1.00
    )

    # 가중 평균 (동일 가중치)
    raw_weight = (relationship + follow_on + reference + market) / 4

    # 최종 가중치 (0.80 ~ 1.05 범위로 조정)
    final_weight = max(0.80, min(1.05, raw_weight))

    return {
        'factors': {
            'relationship': relationship,
            'follow_on': follow_on,
            'reference': reference,
            'market_entry': market
        },
        'raw_weight': raw_weight,
        'final_weight': final_weight
    }
```

### 5.3 전략 가중치 적용 함수

```python
def apply_strategic_weight(
    competitive_price,
    strategic_weight
):
    """
    전략 가중치 적용 함수
    """
    adjustment_amount = competitive_price * (strategic_weight - 1)
    final_price = competitive_price * strategic_weight

    return {
        'competitive_price': competitive_price,
        'strategic_weight': strategic_weight,
        'adjustment_amount': adjustment_amount,
        'final_price': final_price
    }
```

---

## 6. 최종 가격 산정 (Final Pricing)

### 6.1 통합 계산 함수

```python
def calculate_final_price(
    base_cost,
    margin_params,
    risk_factors,
    competitive_params,
    strategic_factors
):
    """
    최종 가격 산정 통합 함수

    Returns:
    - pricing_result: 전체 가격 산정 결과
    """
    # Step 1: 마진 적용
    margin_rate = determine_margin_rate(**margin_params)
    margin_result = apply_margin(base_cost, margin_rate)

    # Step 2: 리스크 프리미엄 적용
    risk_result = calculate_risk_premium(
        risk_factors,
        margin_result['margined_price']
    )

    # Step 3: 경쟁 조정 적용
    competitive_factor = determine_competitive_adjustment(**competitive_params)
    competitive_result = apply_competitive_adjustment(
        risk_result['risk_adjusted_price'],
        competitive_factor
    )

    # Step 4: 전략 가중치 적용
    strategic_result = calculate_strategic_weight(strategic_factors)
    final_result = apply_strategic_weight(
        competitive_result['competitive_price'],
        strategic_result['final_weight']
    )

    # 유효 마진율 계산
    effective_margin = (final_result['final_price'] - base_cost) / base_cost

    return {
        'base_cost': base_cost,
        'margin': margin_result,
        'risk_premium': risk_result,
        'competitive_adjustment': competitive_result,
        'strategic_weight': {
            **strategic_result,
            'final_price': final_result['final_price']
        },
        'final_price': final_result['final_price'],
        'effective_margin_rate': effective_margin * 100,
        'calculation_steps': [
            {'step': 1, 'name': '원가', 'value': base_cost},
            {'step': 2, 'name': '마진 적용', 'value': margin_result['margined_price']},
            {'step': 3, 'name': '리스크 반영', 'value': risk_result['risk_adjusted_price']},
            {'step': 4, 'name': '경쟁 조정', 'value': competitive_result['competitive_price']},
            {'step': 5, 'name': '전략 가중치', 'value': final_result['final_price']}
        ]
    }
```

---

## 7. 가격 범위 산정

### 7.1 가격 범위 계산

```python
def calculate_price_range(base_cost, final_price, negotiation_params):
    """
    가격 범위 계산 함수

    Returns:
    - price_range: 최소/목표/최대 가격
    """
    # 최소 마진 보장
    minimum_margin = negotiation_params.get('minimum_margin', 0.05)
    minimum_price = base_cost * (1 + minimum_margin)

    # 목표 가격 = 계산된 최종 가격
    target_price = final_price

    # 최대 가격 (시장 수용 가능 상한)
    max_premium = negotiation_params.get('max_premium', 0.20)
    maximum_price = target_price * (1 + max_premium)

    return {
        'minimum': {
            'price': minimum_price,
            'margin_rate': minimum_margin * 100,
            'description': '손익분기 + 최소마진'
        },
        'target': {
            'price': target_price,
            'margin_rate': (target_price - base_cost) / base_cost * 100,
            'description': '권장 가격'
        },
        'maximum': {
            'price': maximum_price,
            'margin_rate': (maximum_price - base_cost) / base_cost * 100,
            'description': '시장 수용 상한'
        },
        'break_even': base_cost,
        'negotiation_room': target_price - minimum_price
    }
```

---

## 8. 재무 지표 계산

### 8.1 주요 재무 지표

```python
def calculate_financial_metrics(base_cost, final_price, payment_schedule):
    """
    재무 지표 계산 함수
    """
    # 수익 지표
    gross_profit = final_price - base_cost
    gross_margin = gross_profit / final_price * 100
    markup_rate = gross_profit / base_cost * 100

    # 손익분기점
    break_even_point = base_cost

    # 투자 수익률 (단순화)
    roi = gross_profit / base_cost * 100

    return {
        'gross_profit': gross_profit,
        'gross_margin_percentage': round(gross_margin, 2),
        'markup_rate': round(markup_rate, 2),
        'break_even_point': break_even_point,
        'return_on_investment': round(roi, 2),
        'payment_schedule': payment_schedule
    }
```

---

## 9. 검증 규칙

### 9.1 가격 검증

```yaml
PriceValidation:
  - rule: "최종 가격 >= 원가"
    description: "손실 방지"
    severity: ERROR

  - rule: "최종 가격 <= 예산 상한"
    description: "예산 범위 내"
    severity: WARNING

  - rule: "유효 마진율 >= 최소 마진"
    description: "최소 수익 보장"
    severity: ERROR

  - rule: "minimum <= target <= maximum"
    description: "가격 범위 일관성"
    severity: ERROR
```

### 9.2 합리성 검증

```yaml
ReasonabilityValidation:
  - rule: "FP당 가격이 50-120만원 범위"
    severity: WARNING

  - rule: "유효 마진율이 5-40% 범위"
    severity: WARNING

  - rule: "경쟁 조정 후 가격 변동 < 30%"
    severity: WARNING
```

---

## 10. 계산 결과 예시

```json
{
  "base_cost": 570150000,

  "margin": {
    "rate": 15,
    "amount": 85522500,
    "margined_price": 655672500
  },

  "risk_premium": {
    "risk_level": "MEDIUM",
    "rate": 6,
    "amount": 39340350,
    "risk_adjusted_price": 695012850
  },

  "competitive_adjustment": {
    "factor": 0.95,
    "competitive_price": 660262207
  },

  "strategic_weight": {
    "final_weight": 0.95,
    "final_price": 627249097
  },

  "price_range": {
    "minimum": 598657500,
    "target": 627249097,
    "maximum": 752698916
  },

  "effective_margin_rate": 10.01,

  "financial_metrics": {
    "gross_profit": 57099097,
    "gross_margin_percentage": 9.1,
    "roi": 10.01
  }
}
```

---

## 문서 정보

- **작성일**: 2026-02-25
- **상태**: Phase 6-2 완료
- **다음 단계**: Phase 7 - 문서 분석 레이어 설계
