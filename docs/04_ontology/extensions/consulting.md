# Extension: Advisory Consulting

---

## 1. 개요

### 1.1 목적
Domain Ontology의 `Consulting`을 전문 자문 맥락으로 확장하여
컨설팅 계약, 산출물, 클라이언트 관계, 전문 영역을 상세하게 모델링

### 1.2 확장 구조

```
Domain:Consulting (domain.md)
    └── extends → AdvisoryConsulting
                      ├── hasContract → ConsultingContract
                      ├── hasDeliverable → Deliverable
                      ├── hasEngagement → Engagement
                      ├── hasWorkstream → Workstream
                      └── hasStakeholder → Stakeholder
```

---

## 2. AdvisoryConsulting

### 2.1 Class 정의

```yaml
Class: AdvisoryConsulting
  Extends: Domain:Consulting

  Properties:
    - engagementModel: EngagementModel (enum)
    - serviceType: ServiceType (enum)
    - industryFocus: String[]
    - expertiseAreas: String[]
    - confidentialityLevel: ConfidentialityLevel (enum)
    - clientRelationship: ClientRelationship (enum)
    - riskLevel: RiskLevel (enum)

  Enums:
    EngagementModel:
      - PROJECT               # 프로젝트 기반
      - RETAINER              # 정기 계약
      - ADVISORY_BOARD        # 자문단
      - INTERIM               # 임시 임원/관리자
      - WORKSHOP              # 워크샵/교육

    ServiceType:
      - STRATEGY              # 전략 컨설팅
      - OPERATIONS            # 운영 컨설팅
      - TECHNOLOGY            # 기술 컨설팅
      - TRANSFORMATION        # 변혁 컨설팅
      - IMPLEMENTATION        # 구현 컨설팅
      - ASSESSMENT            # 진단/평가
      - DUE_DILIGENCE         # 실사

    ConfidentialityLevel:
      - PUBLIC                # 공개 가능
      - INTERNAL              # 내부 공유
      - CONFIDENTIAL          # 기밀
      - STRICTLY_CONFIDENTIAL # 엄격 기밀
      - PRIVILEGED            # 법적 보호

    ClientRelationship:
      - NEW_CLIENT            # 신규 고객
      - EXISTING_CLIENT       # 기존 고객
      - STRATEGIC_PARTNER     # 전략적 파트너
      - REFERRAL              # 추천 고객

    RiskLevel:
      - LOW
      - MEDIUM
      - HIGH
      - CRITICAL

  Relationships:
    - hasContract: ConsultingContract (1:1)
    - hasDeliverable: Deliverable (1:N)
    - hasEngagement: Engagement (1:1)
    - hasWorkstream: Workstream (1:N)
    - hasStakeholder: Stakeholder (1:N)
    - hasClient: Participant (1:1)
    - hasConsultant: Participant (1:N)
```

---

## 3. ConsultingContract (컨설팅 계약)

### 3.1 Class 정의

```yaml
Class: ConsultingContract
  Extends: Core:Contract
  Description: 컨설팅 계약 상세

  Additional Properties:
    - contractType: ConsultingContractType (enum)
    - scopeOfWork: String
    - outOfScope: String[]
    - assumptions: String[]
    - constraints: String[]
    - changeRequestProcess: String
    - intellectualPropertyTerms: IPTerms (embedded)
    - liabilityTerms: LiabilityTerms (embedded)
    - terminationTerms: TerminationTerms (embedded)

  Enums:
    ConsultingContractType:
      - MASTER_SERVICE_AGREEMENT  # 기본 서비스 계약
      - STATEMENT_OF_WORK         # 작업 명세서
      - ENGAGEMENT_LETTER         # 약정서
      - NDA                       # 기밀유지계약
      - RETAINER_AGREEMENT        # 정기 계약

  Embedded:
    IPTerms:
      ownershipModel: OwnershipModel (CLIENT_OWNS, CONSULTANT_OWNS, JOINT, LICENSE)
      preExistingIP: String
      deliverableIP: String
      licensingTerms: String (nullable)

    LiabilityTerms:
      liabilityCap: Money
      exclusions: String[]
      indemnification: String

    TerminationTerms:
      noticePeriod: Duration
      terminationForCause: String[]
      terminationForConvenience: String
      postTerminationObligations: String[]

  Relationships:
    - governs: AdvisoryConsulting (1:1)
    - hasAmendment: ContractAmendment (1:N)
```

