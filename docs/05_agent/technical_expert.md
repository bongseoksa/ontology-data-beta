# Phase 5-2: Technical Expert (기술 전문가) 설계

---

## 1. 역할 정의

### 1.1 핵심 역할
프로젝트의 기술적 측면을 분석하여 **개발 규모, 복잡도, 인력 구성, 기간**을 산정

### 1.2 책임 영역

| 영역 | 설명 |
|------|------|
| **기능 분해** | 요구사항을 개발 가능한 기능 단위로 분해 |
| **복잡도 평가** | 기술 난이도 및 구현 복잡도 점수화 |
| **인력 산정** | 필요 역할 및 인원 구성 제안 |
| **기간 추정** | 개발 일정 및 마일스톤 제안 |

---

## 2. 입력 스키마

### 2.1 필수 입력

```json
{
  "projectContext": {
    "projectId": "string",
    "projectType": "NEW_DEVELOPMENT | ENHANCEMENT | MIGRATION",
    "applicationType": "WEB | MOBILE | DESKTOP | API",
    "systemType": "ERP | CRM | CUSTOM | ..."
  },

  "requirements": {
    "features": [
      {
        "featureId": "string",
        "featureName": "string",
        "description": "string",
        "priority": "HIGH | MEDIUM | LOW"
      }
    ],
    "nonFunctional": {
      "expectedUsers": "number",
      "dataVolume": "SMALL | MEDIUM | LARGE | VERY_LARGE",
      "availability": "percentage",
      "securityLevel": "STANDARD | ENHANCED | HIGH"
    }
  },

  "constraints": {
    "techStack": ["string"],
    "integrations": ["string"],
    "timeline": {
      "desiredDuration": "number (months)",
      "hardDeadline": "date | null"
    }
  }
}
```

### 2.2 선택 입력

```json
{
  "existingSystem": {
    "hasLegacy": "boolean",
    "legacyTechStack": ["string"],
    "migrationScope": "string"
  },

  "teamContext": {
    "existingTeam": "boolean",
    "teamSkills": ["string"],
    "constraints": ["string"]
  }
}
```

---

## 3. 출력 스키마

### 3.1 전체 출력 구조

```json
{
  "agentId": "technical_expert",
  "analysisVersion": "1.0",
  "timestamp": "datetime",

  "featureAnalysis": {...},
  "complexityAssessment": {...},
  "resourceEstimation": {...},
  "timelineEstimation": {...},
  "technicalRisks": [...],

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

### 3.2 Feature Analysis (기능 분석)

```json
{
  "featureAnalysis": {
    "totalFeatures": "number",
    "featureBreakdown": [
      {
        "featureId": "string",
        "featureName": "string",
        "featureType": "DATA_ENTRY | WORKFLOW | INTEGRATION | ...",
        "estimatedFP": "number",
        "complexity": "LOW | MEDIUM | HIGH | VERY_HIGH",
        "techComponents": ["string"],
        "dependencies": ["featureId"]
      }
    ],
    "totalEstimatedFP": "number",
    "sizeCategory": "SMALL | MEDIUM | LARGE | ENTERPRISE"
  }
}
```

### 3.3 Complexity Assessment (복잡도 평가)

```json
{
  "complexityAssessment": {
    "technicalComplexity": {
      "score": "float (1-5)",
      "factors": [
        {
          "factor": "NEW_TECHNOLOGY",
          "score": "number",
          "weight": "percentage",
          "rationale": "string"
        }
      ]
    },
    "integrationComplexity": {
      "score": "float (1-5)",
      "externalSystems": "number",
      "complexity": "string"
    },
    "dataComplexity": {
      "score": "float (1-5)",
      "dataVolume": "string",
      "dataModels": "number"
    },
    "overallComplexity": {
      "score": "float (1-5)",
      "adjustmentFactor": "float (0.8-1.5)"
    }
  }
}
```

### 3.4 Resource Estimation (인력 산정)

```json
{
  "resourceEstimation": {
    "teamComposition": [
      {
        "roleType": "PROJECT_MANAGER | TECH_LEAD | BACKEND_DEV | ...",
        "skillLevel": "JUNIOR | MID | SENIOR | EXPERT",
        "headcount": "number",
        "allocation": "percentage",
        "duration": "number (months)",
        "rationale": "string"
      }
    ],
    "totalManMonth": "number",
    "teamSize": "number",
    "productivityAssumption": {
      "fpPerMM": "number",
      "basis": "string"
    }
  }
}
```

### 3.5 Timeline Estimation (일정 추정)

```json
{
  "timelineEstimation": {
    "totalDuration": {
      "optimistic": "number (months)",
      "realistic": "number (months)",
      "pessimistic": "number (months)"
    },
    "phases": [
      {
        "phaseType": "REQUIREMENTS | DESIGN | DEVELOPMENT | ...",
        "duration": "number (weeks)",
        "effortPercentage": "percentage",
        "keyActivities": ["string"],
        "deliverables": ["string"]
      }
    ],
    "milestones": [
      {
        "name": "string",
        "targetWeek": "number",
        "criteria": ["string"]
      }
    ],
    "criticalPath": ["phaseType"]
  }
}
```

### 3.6 Technical Risks (기술 리스크)

```json
{
  "technicalRisks": [
    {
      "riskId": "string",
      "riskType": "TECHNOLOGY | INTEGRATION | PERFORMANCE | SECURITY",
      "description": "string",
      "probability": "LOW | MEDIUM | HIGH",
      "impact": "LOW | MEDIUM | HIGH | CRITICAL",
      "mitigation": "string",
      "affectedAreas": ["string"]
    }
  ]
}
```

---

## 4. 분석 로직

### 4.1 기능점수(FP) 산정 로직

```yaml
FPEstimationLogic:
  # 기능 유형별 기본 FP
  BaselineFP:
    DATA_ENTRY:
      simple: 3
      average: 4
      complex: 6

    DATA_DISPLAY:
      simple: 4
      average: 5
      complex: 7

    WORKFLOW:
      simple: 6
      average: 8
      complex: 12

    INTEGRATION:
      simple: 5
      average: 7
      complex: 10

    REPORT:
      simple: 4
      average: 5
      complex: 7

  # 복잡도 보정
  ComplexityAdjustment:
    LOW: 0.8
    MEDIUM: 1.0
    HIGH: 1.3
    VERY_HIGH: 1.6

  # 계산
  FeatureFP = BaselineFP × ComplexityAdjustment
  TotalFP = SUM(FeatureFP)
