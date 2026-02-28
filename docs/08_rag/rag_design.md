# Phase 8: RAG 설계

---

## 1. RAG 개요

### 1.1 목적
RAG(Retrieval-Augmented Generation)는 **전문가 판단의 근거 보강**에 사용된다.
가격 계산 자체를 수행하지 않으며, LLM 기반 전문가 에이전트가 판단할 때 참고 자료를 제공한다.

### 1.2 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **보조적 역할** | RAG는 계산 엔진이 아닌 참고 자료 제공 도구 |
| **근거 기반** | 전문가 판단에 신뢰성 있는 근거 추가 |
| **도메인 특화** | 소프트웨어 프로젝트 가격 산정 도메인 집중 |

---

## 2. RAG 활용 영역

### 2.1 전문가별 활용 맵핑

```
┌──────────────────────────────────────────────────────────────┐
│                     RAG Knowledge Base                        │
├──────────────────────────────────────────────────────────────┤
│  유사 프로젝트  │  산업 단가  │  공공 기준  │  리스크 사례  │
└───────┬─────────┴──────┬──────┴──────┬──────┴───────┬────────┘
        │                │             │              │
        ▼                ▼             ▼              ▼
┌───────────────┐ ┌──────────────┐ ┌─────────────────────────┐
│ 기술 전문가    │ │ 경제 전문가   │ │      사업 전문가         │
│               │ │              │ │                         │
│ - 기술 난이도  │ │ - 단가 참조   │ │ - 시장 동향             │
│   사례 참고   │ │ - 원가 벤치마크│ │ - 경쟁사 분석           │
│ - 유사 프로젝트│ │ - 마진 기준   │ │ - 협상 사례             │
│   인력 구성   │ │              │ │                         │
└───────────────┘ └──────────────┘ └─────────────────────────┘
```

### 2.2 상세 활용 영역

| 전문가 | 활용 목적 | 검색 대상 | 출력 활용 |
|--------|----------|----------|----------|
| **기술 전문가** | 유사 프로젝트 참조 | 과거 프로젝트 사례 | 복잡도 점수 근거 |
| | 기술 스택 난이도 | 기술별 학습곡선 자료 | 기간 추정 보정 |
| | 인력 구성 참고 | 프로젝트 규모별 팀 구성 | 인력 수 산정 근거 |
| **경제 전문가** | 평균 단가 참고 | 직무별 시장 단가 | 원가 계산 기준 |
| | 공공 단가 기준 | 정부 SW사업 대가 기준 | 공공 프로젝트 산정 |
| | 마진율 벤치마크 | 산업별 평균 마진율 | 마진 제안 근거 |
| **사업 전문가** | 시장 동향 분석 | 산업 트렌드 리포트 | 전략 가중치 조정 |
| | 경쟁 상황 파악 | 경쟁사 포트폴리오 | 경쟁 강도 평가 |
| | 협상 사례 참고 | 과거 협상 기록 | 할인율 범위 설정 |

---

## 3. 지식베이스 구조

### 3.1 문서 카테고리

```yaml
KnowledgeBase:
  ProjectCases:           # 프로젝트 사례
    - project_summary     # 프로젝트 요약
    - team_composition    # 팀 구성
    - duration           # 소요 기간
    - final_price        # 최종 가격
    - lessons_learned    # 교훈

  PricingReferences:      # 가격 참조 자료
    - labor_rates        # 인력 단가
    - government_rates   # 정부 기준 단가
    - industry_benchmarks # 산업 벤치마크

  MarketIntelligence:     # 시장 정보
    - industry_trends    # 산업 동향
    - competitor_info    # 경쟁사 정보
    - technology_trends  # 기술 트렌드

  RiskCases:              # 리스크 사례
    - failed_projects    # 실패 프로젝트
    - cost_overrun       # 비용 초과 사례
    - timeline_issues    # 일정 지연 사례
```

### 3.2 문서 스키마

#### 3.2.1 프로젝트 사례 스키마