---

## 4. Deliverable (산출물)

### 4.1 Class 정의

```yaml
Class: Deliverable
  Description: 컨설팅 산출물

  Properties:
    - deliverableId: String (PK)
    - title: String
    - description: String
    - deliverableType: DeliverableType (enum)
    - format: DeliverableFormat (enum)
    - dueDate: Date
    - submittedDate: Date (nullable)
    - status: DeliverableStatus (enum)
    - version: String
    - reviewCycle: Integer          # 리뷰 횟수
    - acceptanceCriteria: String[]
    - linkedPayment: Percentage (nullable)  # 연결된 지급 비율

  Enums:
    DeliverableType:
      - REPORT                # 보고서
      - PRESENTATION          # 발표 자료
      - RECOMMENDATION        # 권고안
      - ASSESSMENT            # 평가서
      - ROADMAP               # 로드맵
      - IMPLEMENTATION_GUIDE  # 구현 가이드
      - WORKSHOP_MATERIAL     # 워크샵 자료
      - DATA_ANALYSIS         # 데이터 분석
      - PROCESS_DOCUMENTATION # 프로세스 문서
      - TRAINING_MATERIAL     # 교육 자료

    DeliverableFormat:
      - DOCUMENT              # 문서 (PDF, Word)
      - SPREADSHEET           # 스프레드시트
      - PRESENTATION          # 프레젠테이션
      - DASHBOARD             # 대시보드
      - VIDEO                 # 영상
      - INTERACTIVE           # 인터랙티브 콘텐츠

    DeliverableStatus:
      - PLANNED               # 계획됨
      - IN_PROGRESS           # 작성 중
      - INTERNAL_REVIEW       # 내부 리뷰
      - CLIENT_REVIEW         # 고객 리뷰
      - REVISION              # 수정 중
      - SUBMITTED             # 제출됨
      - ACCEPTED              # 승인됨
      - REJECTED              # 거부됨

  Relationships:
    - belongsTo: AdvisoryConsulting (N:1)
    - partOfWorkstream: Workstream (N:1)
    - createdBy: Participant (N:N)
    - reviewedBy: Participant (N:N)
    - hasReview: DeliverableReview (1:N)
```

### 4.2 DeliverableReview

```yaml
Class: DeliverableReview
  Description: 산출물 리뷰

  Properties:
    - reviewId: String (PK)
    - reviewRound: Integer
    - reviewedAt: DateTime
    - reviewerType: ReviewerType (enum)
    - decision: ReviewDecision (enum)
    - comments: String[]
    - changeRequests: ChangeRequest[]

  Enums:
    ReviewerType:
      - INTERNAL              # 내부 리뷰어
      - CLIENT                # 클라이언트
      - STAKEHOLDER           # 이해관계자

    ReviewDecision:
      - APPROVED              # 승인
      - APPROVED_WITH_MINOR   # 경미한 수정 후 승인
      - REVISION_REQUIRED     # 수정 필요
      - REJECTED              # 거부

  Embedded:
    ChangeRequest:
      section: String
      currentContent: String
      requestedChange: String
      priority: Priority
      status: ChangeRequestStatus

  Relationships:
    - forDeliverable: Deliverable (N:1)
    - reviewedBy: Participant (N:1)
```

---

## 5. Engagement (컨설팅 참여)

### 5.1 Class 정의

