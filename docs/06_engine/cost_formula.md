# Phase 6-1: 원가 계산 엔진 설계

---

## 1. 원가 계산 엔진 개요

### 1.1 목적
프로젝트 수행에 필요한 **모든 비용을 정확하게 계산**하여 가격 산정의 기초가 되는 원가를 도출

### 1.2 계산 범위

```
총 원가 (Total Base Cost)
├── 직접비 (Direct Cost)
│   ├── 인건비 (Labor Cost)
│   ├── 인프라비 (Infrastructure Cost)
│   ├── 도구비 (Tool Cost)
│   └── 외부비용 (External Cost)
│
├── 간접비 (Indirect Cost)
│   ├── 제경비 (Overhead)
│   ├── 기술료 (Technical Fee)
│   └── 일반관리비 (Management Fee)
│
└── 예비비 (Contingency)
```

---

## 2. 인건비 계산 (Labor Cost)

### 2.1 기본 공식

```
인건비 = Σ (투입인원 × 투입기간 × 투입률 × 월 노임단가)
       = Σ (M/M × 월 노임단가)
```

### 2.2 상세 계산 로직

```python
def calculate_labor_cost(team_composition, labor_rates):
    """
    인건비 계산 함수

    Parameters:
    - team_composition: 팀 구성 정보 리스트
    - labor_rates: 등급별 노임단가 테이블

    Returns:
    - labor_cost_details: 역할별 인건비 상세
    - total_labor_cost: 총 인건비
    """
    labor_cost_details = []
    total_labor_cost = 0

    for role in team_composition:
        # M/M 계산
        man_month = (
            role.headcount *
            role.duration_months *
            (role.allocation / 100)
        )

        # 기술자 등급 매핑
        tech_grade = map_role_to_grade(role.role_type, role.skill_level)

        # 노임단가 조회
        unit_cost = labor_rates[tech_grade].monthly_rate

        # 인건비 계산
        cost = man_month * unit_cost

        labor_cost_details.append({
            'role_type': role.role_type,
            'skill_level': role.skill_level,
            'tech_grade': tech_grade,
            'headcount': role.headcount,
            'duration': role.duration_months,
            'allocation': role.allocation,
            'man_month': man_month,
            'unit_cost': unit_cost,
            'total_cost': cost
        })

        total_labor_cost += cost

    return labor_cost_details, total_labor_cost
```

### 2.3 역할-등급 매핑 테이블

| 역할 | Skill Level | 기술자 등급 | 비고 |
|------|-------------|------------|------|
| PM | SENIOR | 고급 | |
| PM | EXPERT | 특급 | 대규모 프로젝트 |
| Tech Lead | SENIOR | 고급 | |
| Architect | EXPERT | 특급 | |
| Backend Dev | MID | 중급 | |
| Backend Dev | SENIOR | 고급 | |
| Frontend Dev | MID | 중급 | |
| Frontend Dev | SENIOR | 고급 | |
| QA Engineer | MID | 중급 | |
| DevOps | MID | 중급 | |
| DevOps | SENIOR | 고급 | |
| Junior Dev | JUNIOR | 초급 | |

### 2.4 노임단가 테이블 (2024년 기준 예시)

```yaml
LaborRates:
  # KOSA SW기술자 평균임금 기준
  특급:
    monthly: 12000000
    daily: 550000
    hourly: 69000

  고급:
    monthly: 10000000
    daily: 450000
    hourly: 56000

  중급:
    monthly: 8000000
    daily: 360000
    hourly: 45000

  초급:
    monthly: 5500000
    daily: 250000
    hourly: 31000

  # 노임단가 갱신 정보
  metadata:
    source: "KOSA"
    year: 2024
    effective_date: "2024-09-01"
```

---

## 3. 인프라비 계산 (Infrastructure Cost)

### 3.1 기본 공식

```
인프라비 = Σ (리소스 단가 × 수량 × 사용 기간)
```

### 3.2 상세 계산 로직