```json
{
  "document_type": "project_case",
  "metadata": {
    "document_id": "string",
    "created_at": "datetime",
    "source": "string",
    "confidence_level": "HIGH | MEDIUM | LOW"
  },
  "project": {
    "project_type": "NEW_DEVELOPMENT | ENHANCEMENT | MIGRATION",
    "application_type": "WEB | MOBILE | ENTERPRISE | EMBEDDED",
    "industry": "string",
    "scale": "SMALL | MEDIUM | LARGE | VERY_LARGE"
  },
  "team": {
    "total_members": "number",
    "composition": [
      {
        "role": "string",
        "count": "number",
        "seniority": "JUNIOR | MID | SENIOR"
      }
    ]
  },
  "timeline": {
    "duration_months": "number",
    "phases": [
      {
        "phase_name": "string",
        "duration_months": "number"
      }
    ]
  },
  "pricing": {
    "total_cost": "number",
    "currency": "string",
    "cost_breakdown": {
      "labor": "number",
      "infrastructure": "number",
      "external": "number",
      "overhead": "number"
    },
    "final_price": "number",
    "margin_rate": "number"
  },
  "features": {
    "feature_count": "number",
    "complexity_distribution": {
      "simple": "number",
      "medium": "number",
      "complex": "number"
    }
  },
  "outcome": {
    "success": "boolean",
    "lessons_learned": ["string"],
    "risk_factors_encountered": ["string"]
  }
}
```

#### 3.2.2 단가 참조 스키마

```json
{
  "document_type": "pricing_reference",
  "metadata": {
    "document_id": "string",
    "effective_date": "date",
    "source": "string",
    "region": "string"
  },
  "labor_rates": [
    {
      "role": "string",
      "seniority": "JUNIOR | MID | SENIOR",
      "monthly_rate": {
        "min": "number",
        "max": "number",
        "average": "number",
        "currency": "string"
      },
      "daily_rate": {
        "min": "number",
        "max": "number",
        "average": "number"
      }
    }
  ],
  "reference_type": "MARKET | GOVERNMENT | INTERNAL",
  "notes": "string"
}
```

---

## 4. 임베딩 전략

### 4.1 청킹 전략

```python
CHUNKING_CONFIG = {
    "project_case": {
        "method": "semantic",
        "chunk_size": 1000,
        "overlap": 200,
        "preserve_structure": True
    },
    "pricing_reference": {
        "method": "row_based",
        "chunk_size": 500,
        "overlap": 50,
        "preserve_table": True
    },
    "market_intelligence": {
        "method": "paragraph",
        "chunk_size": 800,
        "overlap": 150
    }
}

def chunk_document(document: dict) -> list:
    """
    문서 유형에 따른 청킹 전략 적용
    """
    doc_type = document['document_type']
    config = CHUNKING_CONFIG.get(doc_type)

    if config['method'] == 'semantic':
        return semantic_chunking(document, config)
    elif config['method'] == 'row_based':
        return row_based_chunking(document, config)
    else:
        return paragraph_chunking(document, config)
```

### 4.2 임베딩 모델

| 모델 | 용도 | 차원 | 비고 |
|------|-----|------|------|
| OpenAI text-embedding-3-large | 프로젝트 사례 | 3072 | 고품질 시맨틱 검색 |
| OpenAI text-embedding-3-small | 단가 참조 | 1536 | 비용 효율 |
| Multilingual-e5 | 한국어 문서 | 1024 | 다국어 지원 |

### 4.3 메타데이터 인덱싱

```python
METADATA_SCHEMA = {
    "project_type": {"type": "keyword", "filterable": True},
    "application_type": {"type": "keyword", "filterable": True},
    "industry": {"type": "keyword", "filterable": True},
    "scale": {"type": "keyword", "filterable": True},
    "team_size": {"type": "integer", "filterable": True},
    "duration_months": {"type": "integer", "filterable": True},
    "total_cost": {"type": "float", "filterable": True},
    "created_at": {"type": "date", "filterable": True},
    "source": {"type": "keyword", "filterable": True}
}
```