```yaml
Class: Engagement
  Description: 컨설팅 참여/수행 관리

  Properties:
    - engagementId: String (PK)
    - phase: EngagementPhase (enum)
    - startDate: Date
    - plannedEndDate: Date
    - actualEndDate: Date (nullable)
    - teamStructure: TeamStructure (embedded)
    - governanceModel: GovernanceModel (embedded)
    - communicationPlan: CommunicationPlan (embedded)
    - riskRegister: Risk[]
    - issueLog: Issue[]
    - changeLog: Change[]

  Enums:
    EngagementPhase:
      - MOBILIZATION          # 착수/준비
      - DISCOVERY             # 현황 분석
      - ANALYSIS              # 심층 분석
      - DESIGN                # 설계/솔루션
      - VALIDATION            # 검증
      - IMPLEMENTATION        # 구현 지원
      - TRANSITION            # 이관/종료

  Embedded:
    TeamStructure:
      engagementPartner: String     # 참여 파트너
      engagementManager: String     # 참여 매니저
      projectManager: String        # 프로젝트 매니저
      teamMembers: TeamMember[]

    TeamMember:
      participantId: String
      role: String
      allocation: Percentage
      startDate: Date
      endDate: Date (nullable)

    GovernanceModel:
      steeringCommittee: SteeringCommittee (nullable)
      reportingFrequency: String
      decisionRights: String[]
      escalationPath: String[]

    SteeringCommittee:
      members: String[]
      meetingFrequency: String
      quorumRequirement: Integer

    CommunicationPlan:
      statusReportFrequency: String
      meetingSchedule: MeetingSchedule[]
      distributionList: DistributionList[]

    MeetingSchedule:
      meetingType: String
      frequency: String
      attendees: String[]
      agenda: String (nullable)

  Relationships:
    - forConsulting: AdvisoryConsulting (1:1)
    - hasStatusReport: StatusReport (1:N)
```

---

## 6. Workstream (작업 흐름)

### 6.1 Class 정의

```yaml
Class: Workstream
  Description: 컨설팅 내 세부 작업 영역

  Properties:
    - workstreamId: String (PK)
    - name: String
    - description: String
    - objective: String
    - lead: String               # Participant ID
    - status: WorkstreamStatus (enum)
    - startDate: Date
    - endDate: Date
    - progress: Percentage
    - dependencies: String[]     # 다른 Workstream IDs

  Enums:
    WorkstreamStatus:
      - NOT_STARTED
      - IN_PROGRESS
      - ON_HOLD
      - COMPLETED
      - CANCELLED

  Relationships:
    - belongsTo: AdvisoryConsulting (N:1)
    - hasDeliverable: Deliverable (1:N)
    - hasActivity: WorkstreamActivity (1:N)
    - ledBy: Participant (N:1)
```

### 6.2 WorkstreamActivity

```yaml
Class: WorkstreamActivity
  Description: Workstream 내 세부 활동

  Properties:
    - activityId: String (PK)
    - name: String
    - description: String
    - activityType: ActivityType (enum)
    - assignedTo: String[]       # Participant IDs
    - startDate: Date
    - endDate: Date
    - effort: Duration           # 예상 공수
    - status: ActivityStatus
    - outputs: String[]

  Enums:
    ActivityType:
      - DATA_COLLECTION       # 데이터 수집
      - INTERVIEW             # 인터뷰
      - ANALYSIS              # 분석
      - WORKSHOP              # 워크샵
      - DOCUMENT_REVIEW       # 문서 검토
      - BENCHMARKING          # 벤치마킹
      - MODELING              # 모델링
      - VALIDATION            # 검증

  Relationships:
    - belongsTo: Workstream (N:1)
    - assignedTo: Participant (N:N)
```

---

## 7. Stakeholder (이해관계자)

### 7.1 Class 정의

