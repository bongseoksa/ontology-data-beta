# Domain Ontology: 활동 유형별 통합 구조

---

## 1. Domain Ontology 개요

### 1.1 목적
Core Ontology의 `Activity`를 구체적인 활동 유형으로 확장하고,
각 활동 유형별 비용(Cost)과 가격(Pricing) 구조를 통합하여 정의

### 1.2 Core → Domain 확장 구조

```
Core:Activity (core_v2.md)
    └── extends → Domain:ActivityTypes
                      ├── Project (프로젝트)
                      ├── Study (스터디)
                      ├── Mentoring (멘토링)
                      └── Consulting (컨설팅)

Core:Cost
    └── extends → Domain:ActivityCost
                      ├── ProjectCost
                      ├── StudyCost
                      ├── MentoringCost
                      └── ConsultingCost

Core:Revenue
    └── extends → Domain:ActivityPricing
                      ├── ProjectPricing
                      ├── StudyPricing
                      ├── MentoringPricing
                      └── ConsultingPricing
```

### 1.3 통합 원칙
- **공통 구조 추출**: 모든 활동 유형에 적용되는 비용/가격 구조
- **활동별 특화**: 각 활동 유형의 고유한 비용 항목과 가격 모델
- **유연한 확장**: 새로운 활동 유형 추가 시 최소 변경

---

## 2. Activity Types (활동 유형 정의)

### 2.1 Project

```yaml
Class: Project
  Extends: Core:Activity
  Description: |
    목표 달성을 위한 일시적 활동.
    소프트웨어 개발, SI, 외주 프로젝트 등.

  Additional Properties:
    - projectType: ProjectType (enum)
    - deliverables: Deliverable[]
    - milestones: Milestone[]
    - complexity: ComplexityLevel (enum)

  Enums:
    ProjectType:
      - NEW_DEVELOPMENT      # 신규 개발
      - ENHANCEMENT          # 기능 개선
      - MIGRATION            # 마이그레이션
      - INTEGRATION          # 시스템 통합
      - MAINTENANCE          # 유지보수
      - POC                  # 개념 검증
      - MVP                  # MVP 개발

  Specific Relationships:
    - hasScope: Scope (1:1)
    - hasFeature: Feature (1:N)
    - hasTimeline: Timeline (1:1)
    - requiresRole: Role (1:N)

  Notes:
    - 상세 정의: extensions/software_project.md
```

### 2.2 Study

```yaml
Class: Study
  Extends: Core:Activity
  Description: |
    학습 목표 달성을 위한 그룹 활동.
    책 스터디, 기술 스터디, 프로젝트 스터디 등.

  Additional Properties:
    - studyType: StudyType (enum)
    - topic: String
    - targetAudience: String
    - maxParticipants: Integer
    - currentParticipants: Integer
    - registrationDeadline: DateTime (nullable)
    - isRecurring: Boolean
    - recurringPattern: RecurringPattern (nullable)

  Enums:
    StudyType:
      - BOOK_STUDY           # 책 스터디
      - TECH_STUDY           # 기술 스터디
      - PROJECT_STUDY        # 프로젝트 기반 스터디
      - CERTIFICATION        # 자격증 스터디
      - PAPER_READING        # 논문 읽기
      - CODE_REVIEW          # 코드 리뷰 스터디

    RecurringPattern:
      - WEEKLY               # 주 1회
      - BIWEEKLY             # 격주
      - MONTHLY              # 월 1회

  Specific Relationships:
    - hasCurriculum: Curriculum (1:1)
    - hasAssignment: Assignment (1:N)
    - hasPresentation: Presentation (1:N)

  Notes:
    - 상세 정의: extensions/study.md
```

### 2.3 Mentoring

