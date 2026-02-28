# MVP 데이터 수집 계획: 중소기업 견적산정

---

## 1. 프로젝트 개요

### 1.1 목표
- Core Ontology 구조를 기반으로 중소기업 SW프로젝트 견적산정용 RAG 시스템 데이터 수집
- 공공 입찰 정보(나라장터)를 크롤링하여 Cost + Project + Pricing 데이터 확보

### 1.2 핵심 설정

| 항목 | 결정 |
|------|------|
| 활용 목적 | RAG 시스템 구축 |
| 데이터 출처 | 나라장터 공공 입찰 정보 크롤링 |
| 크롤링 범위 | SW개발/SI 전체 |
| 저장 형식 | JSONL (라인별 JSON) |

### 1.3 관련 문서

| 문서 | 경로 | 설명 |
|------|------|------|
| Core Ontology v2 | `docs/04_ontology/core_v2.md` | Activity 기반 범용 구조 |
| Cost Ontology | `docs/04_ontology/cost.md` | 원가 산정 모델 |
| Pricing Ontology | `docs/04_ontology/pricing.md` | 가격 산정 모델 |
| SW Project Extension | `docs/04_ontology/extensions/software_project.md` | 소프트웨어 프로젝트 확장 |
| 데이터 요구사항 | `docs/04_ontology/data_requirements.md` | 데이터 수집 가이드 |

---

## 2. 수집 대상 데이터

### 2.1 Cost 데이터 (원가 산정 참조)

| 데이터 | 출처 | 우선순위 | 파일 |
|--------|------|----------|------|
| SW기술자 노임단가 (등급별) | KOSA, 과기정통부 | P0 | `data/cost/labor_rates.jsonl` |
| 제경비율 (110~120%) | SW사업 대가산정 가이드 | P0 | `data/cost/indirect_rates.jsonl` |
| 기술료율 (20~40%) | SW사업 대가산정 가이드 | P0 | `data/cost/indirect_rates.jsonl` |
| FP당 단가 | 대가산정 가이드 | P1 | `data/cost/fp_rates.jsonl` |
| 규모별 보정계수 | 대가산정 가이드 | P1 | `data/cost/adjustment_factors.jsonl` |

### 2.2 Project 구조 데이터 (입찰공고에서 추출)

| 데이터 | 온톨로지 매핑 | 우선순위 |
|--------|--------------|----------|
| 사업명/개요 | `SoftwareProject.activityName`, `description` | P0 |
| 예정가격/추정가 | `Cost.amount` | P0 |
| 사업 기간 | `Timeline.totalDuration` | P0 |
| 기능점수(FP) | `Scope.totalFP` | P1 |
| 투입인력 구성 | `Role[]` | P1 |
| 기술스택 요구사항 | `SoftwareProject.techStack` | P2 |

### 2.3 Pricing 데이터 (낙찰정보에서 추출)

| 데이터 | 온톨로지 매핑 | 우선순위 |
|--------|--------------|----------|
| 낙찰가격 | `Revenue.finalPrice` | P0 |
| 낙찰률 | `MarginPolicy.effectiveRate` (역산) | P0 |
| 참여업체 수 | `CompetitiveAdjustment.competitorCount` | P0 |
| 투찰가격 분포 | `CompetitiveAdjustment.priceRange` | P1 |

---

## 3. 데이터 수집 방법

### 3.1 수집 방법 개요

각 데이터 소스별 특성에 맞는 최적의 수집 방법을 적용합니다.

| 수집 방법 | 설명 | 적용 대상 |
|----------|------|----------|
| **공공데이터 API** | 정부/공공기관 OpenAPI 활용 | 나라장터, 공공데이터포털 |
| **공식 Pricing API** | 클라우드 벤더 제공 API | AWS, GCP, Azure |
| **공개 보고서/통계** | 기관 발행 연간 보고서 | 노임단가, 연봉 통계 |
| **수동 입력** | 정형화된 소량 데이터 직접 입력 | 대가산정 가이드, 개발 도구 가격 |
| **크롤링** | 마지막 수단 (API 없는 경우) | - |

### 3.2 나라장터 데이터 (입찰/낙찰 정보)

#### 권장 방법: 공공데이터포털 API

| 항목 | 내용 |
|------|------|
| **방법** | 조달청 공공데이터 API (REST) |
| **출처** | data.go.kr → 조달청 입찰/낙찰 정보 |
| **장점** | 합법적, 안정적, 구조화된 JSON 응답 |
| **API 목록** | |
| - 입찰공고정보 | 조달청_나라장터 입찰공고정보 |
| - 개찰결과정보 | 조달청_나라장터 개찰결과정보 |
| - 낙찰정보 | 조달청_나라장터 낙찰정보 |

