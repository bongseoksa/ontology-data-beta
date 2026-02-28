# AI 기반 프로젝트 가격산정 시스템 요약 정리

---

# 1. 프로젝트 목적

중소기업 대표가 업로드한 사업계획서를 분석하여
프로젝트 구조를 도출하고 최종 가격을 자동 산정하는
의사결정 지원 시스템을 구축한다.

이 시스템은 단순 견적 계산기가 아니라
문서 이해 + 구조화 + 다중 전문가 판단 + 계산 엔진이 결합된
지능형 가격 산정 엔진이다.

---

# 2. 문제 구조 정의

입력(Input)

* 사업계획서 (비정형 문서)

중간 처리(Process)

1. 문서 분석
2. 프로젝트 구조화
3. 다중 전문가 분석
4. 원가 계산
5. 전략적 가격 조정

출력(Output)

* 최종 가격
* 가격 산정 근거
* 리스크 및 전략 설명

---

# 3. 도메인 범위

산업 범위

* 소프트웨어 산업 한정

계약 유형 범위

* 프로젝트 기반 계약
* 입찰 기반 계약
* (2단계 확장) 정부 과제

제외 범위

* 순수 SaaS 구독 전략
* 타 산업(건설, 제조 등)

---

# 4. 온톨로지 구조

## 4.1 Core Ontology (공통 개념)

* Project
* Cost
* Revenue
* Contract
* Resource
* Risk

## 4.2 Project Ontology

* Scope
* Feature
* Timeline
* Role
* Complexity
* Dependency

## 4.3 Cost Ontology

* LaborCost
* InfrastructureCost
* ToolCost
* IndirectCost
* ExternalCost

## 4.4 Pricing Ontology

* MarginPolicy
* RiskPremium
* CompetitiveAdjustment
* StrategicWeight

산업 확장은 상위 온톨로지를 추가하는 방식이 아니라
Core를 유지한 채 도메인 확장 구조로 진행한다.

---

# 5. 전체 시스템 아키텍처

사업계획서
→ Document Understanding Layer
→ Ontology Mapping Layer
→ Multi-Agent Reasoning Layer
→ Cost Engine
→ Pricing Engine
→ Reporting Layer

---

# 6. Multi-Agent 구조

## 6.1 기술 전문가

역할

* 기능 분해
* 난이도 평가
* 인력 구성 추정
* 기간 추정

출력

* 인력 수
* 개발 기간
* 복잡도 점수

---

## 6.2 사업 전문가

역할

* 시장성 평가
* 경쟁 상황 판단
* 전략 가중치 설정
* 할인 가능 범위 제안

출력

* 전략 가중치
* 경쟁 강도
* 협상 범위

---

## 6.3 경제 전문가

역할

* 원가 계산
* 손익분기점 계산
* 마진 제안
* 리스크 프리미엄 반영

출력

* Base Cost
* Break-even Price
* Recommended Margin

---

# 7. 가격 계산 구조

Base Cost =
(Resource × Duration × Unit Cost)

* Overhead
* External Cost

Final Price =
Base Cost
× (1 + Margin)
× (1 + Risk Premium)
× Strategic Adjustment

최종 통합은 규칙 기반 계산 엔진이 담당하며,
LLM은 판단 및 설명 생성에 활용된다.

---

# 8. RAG 활용 구조

RAG는 가격 계산을 수행하지 않는다.
전문가 판단의 근거 보강에 사용된다.

활용 영역

* 유사 프로젝트 사례 검색
* 평균 단가 참고
* 산업 벤치마크 조회
* 리스크 사례 참고

---

# 9. 실행 단계 요약

1. 프로젝트 목표 확정
2. 도메인 범위 정의
3. Core Ontology 설계
4. Project / Cost / Pricing Ontology 설계
5. 전문가 역할 및 출력 스키마 확정
6. 가격 계산 공식 정의
7. 문서 분석 프로토타입 구현
8. RAG 연동
9. 통합 검증
10. 제품화

---

# 최종 정의

이 시스템은
문서를 입력받아 구조화하고,
다중 전문가 시뮬레이션을 거쳐
정량적 계산 엔진으로 가격을 도출하는

AI 기반 의사결정 자동화 시스템이다.
