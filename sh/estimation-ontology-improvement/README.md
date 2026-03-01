# Estimation Ontology Improvement Pack

- 작성일: 2026-03-01
- 대상: 프로젝트 요구사항 입력 기반 SW 견적 산정 AI
- 목적: 엔지니어 공유용 설계 패키지 (의도, 스키마, 관계도, 검증, 이행)

## 문서 구성

1. `01_design_intent.md`
- 왜 이 구조가 필요한지, 어떤 실패를 줄이는지 설명

2. `02_schema_catalog.md`
- 모듈, 클래스, 핵심 속성, 관계 정의

3. `03_relationship_diagrams.md`
- Context/Class/Flow 관계도 (Mermaid)

4. `04_validation_and_reasoning.md`
- SHACL 검증 규칙, 추론 규칙, 오류 처리 정책

5. `05_data_contract_and_examples.md`
- JSON-LD 데이터 계약, API 입력/출력 최소 필드, 샘플

6. `06_migration_plan.md`
- 기존 `docs/ontology` + `src/schema` 기준 점진 전환 계획

7. `07_minimal_ontology_15_confirmed.md`
- 운영용 최소 온톨로지 15개 클래스 확정본

## 스키마 파일

- `schemas/ontology_v3_core.ttl`: v3 핵심 OWL/RDFS 스키마
- `schemas/ontology_v3_minimal_15.ttl`: 확정 15개 클래스 최소 스키마
- `schemas/ontology_v3_shapes.ttl`: SHACL 검증 규칙
- `schemas/context.json`: JSON-LD 컨텍스트

## 예제 파일

- `examples/sample_estimate_scenario.jsonld`: 요구사항 -> 견적 시나리오 예시

## 빠른 읽기 순서

1. `01_design_intent.md`
2. `03_relationship_diagrams.md`
3. `02_schema_catalog.md`
4. `04_validation_and_reasoning.md`
5. `07_minimal_ontology_15_confirmed.md`
6. `06_migration_plan.md`