```yaml
Class: Stakeholder
  Description: 컨설팅 이해관계자 관리

  Properties:
    - stakeholderId: String (PK)
    - name: String
    - title: String
    - organization: String
    - stakeholderType: StakeholderType (enum)
    - influenceLevel: InfluenceLevel (enum)
    - interestLevel: InterestLevel (enum)
    - engagementStrategy: String
    - communicationPreference: String
    - concerns: String[]
    - expectations: String[]
    - relationshipStatus: RelationshipStatus (enum)

  Enums:
    StakeholderType:
      - SPONSOR               # 스폰서
      - DECISION_MAKER        # 의사결정자
      - INFLUENCER            # 영향력자
      - SUBJECT_MATTER_EXPERT # 주제 전문가
      - END_USER              # 최종 사용자
      - AFFECTED_PARTY        # 영향받는 당사자

    InfluenceLevel:
      - HIGH
      - MEDIUM
      - LOW

    InterestLevel:
      - HIGH
      - MEDIUM
      - LOW

    RelationshipStatus:
      - CHAMPION              # 적극 지지
      - SUPPORTER             # 지지
      - NEUTRAL               # 중립
      - SKEPTIC               # 회의적
      - OPPONENT              # 반대

  Relationships:
    - involvedIn: AdvisoryConsulting (N:N)
    - mapsTo: Participant (N:1, nullable)
```

---

## 8. StatusReport (상태 보고)

### 8.1 Class 정의

```yaml
Class: StatusReport
  Description: 정기 상태 보고

  Properties:
    - reportId: String (PK)
    - reportPeriod: DateRange
    - submittedAt: DateTime
    - overallStatus: RAGStatus (enum)
    - executiveSummary: String
    - accomplishments: String[]
    - plannedActivities: String[]
    - risks: RiskSummary[]
    - issues: IssueSummary[]
    - decisions: DecisionSummary[]
    - metrics: Metric[]
    - budgetStatus: BudgetStatus (embedded)

  Enums:
    RAGStatus:
      - GREEN                 # 정상
      - AMBER                 # 주의
      - RED                   # 위험

  Embedded:
    RiskSummary:
      description: String
      impact: String
      mitigation: String
      owner: String
      status: RAGStatus

    IssueSummary:
      description: String
      impact: String
      resolution: String
      owner: String
      status: IssueStatus

    DecisionSummary:
      decision: String
      madeBy: String
      madeAt: Date
      impact: String

    Metric:
      name: String
      target: String
      actual: String
      trend: Trend (UP, DOWN, STABLE)

    BudgetStatus:
      totalBudget: Money
      spent: Money
      forecast: Money
      variance: Percentage
      status: RAGStatus

  Relationships:
    - forEngagement: Engagement (N:1)
    - createdBy: Participant (N:1)
```

---

## 9. 관계 다이어그램

