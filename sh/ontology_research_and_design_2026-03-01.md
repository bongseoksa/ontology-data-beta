# 프로젝트 견적 AI를 위한 온톨로지 설계 조사 보고서

- 작성일: 2026-03-01
- 대상 저장소: `/home/lsh/dev/ontology-data-beta`
- 목적: "요구사항 입력 -> 소프트웨어 프로젝트 견적 산정 AI"를 위한 온톨로지 구조 제안
- 작성 원칙: 기존 코드와 분리된 리서치 산출물로 작성 (`sh/` 폴더)

---

## 1) 현재 프로젝트 진단 (요약)

현재 저장소는 아래 강점이 있습니다.

- `Core/Cost/Pricing/SoftwareProject`로 온톨로지 개념 분리 완료
- 공공 입찰 데이터(G2B) 수집 -> JSONL 매핑 파이프라인 존재
- 가격 산정 공식(원가 x 마진 x 리스크 x 경쟁/전략 보정)이 명시적

반면, "견적 AI" 관점에서 다음 공백이 큽니다.

- 형식 의미론 부재: 문서가 YAML/텍스트 정의 중심이며 RDF/OWL/SHACL 기반 검증 체계가 없음
- 근거 추적 부재: 산정값이 어떤 문서/데이터/규칙에서 도출되었는지 provenance 모델이 약함
- 불확실성 모델 부재: 단일 점추정 중심, 신뢰구간/확률분포/민감도 분석 구조 미흡
- 요구사항 품질 모델 부재: 요구사항의 명확성/완전성/변경가능성 같은 속성이 독립 모델로 분리되지 않음
- 캘리브레이션 체계 부재: 과거 실적 기반 보정(업종/규모/기술스택별 생산성 계수) 저장·버전관리 구조가 없음

결론: 현재 구조는 "정적 계산 모델"에는 유효하나, "설명가능하고 업데이트 가능한 견적 AI"에는 지식그래프 계층이 추가되어야 합니다.

---

## 2) 업계 모범사례 조사 결과 (핵심)

### 2.1 요구사항/수명주기/측정 표준

- ISO/IEC/IEEE 29148: 요구사항 공학 프로세스, 좋은 요구사항 특성, 정보항목 정의
- ISO/IEC/IEEE 12207: 소프트웨어 생명주기 프로세스 프레임
- ISO/IEC/IEEE 15288: 시스템 생명주기 프로세스와 정합
- ISO/IEC/IEEE 15939: 측정 프로세스(정보요구 -> 측정정의 -> 분석 -> 개선)
- ISO/IEC 25010: 품질특성 기반 비기능 요구사항 정량화 기준

적용 시사점:
- 온톨로지에 `Requirement`, `QualityAttribute`, `Measure`, `AcceptanceCriteria`를 분리하고, 측정가능성(measurability)을 속성으로 강제해야 합니다.

### 2.2 소프트웨어 견적 모범사례

- GAO Cost Estimating and Assessment Guide (GAO-20-195G): WBS 기반 추정, 가정관리, 민감도/리스크 분석, 추정 업데이트의 12-step 실무
- NASA Cost Estimating Handbook v4.0: WBS/방법론/리스크/불확실성/JCL 관점의 운영형 가이드
- COCOMO II: 초기/상세 단계별 파라메트릭 추정 모델
- ISO/IEC 20926 (IFPUG FP): 기능규모 측정 표준
- ISO/IEC 19761 (COSMIC): 기능규모 측정 표준 (2025 재확인)

적용 시사점:
- 견적 산정은 반드시 `규모(size)`, `생산성(productivity)`, `위험(risk)`, `불확실성(uncertainty)`을 분리 모델링해야 하며,
- 단일 숫자 대신 `P50/P80` 같은 확률 관점 결과를 저장해야 합니다.

### 2.3 온톨로지/지식그래프 표준

- RDF 1.1: 트리플/그래프 데이터 모델
- OWL 2: 온톨로지 표현 및 추론
- SHACL: 데이터 제약 검증
- SPARQL 1.1: 질의
- JSON-LD 1.1: 애플리케이션 JSON과 KG 연계
- PROV-O: 산정 근거/출처/책임 추적
- SKOS: 분류체계/코드체계 관리
- DCAT v3 + DCMI Terms: 데이터셋 메타데이터와 버전·배포 정보

적용 시사점:
- "정의(OWL) + 검증(SHACL) + 추적(PROV-O)" 3축을 함께 도입해야 운영에서 무너지지 않습니다.

### 2.4 한국 공공 SW 문맥 (업데이트 확인)

- `SW사업 대가산정 가이드(2025년 개정판)` 공표 (등록일 2025-08-11)
- `2026년 적용 SW기술자 평균임금(조사년도 2025년)` 공표
- 조달청 나라장터 입찰공고 OpenAPI(`data.go.kr`)는 2025-11-03 수정 이력 확인

