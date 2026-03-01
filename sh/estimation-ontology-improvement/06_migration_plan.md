# 06. Migration Plan

## 1) 현재 자산

- 문서 온톨로지: `docs/ontology/*.md`
- 매핑 코드: `src/schema/ontology_mapping.py`
- 데이터: `data/**/*.jsonl`

## 2) 목표 상태

- OWL/Turtle 기반 스키마
- SHACL 자동 검증
- JSON-LD 입출력 표준화
- QuoteVersion + Provenance 중심 운영

## 3) 단계별 이행

### Phase 1 (1~2주)

- v3 namespace 확정
- 기존 클래스 -> 신규 클래스 매핑표 작성
- `ontology_v3_core.ttl` 도입

### Phase 2 (3~4주)

- `ontology_mapping.py` 출력에 JSON-LD 컨텍스트 반영
- `quote:QuoteVersion`, `quote:EstimateRange` 생성 로직 추가

### Phase 3 (5~6주)

- SHACL 배치 검증 파이프라인 연결
- 오류코드 계약(API) 적용

### Phase 4 (7~8주)

- 운영 데이터 이관
- 회귀검증: 기존 견적 대비 오차 및 신뢰구간 비교
- 릴리즈 기준 수립

## 4) 리스크 및 대응

- 리스크: 기존 데이터 누락필드 다수
- 대응: Hard/Soft 검증 분리로 단계적 엄격화

- 리스크: 정책/단가 업데이트 주기 불일치
- 대응: 버전 엔티티와 유효기간 필수화

- 리스크: 팀 학습비용 증가
- 대응: Mermaid 관계도 + 샘플 JSON-LD + 에러코드 문서 동시 제공

## 5) Definition of Done

- 새 견적은 모두 `QuoteVersion`을 생성한다
- 모든 견적은 `prov:wasDerivedFrom` 최소 1개를 갖는다
- SHACL Hard rule 100% 통과 시에만 결과 배포한다

