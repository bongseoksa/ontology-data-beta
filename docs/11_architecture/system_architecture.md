# Phase 11: 최종 프로젝트 아키텍처

---

## 1. 시스템 개요

### 1.1 시스템 정의

**AI 기반 프로젝트 가격산정 시스템**은 사업계획서를 입력받아
다중 전문가 시뮬레이션과 온톨로지 기반 구조화를 통해
프로젝트 가격을 자동 산정하는 의사결정 지원 시스템이다.

### 1.2 핵심 특징

| 특징 | 설명 |
|------|------|
| **문서 이해** | 비정형 사업계획서를 구조화된 데이터로 변환 |
| **온톨로지 기반** | 도메인 지식을 온톨로지로 체계화 |
| **다중 전문가** | 기술/경제/사업 전문가 시뮬레이션 |
| **규칙 + AI** | 규칙 기반 계산 + LLM 기반 판단의 하이브리드 |
| **RAG 보강** | 유사 사례 및 벤치마크 기반 근거 강화 |

### 1.3 전체 시스템 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Web App   │  │   API Client │  │  Admin UI   │  │  Dashboard  │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
└─────────┼────────────────┼────────────────┼────────────────┼────────────────┘
          │                │                │                │
          └────────────────┴────────────────┴────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                API GATEWAY                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Auth      │  │Rate Limiting│  │   Routing   │  │   Logging   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            APPLICATION LAYER                                 │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                        ORCHESTRATION SERVICE                           │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐               │ │
│  │  │ Workflow │  │  State   │  │  Error   │  │ Tracing  │               │ │
│  │  │ Engine   │  │  Machine │  │ Handler  │  │          │               │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘               │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                      │                                       │
│         ┌────────────────────────────┼────────────────────────────┐         │
│         │                            │                            │         │
│         ▼                            ▼                            ▼         │
│  ┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐  │
│  │    DOCUMENT     │    │      ANALYSIS       │    │     SYNTHESIS       │  │
│  │    SERVICE      │    │      SERVICE        │    │      SERVICE        │  │
│  │                 │    │                     │    │                     │  │
│  │ - Parsing       │    │ - Technical Agent   │    │ - Conflict Resolver │  │
│  │ - Extraction    │    │ - Economic Agent    │    │ - Price Calculator  │  │
│  │ - Validation    │    │ - Business Agent    │    │ - Explanation Gen   │  │
│  │ - Mapping       │    │ - RAG Integration   │    │                     │  │
│  └────────┬────────┘    └──────────┬──────────┘    └──────────┬──────────┘  │
│           │                        │                          │              │
└───────────┼────────────────────────┼──────────────────────────┼──────────────┘
            │                        │                          │
            ▼                        ▼                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DOMAIN LAYER                                    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                         ONTOLOGY ENGINE                                  ││
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐        ││
│  │  │    Core    │  │  Project   │  │    Cost    │  │  Pricing   │        ││
│  │  │  Ontology  │  │  Ontology  │  │  Ontology  │  │  Ontology  │        ││
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘        ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                         CALCULATION ENGINE                               ││
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐        ││
│  │  │    Cost    │  │   Pricing  │  │    Risk    │  │  Strategy  │        ││
│  │  │  Formula   │  │  Formula   │  │  Premium   │  │ Adjustment │        ││
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘        ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           INFRASTRUCTURE LAYER                               │
│                                                                              │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐ │
│  │     LLM       │  │   Vector DB   │  │  Relational   │  │    Cache      │ │
│  │   Gateway     │  │   (RAG)       │  │      DB       │  │   (Redis)     │ │
│  └───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘ │
│                                                                              │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐ │
│  │    Object     │  │    Message    │  │  Monitoring   │  │    Logging    │ │
│  │   Storage     │  │    Queue      │  │   (Metrics)   │  │   (Traces)    │ │
│  └───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 레이어별 상세 설계

### 2.1 Presentation Layer

```yaml
Components:
  WebApp:
    framework: "React / Next.js"
    features:
      - 사업계획서 업로드
      - 실시간 진행 상황 표시
      - 결과 시각화
      - 리포트 다운로드

  AdminUI:
    framework: "React Admin"
    features:
      - 시스템 설정 관리
      - 온톨로지 편집
      - RAG 데이터 관리
      - 사용자 관리

  Dashboard:
    framework: "Grafana / Custom"
    features:
      - 실시간 메트릭
      - 정확성 트렌드
      - 시스템 건강 상태
```

### 2.2 API Gateway