적용 시사점:
- 국내 공공견적 대응 시 `기준문서 버전`, `적용연도`, `단가 출처`를 엔티티로 반드시 관리해야 함

---

## 3) 제안 온톨로지 구조 (v3 권고안)

### 3.1 모듈 구조

권장 네임스페이스:

- `base:` 상위 공통 개념
- `req:` 요구사항 온톨로지
- `size:` 규모측정 온톨로지
- `cost:` 원가 온톨로지
- `price:` 가격/전략 온톨로지
- `risk:` 리스크/불확실성 온톨로지
- `quote:` 견적 결과/시나리오 온톨로지
- `prov:` 출처/근거 (W3C PROV-O 재사용)
- `dcat:` 데이터셋 메타데이터 (재사용)

### 3.2 핵심 클래스 (권장 최소 집합)

`base:`
- `base:Project`
- `base:Stakeholder`
- `base:Artifact`
- `base:Assumption`
- `base:Constraint`
- `base:Decision`

`req:`
- `req:RequirementSet`
- `req:Requirement`
- `req:FunctionalRequirement`
- `req:NonFunctionalRequirement`
- `req:QualityAttribute` (ISO 25010 정렬)
- `req:AcceptanceCriterion`
- `req:RequirementChange`

`size:`
- `size:SizeEstimate`
- `size:FunctionPointEstimate` (IFPUG)
- `size:COSMICEstimate`
- `size:SizeDriver`

`cost:`
- `cost:CostEstimate`
- `cost:LaborCost`
- `cost:InfrastructureCost`
- `cost:ToolCost`
- `cost:IndirectCost`
- `cost:RateCard` (연도/출처/적용범위 포함)

`risk:`
- `risk:RiskItem`
- `risk:RiskScore`
- `risk:UncertaintyDistribution`
- `risk:ConfidenceLevel`
- `risk:SensitivityResult`

`price:`
- `price:PricingPolicy`
- `price:MarginPolicy`
- `price:CompetitiveAdjustment`
- `price:StrategicWeight`

`quote:`
- `quote:EstimateScenario`
- `quote:Quote`
- `quote:QuoteVersion`
- `quote:EstimateRange` (min / p50 / p80 / max)
- `quote:Recommendation`

### 3.3 핵심 관계

- `req:Requirement -> size:SizeEstimate` (`req:drivesSize`)
- `size:SizeEstimate -> cost:CostEstimate` (`size:informsCost`)
- `cost:CostEstimate -> price:PricingPolicy` (`price:pricedBy`)
- `risk:RiskScore -> quote:EstimateRange` (`risk:adjustsRange`)
- `quote:QuoteVersion -> prov:Entity` (근거 문서/데이터셋/모델 버전 연결)
- `quote:QuoteVersion -> base:Assumption` (가정 목록)
- `quote:QuoteVersion -> req:RequirementSet` (입력 요구사항 스냅샷)

---

## 4) 설계 원칙 (실행 중심)

1. 분리 원칙
- 요구사항, 규모, 원가, 가격, 리스크, 견적결과를 독립 모듈로 분리

2. 버전 원칙
- `QuoteVersion`, `RateCard`, `PricingPolicy`는 모두 유효기간(`validFrom`, `validTo`) 필수

3. 근거 원칙
- 최종 견적 수치는 모두 `prov:wasDerivedFrom`로 원문 근거 연결

4. 불확실성 원칙
- 단일 값 저장 금지, 최소 `pointEstimate + range + confidence` 저장

5. 검증 원칙
- SHACL로 "필수 입력 누락", "범위 이상치", "연도-단가 불일치"를 자동 검증

---

## 5) SHACL 검증 규칙 예시 (권장)

- 규칙 A: `quote:QuoteVersion`는 반드시 1개 이상의 `prov:wasDerivedFrom` 가져야 함
- 규칙 B: `cost:LaborCost`는 `rateYear`와 `rateSource`가 비어 있으면 invalid
- 규칙 C: `req:NonFunctionalRequirement`가 `Security`면 `risk:RiskItem` 최소 1개 필요
- 규칙 D: `quote:EstimateRange`는 `min <= p50 <= p80 <= max`를 만족해야 함
- 규칙 E: 공공 프로젝트(`clientType=PUBLIC`)는 `pricingPolicy`에 공공 기준 적용근거 필요

---

## 6) 저장/질의 아키텍처 제안

권장 저장 형태:
- 운영 입력/출력: JSON-LD
- 지식 저장소: RDF triple store
- 검증: SHACL 엔진
- 분석 질의: SPARQL + 애플리케이션 레이어 SQL/OLAP 혼합