---

## 5. 검색 전략

### 5.1 쿼리 생성

```python
def generate_search_query(
    agent_type: str,
    project_context: dict,
    search_intent: str
) -> dict:
    """
    전문가 유형과 검색 의도에 따른 쿼리 생성
    """
    base_query = {
        "text_query": "",
        "filters": {},
        "boost_fields": [],
        "top_k": 5
    }

    if agent_type == "technical_expert":
        base_query["text_query"] = f"""
        프로젝트 유형: {project_context['project_type']}
        기능 복잡도: {project_context['complexity']}
        기술 스택: {project_context['tech_stack']}
        유사한 프로젝트의 인력 구성과 기간 정보
        """
        base_query["filters"] = {
            "project_type": project_context['project_type'],
            "scale": project_context.get('scale')
        }
        base_query["boost_fields"] = ["team", "timeline", "features"]

    elif agent_type == "economic_expert":
        base_query["text_query"] = f"""
        직무별 단가 정보
        {project_context['required_roles']}
        마진율 벤치마크
        """
        base_query["filters"] = {
            "document_type": ["pricing_reference", "project_case"]
        }
        base_query["boost_fields"] = ["pricing", "labor_rates"]

    elif agent_type == "business_expert":
        base_query["text_query"] = f"""
        산업: {project_context['industry']}
        시장 동향 및 경쟁 상황
        협상 전략
        """
        base_query["filters"] = {
            "industry": project_context['industry']
        }
        base_query["boost_fields"] = ["market", "competition"]

    return base_query
```

### 5.2 하이브리드 검색

```python
def hybrid_search(query: dict, vector_store) -> list:
    """
    벡터 검색 + 키워드 검색 하이브리드
    """
    # 1. 벡터 검색 (시맨틱)
    vector_results = vector_store.similarity_search(
        query=query["text_query"],
        k=query["top_k"] * 2,
        filter=query["filters"]
    )

    # 2. 키워드 검색 (BM25)
    keyword_results = vector_store.keyword_search(
        query=query["text_query"],
        k=query["top_k"] * 2,
        filter=query["filters"]
    )

    # 3. RRF (Reciprocal Rank Fusion) 기반 결합
    combined = reciprocal_rank_fusion(
        vector_results,
        keyword_results,
        k=60  # RRF 상수
    )

    # 4. 부스팅 적용
    boosted = apply_field_boost(
        combined,
        boost_fields=query["boost_fields"]
    )

    return boosted[:query["top_k"]]
```

### 5.3 컨텍스트 윈도우 최적화

```python
def optimize_context(
    retrieved_docs: list,
    max_tokens: int = 4000
) -> str:
    """
    검색 결과를 LLM 컨텍스트에 최적화
    """
    context_parts = []
    current_tokens = 0

    for doc in retrieved_docs:
        doc_tokens = count_tokens(doc['content'])

        if current_tokens + doc_tokens > max_tokens:
            # 문서 요약
            summarized = summarize_document(
                doc['content'],
                max_tokens=(max_tokens - current_tokens) // 2
            )
            context_parts.append(format_context(doc, summarized))
            break
        else:
            context_parts.append(format_context(doc, doc['content']))
            current_tokens += doc_tokens

    return "\n---\n".join(context_parts)


def format_context(doc: dict, content: str) -> str:
    """
    검색 결과 포맷팅
    """
    return f"""
[출처: {doc['metadata']['source']}]
[유형: {doc['metadata']['document_type']}]
[신뢰도: {doc['metadata'].get('confidence_level', 'N/A')}]

{content}
"""
```

---

## 6. 전문가별 RAG 통합

### 6.1 기술 전문가 RAG 통합