```python
def calculate_infrastructure_cost(infra_requirements, duration_months):
    """
    인프라 비용 계산 함수

    Parameters:
    - infra_requirements: 인프라 요구사항 리스트
    - duration_months: 프로젝트 기간 (월)

    Returns:
    - infra_cost_details: 항목별 인프라 비용
    - total_infra_cost: 총 인프라 비용
    """
    infra_cost_details = []
    total_infra_cost = 0

    for infra in infra_requirements:
        # 환경별 사용 기간 계산
        if infra.environment == 'DEVELOPMENT':
            use_duration = duration_months
        elif infra.environment == 'STAGING':
            use_duration = duration_months * 0.5  # 후반 50% 사용
        elif infra.environment == 'PRODUCTION':
            use_duration = 1  # 초기 구축 비용만 (운영 비용 제외)

        # 비용 계산
        cost = infra.unit_cost * infra.quantity * use_duration

        infra_cost_details.append({
            'component_type': infra.component_type,
            'environment': infra.environment,
            'specification': infra.specification,
            'unit_cost': infra.unit_cost,
            'quantity': infra.quantity,
            'duration': use_duration,
            'total_cost': cost
        })

        total_infra_cost += cost

    return infra_cost_details, total_infra_cost
```

### 3.3 인프라 비용 템플릿

| 환경 | 항목 | 월 단가 (예시) | 비고 |
|------|------|---------------|------|
| 개발 | 개발 서버 (VM) | 200,000원 | t3.medium 급 |
| 개발 | 개발 DB | 150,000원 | RDS 소형 |
| 개발 | 스토리지 | 50,000원 | 100GB |
| 스테이징 | 스테이징 서버 | 300,000원 | t3.large 급 |
| 스테이징 | 스테이징 DB | 250,000원 | RDS 중형 |
| 공통 | CI/CD 인프라 | 100,000원 | Jenkins/GitLab |
| 공통 | 모니터링 | 50,000원 | CloudWatch 등 |

---

## 4. 도구비 계산 (Tool Cost)

### 4.1 기본 공식

```
도구비 = Σ (라이선스 단가 × 사용자 수 × 사용 기간)
       + 일회성 도구 비용
```

### 4.2 상세 계산 로직

```python
def calculate_tool_cost(tool_requirements, team_size, duration_months):
    """
    도구/라이선스 비용 계산 함수
    """
    tool_cost_details = []
    total_tool_cost = 0

    for tool in tool_requirements:
        if tool.license_type == 'SUBSCRIPTION':
            # 구독형: 사용자 × 기간
            user_count = min(tool.user_count or team_size, team_size)
            cost = tool.unit_cost * user_count * duration_months
        elif tool.license_type == 'PERPETUAL':
            # 영구 라이선스: 일회성
            cost = tool.unit_cost * (tool.quantity or 1)
        elif tool.license_type == 'OPEN_SOURCE':
            # 오픈소스: 무료
            cost = 0
        else:
            cost = tool.unit_cost * duration_months

        tool_cost_details.append({
            'tool_name': tool.tool_name,
            'license_type': tool.license_type,
            'unit_cost': tool.unit_cost,
            'user_count': user_count if tool.license_type == 'SUBSCRIPTION' else None,
            'duration': duration_months,
            'total_cost': cost
        })

        total_tool_cost += cost

    return tool_cost_details, total_tool_cost
```

### 4.3 일반 도구 비용 템플릿

| 카테고리 | 도구 | 월 단가/인 | 라이선스 유형 |
|----------|------|-----------|-------------|
| IDE | IntelliJ IDEA | 20,000원 | 구독 |
| 협업 | Jira | 10,000원 | 구독 |
| 협업 | Confluence | 7,000원 | 구독 |
| 버전관리 | GitHub Enterprise | 25,000원 | 구독 |
| CI/CD | GitLab CI | 무료/유료 | 오픈소스/구독 |
| 디자인 | Figma | 18,000원 | 구독 |
| 테스트 | Selenium | 무료 | 오픈소스 |

---

## 5. 외부비용 계산 (External Cost)

### 5.1 기본 공식

```
외부비용 = 외주비 + 컨설팅비 + 기타 외부비용
```

### 5.2 상세 계산 로직

