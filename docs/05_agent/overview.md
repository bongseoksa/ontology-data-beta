# Phase 5-1: Multi-Agent 구조 개요

---

## 1. Multi-Agent 아키텍처 개요

### 1.1 설계 철학
- **전문성 분리**: 각 도메인 전문가의 독립적 판단
- **협업 구조**: 전문가 간 정보 교환 및 상호 보완
- **투명성**: 각 판단 과정과 근거의 명확한 추적
- **확장성**: 새로운 전문가 추가 용이

### 1.2 전체 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                          │
│                  (에이전트 조율 및 통합)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│  │  Technical  │   │  Business   │   │  Economic   │           │
│  │   Expert    │   │   Expert    │   │   Expert    │           │
│  │             │   │             │   │             │           │
│  │ • 기능 분해  │   │ • 시장 분석  │   │ • 원가 계산  │           │
│  │ • 난이도 평가│   │ • 경쟁 분석  │   │ • 마진 제안  │           │
│  │ • 인력 산정  │   │ • 전략 가중치│   │ • 리스크 반영│           │
│  │ • 기간 추정  │   │ • 협상 범위  │   │ • BEP 계산  │           │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘           │
│         │                 │                 │                  │
│         └─────────────────┼─────────────────┘                  │
│                           ▼                                    │
│                  ┌─────────────────┐                           │
│                  │   Synthesis     │                           │
│                  │   (결과 통합)    │                           │
│                  └─────────────────┘                           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                       RAG Layer                                 │
│                 (지식 검색 및 근거 보강)                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 에이전트 역할 정의

### 2.1 Technical Expert (기술 전문가)

| 항목 | 내용 |
|------|------|
| **역할** | 프로젝트의 기술적 분석 및 구조화 |
| **입력** | 사업계획서 구조화 데이터, 기능 목록 |
| **출력** | 복잡도 점수, 인력 구성, 기간 추정 |
| **RAG 활용** | 유사 기술 스택 사례, 생산성 벤치마크 |

### 2.2 Business Expert (사업 전문가)

| 항목 | 내용 |
|------|------|
| **역할** | 시장 및 경쟁 환경 분석, 전략적 판단 |
| **입력** | 프로젝트 정보, 고객 정보, 시장 데이터 |
| **출력** | 전략 가중치, 경쟁 강도, 협상 범위 |
| **RAG 활용** | 시장 동향, 경쟁사 가격 사례 |

### 2.3 Economic Expert (경제 전문가)

| 항목 | 내용 |
|------|------|
| **역할** | 비용 계산 및 가격 산정 |
| **입력** | 인력/기간 데이터, 비용 기준, 전략 가중치 |
| **출력** | 원가, 마진, 최종 가격, 손익분기점 |
| **RAG 활용** | 단가 기준, 마진율 벤치마크 |

---

## 3. 에이전트 협업 흐름

### 3.1 순차적 협업 (Sequential)

```
[입력: 사업계획서 구조화 데이터]
         │
         ▼
┌─────────────────┐
│ Technical Expert│ ──► 복잡도, 인력, 기간
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Business Expert │ ──► 전략 가중치, 경쟁 조정
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Economic Expert │ ──► 원가, 마진, 최종 가격
└────────┬────────┘
         │
         ▼
[출력: 가격 산정 결과]
```

### 3.2 피드백 루프 (Iterative)

```
Technical Expert ──┐
                   │
Business Expert  ──┼──► Synthesis ──► 불일치 감지?
                   │                      │
Economic Expert ──┘                       │ Yes
                                          ▼
                                    재조정 요청
                                          │
                                          ▼
                              관련 Expert에게 피드백
```

### 3.3 협업 규칙

```yaml
CollaborationRules:
  # 데이터 의존성
  Dependencies:
    EconomicExpert:
      requires: [TechnicalExpert.output]
      optional: [BusinessExpert.output]

    BusinessExpert:
      requires: [ProjectData]
      optional: [TechnicalExpert.output]

  # 충돌 해결
  ConflictResolution:
    - rule: "기술적 제약 우선"
      when: "비용 vs 기술 가능성 충돌"
      priority: TechnicalExpert

    - rule: "사업 전략 고려"
      when: "마진 vs 경쟁력 충돌"
      priority: BusinessExpert

    - rule: "최소 마진 보장"
      when: "가격 vs 수익성 충돌"
      priority: EconomicExpert
```

---

## 4. 입출력 인터페이스

### 4.1 공통 입력 스키마

```json
{
  "projectContext": {
    "projectId": "string",
    "projectName": "string",
    "projectType": "enum",
    "clientInfo": {
      "clientName": "string",
      "clientType": "enum",
      "industry": "string"
    },
    "contractType": "enum"
  },

  "parsedDocument": {
    "features": [...],
    "requirements": [...],
    "constraints": [...],
    "timeline": {...}
  },

  "marketContext": {
    "competitionLevel": "enum",
    "marketPosition": "enum",
    "strategicImportance": "enum"
  }
}
```

### 4.2 공통 출력 스키마

```json
{
  "agentId": "string",
  "agentType": "enum",
  "timestamp": "datetime",

  "analysis": {
    // 에이전트별 분석 결과
  },

  "recommendations": [
    {
      "type": "string",
      "value": "any",
      "confidence": "float (0-1)",
      "rationale": "string"
    }
  ],

  "metadata": {
    "processingTime": "duration",
    "ragQueriesUsed": ["string"],
    "confidenceScore": "float"
  }
}
```