```yaml
APIGateway:
  technology: "Kong / AWS API Gateway"

  endpoints:
    - path: "/api/v1/estimates"
      methods: [POST, GET]
      description: "가격 산정 요청 및 조회"

    - path: "/api/v1/estimates/{id}/status"
      methods: [GET]
      description: "진행 상태 조회"

    - path: "/api/v1/estimates/{id}/result"
      methods: [GET]
      description: "산정 결과 조회"

    - path: "/api/v1/documents"
      methods: [POST]
      description: "문서 업로드"

    - path: "/api/v1/feedback"
      methods: [POST]
      description: "피드백 제출"

  middleware:
    - authentication: "JWT"
    - rate_limiting: "100 req/min per user"
    - request_validation: "OpenAPI spec"
    - logging: "Structured JSON"
```

### 2.3 Application Layer

#### 2.3.1 Orchestration Service

```python
class EstimationOrchestrator:
    """
    가격 산정 워크플로우 오케스트레이터
    """
    def __init__(
        self,
        document_service: DocumentService,
        analysis_service: AnalysisService,
        synthesis_service: SynthesisService,
        evaluation_service: EvaluationService
    ):
        self.document_service = document_service
        self.analysis_service = analysis_service
        self.synthesis_service = synthesis_service
        self.evaluation_service = evaluation_service
        self.state_machine = EstimationStateMachine()

    async def process_estimation(
        self,
        request: EstimationRequest
    ) -> EstimationResult:
        """
        전체 가격 산정 프로세스 실행
        """
        trace = DecisionTrace(request.project_id)

        try:
            # 1. 문서 분석
            self.state_machine.transition(State.DOCUMENT_PROCESSING)
            document_result = await self.document_service.process(
                request.document,
                trace
            )

            # 2. 다중 전문가 분석 (병렬)
            self.state_machine.transition(State.EXPERT_ANALYSIS)
            analysis_results = await self.analysis_service.analyze_parallel(
                document_result,
                trace
            )

            # 3. 통합 및 가격 계산
            self.state_machine.transition(State.SYNTHESIS)
            synthesis_result = await self.synthesis_service.synthesize(
                document_result,
                analysis_results,
                trace
            )

            # 4. 검증
            self.state_machine.transition(State.VALIDATION)
            validation_result = await self.evaluation_service.validate(
                synthesis_result
            )

            # 5. 결과 생성
            self.state_machine.transition(State.COMPLETED)
            return EstimationResult(
                project_id=request.project_id,
                pricing=synthesis_result.pricing,
                explanation=synthesis_result.explanation,
                validation=validation_result,
                trace=trace.export()
            )

        except Exception as e:
            self.state_machine.transition(State.FAILED)
            return self.handle_error(e, trace)
```

#### 2.3.2 Document Service

```python
class DocumentService:
    """
    문서 분석 서비스
    """
    def __init__(
        self,
        parser: DocumentParser,
        extractor: InformationExtractor,
        mapper: OntologyMapper,
        validator: DataValidator
    ):
        self.parser = parser
        self.extractor = extractor
        self.mapper = mapper
        self.validator = validator

    async def process(
        self,
        document: UploadedDocument,
        trace: DecisionTrace
    ) -> DocumentAnalysisResult:
        """
        문서 처리 파이프라인
        """
        # 1. 파싱
        text = await self.parser.parse(document)
        trace.add_step("parsing", {"doc_type": document.type}, {"text_length": len(text)})

        # 2. 정보 추출
        extracted = await self.extractor.extract(text)
        trace.add_step("extraction", {"text_length": len(text)}, {"fields": list(extracted.keys())})

        # 3. 온톨로지 매핑
        mapped = await self.mapper.map(extracted)
        trace.add_step("mapping", {"fields": list(extracted.keys())}, {"ontology_entities": list(mapped.keys())})

        # 4. 검증
        validated = await self.validator.validate(mapped)

        return DocumentAnalysisResult(
            raw_text=text,
            extracted_data=extracted,
            ontology_mapped=mapped,
            validation=validated
        )
```

#### 2.3.3 Analysis Service