```
수집 대상 데이터:
├── 입찰공고
│   ├── 사업 개요 (bidNtceNm, bidNtceDtl)
│   ├── 예정가격 (presmptPrc)
│   ├── 사업 기간 (ntceBgnDt, ntceEndDt)
│   └── 업종 분류 (indstrytyNm)
│
└── 낙찰정보
    ├── 낙찰가격 (sucsfbidAmt)
    ├── 낙찰업체 (sucsfbidCorpNm)
    ├── 투찰현황 (bddprPrtcptCnum)
    └── 낙찰률 (계산: 낙찰가/예정가)
```

#### 수집 흐름 (API 기반)

```
[1] 공공데이터포털 API 인증
    - 서비스 키 발급 (data.go.kr)
    - 일일 호출 제한 확인 (보통 1,000~10,000건/일)

[2] 입찰공고 조회 API 호출
    - 필터: 업종="소프트웨어개발", "정보시스템"
    - 기간: 최근 1~3년

[3] 개찰/낙찰 결과 API 호출
    - 공고번호 기준 매핑

[4] 온톨로지 스키마 변환
    - API 응답 → JSONL 저장

[5] 첨부파일 처리 (선택, 별도 크롤링)
    - RFP PDF → 텍스트 추출
```

#### 백업 방법: 웹 크롤링

> API로 제공되지 않는 상세 정보(첨부파일, 과업지시서 등)가 필요한 경우에만 사용

| 항목 | 내용 |
|------|------|
| **사이트** | g2b.go.kr |
| **주의사항** | robots.txt 준수, 1초/요청 제한 |
| **대상** | 첨부파일(RFP, 과업지시서) 다운로드 |

### 3.3 노임단가 데이터 (핵심 참조 데이터)

#### 권장 방법: 공개 보고서 + 수동 입력

| 출처 | 수집 방법 | 갱신 주기 | 비고 |
|------|----------|----------|------|
| **KOSA SW기술자 평균임금** | PDF 다운로드 → 수동 입력 | 연 1회 (9월) | 공공사업 표준, 4개 등급 |
| **SW사업 대가산정 가이드** | PDF 다운로드 → 수동 입력 | 연 1회 | 과기정통부 발간 |
| **KITA 기술노임단가** | PDF 다운로드 → 수동 입력 | 연 1회 | 기술사 등급 참조용 |

#### 수동 입력 권장 이유

- 연 1회 발표, 데이터 양 적음 (등급별 4~6행)
- PDF 파싱 오류 가능성 > 수동 입력 비용
- 정확성이 핵심인 기준 데이터

#### 민간 시장 연봉 참조

| 출처 | 수집 방법 | 비고 |
|------|----------|------|
| **사람인 연봉 리포트** | 연간 보고서 PDF 활용 | saramin.co.kr/hr-report |
| **원티드 인사이트** | 공개 통계 페이지 | wanted.co.kr/insight |
| **로버트월터스 연봉조사** | 연간 리포트 PDF | 글로벌 기준 참고 |
| **JobKorea 연봉 통계** | 공개 통계 활용 | jobkorea.co.kr |

> ⚠️ **크롤링 지양**: 채용 플랫폼 직접 크롤링은 ToS 위반 가능. 공개 보고서/통계 활용 권장

### 3.4 클라우드 인프라비

#### 권장 방법: 공식 Pricing API

| 벤더 | API | 특징 |
|------|-----|------|
| **AWS** | AWS Price List API | 실시간 가격, JSON/CSV |
| **GCP** | Cloud Billing Catalog API | SKU 기반 가격 조회 |
| **Azure** | Retail Prices API | REST API, 인증 불필요 |
| **NCloud** | 공식 API 없음 | 가격표 페이지 참조 |

#### AWS Price List API 예시

```python
# AWS Price List API 활용
import boto3

client = boto3.client('pricing', region_name='us-east-1')
response = client.get_products(
    ServiceCode='AmazonEC2',
    Filters=[
        {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': 't3.medium'},
        {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': 'Asia Pacific (Seoul)'}
    ]
)
```

#### 수집 대상 가격 정보

| 서비스 유형 | 수집 항목 | 저장 위치 |
|------------|----------|----------|
| 컴퓨팅 | EC2/VM 인스턴스별 시간당 가격 | `data/cost/cloud_compute.jsonl` |
| 스토리지 | S3/GCS/Blob GB당 가격 | `data/cost/cloud_storage.jsonl` |
| 데이터베이스 | RDS/CloudSQL 인스턴스 가격 | `data/cost/cloud_database.jsonl` |
| 네트워크 | 데이터 전송 GB당 가격 | `data/cost/cloud_network.jsonl` |