```yaml
Class: Mentoring
  Extends: Core:Activity
  Description: |
    멘토의 지도 아래 멘티가 성장하는 활동.
    1:1 멘토링, 그룹 멘토링, 피어 멘토링 등.

  Additional Properties:
    - mentoringType: MentoringType (enum)
    - focusAreas: String[]
    - goals: MentoringGoal[]
    - frequency: SessionFrequency (enum)
    - totalSessions: Integer (nullable)
    - completedSessions: Integer

  Enums:
    MentoringType:
      - ONE_ON_ONE           # 1:1 멘토링
      - GROUP                # 그룹 멘토링 (1:N)
      - PEER                 # 피어 멘토링
      - REVERSE              # 리버스 멘토링

    SessionFrequency:
      - WEEKLY               # 주 1회
      - BIWEEKLY             # 격주
      - MONTHLY              # 월 1회
      - ON_DEMAND            # 필요 시

  Specific Relationships:
    - hasMentor: Participant (1:1)
    - hasMentee: Participant (1:N)
    - hasGoal: MentoringGoal (1:N)
    - hasFeedback: Feedback (1:N)

  Notes:
    - 상세 정의: extensions/mentoring.md
```

### 2.4 Consulting

```yaml
Class: Consulting
  Extends: Core:Activity
  Description: |
    전문가가 클라이언트에게 자문을 제공하는 활동.
    기술 컨설팅, 전략 컨설팅, 프로세스 컨설팅 등.

  Additional Properties:
    - consultingType: ConsultingType (enum)
    - engagementType: EngagementType (enum)
    - industryDomain: String
    - expertiseAreas: String[]
    - confidentialityLevel: ConfidentialityLevel (enum)

  Enums:
    ConsultingType:
      - TECHNICAL            # 기술 컨설팅
      - ARCHITECTURE         # 아키텍처 컨설팅
      - STRATEGY             # 전략 컨설팅
      - PROCESS              # 프로세스 컨설팅
      - ASSESSMENT           # 진단/평가

    EngagementType:
      - ONE_TIME             # 일회성
      - RETAINER             # 정기 계약
      - PROJECT_BASED        # 프로젝트 기반
      - ADVISORY             # 자문역

    ConfidentialityLevel:
      - PUBLIC               # 공개 가능
      - CONFIDENTIAL         # 기밀
      - STRICTLY_CONFIDENTIAL # 엄격 기밀

  Specific Relationships:
    - hasClient: Participant (1:1)
    - hasConsultant: Participant (1:N)
    - hasDeliverable: Deliverable (1:N)
    - hasContract: Contract (1:1)

  Notes:
    - 상세 정의: extensions/consulting.md
```

---

## 3. ActivityCost (활동 비용 통합)

### 3.1 기본 구조

```yaml
Class: ActivityCost
  Extends: Core:Cost
  Description: 활동 유형별 비용 구조 통합

  Properties:
    - costId: String (PK)
    - activityId: String (FK)
    - activityType: ActivityType (enum)
    - totalCost: Money
    - calculatedAt: DateTime

  Derived Properties:
    - totalDirectCost: Money
    - totalIndirectCost: Money
    - costBreakdown: CostBreakdown[]

  Relationships:
    - belongsTo: Activity (N:1)
    - hasComponent: CostComponent (1:N)
```

### 3.2 CostComponent (비용 구성요소)

```yaml
Class: CostComponent
  Description: 개별 비용 항목

  Properties:
    - componentId: String (PK)
    - componentType: CostComponentType (enum)
    - category: CostCategory (enum)
    - description: String
    - amount: Money
    - unit: CostUnit (enum)
    - quantity: Decimal
    - duration: Duration (nullable)
    - calculatedCost: Money

  Enums:
    CostCategory:
      - DIRECT               # 직접비
      - INDIRECT             # 간접비
      - CONTINGENCY          # 예비비

  Calculation:
    calculatedCost = amount × quantity (또는 amount × quantity × duration)
```

### 3.3 활동 유형별 CostComponentType