```
┌────────────────────────────────────────────────────────────────┐
│                     AdvisoryConsulting                          │
│  (extends Domain:Consulting)                                    │
│                                                                 │
│  ┌────────────────┐                    ┌────────────────┐      │
│  │ConsultingContract│                  │   Engagement   │      │
│  │                │                    │                │      │
│  │ - scopeOfWork  │                    │ - phase        │      │
│  │ - IP terms     │                    │ - team         │      │
│  │ - liability    │                    │ - governance   │      │
│  └────────────────┘                    └───────┬────────┘      │
│                                                │               │
│                                                │ has           │
│                                                ▼               │
│  ┌────────────────┐    ┌────────────────┐ ┌────────────────┐  │
│  │   Workstream   │───►│  Deliverable   │ │  StatusReport  │  │
│  │                │    │                │ │                │  │
│  │ - objective    │    │ - type         │ │ - RAG status   │  │
│  │ - progress     │    │ - status       │ │ - metrics      │  │
│  └───────┬────────┘    └───────┬────────┘ └────────────────┘  │
│          │                     │                               │
│          │ has                 │ has                           │
│          ▼                     ▼                               │
│  ┌────────────────┐    ┌────────────────┐                     │
│  │WorkstreamActivity│  │DeliverableReview│                     │
│  │                │    │                │                     │
│  │ - interview    │    │ - decision     │                     │
│  │ - analysis     │    │ - comments     │                     │
│  └────────────────┘    └────────────────┘                     │
│                                                                 │
│  ┌────────────────┐                                            │
│  │  Stakeholder   │                                            │
│  │                │                                            │
│  │ - influence    │                                            │
│  │ - relationship │                                            │
│  └────────────────┘                                            │
│                                                                 │
│  ┌───────────┐           ┌────────────┐                       │
│  │ Client    │───────────│ Consultant │                       │
│  │(Participant)          │(Participant)                        │
│  └───────────┘           └────────────┘                       │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 10. JSON 예시

```json
{
  "advisoryConsulting": {
    "activityId": "CONSULT-2026-001",
    "activityName": "AI 전략 수립 컨설팅",
    "activityType": "CONSULTING",
    "consultingType": "STRATEGY",
    "engagementModel": "PROJECT",
    "serviceType": "STRATEGY",
    "confidentialityLevel": "CONFIDENTIAL",
    "industryFocus": ["Technology", "Financial Services"],
    "expertiseAreas": ["AI/ML Strategy", "Digital Transformation"],

    "contract": {
      "contractType": "STATEMENT_OF_WORK",
      "scopeOfWork": "AI 도입 전략 수립 및 로드맵 개발",
      "outOfScope": ["시스템 구현", "데이터 마이그레이션"],
      "contractValue": { "amount": 150000000, "currency": "KRW" },
      "intellectualPropertyTerms": {
        "ownershipModel": "CLIENT_OWNS",
        "preExistingIP": "컨설턴트의 기존 방법론 및 프레임워크는 제외"
      }
    },

    "engagement": {
      "phase": "ANALYSIS",
      "startDate": "2026-03-01",
      "plannedEndDate": "2026-05-31",
      "teamStructure": {
        "engagementPartner": "Partner A",
        "engagementManager": "Manager B",
        "teamMembers": [
          { "role": "Senior Consultant", "allocation": 100 },
          { "role": "Consultant", "allocation": 100 },
          { "role": "Analyst", "allocation": 50 }
        ]
      }
    },

    "workstreams": [
      {
        "name": "현황 분석",
        "objective": "현재 AI 역량 및 기회 영역 파악",
        "status": "COMPLETED",
        "progress": 100
      },
      {
        "name": "전략 수립",
        "objective": "AI 도입 전략 및 우선순위 도출",
        "status": "IN_PROGRESS",
        "progress": 60
      },
      {
        "name": "로드맵 개발",
        "objective": "3개년 AI 도입 로드맵 수립",
        "status": "NOT_STARTED",
        "progress": 0
      }
    ],

    "deliverables": [
      {
        "title": "현황 분석 보고서",
        "deliverableType": "ASSESSMENT",
        "status": "ACCEPTED",
        "dueDate": "2026-03-31",
        "submittedDate": "2026-03-28"
      },
      {
        "title": "AI 전략 권고안",
        "deliverableType": "RECOMMENDATION",
        "status": "IN_PROGRESS",
        "dueDate": "2026-04-30",
        "linkedPayment": 40
      },
      {
        "title": "구현 로드맵",
        "deliverableType": "ROADMAP",
        "status": "PLANNED",
        "dueDate": "2026-05-31",
        "linkedPayment": 30
      }
    ],

    "stakeholders": [
      {
        "name": "최고경영자",
        "stakeholderType": "SPONSOR",
        "influenceLevel": "HIGH",
        "interestLevel": "HIGH",
        "relationshipStatus": "CHAMPION"
      },
      {
        "name": "IT 본부장",
        "stakeholderType": "DECISION_MAKER",
        "influenceLevel": "HIGH",
        "interestLevel": "HIGH",
        "relationshipStatus": "SUPPORTER"
      }
    ],

    "latestStatusReport": {
      "reportPeriod": {
        "startDate": "2026-04-01",
        "endDate": "2026-04-15"
      },
      "overallStatus": "GREEN",
      "executiveSummary": "전략 수립 단계 순조롭게 진행 중",
      "accomplishments": [
        "이해관계자 인터뷰 12건 완료",
        "AI 활용 사례 벤치마킹 완료"
      ],
      "budgetStatus": {
        "totalBudget": { "amount": 150000000, "currency": "KRW" },
        "spent": { "amount": 60000000, "currency": "KRW" },
        "forecast": { "amount": 145000000, "currency": "KRW" },
        "variance": -3.3,
        "status": "GREEN"
      }
    }
  }
}
```

---

## 문서 정보

- **작성일**: 2026-02-27
- **버전**: 1.0
- **의존 문서**: domain.md, core_v2.md