### 3.5 개발 도구 및 SaaS 가격

#### 권장 방법: 수동 입력 + 주기적 검토

| 카테고리 | 도구 | 가격 유형 | 수집 방법 |
|----------|------|----------|----------|
| IDE | IntelliJ, WebStorm | 월/연 구독 | 공식 사이트 확인, 수동 입력 |
| CI/CD | GitHub Actions | 사용량/분 | 공식 가격표 수동 입력 |
| 협업 | Jira, Confluence | 사용자/월 | 공식 가격표 수동 입력 |
| 디자인 | Figma | 사용자/월 | 공식 가격표 수동 입력 |
| 모니터링 | Datadog | 호스트/월 | 공식 가격표 수동 입력 |

#### 수동 입력 권장 이유

- 가격 변동 빈도 낮음 (분기/연 단위)
- API 제공하지 않는 경우 다수
- 데이터 양 적음 (도구당 3~5개 플랜)

#### 저장 스키마

```json
{"type":"tool_price","category":"IDE","name":"IntelliJ IDEA Ultimate","plan":"Annual","price":599,"currency":"USD","unit":"user/year","source":"jetbrains.com","updatedAt":"2026-02-28"}
```

### 3.6 대가산정 기준 (제경비율, 기술료 등)

#### 권장 방법: 수동 입력

| 출처 | 데이터 | 수집 방법 |
|------|--------|----------|
| **SW사업 대가산정 가이드** | 제경비율, 기술료율, FP단가 | PDF에서 수동 추출 |
| **기업회계기준** | 일반관리비율 | 공식 문서 참조 |
| **조달청 원가계산 기준** | 보정계수, 적용률 | 공식 문서 참조 |

#### 수동 입력 대상 (연 1회 갱신)

- 제경비율: 110~120%
- 기술료율: 20~40%
- 일반관리비율: 6%
- FP당 단가 (개발유형별)
- 규모별/난이도별 보정계수

### 3.7 외부비용 (감리, 인증, 교육 등)

#### 권장 방법: 공공데이터 + 업계 가이드라인

| 유형 | 수집 방법 | 출처 |
|------|----------|------|
| **감리비** | 공공데이터 API | 정보시스템감리 대가기준 (NIA) |
| **ISMS 인증** | 수동 입력 | KISA 인증 안내 |
| **교육비** | 수동 입력 | 교육기관 공개 가격표 |
| **외주 개발** | 업계 참조 | 노임단가 기반 추정 |

> 💡 **외부비용 추정 방식**: 실제 견적 수집은 비현실적. 노임단가 기반 추정값 또는 공공 기준 활용

### 3.8 데이터 수집 우선순위 정리

| 우선순위 | 데이터 | 수집 방법 | 난이도 | 비고 |
|---------|--------|----------|--------|------|
| **P0** | 나라장터 입찰/낙찰 | 공공데이터 API | 중 | API 키 필요 |
| **P0** | KOSA 노임단가 | 수동 입력 | 하 | 연 1회, 소량 |
| **P0** | 제경비/기술료율 | 수동 입력 | 하 | 연 1회, 소량 |
| **P1** | 클라우드 가격 | Pricing API | 중 | AWS/GCP/Azure |
| **P1** | FP당 단가 | 수동 입력 | 하 | 대가산정 가이드 |
| **P2** | 개발 도구 가격 | 수동 입력 | 하 | 분기별 검토 |
| **P2** | 민간 연봉 통계 | 공개 보고서 | 하 | 연간 리포트 |
| **P3** | 감리/인증비 | 공공 기준 | 하 | NIA/KISA 기준 |

---

## 4. JSONL 데이터 스키마

### 4.1 Cost Reference

#### `data/cost/labor_rates.jsonl`
```json
{"type":"labor_rate","grade":"특급","gradeCode":"EXPERT","monthlyRate":12000000,"dailyRate":550000,"hourlyRate":68750,"minExperience":12,"year":2026,"source":"KOSA","sourceUrl":"https://kosa.or.kr"}
{"type":"labor_rate","grade":"고급","gradeCode":"SENIOR","monthlyRate":10000000,"dailyRate":450000,"hourlyRate":56250,"minExperience":7,"year":2026,"source":"KOSA","sourceUrl":"https://kosa.or.kr"}
{"type":"labor_rate","grade":"중급","gradeCode":"MID","monthlyRate":8000000,"dailyRate":360000,"hourlyRate":45000,"minExperience":3,"year":2026,"source":"KOSA","sourceUrl":"https://kosa.or.kr"}
{"type":"labor_rate","grade":"초급","gradeCode":"JUNIOR","monthlyRate":5500000,"dailyRate":250000,"hourlyRate":31250,"minExperience":0,"year":2026,"source":"KOSA","sourceUrl":"https://kosa.or.kr"}
```