```yaml
CostComponentType:
  # ═══════════════════════════════════════════════
  # 공통 비용 (모든 활동 유형)
  # ═══════════════════════════════════════════════
  COMMON:
    - PLATFORM_FEE:
        description: "플랫폼/시스템 비용"
        unit: [FIXED, MONTHLY]
        category: INDIRECT

    - ADMIN_FEE:
        description: "운영/관리 비용"
        unit: [FIXED, PERCENTAGE]
        category: INDIRECT
        typicalRate: "5-15%"

    - COMMUNICATION_FEE:
        description: "커뮤니케이션 도구 비용"
        unit: [MONTHLY]
        category: INDIRECT

  # ═══════════════════════════════════════════════
  # Project 특화 비용
  # ═══════════════════════════════════════════════
  PROJECT:
    - LABOR:
        description: "인건비 (개발자, PM, QA 등)"
        unit: [MAN_MONTH, DAILY, HOURLY]
        category: DIRECT
        weight: "55-70%"

    - INFRASTRUCTURE:
        description: "인프라비 (서버, DB, 네트워크)"
        unit: [MONTHLY, FIXED]
        category: DIRECT

    - TOOL:
        description: "도구비 (IDE, 협업 도구, 라이선스)"
        unit: [MONTHLY, FIXED, PER_SEAT]
        category: DIRECT

    - EXTERNAL:
        description: "외주비 (외부 개발사, 디자인)"
        unit: [FIXED, PROJECT]
        category: DIRECT

    - OVERHEAD:
        description: "제경비"
        unit: [PERCENTAGE]
        category: INDIRECT
        typicalRate: "110-120% of LABOR"

    - TECHNICAL_FEE:
        description: "기술료"
        unit: [PERCENTAGE]
        category: INDIRECT
        typicalRate: "20-40% of (LABOR + OVERHEAD)"

    - CONTINGENCY:
        description: "리스크 예비비"
        unit: [PERCENTAGE]
        category: CONTINGENCY
        typicalRate: "3-12%"

  # ═══════════════════════════════════════════════
  # Study 특화 비용
  # ═══════════════════════════════════════════════
  STUDY:
    - INSTRUCTOR_FEE:
        description: "강사비 (외부 강사 초빙 시)"
        unit: [PER_SESSION, HOURLY]
        category: DIRECT

    - VENUE_FEE:
        description: "장소비 (회의실, 강의실)"
        unit: [PER_SESSION, HOURLY, MONTHLY]
        category: DIRECT

    - MATERIAL_FEE:
        description: "자료비 (교재, 인쇄물)"
        unit: [PER_PERSON, FIXED]
        category: DIRECT

    - CATERING:
        description: "다과비"
        unit: [PER_PERSON, PER_SESSION]
        category: DIRECT
        optional: true

    - CERTIFICATE_FEE:
        description: "수료증 발급비"
        unit: [PER_PERSON]
        category: DIRECT
        optional: true

  # ═══════════════════════════════════════════════
  # Mentoring 특화 비용
  # ═══════════════════════════════════════════════
  MENTORING:
    - MENTOR_FEE:
        description: "멘토 비용"
        unit: [PER_SESSION, HOURLY, MONTHLY]
        category: DIRECT
        weight: "60-80%"

    - SESSION_FEE:
        description: "세션 운영 비용"
        unit: [PER_SESSION]
        category: DIRECT

    - MATCHING_FEE:
        description: "매칭 비용 (플랫폼 수수료)"
        unit: [PERCENTAGE]
        category: INDIRECT
        typicalRate: "10-15%"

  # ═══════════════════════════════════════════════
  # Consulting 특화 비용
  # ═══════════════════════════════════════════════
  CONSULTING:
    - CONSULTANT_FEE:
        description: "컨설턴트 비용"
        unit: [DAILY, HOURLY, PROJECT]
        category: DIRECT
        weight: "50-70%"

    - RESEARCH_FEE:
        description: "리서치 비용"
        unit: [FIXED, HOURLY]
        category: DIRECT

    - REPORT_FEE:
        description: "보고서 작성 비용"
        unit: [FIXED, PER_DELIVERABLE]
        category: DIRECT

    - TRAVEL_FEE:
        description: "출장비"
        unit: [ACTUAL, FIXED]
        category: DIRECT
        optional: true

    - FIRM_OVERHEAD:
        description: "펌 오버헤드"
        unit: [PERCENTAGE]
        category: INDIRECT
        typicalRate: "30-50%"
```