```python
class AnalysisService:
    """
    다중 전문가 분석 서비스
    """
    def __init__(
        self,
        technical_agent: TechnicalExpertAgent,
        economic_agent: EconomicExpertAgent,
        business_agent: BusinessExpertAgent,
        rag_service: RAGService
    ):
        self.technical_agent = technical_agent
        self.economic_agent = economic_agent
        self.business_agent = business_agent
        self.rag_service = rag_service

    async def analyze_parallel(
        self,
        document_result: DocumentAnalysisResult,
        trace: DecisionTrace
    ) -> AnalysisResults:
        """
        병렬 전문가 분석
        """
        # RAG 검색 (공통)
        rag_context = await self.rag_service.retrieve(
            document_result.ontology_mapped
        )

        # 병렬 분석 실행
        technical_task = self.technical_agent.analyze(
            document_result, rag_context, trace
        )
        economic_task = self.economic_agent.analyze(
            document_result, rag_context, trace
        )
        business_task = self.business_agent.analyze(
            document_result, rag_context, trace
        )

        technical, economic, business = await asyncio.gather(
            technical_task, economic_task, business_task
        )

        return AnalysisResults(
            technical=technical,
            economic=economic,
            business=business,
            rag_context=rag_context
        )
```

#### 2.3.4 Synthesis Service

```python
class SynthesisService:
    """
    통합 및 가격 계산 서비스
    """
    def __init__(
        self,
        conflict_resolver: ConflictResolver,
        price_calculator: PriceCalculator,
        explanation_generator: ExplanationGenerator
    ):
        self.conflict_resolver = conflict_resolver
        self.price_calculator = price_calculator
        self.explanation_generator = explanation_generator

    async def synthesize(
        self,
        document_result: DocumentAnalysisResult,
        analysis_results: AnalysisResults,
        trace: DecisionTrace
    ) -> SynthesisResult:
        """
        분석 결과 통합 및 최종 가격 산출
        """
        # 1. 충돌 감지 및 해결
        conflicts = self.conflict_resolver.detect(analysis_results)
        resolved = self.conflict_resolver.resolve(analysis_results, conflicts)
        trace.add_step("conflict_resolution", {"conflicts": len(conflicts)}, resolved)

        # 2. 가격 계산
        pricing = self.price_calculator.calculate(resolved)
        trace.add_step("price_calculation", resolved, pricing)

        # 3. 설명 생성
        explanation = await self.explanation_generator.generate(
            document_result,
            resolved,
            pricing,
            conflicts
        )

        return SynthesisResult(
            pricing=pricing,
            explanation=explanation,
            conflicts_resolved=conflicts,
            adjusted_analysis=resolved
        )
```

---

## 3. Domain Layer 상세

### 3.1 Ontology Engine

```python
class OntologyEngine:
    """
    온톨로지 관리 및 추론 엔진
    """
    def __init__(self):
        self.ontologies = {
            "core": CoreOntology(),
            "project": ProjectOntology(),
            "cost": CostOntology(),
            "pricing": PricingOntology()
        }

    def validate_entity(self, entity_type: str, data: dict) -> bool:
        """엔티티 유효성 검증"""
        schema = self.get_schema(entity_type)
        return schema.validate(data)

    def infer_relations(self, entities: list) -> list:
        """관계 추론"""
        relations = []
        for entity in entities:
            related = self.find_related_concepts(entity)
            relations.extend(related)
        return relations

    def map_to_ontology(self, extracted_data: dict) -> dict:
        """추출 데이터를 온톨로지에 매핑"""
        mapped = {}

        # 프로젝트 엔티티
        mapped["project"] = self.ontologies["project"].create_entity(
            extracted_data.get("project_basic", {})
        )

        # 스코프 엔티티
        mapped["scope"] = self.ontologies["project"].create_scope(
            extracted_data.get("functional_requirements", {})
        )

        # 비용 구조
        mapped["cost_structure"] = self.ontologies["cost"].create_structure(
            extracted_data
        )

        return mapped
```

### 3.2 Calculation Engine