```python
def calculate_external_cost(external_requirements):
    """
    외부 비용 계산 함수
    """
    external_cost_details = []
    total_external_cost = 0

    for item in external_requirements:
        if item.expense_type == 'OUTSOURCING':
            # 외주: M/M 기반 또는 고정가
            cost = item.man_months * item.unit_cost if item.man_months else item.fixed_cost
        elif item.expense_type == 'CONSULTING':
            # 컨설팅: 일수 또는 고정가
            cost = item.days * item.daily_rate if item.days else item.fixed_cost
        elif item.expense_type == 'DESIGN_SERVICE':
            # 디자인: 페이지/화면 단위 또는 고정가
            cost = item.screens * item.per_screen_cost if item.screens else item.fixed_cost
        else:
            cost = item.fixed_cost or 0

        external_cost_details.append({
            'expense_type': item.expense_type,
            'vendor_name': item.vendor_name,
            'description': item.description,
            'total_cost': cost
        })

        total_external_cost += cost

    return external_cost_details, total_external_cost
```

---

## 6. 간접비 계산 (Indirect Cost)

### 6.1 공공사업 기준 계산

```python
def calculate_indirect_cost_public(direct_labor_cost, direct_expense):
    """
    공공사업 기준 간접비 계산 (SW사업 대가산정 가이드)

    공식:
    SW개발비 = 직접인건비 + 제경비 + 기술료 + 직접경비

    - 제경비 = 직접인건비 × 제경비율 (110~120%)
    - 기술료 = (직접인건비 + 제경비) × 기술료율 (20~40%)
    """
    # 기본 요율 (중간값 적용)
    OVERHEAD_RATE = 1.10  # 110%
    TECH_FEE_RATE = 0.25  # 25%

    # 제경비 계산
    overhead = direct_labor_cost * OVERHEAD_RATE

    # 기술료 계산
    tech_fee = (direct_labor_cost + overhead) * TECH_FEE_RATE

    return {
        'overhead': {
            'rate': OVERHEAD_RATE * 100,
            'base': direct_labor_cost,
            'amount': overhead
        },
        'technical_fee': {
            'rate': TECH_FEE_RATE * 100,
            'base': direct_labor_cost + overhead,
            'amount': tech_fee
        },
        'total_indirect': overhead + tech_fee
    }
```

### 6.2 민간사업 기준 계산

```python
def calculate_indirect_cost_private(total_direct_cost):
    """
    민간사업 기준 간접비 계산 (간소화)

    일반적으로 직접비의 30~50%를 간접비로 적용
    """
    INDIRECT_RATE = 0.40  # 40%

    indirect_cost = total_direct_cost * INDIRECT_RATE

    return {
        'indirect': {
            'rate': INDIRECT_RATE * 100,
            'base': total_direct_cost,
            'amount': indirect_cost
        },
        'total_indirect': indirect_cost
    }
```

### 6.3 간접비율 가이드

| 구분 | 항목 | 비율 | 산정 기준 |
|------|------|:----:|----------|
| 공공 | 제경비 | 110~120% | 직접인건비 |
| 공공 | 기술료 | 20~40% | 직접인건비 + 제경비 |
| 민간 | 간접비 | 30~50% | 직접비 합계 |
| 민간 | 일반관리비 | 5~10% | 직접비 + 간접비 |

---

## 7. 예비비 계산 (Contingency)

### 7.1 기본 공식

```
예비비 = (직접비 + 간접비) × 예비비율
```

### 7.2 예비비율 결정 로직

```python
def calculate_contingency(base_cost, risk_level, project_type):
    """
    예비비 계산 함수

    예비비율은 리스크 수준과 프로젝트 유형에 따라 결정
    """
    # 기본 예비비율 (리스크 수준별)
    contingency_rates = {
        'LOW': 0.03,      # 3%
        'MEDIUM': 0.05,   # 5%
        'HIGH': 0.08,     # 8%
        'CRITICAL': 0.12  # 12%
    }

    # 프로젝트 유형별 가산
    type_adjustment = {
        'NEW_DEVELOPMENT': 0.02,  # 신규 개발 +2%
        'ENHANCEMENT': 0.00,      # 기능 개선 0%
        'MIGRATION': 0.03,        # 마이그레이션 +3%
        'INTEGRATION': 0.02       # 시스템 통합 +2%
    }

    base_rate = contingency_rates.get(risk_level, 0.05)
    adjustment = type_adjustment.get(project_type, 0.00)
    final_rate = min(base_rate + adjustment, 0.15)  # 최대 15%

    contingency_amount = base_cost * final_rate

    return {
        'rate': final_rate * 100,
        'base': base_cost,
        'amount': contingency_amount
    }
```