### 3.4 활동 유형별 비용 구조 비중

```yaml
CostStructureWeight:
  Project:
    DirectCost: "55-65%"
      - LABOR: "70-80%"
      - INFRASTRUCTURE: "10-15%"
      - TOOL: "5-10%"
      - EXTERNAL: "0-15%"
    IndirectCost: "35-45%"
      - OVERHEAD: "70%"
      - TECHNICAL_FEE: "30%"
    Contingency: "3-12%"

  Study:
    DirectCost: "60-80%"
      - INSTRUCTOR_FEE: "40-60%"
      - VENUE_FEE: "20-30%"
      - MATERIAL_FEE: "10-20%"
    IndirectCost: "20-40%"
      - ADMIN_FEE: "10-15%"
      - PLATFORM_FEE: "5-10%"

  Mentoring:
    DirectCost: "70-85%"
      - MENTOR_FEE: "80-90%"
      - SESSION_FEE: "10-20%"
    IndirectCost: "15-30%"
      - MATCHING_FEE: "10-15%"
      - ADMIN_FEE: "5-10%"

  Consulting:
    DirectCost: "50-70%"
      - CONSULTANT_FEE: "60-80%"
      - RESEARCH_FEE: "10-20%"
      - REPORT_FEE: "10-15%"
    IndirectCost: "30-50%"
      - FIRM_OVERHEAD: "30-50%"
```

### 3.5 비용 계산 공식

```yaml
CostFormula:
  # ─────────────────────────────────────────────
  # Project 비용 계산 (공공사업 기준)
  # ─────────────────────────────────────────────
  Project:
    DirectCost: |
      LaborCost + InfrastructureCost + ToolCost + ExternalCost

    LaborCost: |
      SUM(headcount × duration × allocation × unitCost)

    IndirectCost: |
      Overhead = LaborCost × 110-120%
      TechnicalFee = (LaborCost + Overhead) × 20-40%

    TotalCost: |
      DirectCost + IndirectCost + Contingency

  # ─────────────────────────────────────────────
  # Study 비용 계산
  # ─────────────────────────────────────────────
  Study:
    DirectCost: |
      (InstructorFee + VenueFee) × Sessions + MaterialFee × Participants

    IndirectCost: |
      DirectCost × AdminFeeRate + PlatformFee

    TotalCost: |
      DirectCost + IndirectCost

    PerPersonCost: |
      TotalCost / ExpectedParticipants

  # ─────────────────────────────────────────────
  # Mentoring 비용 계산
  # ─────────────────────────────────────────────
  Mentoring:
    DirectCost: |
      MentorFee × Sessions + SessionFee × Sessions

    IndirectCost: |
      DirectCost × MatchingFeeRate + AdminFee

    TotalCost: |
      DirectCost + IndirectCost

    PerMenteeCost:  # 그룹 멘토링의 경우
      TotalCost / MenteeCount

  # ─────────────────────────────────────────────
  # Consulting 비용 계산
  # ─────────────────────────────────────────────
  Consulting:
    DirectCost: |
      ConsultantFee × Duration + ResearchFee + ReportFee + TravelFee

    IndirectCost: |
      DirectCost × FirmOverheadRate

    TotalCost: |
      DirectCost + IndirectCost
```

---

## 4. ActivityPricing (활동 가격 통합)

### 4.1 기본 구조