#### `data/cost/indirect_rates.jsonl`
```json
{"type":"indirect_rate","category":"제경비","rateType":"overhead","minRate":110,"maxRate":120,"defaultRate":110,"baseOn":"직접인건비","year":2026,"source":"SW사업 대가산정 가이드"}
{"type":"indirect_rate","category":"기술료","rateType":"technicalFee","minRate":20,"maxRate":40,"defaultRate":25,"baseOn":"직접인건비+제경비","year":2026,"source":"SW사업 대가산정 가이드"}
{"type":"indirect_rate","category":"일반관리비","rateType":"adminFee","minRate":6,"maxRate":6,"defaultRate":6,"baseOn":"직접비","year":2026,"source":"기업회계기준"}
```

### 4.2 Project Sample

#### `data/project/g2b_projects.jsonl`
```json
{"bidId":"G2B-2026-001","title":"OO관리시스템 구축","description":"...","scope":{"totalFP":850,"moduleCount":8,"screenCount":45},"timeline":{"duration":6,"unit":"MONTH","startDate":"2026-04-01"},"estimatedPrice":500000000,"category":"WEB_APPLICATION","systemType":"CRM","techStack":["Java","Spring","PostgreSQL"],"source":"나라장터","crawledAt":"2026-02-28T10:00:00Z"}
```

### 4.3 Pricing Data

#### `data/pricing/bid_results.jsonl`
```json
{"bidId":"G2B-2026-001","estimatedPrice":500000000,"winningPrice":450000000,"winningRate":90.0,"competitorCount":5,"bidDate":"2026-01-15","winnerName":"OO시스템(주)","contractType":"협상에의한계약","impliedMargin":10.0}
```

---

## 5. 구현 단계

### Step 1: 참조 데이터 수집 (수동/반자동)
- [x] 폴더 구조 생성
- [ ] 2026년 SW기술자 노임단가표 입력
- [ ] SW사업 대가산정 가이드에서 비율 추출
- [ ] `data/cost/` 폴더에 JSONL로 저장

### Step 2: 나라장터 크롤러 개발
- [ ] 입찰공고 검색 및 목록 수집
- [ ] 상세 페이지 파싱 (사업개요, 금액, 기간)
- [ ] 낙찰정보 수집
- [ ] Rate limiting 및 에러 처리

### Step 3: 데이터 파싱 및 구조화
- [ ] HTML → 온톨로지 필드 매핑
- [ ] JSONL 형식으로 저장
- [ ] 데이터 검증 스크립트

### Step 4: RAG 준비
- [ ] JSONL 데이터 검토 및 정제
- [ ] 메타데이터 보강
- [ ] 벡터 임베딩 (선택)

---

## 6. 산출물 구조

