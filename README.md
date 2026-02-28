# Ontology Data Beta

중소기업 SW 프로젝트 견적산정을 위한 온톨로지 기반 데이터 수집 및 RAG 시스템 구축 프로젝트입니다.

---

## 프로젝트 개요

### 목표
- Core Ontology 구조를 기반으로 중소기업 SW 프로젝트 견적산정용 RAG 시스템 데이터 수집
- 공공 입찰 정보(나라장터)를 크롤링하여 Cost + Project + Pricing 데이터 확보

### 핵심 기능
- **원가 산정**: Cost Ontology 기반 인건비, 인프라비, 도구비 등 비용 계산
- **가격 산정**: Pricing Ontology 기반 마진, 리스크 프리미엄, 경쟁 조정 적용
- **데이터 수집**: 나라장터 공공 입찰 정보 크롤링 및 JSONL 형식 저장

---

## 용어 정의

### FP (Function Point, 기능점수)
FP(Function Point, 기능점수) 단가는 소프트웨어(SW) 개발 규모를 기능적 관점에서 측정하여 1 기능점수(1 FP)당 얼마의 비용(개발비)을 투입할 것인지를 정한 객관적인 기준 금액을 의미합니다.

### Activity (활동)
모든 활동의 상위 추상 개념으로, 프로젝트, 스터디, 멘토링, 컨설팅 등 다양한 활동 유형의 공통 속성을 정의합니다. 가격 산정과 운영 관리 모두를 지원하는 Core Ontology의 중심 개념입니다.

### Cost (원가)
활동 수행에 발생하는 모든 비용을 의미합니다. 직접비(인건비, 인프라비, 도구비, 외주비)와 간접비(제경비, 기술료)로 구분됩니다.

### Pricing (가격)
원가(Cost)에서 최종 가격(Price)으로 변환하는 과정에서 적용되는 마진 정책, 리스크 프리미엄, 경쟁 조정, 전략적 가중치를 포함한 가격 산정 체계입니다.

### M/M (Man-Month, 맨먼스)
인력 투입량을 나타내는 단위로, 1명의 인력이 1개월 동안 투입되는 것을 의미합니다.
- **계산식**: M/M = 인원 수 × 투입 기간(월) × (투입률 / 100)

### 노임단가
SW 기술자의 등급별 월/일 급여 기준 단가입니다. KOSA(한국소프트웨어산업협회)에서 매년 9월 발표하며, 공공사업 표준으로 사용됩니다.
- **특급**: 경력 12년 이상
- **고급**: 경력 7~12년
- **중급**: 경력 3~7년
- **초급**: 경력 3년 미만

### 제경비 (Overhead)
직접인건비를 기준으로 산정되는 간접비로, 사무실 임차료, 관리비, 복리후생비 등이 포함됩니다. SW사업 대가산정 가이드 기준 직접인건비의 110~120%를 적용합니다.

### 기술료 (Technical Fee)
기술 개발에 대한 이윤으로, (직접인건비 + 제경비)를 기준으로 20~40%를 적용합니다.

### SI (System Integration)
시스템 통합을 의미하며, 기업의 정보시스템을 설계, 개발, 구축하는 사업을 말합니다.

### RFP (Request for Proposal, 제안요청서)
발주자가 사업자에게 제출하는 문서로, 프로젝트의 목적, 범위, 요구사항, 일정 등을 명시합니다.

### WBS (Work Breakdown Structure, 작업분해구조)
프로젝트의 범위와 산출물을 계층적으로 분해한 구조로, 작업 단위와 일정 계획의 기초가 됩니다.

### JSONL (JSON Lines)
각 라인이 독립적인 JSON 객체로 구성된 파일 형식으로, 대용량 데이터 처리 및 스트리밍에 적합합니다.

### RAG (Retrieval-Augmented Generation)
검색 증강 생성 기술로, 외부 데이터 소스에서 관련 정보를 검색하여 LLM의 응답 생성을 보강하는 방법론입니다.

---

## 문서 구조