```yaml
Class: ActivityPricing
  Extends: Core:Revenue
  Description: 활동 유형별 가격 정책 통합

  Properties:
    - pricingId: String (PK)
    - activityId: String (FK)
    - activityType: ActivityType (enum)
    - pricingModel: PricingModel (enum)
    - baseCost: Money
    - finalPrice: Money
    - pricePerUnit: Money (nullable)  # 인당, 세션당 등
    - calculatedAt: DateTime

  Relationships:
    - basedOn: ActivityCost (1:1)
    - appliesMargin: MarginPolicy (0:1)
    - appliesRiskPremium: RiskPremium (0:1)
    - appliesDiscount: DiscountPolicy (0:N)
```

### 4.2 PricingModel (가격 모델)

```yaml
PricingModel:
  # ═══════════════════════════════════════════════
  # 공통 가격 모델
  # ═══════════════════════════════════════════════
  COMMON:
    - COST_PLUS:
        description: "원가 + 마진"
        formula: "BaseCost × (1 + MarginRate)"
        usage: ["Project", "Consulting"]

    - VALUE_BASED:
        description: "가치 기반 가격"
        formula: "ExpectedValue × ValueCaptureRate"
        usage: ["Consulting", "Mentoring"]

  # ═══════════════════════════════════════════════
  # Project 가격 모델
  # ═══════════════════════════════════════════════
  PROJECT:
    - FIXED_PRICE:
        description: "고정가"
        formula: "BaseCost × (1 + Margin) × (1 + RiskPremium)"
        usage: ["SI", "외주"]

    - TIME_AND_MATERIAL:
        description: "시간/자재 기반"
        formula: "ActualHours × HourlyRate + Materials"
        usage: ["유지보수", "장기 프로젝트"]

    - MILESTONE_BASED:
        description: "마일스톤 기반"
        formula: "SUM(MilestonePayment)"
        usage: ["대규모 프로젝트"]

  # ═══════════════════════════════════════════════
  # Study 가격 모델
  # ═══════════════════════════════════════════════
  STUDY:
    - PER_PERSON:
        description: "인당 비용"
        formula: "TotalCost / Participants"
        usage: ["유료 스터디"]

    - FLAT_FEE:
        description: "정액제"
        formula: "FixedPrice (참여자 수 무관)"
        usage: ["소규모 스터디"]

    - FREE:
        description: "무료"
        formula: "0 (커뮤니티 스터디)"
        usage: ["커뮤니티", "오픈 스터디"]

    - TIERED:
        description: "구간별 차등"
        formula: "참여자 수에 따른 단계별 가격"
        usage: ["규모 탄력적 스터디"]

  # ═══════════════════════════════════════════════
  # Mentoring 가격 모델
  # ═══════════════════════════════════════════════
  MENTORING:
    - PER_SESSION:
        description: "세션당"
        formula: "SessionPrice × Sessions"
        usage: ["1:1 멘토링"]

    - MONTHLY_SUBSCRIPTION:
        description: "월정액"
        formula: "MonthlyFee × Months"
        usage: ["정기 멘토링"]

    - PACKAGE:
        description: "패키지"
        formula: "PackagePrice (세션 묶음)"
        usage: ["집중 멘토링"]

    - FREE:
        description: "무료 (피어 멘토링)"
        formula: "0"
        usage: ["커뮤니티"]

  # ═══════════════════════════════════════════════
  # Consulting 가격 모델
  # ═══════════════════════════════════════════════
  CONSULTING:
    - HOURLY:
        description: "시간당"
        formula: "HourlyRate × Hours"
        usage: ["단기 자문"]

    - DAILY:
        description: "일당"
        formula: "DailyRate × Days"
        usage: ["현장 컨설팅"]

    - PROJECT_BASED:
        description: "프로젝트 기반"
        formula: "FixedProjectFee"
        usage: ["범위 확정 프로젝트"]

    - RETAINER:
        description: "정기 계약"
        formula: "MonthlyFee × Months"
        usage: ["지속적 자문"]

    - SUCCESS_FEE:
        description: "성과 기반"
        formula: "BaseFee + (Value × SuccessRate)"
        usage: ["성과 연동"]
```