---

## 5. Orchestration Layer

### 5.1 역할

| 기능 | 설명 |
|------|------|
| **스케줄링** | 에이전트 실행 순서 결정 |
| **데이터 라우팅** | 에이전트 간 데이터 전달 |
| **충돌 해결** | 상충되는 판단 조정 |
| **품질 검증** | 출력 유효성 검사 |
| **결과 통합** | 최종 결과 합성 |

### 5.2 오케스트레이션 로직

```yaml
OrchestrationWorkflow:
  Steps:
    1_InitializeContext:
      action: "프로젝트 컨텍스트 로드"
      output: SharedContext

    2_RunTechnicalAnalysis:
      agent: TechnicalExpert
      input: [SharedContext, ParsedDocument]
      output: TechnicalAnalysis

    3_RunBusinessAnalysis:
      agent: BusinessExpert
      input: [SharedContext, TechnicalAnalysis]
      parallel: true  # 기술 분석과 병렬 가능
      output: BusinessAnalysis

    4_RunEconomicAnalysis:
      agent: EconomicExpert
      input: [TechnicalAnalysis, BusinessAnalysis]
      output: EconomicAnalysis

    5_ValidateConsistency:
      action: "일관성 검증"
      input: [TechnicalAnalysis, BusinessAnalysis, EconomicAnalysis]
      onConflict: "ResolveConflict"

    6_SynthesizeResults:
      action: "최종 결과 통합"
      output: FinalPricingResult
```

### 5.3 에러 처리

```yaml
ErrorHandling:
  AgentTimeout:
    threshold: "30 seconds"
    action: "retry with fallback"
    maxRetries: 2

  InconsistentOutput:
    action: "request clarification from agent"
    escalation: "human review if unresolved"

  LowConfidenceScore:
    threshold: 0.6
    action: "flag for review"
    supplement: "request additional RAG queries"
```

---

## 6. RAG 통합

### 6.1 에이전트별 RAG 활용

| 에이전트 | RAG 쿼리 유형 | 예시 |
|----------|-------------|------|
| Technical | 기술 사례 검색 | "React Native 앱 개발 기간 사례" |
| Technical | 생산성 벤치마크 | "FP 500급 웹 프로젝트 생산성" |
| Business | 시장 동향 | "2024년 금융권 SI 시장 현황" |
| Business | 경쟁 가격 | "CRM 구축 프로젝트 낙찰 사례" |
| Economic | 단가 기준 | "고급 Java 개발자 월 단가" |
| Economic | 마진율 참조 | "중형 SI 프로젝트 평균 마진율" |

### 6.2 RAG 쿼리 인터페이스

```json
{
  "ragQuery": {
    "agentId": "technical_expert",
    "queryType": "BENCHMARK",
    "query": "500FP급 웹 애플리케이션 개발 기간",
    "filters": {
      "industry": ["금융", "공공"],
      "recency": "3years",
      "projectSize": ["MEDIUM", "LARGE"]
    },
    "topK": 5
  }
}
```

---

## 7. 에이전트 구현 가이드

### 7.1 LLM 프롬프트 구조

```yaml
AgentPromptStructure:
  SystemPrompt:
    - 역할 정의
    - 전문 도메인 설명
    - 출력 형식 지정
    - 제약 조건

  UserPrompt:
    - 프로젝트 컨텍스트
    - 분석 대상 데이터
    - 특별 지시사항

  RAGContext:
    - 검색된 관련 문서
    - 벤치마크 데이터
```

### 7.2 에이전트 구현 패턴

```python
# 의사 코드
class BaseExpertAgent:
    def __init__(self, llm, rag_retriever):
        self.llm = llm
        self.rag = rag_retriever

    def analyze(self, context, input_data):
        # 1. RAG 쿼리로 관련 정보 검색
        rag_context = self.rag.retrieve(self.build_query(input_data))

        # 2. 프롬프트 구성
        prompt = self.build_prompt(context, input_data, rag_context)

        # 3. LLM 호출
        response = self.llm.generate(prompt)

        # 4. 응답 파싱 및 검증
        result = self.parse_response(response)
        self.validate(result)

        return result
```

---

## 8. 품질 보증

### 8.1 신뢰도 점수 산정

```yaml
ConfidenceScoring:
  Factors:
    - ragMatchQuality: "RAG 결과 관련성" (weight: 30%)
    - dataCompleteness: "입력 데이터 완전성" (weight: 25%)
    - internalConsistency: "분석 내부 일관성" (weight: 25%)
    - historicalAccuracy: "과거 정확도" (weight: 20%)

  Thresholds:
    HIGH: ">= 0.8"
    MEDIUM: "0.6 - 0.8"
    LOW: "< 0.6"
```

### 8.2 검증 체크리스트

```yaml
ValidationChecklist:
  TechnicalExpert:
    - "인력 구성이 프로젝트 규모에 적합한가?"
    - "기간 추정이 FP 대비 합리적인가?"
    - "복잡도 점수가 기능별로 일관성 있는가?"

  BusinessExpert:
    - "경쟁 분석이 시장 데이터와 일치하는가?"
    - "전략 가중치가 고객 상황에 적합한가?"

  EconomicExpert:
    - "원가 계산이 정확한가?"
    - "마진율이 업계 기준 내인가?"
    - "최종 가격이 예산 범위 내인가?"
```

---

## 문서 정보

- **작성일**: 2026-02-25
- **상태**: Phase 5-1 완료
- **다음 문서**: technical_expert.md