```

### 4.2 복잡도 평가 로직

```yaml
ComplexityEvaluationLogic:
  TechnicalFactors:
    - factor: "NEW_TECHNOLOGY"
      evaluation: |
        - 팀 경험 있는 기술: 1
        - 일부 경험: 2-3
        - 신기술 도입: 4-5
      weight: 20%

    - factor: "ARCHITECTURE_COMPLEXITY"
      evaluation: |
        - 단일 서버: 1
        - MSA 5개 미만: 2-3
        - MSA 5개 이상: 4-5
      weight: 15%

    - factor: "DATA_COMPLEXITY"
      evaluation: |
        - 테이블 20개 미만: 1
        - 20-50개: 2-3
        - 50개 이상: 4-5
      weight: 15%

  IntegrationFactors:
    - factor: "EXTERNAL_SYSTEMS"
      evaluation: |
        - 연동 1-2개: 1-2
        - 연동 3-5개: 3
        - 연동 6개 이상: 4-5
      weight: 20%

    - factor: "LEGACY_INTEGRATION"
      evaluation: |
        - 레거시 없음: 1
        - 문서화된 레거시: 2-3
        - 미문서화 레거시: 4-5
      weight: 15%

  CalculationFormula:
    overallScore = SUM(factor.score × factor.weight)
    adjustmentFactor = 0.8 + (overallScore - 1) × 0.15
```

### 4.3 인력 산정 로직

```yaml
ResourceEstimationLogic:
  # FP 기반 M/M 추정
  ProductivityBenchmark:
    projectType:
      SI_LARGE:
        fpPerMM: 8-10
      SI_MEDIUM:
        fpPerMM: 10-12
      CUSTOM_DEV:
        fpPerMM: 12-15
      STARTUP_MVP:
        fpPerMM: 15-20

  # 역할 구성 가이드
  TeamCompositionGuide:
    SMALL_PROJECT: # < 300 FP
      PM: {count: 1, allocation: 50}
      TECH_LEAD: {count: 0.5, allocation: 100}
      DEVELOPER: {count: 2-3, allocation: 100}
      QA: {count: 0.5, allocation: 100}

    MEDIUM_PROJECT: # 300-1000 FP
      PM: {count: 1, allocation: 100}
      TECH_LEAD: {count: 1, allocation: 100}
      BACKEND_DEV: {count: 2-4, allocation: 100}
      FRONTEND_DEV: {count: 1-2, allocation: 100}
      DBA: {count: 0.5, allocation: 100}
      QA: {count: 1-2, allocation: 100}

    LARGE_PROJECT: # > 1000 FP
      PM: {count: 1-2, allocation: 100}
      TECH_LEAD: {count: 1-2, allocation: 100}
      ARCHITECT: {count: 1, allocation: 100}
      BACKEND_DEV: {count: 5-10, allocation: 100}
      FRONTEND_DEV: {count: 2-5, allocation: 100}
      DBA: {count: 1, allocation: 100}
      DEVOPS: {count: 1, allocation: 100}
      QA: {count: 2-5, allocation: 100}