### 4.3 MarginPolicy (마진 정책)

```yaml
Class: MarginPolicy
  Properties:
    - marginType: MarginType (enum)
    - targetRate: Percentage
    - minRate: Percentage
    - maxRate: Percentage
    - calculatedMargin: Money

  Enums:
    MarginType:
      - FIXED_RATE           # 고정 마진율
      - TIERED               # 규모별 차등
      - VALUE_BASED          # 가치 기반
      - COMPETITIVE          # 경쟁 기반

MarginGuideline:
  # ─────────────────────────────────────────────
  # Project 마진
  # ─────────────────────────────────────────────
  Project:
    SI_PROJECT:
      typical: "10-15%"
      range: [5, 20]
      note: "공공사업 기준"

    CUSTOM_DEVELOPMENT:
      typical: "15-25%"
      range: [10, 35]

    SOLUTION_CUSTOMIZATION:
      typical: "20-30%"
      range: [15, 40]

  # ─────────────────────────────────────────────
  # Study 마진
  # ─────────────────────────────────────────────
  Study:
    COMMUNITY_STUDY:
      typical: "0-10%"
      note: "비영리/커뮤니티"

    PAID_STUDY:
      typical: "20-40%"
      note: "교육 서비스"

    CORPORATE_TRAINING:
      typical: "40-60%"
      note: "기업 교육"

  # ─────────────────────────────────────────────
  # Mentoring 마진
  # ─────────────────────────────────────────────
  Mentoring:
    PEER_MENTORING:
      typical: "0-5%"
      note: "플랫폼 수수료만"

    PROFESSIONAL_MENTORING:
      typical: "15-30%"

    EXECUTIVE_COACHING:
      typical: "30-50%"

  # ─────────────────────────────────────────────
  # Consulting 마진
  # ─────────────────────────────────────────────
  Consulting:
    ADVISORY:
      typical: "30-50%"

    IMPLEMENTATION:
      typical: "20-35%"

    STRATEGY:
      typical: "40-60%"
```

### 4.4 DiscountPolicy (할인 정책)

```yaml
Class: DiscountPolicy
  Properties:
    - discountType: DiscountType (enum)
    - discountRate: Percentage
    - discountAmount: Money (nullable)
    - conditions: String
    - validFrom: Date
    - validTo: Date

  Enums:
    DiscountType:
      # 공통
      - EARLY_BIRD:
          description: "조기 등록 할인"
          typicalRate: "10-20%"

      - LOYALTY:
          description: "재참여/기존 고객 할인"
          typicalRate: "5-15%"

      - REFERRAL:
          description: "추천 할인"
          typicalRate: "5-10%"

      - VOLUME:
          description: "대량/그룹 할인"
          typicalRate: "10-30%"

      # Study/Mentoring
      - STUDENT:
          description: "학생 할인"
          typicalRate: "20-30%"

      - COMMUNITY_MEMBER:
          description: "커뮤니티 회원 할인"
          typicalRate: "10-20%"

      # Project/Consulting
      - LONG_TERM:
          description: "장기 계약 할인"
          typicalRate: "5-15%"

      - STRATEGIC:
          description: "전략적 할인 (포트폴리오, 레퍼런스)"
          typicalRate: "10-20%"
```

### 4.5 범용 가격 계산 공식