```python
def technical_expert_with_rag(
    project_data: dict,
    rag_service: RAGService
) -> dict:
    """
    기술 전문가 판단에 RAG 통합
    """
    # 1. 유사 프로젝트 검색
    similar_projects = rag_service.search(
        query_type="similar_project",
        context={
            "project_type": project_data["project_type"],
            "features": project_data["features"],
            "tech_stack": project_data["tech_stack"]
        }
    )

    # 2. 기술 난이도 참고 자료 검색
    tech_references = rag_service.search(
        query_type="tech_complexity",
        context={
            "tech_stack": project_data["tech_stack"]
        }
    )

    # 3. LLM 프롬프트에 RAG 결과 포함
    prompt = f"""
    ## 현재 프로젝트
    {format_project_data(project_data)}

    ## 참고 자료: 유사 프로젝트 사례
    {format_rag_results(similar_projects)}

    ## 참고 자료: 기술 난이도 정보
    {format_rag_results(tech_references)}

    위 정보를 참고하여 다음을 판단해주세요:
    1. 기능 복잡도 점수
    2. 필요 인력 구성
    3. 예상 개발 기간

    판단 근거를 명시해주세요.
    """

    return llm.generate(prompt, schema=TECHNICAL_OUTPUT_SCHEMA)
```

### 6.2 경제 전문가 RAG 통합

```python
def economic_expert_with_rag(
    project_data: dict,
    technical_output: dict,
    rag_service: RAGService
) -> dict:
    """
    경제 전문가 판단에 RAG 통합
    """
    # 1. 인력 단가 검색
    labor_rates = rag_service.search(
        query_type="labor_rates",
        context={
            "roles": technical_output["required_roles"],
            "region": project_data.get("region", "KOREA")
        }
    )

    # 2. 마진 벤치마크 검색
    margin_benchmarks = rag_service.search(
        query_type="margin_benchmark",
        context={
            "industry": project_data["industry"],
            "project_type": project_data["project_type"]
        }
    )

    # 3. 공공 단가 기준 (해당 시)
    if project_data.get("contract_type") == "GOVERNMENT":
        government_rates = rag_service.search(
            query_type="government_rates",
            context={
                "year": datetime.now().year
            }
        )

    prompt = f"""
    ## 프로젝트 정보
    {format_project_data(project_data)}

    ## 기술 전문가 분석 결과
    {format_technical_output(technical_output)}

    ## 참고 자료: 인력 단가
    {format_rag_results(labor_rates)}

    ## 참고 자료: 마진 벤치마크
    {format_rag_results(margin_benchmarks)}

    위 정보를 기반으로 다음을 산정해주세요:
    1. 기본 원가 (Base Cost)
    2. 손익분기점 가격
    3. 권장 마진율

    계산 근거를 명시해주세요.
    """

    return llm.generate(prompt, schema=ECONOMIC_OUTPUT_SCHEMA)
```

### 6.3 사업 전문가 RAG 통합

```python
def business_expert_with_rag(
    project_data: dict,
    rag_service: RAGService
) -> dict:
    """
    사업 전문가 판단에 RAG 통합
    """
    # 1. 시장 동향 검색
    market_trends = rag_service.search(
        query_type="market_trends",
        context={
            "industry": project_data["industry"],
            "application_type": project_data["application_type"]
        }
    )

    # 2. 경쟁 정보 검색
    competition_info = rag_service.search(
        query_type="competition",
        context={
            "industry": project_data["industry"]
        }
    )

    # 3. 협상 사례 검색
    negotiation_cases = rag_service.search(
        query_type="negotiation_history",
        context={
            "client_type": project_data.get("client_type"),
            "project_scale": project_data.get("scale")
        }
    )

    prompt = f"""
    ## 프로젝트 정보
    {format_project_data(project_data)}

    ## 참고 자료: 시장 동향
    {format_rag_results(market_trends)}

    ## 참고 자료: 경쟁 상황
    {format_rag_results(competition_info)}

    ## 참고 자료: 협상 사례
    {format_rag_results(negotiation_cases)}

    위 정보를 기반으로 다음을 평가해주세요:
    1. 전략적 중요도 가중치
    2. 경쟁 강도
    3. 권장 할인 범위

    판단 근거를 명시해주세요.
    """

    return llm.generate(prompt, schema=BUSINESS_OUTPUT_SCHEMA)
```