```

### 4.4 기간 추정 로직

```yaml
TimelineEstimationLogic:
  # 기본 공식
  BaseDuration = TotalManMonth / AverageTeamSize

  # 3점 추정
  ThreePointEstimate:
    optimistic: BaseDuration × 0.85
    realistic: BaseDuration × 1.0
    pessimistic: BaseDuration × 1.3

  # 단계별 비율
  PhaseDistribution:
    INITIATION: 5%
    REQUIREMENTS: 10-15%
    DESIGN: 15-20%
    DEVELOPMENT: 35-45%
    TESTING: 15-20%
    DEPLOYMENT: 5-10%

  # 복잡도 보정
  ComplexityAdjustment:
    HIGH_COMPLEXITY: +15%
    TIGHT_DEADLINE: +10% (리스크 증가)
    NEW_TEAM: +20%
```

---

## 5. RAG 활용 전략

### 5.1 RAG 쿼리 시나리오

| 시나리오 | 쿼리 예시 | 활용 목적 |
|----------|----------|----------|
| FP 벤치마크 | "웹 CRM 500FP 개발 기간" | 기간 추정 검증 |
| 기술 스택 사례 | "React + Spring Boot 프로젝트 생산성" | 생산성 가정 보강 |
| 인력 구성 | "10인 이상 SI 프로젝트 팀 구성" | 팀 구성 참조 |
| 리스크 사례 | "레거시 연동 프로젝트 실패 사례" | 리스크 식별 |

### 5.2 RAG 쿼리 템플릿

```json
{
  "queryTemplates": {
    "FP_BENCHMARK": {
      "query": "{applicationType} {systemType} {fpRange}FP 개발 사례",
      "filters": {
        "projectSize": "{sizeCategory}",
        "industry": "{industry}",
        "recency": "5years"
      }
    },
    "PRODUCTIVITY": {
      "query": "{techStack} 프로젝트 FP당 개발 기간",
      "filters": {
        "projectType": "{projectType}"
      }
    },
    "TEAM_COMPOSITION": {
      "query": "{sizeCategory} {applicationType} 프로젝트 팀 구성",
      "filters": {
        "teamSize": "{expectedTeamSize}"
      }
    }
  }
}
```

---

## 6. LLM 프롬프트 설계

### 6.1 시스템 프롬프트

```
당신은 소프트웨어 프로젝트의 기술 전문가입니다.

역할:
- 요구사항을 분석하여 기능을 분해합니다
- 각 기능의 기술적 복잡도를 평가합니다
- 필요한 인력 구성과 기간을 산정합니다
- 기술적 리스크를 식별합니다

원칙:
1. 보수적 추정: 낙관적이기보다 현실적으로 추정
2. 근거 제시: 모든 판단에 구체적 근거 제시
3. 리스크 고려: 잠재적 기술 리스크 명시
4. 업계 기준 참조: 제공된 벤치마크 데이터 활용

출력 형식:
JSON 형식으로 출력하며, 지정된 스키마를 엄격히 따릅니다.
```

### 6.2 사용자 프롬프트 템플릿

```
## 프로젝트 정보
{projectContext}

## 요구사항
{requirements}

## 제약 조건
{constraints}

## 참조 데이터 (RAG)
{ragContext}

## 분석 요청
위 정보를 바탕으로 다음을 분석해주세요:
1. 기능별 FP 및 복잡도 평가
2. 전체 복잡도 점수 및 조정 계수
3. 추천 팀 구성 및 M/M 산정
4. 개발 일정 및 마일스톤 제안
5. 식별된 기술 리스크

분석 결과는 지정된 JSON 스키마로 출력해주세요.
```

---

## 7. 검증 규칙

### 7.1 출력 검증

```yaml
ValidationRules:
  FeatureAnalysis:
    - "totalEstimatedFP > 0"
    - "각 기능의 FP 합 = totalEstimatedFP"
    - "sizeCategory가 FP 범위와 일치"

  ComplexityAssessment:
    - "모든 점수가 1-5 범위 내"
    - "adjustmentFactor가 0.8-1.5 범위 내"

  ResourceEstimation:
    - "totalManMonth > 0"
    - "팀 구성이 프로젝트 규모에 적합"
    - "역할별 duration이 총 기간 이내"

  TimelineEstimation:
    - "optimistic <= realistic <= pessimistic"
    - "phase effort 합계 = 100%"
```

### 7.2 일관성 검증

```yaml
ConsistencyChecks:
  - check: "FP vs M/M 비율"
    rule: "totalFP / totalManMonth가 8-20 범위 내"
    severity: WARNING

  - check: "팀 규모 vs 기간"
    rule: "팀 규모가 최소 기간 충족 가능"
    severity: ERROR

  - check: "복잡도 vs 인력 수준"
    rule: "높은 복잡도 시 Senior 이상 포함"
    severity: WARNING
```

---

## 문서 정보

- **작성일**: 2026-02-25
- **상태**: Phase 5-2 완료
- **다음 문서**: business_expert.md