---

## 8. 총 원가 계산 (Total Base Cost)

### 8.1 통합 계산 함수

```python
def calculate_total_base_cost(
    team_composition,
    labor_rates,
    infra_requirements,
    tool_requirements,
    external_requirements,
    duration_months,
    contract_type,
    risk_level,
    project_type
):
    """
    총 원가 계산 통합 함수

    Returns:
    - cost_breakdown: 상세 비용 내역
    - total_base_cost: 총 원가
    """
    # 1. 인건비 계산
    labor_details, total_labor = calculate_labor_cost(
        team_composition, labor_rates
    )

    # 2. 인프라비 계산
    infra_details, total_infra = calculate_infrastructure_cost(
        infra_requirements, duration_months
    )

    # 3. 도구비 계산
    team_size = sum(r.headcount for r in team_composition)
    tool_details, total_tool = calculate_tool_cost(
        tool_requirements, team_size, duration_months
    )

    # 4. 외부비용 계산
    external_details, total_external = calculate_external_cost(
        external_requirements
    )

    # 5. 직접비 합계
    total_direct = total_labor + total_infra + total_tool + total_external
    direct_expense = total_infra + total_tool + total_external

    # 6. 간접비 계산
    if contract_type == 'PUBLIC':
        indirect_result = calculate_indirect_cost_public(
            total_labor, direct_expense
        )
    else:
        indirect_result = calculate_indirect_cost_private(total_direct)

    # 7. 예비비 계산
    base_for_contingency = total_direct + indirect_result['total_indirect']
    contingency_result = calculate_contingency(
        base_for_contingency, risk_level, project_type
    )

    # 8. 총 원가
    total_base_cost = (
        total_direct +
        indirect_result['total_indirect'] +
        contingency_result['amount']
    )

    return {
        'direct_cost': {
            'labor': {'details': labor_details, 'total': total_labor},
            'infrastructure': {'details': infra_details, 'total': total_infra},
            'tool': {'details': tool_details, 'total': total_tool},
            'external': {'details': external_details, 'total': total_external},
            'total': total_direct
        },
        'indirect_cost': indirect_result,
        'contingency': contingency_result,
        'total_base_cost': total_base_cost
    }
```

### 8.2 계산 결과 예시

```json
{
  "direct_cost": {
    "labor": {"total": 200000000},
    "infrastructure": {"total": 5000000},
    "tool": {"total": 3000000},
    "external": {"total": 10000000},
    "total": 218000000
  },
  "indirect_cost": {
    "overhead": {"rate": 110, "amount": 220000000},
    "technical_fee": {"rate": 25, "amount": 105000000},
    "total_indirect": 325000000
  },
  "contingency": {
    "rate": 5,
    "amount": 27150000
  },
  "total_base_cost": 570150000
}
```

---

## 9. 검증 규칙

### 9.1 계산 검증

```yaml
ValidationRules:
  LaborCost:
    - "모든 역할의 M/M 합계 = Technical Expert의 totalManMonth"
    - "개별 인건비 = M/M × 월단가 (허용 오차 1원)"

  DirectCost:
    - "직접비 합계 = 인건비 + 인프라비 + 도구비 + 외부비용"

  IndirectCost:
    - "제경비 = 직접인건비 × 제경비율"
    - "기술료 = (직접인건비 + 제경비) × 기술료율"

  TotalCost:
    - "총원가 = 직접비 + 간접비 + 예비비"
    - "총원가 > 0"
```

### 9.2 합리성 검증

```yaml
ReasonabilityChecks:
  - check: "인건비 비율"
    rule: "인건비 / 총원가 >= 60%"
    warning: "인건비 비율이 너무 낮음"

  - check: "간접비 비율"
    rule: "간접비 / 직접비 <= 1.5"
    warning: "간접비 비율이 너무 높음"

  - check: "FP당 원가"
    rule: "총원가 / FP가 50~100만원 범위"
    warning: "FP당 원가가 범위 벗어남"
```

---

## 문서 정보

- **작성일**: 2026-02-25
- **상태**: Phase 6-1 완료
- **다음 문서**: pricing_formula.md