```python
class CalculationEngine:
    """
    가격 계산 엔진
    """
    def __init__(self, config: CalculationConfig):
        self.config = config
        self.cost_calculator = CostCalculator(config)
        self.pricing_calculator = PricingCalculator(config)

    def calculate_cost(self, analysis: AnalysisResults) -> CostBreakdown:
        """
        원가 계산
        """
        # 인건비
        labor_cost = self.cost_calculator.calculate_labor(
            roles=analysis.technical.required_roles,
            duration=analysis.technical.estimated_duration
        )

        # 인프라 비용
        infra_cost = self.cost_calculator.calculate_infrastructure(
            tech_stack=analysis.technical.tech_requirements,
            duration=analysis.technical.estimated_duration
        )

        # 외부 비용
        external_cost = self.cost_calculator.calculate_external(
            analysis.technical.external_dependencies
        )

        # 간접비
        overhead = self.cost_calculator.calculate_overhead(
            labor_cost + infra_cost + external_cost
        )

        return CostBreakdown(
            labor=labor_cost,
            infrastructure=infra_cost,
            external=external_cost,
            overhead=overhead,
            total=labor_cost + infra_cost + external_cost + overhead
        )

    def calculate_price(
        self,
        cost: CostBreakdown,
        analysis: AnalysisResults
    ) -> PricingResult:
        """
        최종 가격 계산
        """
        base_cost = cost.total

        # 마진 적용
        margin_rate = analysis.economic.recommended_margin
        margin_amount = base_cost * margin_rate

        # 리스크 프리미엄
        risk_rate = analysis.economic.risk_premium
        risk_amount = base_cost * risk_rate

        # 전략 조정
        strategic_weight = analysis.business.strategic_weight
        price_before_strategy = base_cost + margin_amount + risk_amount
        final_price = price_before_strategy * strategic_weight

        return PricingResult(
            base_cost=base_cost,
            margin_rate=margin_rate,
            margin_amount=margin_amount,
            risk_premium_rate=risk_rate,
            risk_premium_amount=risk_amount,
            strategic_weight=strategic_weight,
            final_price=final_price,
            price_range=self.calculate_range(
                final_price,
                analysis.business.discount_range
            )
        )
```

---

## 4. Infrastructure Layer 상세

### 4.1 기술 스택

```yaml
Infrastructure:
  Compute:
    primary: "Kubernetes (EKS/GKE)"
    serverless: "AWS Lambda (for async tasks)"

  LLM:
    primary: "OpenAI GPT-4"
    fallback: "Claude 3"
    gateway: "LiteLLM / Custom Gateway"

  VectorDB:
    primary: "Pinecone"
    alternative: "Weaviate"
    embedding: "text-embedding-3-large"

  RelationalDB:
    primary: "PostgreSQL"
    read_replicas: 2
    connection_pool: "PgBouncer"

  Cache:
    primary: "Redis Cluster"
    use_cases:
      - Session
      - Rate Limiting
      - Calculation Cache
      - RAG Cache

  ObjectStorage:
    primary: "S3"
    use_cases:
      - Document Storage
      - Report Storage
      - Backup

  MessageQueue:
    primary: "SQS / Redis Streams"
    use_cases:
      - Async Processing
      - Event Publishing

  Monitoring:
    metrics: "Prometheus + Grafana"
    logging: "ELK Stack"
    tracing: "Jaeger / OpenTelemetry"
    alerting: "PagerDuty"
```

### 4.2 LLM Gateway

```python
class LLMGateway:
    """
    LLM 호출 관리 게이트웨이
    """
    def __init__(self, config: LLMConfig):
        self.config = config
        self.providers = {
            "openai": OpenAIProvider(config.openai),
            "anthropic": AnthropicProvider(config.anthropic)
        }
        self.rate_limiter = RateLimiter(config.rate_limits)
        self.cache = LLMCache(config.cache)

    async def generate(
        self,
        prompt: str,
        model: str = "gpt-4",
        schema: Optional[dict] = None,
        **kwargs
    ) -> LLMResponse:
        """
        LLM 호출
        """
        # 캐시 확인
        cache_key = self.cache.generate_key(prompt, model)
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        # Rate limiting
        await self.rate_limiter.acquire(model)

        # 호출
        provider = self.get_provider(model)
        try:
            response = await provider.generate(prompt, schema=schema, **kwargs)

            # 캐시 저장
            await self.cache.set(cache_key, response)

            return response
        except ProviderError as e:
            # Fallback
            return await self.fallback_generate(prompt, schema, **kwargs)

    def get_provider(self, model: str) -> LLMProvider:
        if model.startswith("gpt"):
            return self.providers["openai"]
        elif model.startswith("claude"):
            return self.providers["anthropic"]
        raise ValueError(f"Unknown model: {model}")
```

### 4.3 데이터베이스 스키마