```
ontology-data-beta/
├── docs/
│   └── data-project/
│       └── planning.md          # 이 계획 문서
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

## 7. 온톨로지 연계

### 7.1 Core Ontology 매핑

| 수집 데이터 | Core Ontology | Extension | 비고 |
|------------|---------------|-----------|------|
| 사업 정보 | Activity → Project | SoftwareProject | activityType: PROJECT |
| 금액 정보 | Cost | ProjectCost | costType별 분리 |
| 기간/일정 | Timeline | Phase, Milestone | phaseType 매핑 |
| 인력 구성 | Resource | Role | roleType, skillLevel |
| 낙찰 결과 | Revenue | Pricing | finalPrice |

### 7.1.1 Project 상속 구조 (Activity 기반)

```mermaid
classDiagram
    %% ═══════════════════════════════════════════════
    %% Core Ontology: Activity (Abstract)
    %% ═══════════════════════════════════════════════
    class Activity {
        <<abstract>>
        +String activityId
        +String activityName
        +ActivityType activityType
        +ActivityStatus status
        +Date startDate
        +Date endDate
        +String description
        +Visibility visibility
        +DateTime createdAt
        +DateTime updatedAt
    }

    %% ═══════════════════════════════════════════════
    %% Domain Ontology: Project
    %% ═══════════════════════════════════════════════
    class Project {
        +ProjectType projectType
        +Deliverable[] deliverables
        +Milestone[] milestones
        +ComplexityLevel complexity
    }

    %% ═══════════════════════════════════════════════
    %% 상속 관계
    %% ═══════════════════════════════════════════════
    Activity <|-- Project

    %% ═══════════════════════════════════════════════
    %% Enum 정의
    %% ═══════════════════════════════════════════════
    class ProjectType {
        <<enumeration>>
        NEW_DEVELOPMENT
        ENHANCEMENT
        MIGRATION
        INTEGRATION
        MAINTENANCE
        POC
        MVP
    }

    Project --> ProjectType

    %% ═══════════════════════════════════════════════
    %% Project 고유 관계 (domain.md)
    %% ═══════════════════════════════════════════════
    class Scope {
        +String scopeId
    }
    class Feature {
        +String featureId
    }
    class Timeline {
        +Date start
        +Date end
    }
    class Role {
        +String roleId
    }
    class Deliverable {
        +String deliverableId
    }

    Project "1" --> "1" Scope : hasScope
    Project "1" --> "*" Feature : hasFeature
    Project "1" --> "1" Timeline : hasTimeline
    Project "1" --> "*" Role : requiresRole

    %% ═══════════════════════════════════════════════
    %% Cost & Pricing 확장 (domain.md)
    %% ═══════════════════════════════════════════════
    class ActivityCost {
        <<abstract>>
        +String costId
        +Money totalCost
    }

    class ProjectCost {
        +Money laborCost
        +Money infrastructureCost
        +Money toolCost
        +Money externalCost
        +Money overhead
        +Money technicalFee
    }

    ActivityCost <|-- ProjectCost
    Project --> ProjectCost

    class ActivityPricing {
        <<abstract>>
        +String pricingId
        +PricingModel pricingModel
        +Money finalPrice
    }

    class ProjectPricing {
        +FIXED_PRICE
        +TIME_AND_MATERIAL
        +MILESTONE_BASED
    }

    ActivityPricing <|-- ProjectPricing
    ProjectCost --> ProjectPricing
```

### 7.2 Pricing Ontology 연계

| 수집 데이터 | Pricing 필드 | 활용 |
|------------|-------------|------|
| 낙찰률 | MarginPolicy.effectiveRate | 실제 마진율 역산 |
| 경쟁업체 수 | CompetitiveAdjustment.competitorCount | 경쟁 수준 분석 |
| 예정가-낙찰가 | PriceRange | 협상 범위 참고 |
| 계약 유형 | Contract.contractType | 가격 전략 참고 |

### 7.3 데이터 흐름

```
[입찰공고] ────────────────────────────────────────────┐
    │                                                   │
    ├── 사업명 → SoftwareProject.activityName          │
    ├── 예정가격 → Cost.baseCost                        │
    ├── 기간 → Timeline.totalDuration                   │
    └── RFP → Scope, Feature, Role (파싱 시)           │
                                                        │
[낙찰정보] ────────────────────────────────────────────┤
    │                                                   │
    ├── 낙찰가 → Revenue.finalPrice                     │
    ├── 낙찰률 → MarginPolicy 분석                      ├──► RAG System
    ├── 경쟁사 수 → CompetitiveAdjustment              │
    └── 투찰 분포 → PriceRange                          │
                                                        │
[참조 데이터] ──────────────────────────────────────────┘
    │
    ├── 노임단가 → LaborCost.unitCost
    ├── 제경비율 → IndirectCost.rate
    └── FP단가 → Scope 기반 비용 산정
```

---

## 8. 주의사항

### 8.1 법적 사항
- 나라장터는 공공데이터로 활용 가능 (공공데이터 개방 정책)
- 로봇 배제 표준(robots.txt) 확인 및 준수
- 과도한 요청 방지: 1초당 1요청 이하 권장

### 8.2 데이터 품질
- **중복 제거**: bidId 기준 유니크 보장
- **결측값 처리**: FP 정보 없는 경우 `null` 또는 추정값 표시
- **버전 관리**: 연도별 노임단가 등 시계열 데이터 관리

### 8.3 개인정보
- 입찰 참여 업체명: 공개 정보로 수집 가능
- 담당자 연락처: 수집하지 않음
- 낙찰 업체 정보: 공개 범위 내 수집

---

## 문서 정보

- **작성일**: 2026-02-28
- **버전**: 1.0
- **상태**: 구현 진행 중
- **관련 문서**:
  - `docs/04_ontology/core_v2.md`
  - `docs/04_ontology/data_requirements.md`