권장 그래프 분리:
- Graph 1: TBox(온톨로지 스키마)
- Graph 2: ABox(프로젝트/견적 인스턴스)
- Graph 3: Provenance(출처/변환 이력)
- Graph 4: Reference Data(단가표/계수표/분류체계)

---

## 7) 기존 저장소와의 연결 방식

현재 `docs/ontology/*.md` 구조를 즉시 폐기하지 않고 아래 순서로 점진 전환 권장.

1. `docs` 정의를 v3 클래스에 매핑 테이블로 정리
2. `src/schema/ontology_mapping.py` 출력을 JSON-LD 컨텍스트 포함 형태로 확장
3. SHACL 검증을 배치 파이프라인에 추가
4. 견적 결과에 provenance 링크와 시나리오 버전 추가

이 방식이면 기존 JSONL 파이프라인을 유지하면서 지식그래프 기반 정합성을 확보할 수 있습니다.

---

## 8) 8주 실행 로드맵

1주차
- v3 온톨로지 스코프 확정
- 용어사전(SKOS) 초안

2~3주차
- OWL 클래스/속성 정의
- SHACL 규칙 1차 구현

4주차
- 기존 데이터(JSONL) -> JSON-LD 매핑
- provenance 연결

5~6주차
- 견적 엔진 입력/출력 스키마 정합
- 시나리오 버전/P50-P80 저장

7주차
- 회귀 검증(기존 견적 vs v3)
- 예외케이스 정제

8주차
- 운영가이드/데이터 거버넌스 문서화
- 릴리스 기준 확정

---

## 9) 즉시 적용 가능한 우선 과제 (실무 우선순위)

- P0: `QuoteVersion`, `Assumption`, `EvidenceSource` 3개 클래스부터 추가
- P0: 단가표/정책표에 유효기간과 출처 URI 강제
- P1: SHACL로 견적 실패 원인을 사람이 읽을 수 있는 에러로 반환
- P1: 리스크 프리미엄을 단일 퍼센트에서 `요인별 분해` 구조로 전환
- P2: FP + COSMIC 병행 저장 후 도메인별 성능 비교

---

## 10) 조사 출처 (원문 링크)

### 견적/프로세스/측정
- GAO Cost Estimating and Assessment Guide: https://www.gao.gov/products/gao-20-195g
- NASA Cost Estimating Handbook v4.0: https://www.nasa.gov/ocfo/ppc-corner/nasa-cost-estimating-handbook-ceh/
- COCOMO II (Boehm CSSE): https://barryboehm.org/tools/cocomo-ii/
- ISO/IEC/IEEE 29148:2018: https://www.iso.org/standard/72089.html
- ISO/IEC/IEEE 12207:2017: https://www.iso.org/standard/63712.html
- ISO/IEC 25010:2023: https://www.iso.org/standard/78176.html
- ISO/IEC 20926:2009 (IFPUG FP): https://www.iso.org/standard/51717.html
- ISO/IEC 19761:2011 (COSMIC): https://www.iso.org/standard/54849.html
- COSMIC Measurement Manual v5.0: https://cosmic-sizing.org/publications/measurement-manual-v5-0-may-2020-part-2-guidelines/

### 온톨로지/지식그래프/메타데이터
- RDF 1.1 Concepts: https://www.w3.org/TR/rdf11-concepts/
- OWL 2 Overview: https://www.w3.org/TR/owl2-overview/
- SHACL: https://www.w3.org/TR/shacl/
- SPARQL 1.1 Query: https://www.w3.org/TR/sparql11-query/
- JSON-LD 1.1: https://www.w3.org/TR/json-ld11/
- PROV-O: https://www.w3.org/TR/prov-o/
- SKOS Reference: https://www.w3.org/TR/skos-reference/
- DCAT v3: https://www.w3.org/TR/vocab-dcat-3/
- DCMI Metadata Terms: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/

### 한국 공공 SW/데이터
- SW사업 대가산정 가이드(2025년 개정판): https://www.sw.or.kr/site/sw/ex/board/View.do?cbIdx=276&bcIdx=63607
- 2026년 적용 SW기술자 평균임금 공표: https://www.sw.or.kr/site/sw/ex/board/View.do?cbIdx=304&bcIdx=64717
- 조달청 나라장터 입찰공고 OpenAPI: https://www.data.go.kr/data/15129394/openapi.do

---

## 11) 참고 메모

- 본 문서는 "표준 원칙 + 실무 적용" 관점의 설계 제안이며, 상세 클래스/속성 URI와 SHACL shape 파일은 후속 산출물로 분리 생성하는 것이 적절합니다.
- 일부 국제표준 본문은 유료이므로, 본 조사에서는 표준의 공식 abstract/메타데이터와 공개 가이드를 기준으로 설계 원칙을 도출했습니다.