```sql
-- 프로젝트 견적 요청
CREATE TABLE estimation_requests (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- 문서 정보
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    request_id UUID REFERENCES estimation_requests(id),
    file_name VARCHAR(255),
    file_type VARCHAR(50),
    file_size INTEGER,
    storage_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 추출 결과
CREATE TABLE extraction_results (
    id UUID PRIMARY KEY,
    request_id UUID REFERENCES estimation_requests(id),
    extracted_data JSONB,
    ontology_mapped JSONB,
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 전문가 분석 결과
CREATE TABLE expert_analyses (
    id UUID PRIMARY KEY,
    request_id UUID REFERENCES estimation_requests(id),
    expert_type VARCHAR(50),  -- TECHNICAL, ECONOMIC, BUSINESS
    analysis_result JSONB,
    rag_references JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 최종 견적 결과
CREATE TABLE estimation_results (
    id UUID PRIMARY KEY,
    request_id UUID REFERENCES estimation_requests(id),
    final_price DECIMAL(15, 2),
    price_range_min DECIMAL(15, 2),
    price_range_max DECIMAL(15, 2),
    price_breakdown JSONB,
    confidence FLOAT,
    explanation TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 피드백
CREATE TABLE feedbacks (
    id UUID PRIMARY KEY,
    request_id UUID REFERENCES estimation_requests(id),
    feedback_type VARCHAR(50),  -- CONTRACT, USER, EXPERT
    feedback_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 의사결정 트레이스
CREATE TABLE decision_traces (
    id UUID PRIMARY KEY,
    request_id UUID REFERENCES estimation_requests(id),
    trace_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 5. 배포 아키텍처

### 5.1 Kubernetes 구성

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pricing-orchestrator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pricing-orchestrator
  template:
    metadata:
      labels:
        app: pricing-orchestrator
    spec:
      containers:
        - name: orchestrator
          image: pricing-system/orchestrator:latest
          ports:
            - containerPort: 8000
          resources:
            requests:
              memory: "512Mi"
              cpu: "500m"
            limits:
              memory: "2Gi"
              cpu: "2000m"
          env:
            - name: LLM_API_KEY
              valueFrom:
                secretKeyRef:
                  name: llm-secrets
                  key: api-key
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: pricing-orchestrator-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pricing-orchestrator
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

### 5.2 서비스 구성

```
┌─────────────────────────────────────────────────────────────────┐
│                        Production Cluster                        │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Ingress Controller                     │   │
│  │                  (NGINX / AWS ALB)                        │   │
│  └─────────────────────────┬────────────────────────────────┘   │
│                            │                                     │
│  ┌─────────────────────────┼────────────────────────────────┐   │
│  │                  Service Mesh (Istio)                     │   │
│  │                                                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │   │
│  │  │ Orchestrator │  │  Document   │  │  Analysis   │       │   │
│  │  │   Service   │  │   Service   │  │   Service   │       │   │
│  │  │  (3 pods)   │  │  (2 pods)   │  │  (3 pods)   │       │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │   │
│  │                                                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │   │
│  │  │  Synthesis  │  │  Evaluation │  │     RAG     │       │   │
│  │  │   Service   │  │   Service   │  │   Service   │       │   │
│  │  │  (2 pods)   │  │  (2 pods)   │  │  (2 pods)   │       │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │   │
│  │                                                           │   │
│  └───────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                     Data Layer                            │   │
│  │                                                           │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │   │
│  │  │PostgreSQL│  │  Redis  │  │Pinecone │  │   S3    │     │   │
│  │  │ (RDS)   │  │ Cluster │  │ (SaaS)  │  │         │     │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. 보안 아키텍처

### 6.1 보안 레이어

```yaml
SecurityLayers:
  Network:
    - VPC 격리
    - Private Subnet for services
    - WAF for API Gateway
    - DDoS Protection

  Authentication:
    - JWT 토큰 기반
    - OAuth 2.0 지원
    - API Key for B2B

  Authorization:
    - RBAC (Role-Based Access Control)
    - Resource-level permissions

  DataProtection:
    - Encryption at rest (AES-256)
    - Encryption in transit (TLS 1.3)
    - PII masking in logs

  Secrets:
    - AWS Secrets Manager
    - Kubernetes Secrets (encrypted)
    - Rotation policy
```

### 6.2 데이터 보안

```python
class DataSecurityService:
    """
    데이터 보안 서비스
    """
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.encryptor = AESEncryptor(config.encryption_key)

    def encrypt_document(self, document: bytes) -> bytes:
        """문서 암호화"""
        return self.encryptor.encrypt(document)

    def mask_pii(self, text: str) -> str:
        """PII 마스킹"""
        patterns = {
            "phone": r'\d{2,3}-\d{3,4}-\d{4}',
            "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "rrn": r'\d{6}-\d{7}'
        }
        masked = text
        for name, pattern in patterns.items():
            masked = re.sub(pattern, f'[MASKED_{name.upper()}]', masked)
        return masked

    def audit_log(self, action: str, user_id: str, resource: str):
        """감사 로그"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "user_id": user_id,
            "resource": resource,
            "ip_address": get_client_ip()
        }
        self.audit_logger.log(log_entry)
```