```yaml
UniversalPricingFormula:
  # ─────────────────────────────────────────────
  # 기본 공식 (모든 활동 유형 공통)
  # ─────────────────────────────────────────────
  BaseFormula: |
    FinalPrice = BaseCost × (1 + MarginRate) × (1 + RiskPremium) × Adjustments

  Components:
    BaseCost: "ActivityCost.totalCost"
    MarginRate: "MarginPolicy.targetRate"
    RiskPremium: "RiskPremium.premiumRate (Project/Consulting에 적용)"
    Adjustments: "CompetitiveAdjustment × StrategicWeight × (1 - DiscountRate)"

  # ─────────────────────────────────────────────
  # 활동 유형별 가격 계산
  # ─────────────────────────────────────────────
  ByActivityType:
    Project:
      formula: |
        FinalPrice = BaseCost × (1 + Margin) × (1 + RiskPremium) × CompetitiveAdj × StrategicWeight
      output:
        - finalPrice: "총 프로젝트 가격"
        - priceRange: "[floor, target, ceiling]"
        - paymentSchedule: "마일스톤별 지급 계획"

    Study:
      formula: |
        TotalPrice = BaseCost × (1 + Margin) × (1 - EarlyBirdDiscount)
        PerPersonPrice = TotalPrice / ExpectedParticipants
      output:
        - perPersonPrice: "인당 참가비"
        - minParticipants: "최소 참여 인원 (손익분기)"
        - earlyBirdPrice: "조기 등록 가격"

    Mentoring:
      formula: |
        PackagePrice = (MentorFee + OperatingCost) × Sessions × (1 + Margin)
        PerSessionPrice = PackagePrice / Sessions
      output:
        - perSessionPrice: "세션당 가격"
        - packagePrice: "패키지 가격"
        - monthlyPrice: "월정액 (해당 시)"

    Consulting:
      formula: |
        FinalPrice = (ConsultantCost × Duration + FixedCosts) × (1 + FirmMargin)
      output:
        - dailyRate: "일당"
        - projectPrice: "프로젝트 총액"
        - retainerFee: "월정 자문료"
```

---

## 5. 관계 다이어그램

### 5.1 Activity Types 구조

```
                    Core:Activity (core_v2.md)
                           │
         ┌─────────────────┼─────────────────┬─────────────────┐
         │                 │                 │                 │
         ▼                 ▼                 ▼                 ▼
    ┌─────────┐      ┌───────────┐    ┌───────────┐    ┌────────────┐
    │ Project │      │   Study   │    │ Mentoring │    │ Consulting │
    └────┬────┘      └─────┬─────┘    └─────┬─────┘    └──────┬─────┘
         │                 │                 │                 │
         ▼                 ▼                 ▼                 ▼
 ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
 │ ProjectCost   │ │  StudyCost    │ │MentoringCost  │ │ConsultingCost │
 │ ProjectPricing│ │ StudyPricing  │ │MentoringPricing│ │ConsultingPricing│
 └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘
         │                 │                 │                 │
         └─────────────────┴─────────────────┴─────────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │ Core:Revenue  │
                            │ (finalPrice)  │
                            └───────────────┘
```

### 5.2 Cost → Pricing 흐름