| 문서 | 경로 | 설명 |
|------|------|------|
| Core Ontology v2 | `docs/ontology/core.md` | Activity 기반 범용 구조 |
| Cost Ontology | `docs/ontology/cost.md` | 원가 산정 모델 |
| Pricing Ontology | `docs/ontology/pricing.md` | 가격 산정 모델 |
| SW Project Extension | `docs/ontology/software-project.md` | 소프트웨어 프로젝트 확장 |
| 데이터 요구사항 | `docs/ontology/data-requirements.md` | 데이터 수집 가이드 |
| 수집 계획 | `docs/planning.md` | MVP 데이터 수집 계획 |

---

## 프로젝트 구조

```
ontology-data-beta/
├── docs/
│   ├── planning.md              # MVP 데이터 수집 계획
│   └── ontology/
│       ├── core.md              # Core Ontology v2
│       ├── cost.md              # Cost Ontology
│       ├── pricing.md           # Pricing Ontology
│       ├── software-project.md  # SW Project Extension
│       └── data-requirements.md # 데이터 요구사항
│
├── data/
│   ├── cost/
│   │   ├── labor_rates.jsonl    # 노임단가
│   │   ├── indirect_rates.jsonl # 제경비/기술료율
│   │   ├── fp_rates.jsonl       # FP당 단가
│   │   └── adjustment_factors.jsonl # 보정계수
│   │
│   ├── project/
│   │   └── g2b_projects.jsonl   # 프로젝트 구조 샘플
│   │
│   └── pricing/
│       └── bid_results.jsonl    # 입찰/낙찰 정보
│
└── src/
    ├── crawler/
    │   └── g2b_crawler.py       # 나라장터 크롤러
    ├── parser/
    │   └── bid_parser.py        # 입찰공고 파서
    └── schema/
        └── ontology_mapping.py  # 온톨로지 매핑
```

---

## 수집 데이터

### Cost 데이터 (원가 산정 참조)

| 데이터 | 출처 | 우선순위 |
|--------|------|----------|
| SW기술자 노임단가 (등급별) | KOSA, 과기정통부 | P0 |
| 제경비율 (110~120%) | SW사업 대가산정 가이드 | P0 |
| 기술료율 (20~40%) | SW사업 대가산정 가이드 | P0 |
| FP당 단가 | 대가산정 가이드 | P1 |
| 규모별 보정계수 | 대가산정 가이드 | P1 |

### Project 구조 데이터 (입찰공고에서 추출)

| 데이터 | 온톨로지 매핑 | 우선순위 |
|--------|--------------|----------|
| 사업명/개요 | `SoftwareProject.activityName` | P0 |
| 예정가격/추정가 | `Cost.amount` | P0 |
| 사업 기간 | `Timeline.totalDuration` | P0 |
| 기능점수(FP) | `Scope.totalFP` | P1 |
| 투입인력 구성 | `Role[]` | P1 |

### Pricing 데이터 (낙찰정보에서 추출)

| 데이터 | 온톨로지 매핑 | 우선순위 |
|--------|--------------|----------|
| 낙찰가격 | `Revenue.finalPrice` | P0 |
| 낙찰률 | `MarginPolicy.effectiveRate` | P0 |
| 참여업체 수 | `CompetitiveAdjustment.competitorCount` | P0 |

---

## 견적 산정 흐름

```
[입력 데이터]          [산정 엔진]           [출력]

사업계획서 ────┐
요구사항 ──────┼────► Cost Ontology ──► 원가 산정
범위/규모 ─────┘      (인건비, 인프라비 등)    │
                                              ▼
마진 정책 ─────┐
리스크 평가 ───┼────► Pricing Ontology ──► 최종 견적
경쟁 상황 ─────┘      (마진, 리스크 프리미엄)
```

### 가격 계산 공식

```
최종가격 = 원가 × (1 + 마진율) × (1 + 리스크프리미엄) × 경쟁조정계수 × 전략가중치
```

---

## 참고 자료

- [KOSA SW기술자 평균임금](https://kosa.or.kr)
- [SW사업 대가산정 가이드](https://www.msit.go.kr)
- [나라장터 (G2B)](https://g2b.go.kr)
- [공공데이터포털](https://data.go.kr)

---

## 라이선스

이 프로젝트는 비공개입니다.

---

## 문서 정보

- **작성일**: 2026-02-28
- **버전**: 1.0