---

## 7. 모니터링 및 운영

### 7.1 메트릭 정의

```yaml
Metrics:
  Business:
    - estimation_requests_total: "총 견적 요청 수"
    - estimation_success_rate: "견적 성공률"
    - average_processing_time: "평균 처리 시간"
    - accuracy_mape: "가격 정확도 (MAPE)"

  Technical:
    - request_latency_p50: "요청 지연 시간 (p50)"
    - request_latency_p99: "요청 지연 시간 (p99)"
    - llm_call_count: "LLM 호출 횟수"
    - llm_token_usage: "LLM 토큰 사용량"
    - rag_retrieval_time: "RAG 검색 시간"

  Infrastructure:
    - cpu_utilization: "CPU 사용률"
    - memory_utilization: "메모리 사용률"
    - db_connection_pool: "DB 커넥션 풀"
    - cache_hit_rate: "캐시 히트율"
```

### 7.2 알림 규칙

```yaml
AlertRules:
  - name: HighErrorRate
    condition: "error_rate > 5%"
    duration: "5m"
    severity: critical
    notification: pagerduty

  - name: HighLatency
    condition: "p99_latency > 30s"
    duration: "10m"
    severity: warning
    notification: slack

  - name: LLMQuotaWarning
    condition: "llm_daily_tokens > 80% of quota"
    severity: warning
    notification: email

  - name: AccuracyDegradation
    condition: "weekly_mape > 20%"
    severity: warning
    notification: email
```

---

## 8. 단계별 구현 로드맵

### 8.1 Phase 구분

```
Phase 1: Foundation (MVP)
├── Document Service (기본 파싱)
├── Technical Agent (단독)
├── Simple Cost Calculator
└── Basic API

Phase 2: Multi-Agent
├── Economic Agent
├── Business Agent
├── Conflict Resolution (기본)
└── Enhanced Explanation

Phase 3: RAG Integration
├── Vector DB 구축
├── Knowledge Base 구축
├── RAG 통합
└── 근거 기반 설명

Phase 4: Evaluation & Optimization
├── Feedback Collection
├── Accuracy Measurement
├── Auto-tuning
└── Dashboard

Phase 5: Production Ready
├── Security Hardening
├── Performance Optimization
├── Monitoring Complete
└── Documentation
```

### 8.2 기술 의존성

```
┌─────────────────────────────────────────────────────────────────┐
│                         Phase 5                                  │
│  Security, Performance, Monitoring                               │
└─────────────────────────────┬───────────────────────────────────┘
                              │ depends on
┌─────────────────────────────▼───────────────────────────────────┐
│                         Phase 4                                  │
│  Evaluation Framework                                            │
└─────────────────────────────┬───────────────────────────────────┘
                              │ depends on
┌─────────────────────────────▼───────────────────────────────────┐
│                         Phase 3                                  │
│  RAG Integration                                                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │ depends on
┌─────────────────────────────▼───────────────────────────────────┐
│                         Phase 2                                  │
│  Multi-Agent System                                              │
└─────────────────────────────┬───────────────────────────────────┘
                              │ depends on
┌─────────────────────────────▼───────────────────────────────────┐
│                         Phase 1                                  │
│  Foundation (MVP)                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. 리스크 및 완화 전략

### 9.1 기술 리스크

| 리스크 | 영향 | 확률 | 완화 전략 |
|--------|------|------|----------|
| LLM API 장애 | 높음 | 중 | 다중 provider, 폴백 로직 |
| 정확도 미달 | 높음 | 중 | 지속적 평가, 피드백 반영 |
| 확장성 한계 | 중 | 낮 | 비동기 처리, 캐싱 |
| 데이터 품질 | 중 | 중 | 검증 강화, 사용자 확인 |

### 9.2 운영 리스크

| 리스크 | 영향 | 확률 | 완화 전략 |
|--------|------|------|----------|
| 비용 초과 | 중 | 중 | 사용량 모니터링, 최적화 |
| 보안 사고 | 높음 | 낮 | 보안 감사, 침투 테스트 |
| 인력 이탈 | 중 | 중 | 문서화, 지식 공유 |

---

## 문서 정보

- **작성일**: 2026-02-26
- **상태**: Phase 11 완료
- **버전**: 1.0
- **전체 설계 완료**