```
┌─────────────────────────────────────────────────────────────────┐
│                        ActivityCost                              │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │ CostComponent │  │ CostComponent │  │ CostComponent │ ...   │
│  │ (LABOR)       │  │ (INFRA)       │  │ (TOOL)        │       │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘       │
│          └──────────────────┼──────────────────┘               │
│                             │ SUM                               │
│                             ▼                                   │
│                      ┌─────────────┐                            │
│                      │  BaseCost   │                            │
│                      └──────┬──────┘                            │
└─────────────────────────────┼───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      ActivityPricing                             │
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         │                    │                    │             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │MarginPolicy │     │RiskPremium  │     │DiscountPolicy│       │
│  │  × (1+m)    │     │  × (1+r)    │     │  × (1-d)    │       │
│  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘       │
│         └────────────────────┼────────────────────┘             │
│                              │                                   │
│                              ▼                                   │
│                      ┌─────────────┐                            │
│                      │ FinalPrice  │                            │
│                      └─────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. JSON 예시

### 6.1 Study 비용 및 가격

```json
{
  "activity": {
    "activityType": "STUDY",
    "activityName": "Claude API 심화 스터디",
    "sessions": 8,
    "expectedParticipants": 15
  },
  "activityCost": {
    "components": [
      {
        "componentType": "VENUE_FEE",
        "amount": 50000,
        "unit": "PER_SESSION",
        "quantity": 8,
        "calculatedCost": 400000
      },
      {
        "componentType": "MATERIAL_FEE",
        "amount": 20000,
        "unit": "PER_PERSON",
        "quantity": 15,
        "calculatedCost": 300000
      },
      {
        "componentType": "PLATFORM_FEE",
        "amount": 50000,
        "unit": "MONTHLY",
        "quantity": 2,
        "calculatedCost": 100000
      },
      {
        "componentType": "ADMIN_FEE",
        "amount": 80000,
        "unit": "FIXED",
        "quantity": 1,
        "calculatedCost": 80000
      }
    ],
    "totalDirectCost": 700000,
    "totalIndirectCost": 180000,
    "totalCost": 880000
  },
  "activityPricing": {
    "pricingModel": "PER_PERSON",
    "baseCost": 880000,
    "marginRate": 0.20,
    "discounts": [
      {
        "discountType": "EARLY_BIRD",
        "discountRate": 0.10,
        "validTo": "2026-02-20"
      }
    ],
    "regularPerPersonPrice": 70400,
    "earlyBirdPerPersonPrice": 63360,
    "minParticipants": 10,
    "breakEvenParticipants": 8
  }
}
```

### 6.2 Mentoring 비용 및 가격

```json
{
  "activity": {
    "activityType": "MENTORING",
    "activityName": "시니어 개발자 1:1 멘토링",
    "mentoringType": "ONE_ON_ONE",
    "totalSessions": 12,
    "frequency": "BIWEEKLY"
  },
  "activityCost": {
    "components": [
      {
        "componentType": "MENTOR_FEE",
        "amount": 150000,
        "unit": "PER_SESSION",
        "quantity": 12,
        "calculatedCost": 1800000
      },
      {
        "componentType": "PLATFORM_FEE",
        "amount": 30000,
        "unit": "MONTHLY",
        "quantity": 6,
        "calculatedCost": 180000
      },
      {
        "componentType": "MATCHING_FEE",
        "amount": 198000,
        "unit": "FIXED",
        "note": "10% of MentorFee + Platform",
        "calculatedCost": 198000
      }
    ],
    "totalDirectCost": 1980000,
    "totalIndirectCost": 198000,
    "totalCost": 2178000
  },
  "activityPricing": {
    "pricingModel": "PACKAGE",
    "baseCost": 2178000,
    "marginRate": 0.25,
    "packagePrice": 2722500,
    "perSessionPrice": 226875,
    "alternativeModels": {
      "monthly": {
        "model": "MONTHLY_SUBSCRIPTION",
        "price": 453750
      }
    }
  }
}
```

---

## 7. Extensions 연계

각 활동 유형의 상세 정의는 extensions/ 디렉토리 참조:

| 활동 유형 | Extension 파일 | 상세 내용 |
|-----------|----------------|----------|
| Project | `extensions/software_project.md` | Scope, Feature, Timeline, Role, Complexity |
| Study | `extensions/study.md` | Assignment, Presentation, LearningObjective |
| Mentoring | `extensions/mentoring.md` | MentoringGoal, Feedback, ProgressTracking |
| Consulting | `extensions/consulting.md` | Deliverable, ConsultingContract, Engagement |

---

## 문서 정보

- **작성일**: 2026-02-27
- **버전**: 1.0
- **의존 문서**: core_v2.md
- **확장 문서**:
  - extensions/software_project.md
  - extensions/study.md
  - extensions/mentoring.md
  - extensions/consulting.md
- **이전 버전 참조**:
  - project.md (v1)
  - cost.md (v1)
  - pricing.md (v1)