---

## 7. 벡터 DB 구성

### 7.1 기술 스택 선택

| 옵션 | 특징 | 적합성 |
|------|------|--------|
| **Pinecone** | 관리형, 확장성 우수 | 프로덕션 환경 |
| **Weaviate** | 하이브리드 검색, 자체 호스팅 | 온프레미스 |
| **Qdrant** | 고성능, 필터링 강점 | 중규모 |
| **Chroma** | 경량, 로컬 개발 | 프로토타입 |

### 7.2 컬렉션 구조

```python
COLLECTIONS = {
    "project_cases": {
        "description": "과거 프로젝트 사례",
        "embedding_model": "text-embedding-3-large",
        "dimension": 3072,
        "distance_metric": "cosine",
        "indexes": ["project_type", "industry", "scale"]
    },
    "pricing_references": {
        "description": "단가 및 가격 참조",
        "embedding_model": "text-embedding-3-small",
        "dimension": 1536,
        "distance_metric": "cosine",
        "indexes": ["reference_type", "effective_date"]
    },
    "market_intelligence": {
        "description": "시장 및 경쟁 정보",
        "embedding_model": "text-embedding-3-small",
        "dimension": 1536,
        "distance_metric": "cosine",
        "indexes": ["industry", "created_at"]
    },
    "risk_cases": {
        "description": "리스크 사례",
        "embedding_model": "text-embedding-3-small",
        "dimension": 1536,
        "distance_metric": "cosine",
        "indexes": ["risk_type", "severity"]
    }
}
```

---

## 8. 데이터 수집 및 관리

### 8.1 데이터 소스

| 소스 | 데이터 유형 | 수집 방법 | 갱신 주기 |
|------|-----------|----------|----------|
| 내부 프로젝트 기록 | 프로젝트 사례 | 시스템 연동 | 프로젝트 완료 시 |
| SW사업대가기준 | 공공 단가 | 수동 입력 | 연 1회 |
| 채용 플랫폼 | 인력 시장 단가 | 크롤링/API | 월 1회 |
| 산업 리포트 | 시장 동향 | 수동 입력 | 분기 1회 |

### 8.2 데이터 품질 관리

```yaml
DataQualityRules:
  Completeness:
    - required_fields_present: true
    - minimum_content_length: 100

  Consistency:
    - date_format: ISO8601
    - currency_format: standardized

  Accuracy:
    - source_verification: required
    - confidence_tagging: required

  Timeliness:
    - max_age_months: 24
    - deprecation_warning: 18
```

---

## 9. 평가 및 모니터링

### 9.1 검색 품질 메트릭

| 메트릭 | 설명 | 목표값 |
|--------|------|--------|
| **Precision@K** | 상위 K개 결과 중 관련 문서 비율 | > 0.8 |
| **Recall** | 전체 관련 문서 중 검색된 비율 | > 0.7 |
| **MRR** | 첫 관련 문서 순위의 역수 평균 | > 0.75 |
| **NDCG** | 순위 가중 관련성 점수 | > 0.8 |

### 9.2 모니터링 대시보드

```python
MONITORING_METRICS = {
    "search_latency_ms": {
        "type": "histogram",
        "buckets": [50, 100, 200, 500, 1000]
    },
    "retrieval_quality": {
        "type": "gauge",
        "dimensions": ["agent_type", "query_type"]
    },
    "cache_hit_rate": {
        "type": "counter",
        "labels": ["hit", "miss"]
    },
    "index_freshness_hours": {
        "type": "gauge"
    }
}
```

---

## 문서 정보

- **작성일**: 2026-02-26
- **상태**: Phase 8 완료
- **다음 단계**: Phase 9 - 통합 의사결정 레이어
