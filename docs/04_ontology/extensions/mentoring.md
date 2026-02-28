# Extension: Coaching Mentoring

---

## 1. 개요

### 1.1 목적
Domain Ontology의 `Mentoring`을 코칭/멘토링 맥락으로 확장하여
멘토-멘티 관계, 목표 설정, 피드백, 진행 추적을 상세하게 모델링

### 1.2 확장 구조

```
Domain:Mentoring (domain.md)
    └── extends → CoachingMentoring
                      ├── hasGoal → MentoringGoal
                      ├── hasFeedback → MentoringFeedback
                      ├── hasActionItem → ActionItem
                      ├── hasProgressTracking → ProgressTracking
                      └── hasAgreement → MentoringAgreement
```

---

## 2. CoachingMentoring

### 2.1 Class 정의

```yaml
Class: CoachingMentoring
  Extends: Domain:Mentoring

  Properties:
    - coachingStyle: CoachingStyle (enum)
    - programStructure: ProgramStructure (enum)
    - matchingMethod: MatchingMethod (enum)
    - communicationChannels: CommunicationChannel[]
    - sessionFormat: SessionFormat (enum)
    - confidentialityAgreed: Boolean

  Enums:
    CoachingStyle:
      - DIRECTIVE            # 지시적 - 멘토가 방향 제시
      - FACILITATIVE         # 촉진적 - 멘티 스스로 발견 유도
      - COLLABORATIVE        # 협력적 - 함께 문제 해결
      - TRANSFORMATIONAL     # 변혁적 - 근본적 관점 변화
      - SITUATIONAL          # 상황적 - 상황에 따라 조절

    ProgramStructure:
      - STRUCTURED           # 구조화된 커리큘럼
      - SEMI_STRUCTURED      # 반구조화 (프레임워크 + 유연성)
      - UNSTRUCTURED         # 비구조화 (멘티 주도)

    MatchingMethod:
      - SELF_SELECTED        # 멘티가 멘토 선택
      - ADMIN_MATCHED        # 운영자 매칭
      - ALGORITHM_MATCHED    # 알고리즘 매칭
      - MUTUAL_SELECTION     # 상호 선택

    CommunicationChannel:
      - VIDEO_CALL           # 화상 통화
      - VOICE_CALL           # 음성 통화
      - IN_PERSON            # 대면
      - CHAT                 # 메시지/채팅
      - EMAIL                # 이메일
      - ASYNC_VIDEO          # 비동기 영상

    SessionFormat:
      - REGULAR              # 정기 세션
      - ON_DEMAND            # 필요 시
      - INTENSIVE            # 집중 세션
      - MIXED                # 혼합

  Relationships:
    - hasMentor: Participant (1:1)
    - hasMentee: Participant (1:N)
    - hasGoal: MentoringGoal (1:N)
    - hasFeedback: MentoringFeedback (1:N)
    - hasActionItem: ActionItem (1:N)
    - hasProgressTracking: ProgressTracking (1:1)
    - hasAgreement: MentoringAgreement (0:1)
```

---

## 3. MentoringGoal (멘토링 목표)

### 3.1 Class 정의

```yaml
Class: MentoringGoal
  Description: 멘토링의 구체적 목표

  Properties:
    - goalId: String (PK)
    - title: String
    - description: String
    - goalType: GoalType (enum)
    - category: GoalCategory (enum)
    - targetDate: Date
    - priority: Priority (enum)
    - status: GoalStatus (enum)
    - progress: Percentage
    - measurableCriteria: String[]     # 측정 가능한 기준
    - milestones: GoalMilestone[]

  Enums:
    GoalType:
      - OUTCOME_GOAL         # 결과 목표 (달성할 것)
      - PROCESS_GOAL         # 과정 목표 (수행할 것)
      - LEARNING_GOAL        # 학습 목표 (배울 것)
      - BEHAVIOR_GOAL        # 행동 변화 목표

    GoalCategory:
      - TECHNICAL            # 기술 역량
      - CAREER               # 커리어 개발
      - LEADERSHIP           # 리더십
      - COMMUNICATION        # 커뮤니케이션
      - PROBLEM_SOLVING      # 문제 해결
      - PROJECT_MANAGEMENT   # 프로젝트 관리
      - PERSONAL_GROWTH      # 개인 성장
      - WORK_LIFE_BALANCE    # 워라밸

    Priority:
      - HIGH
      - MEDIUM
      - LOW

    GoalStatus:
      - NOT_STARTED          # 시작 전
      - IN_PROGRESS          # 진행 중
      - ON_HOLD              # 보류
      - ACHIEVED             # 달성
      - MODIFIED             # 수정됨
      - ABANDONED            # 포기

  Embedded:
    GoalMilestone:
      title: String
      targetDate: Date
      completed: Boolean
      completedAt: DateTime (nullable)
      notes: String (nullable)

  Relationships:
    - belongsTo: CoachingMentoring (N:1)
    - setBy: Participant (N:1)         # 누가 설정했는지
    - trackedIn: ActionItem (1:N)
```

---

## 4. MentoringFeedback (멘토링 피드백)

### 4.1 Class 정의

```yaml
Class: MentoringFeedback
  Description: 세션별 또는 전체 멘토링에 대한 피드백

  Properties:
    - feedbackId: String (PK)
    - feedbackType: FeedbackType (enum)
    - direction: FeedbackDirection (enum)
    - sessionId: String (nullable)     # 세션별 피드백인 경우
    - content: String
    - strengths: String[]
    - areasForImprovement: String[]
    - actionableInsights: String[]
    - overallRating: Integer (1-5)
    - wouldRecommend: Boolean (nullable)
    - isAnonymous: Boolean
    - createdAt: DateTime

  Enums:
    FeedbackType:
      - SESSION_FEEDBACK     # 개별 세션 피드백
      - PROGRESS_FEEDBACK    # 진행 상황 피드백
      - MIDTERM_REVIEW       # 중간 리뷰
      - FINAL_REVIEW         # 최종 리뷰
      - GENERAL              # 일반 피드백

    FeedbackDirection:
      - MENTOR_TO_MENTEE     # 멘토 → 멘티
      - MENTEE_TO_MENTOR     # 멘티 → 멘토
      - SELF_REFLECTION      # 자기 성찰

  Relationships:
    - forMentoring: CoachingMentoring (N:1)
    - forSession: Session (N:1, nullable)
    - givenBy: Participant (N:1)
    - givenTo: Participant (N:1)
```

---

## 5. ActionItem (실행 항목)

### 5.1 Class 정의

```yaml
Class: ActionItem
  Description: 세션에서 도출된 실행 항목

  Properties:
    - actionId: String (PK)
    - title: String
    - description: String
    - actionType: ActionType (enum)
    - assignedTo: String             # Participant ID
    - dueDate: Date
    - priority: Priority (enum)
    - status: ActionStatus (enum)
    - completedAt: DateTime (nullable)
    - evidence: String (nullable)    # 완료 증거/결과물
    - blockers: String[]             # 장애 요소

  Enums:
    ActionType:
      - LEARNING             # 학습 과제
      - PRACTICE             # 실습 과제
      - REFLECTION           # 성찰 과제
      - NETWORKING           # 네트워킹
      - PROJECT_WORK         # 프로젝트 작업
      - READING              # 읽기
      - CONVERSATION         # 대화/미팅
      - EXPERIMENT           # 실험/시도

    ActionStatus:
      - NOT_STARTED
      - IN_PROGRESS
      - BLOCKED
      - COMPLETED
      - CANCELLED
      - DEFERRED

  Relationships:
    - belongsTo: CoachingMentoring (N:1)
    - derivedFromSession: Session (N:1, nullable)
    - supportsGoal: MentoringGoal (N:N)
    - assignedTo: Participant (N:1)
```

---

## 6. ProgressTracking (진행 추적)

### 6.1 Class 정의

```yaml
Class: ProgressTracking
  Description: 멘토링 전체 진행 상황 추적

  Properties:
    - trackingId: String (PK)
    - overallProgress: Percentage
    - goalsAchieved: Integer
    - totalGoals: Integer
    - sessionsCompleted: Integer
    - totalSessions: Integer
    - actionItemsCompleted: Integer
    - totalActionItems: Integer
    - currentPhase: MentoringPhase (enum)
    - healthStatus: HealthStatus (enum)
    - lastReviewDate: Date
    - nextReviewDate: Date
    - notes: String

  Enums:
    MentoringPhase:
      - ONBOARDING           # 온보딩 (관계 구축)
      - EXPLORATION          # 탐색 (목표 설정)
      - DEVELOPMENT          # 개발 (실행)
      - EVALUATION           # 평가
      - TRANSITION           # 전환 (종료 준비)
      - COMPLETED            # 완료

    HealthStatus:
      - EXCELLENT            # 매우 좋음
      - GOOD                 # 좋음
      - AT_RISK              # 주의 필요
      - STRUGGLING           # 어려움
      - INACTIVE             # 비활성

  Relationships:
    - forMentoring: CoachingMentoring (1:1)
    - hasCheckpoint: ProgressCheckpoint (1:N)
```

### 6.2 ProgressCheckpoint

```yaml
Class: ProgressCheckpoint
  Description: 정기 진행 점검

  Properties:
    - checkpointId: String (PK)
    - checkpointDate: Date
    - checkpointType: CheckpointType (enum)
    - progressSummary: String
    - challengesFaced: String[]
    - lessonLearned: String[]
    - nextSteps: String[]
    - satisfactionMentor: Integer (1-5)
    - satisfactionMentee: Integer (1-5)

  Enums:
    CheckpointType:
      - WEEKLY_CHECK         # 주간 체크
      - MONTHLY_REVIEW       # 월간 리뷰
      - QUARTERLY_REVIEW     # 분기 리뷰
      - MILESTONE_REVIEW     # 마일스톤 리뷰
      - AD_HOC               # 비정기

  Relationships:
    - belongsTo: ProgressTracking (N:1)
```

---

## 7. MentoringAgreement (멘토링 합의서)

### 7.1 Class 정의

```yaml
Class: MentoringAgreement
  Description: 멘토-멘티 간 합의 사항

  Properties:
    - agreementId: String (PK)
    - agreedOn: Date
    - validUntil: Date
    - expectations: AgreementExpectation (embedded)
    - commitments: AgreementCommitment (embedded)
    - boundaries: String[]           # 경계 설정
    - confidentialityTerms: String
    - communicationPreferences: CommunicationPreference (embedded)
    - escalationProcess: String
    - terminationClause: String

  Embedded:
    AgreementExpectation:
      mentorExpectations: String[]   # 멘토가 기대하는 것
      menteeExpectations: String[]   # 멘티가 기대하는 것

    AgreementCommitment:
      mentorCommitments: String[]    # 멘토의 약속
      menteeCommitments: String[]    # 멘티의 약속

    CommunicationPreference:
      preferredChannels: CommunicationChannel[]
      responseTimeExpectation: String
      meetingFrequency: String
      cancellationPolicy: String

  Relationships:
    - forMentoring: CoachingMentoring (1:1)
    - signedByMentor: Participant (N:1)
    - signedByMentee: Participant (N:1)
```

---

## 8. MentoringSession (멘토링 세션 확장)

### 8.1 Class 정의 (Core:Session 확장)

```yaml
Class: MentoringSession
  Extends: Core:Session
  Description: 멘토링 세션 특화 속성

  Additional Properties:
    - sessionObjective: String       # 세션 목표
    - preSessionPrep: String[]       # 사전 준비 사항
    - topicsDiscussed: String[]      # 논의 주제
    - keyInsights: String[]          # 핵심 인사이트
    - actionItemsCreated: Integer    # 생성된 액션 아이템 수
    - menteeEnergy: Integer (1-5)    # 멘티 에너지 레벨
    - sessionEffectiveness: Integer (1-5)  # 세션 효과성

  Relationships:
    - hasActionItem: ActionItem (1:N)
    - hasFeedback: MentoringFeedback (1:N)
```

---

## 9. 관계 다이어그램

```
┌────────────────────────────────────────────────────────────────┐
│                    CoachingMentoring                            │
│  (extends Domain:Mentoring)                                     │
│                                                                 │
│  ┌────────────────┐                    ┌────────────────┐      │
│  │MentoringAgreement│                  │ProgressTracking │      │
│  │                │                    │                │      │
│  │ - expectations │                    │ - progress %   │      │
│  │ - commitments  │                    │ - health       │      │
│  └────────────────┘                    └───────┬────────┘      │
│                                                │               │
│                                                │ has           │
│                                                ▼               │
│  ┌────────────────┐    ┌────────────────┐ ┌────────────────┐  │
│  │ MentoringGoal  │    │  ActionItem    │ │ProgressCheckpoint│ │
│  │                │◄───│                │ │                │  │
│  │ - milestones   │    │ - dueDate      │ │ - summary      │  │
│  │ - progress     │    │ - status       │ │ - satisfaction │  │
│  └───────┬────────┘    └───────┬────────┘ └────────────────┘  │
│          │                     │                               │
│          │ tracked by          │ derived from                  │
│          ▼                     ▼                               │
│  ┌────────────────────────────────────────────────────────┐   │
│  │                  MentoringSession                       │   │
│  │  (extends Core:Session)                                 │   │
│  │                                                         │   │
│  │  - sessionObjective                                     │   │
│  │  - topicsDiscussed                                      │   │
│  │  - keyInsights                                          │   │
│  └────────────────────────────────────────────────────────┘   │
│                              │                                 │
│                              │ has                             │
│                              ▼                                 │
│                    ┌────────────────┐                         │
│                    │MentoringFeedback│                         │
│                    │                │                         │
│                    │ - strengths    │                         │
│                    │ - improvements │                         │
│                    └────────────────┘                         │
│                                                                 │
│  ┌─────────┐           ┌─────────┐                            │
│  │ Mentor  │───────────│ Mentee  │                            │
│  │(Participant)        │(Participant)                          │
│  └─────────┘           └─────────┘                            │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 10. JSON 예시

```json
{
  "coachingMentoring": {
    "activityId": "MENTOR-2026-001",
    "activityName": "시니어 개발자 커리어 멘토링",
    "activityType": "MENTORING",
    "mentoringType": "ONE_ON_ONE",
    "coachingStyle": "COLLABORATIVE",
    "programStructure": "SEMI_STRUCTURED",
    "sessionFormat": "REGULAR",
    "frequency": "BIWEEKLY",
    "totalSessions": 12,

    "mentor": {
      "participantId": "PART-M001",
      "name": "김멘토",
      "role": "MENTOR",
      "expertise": ["Backend", "Architecture", "Career Development"]
    },

    "mentee": {
      "participantId": "PART-E001",
      "name": "이멘티",
      "role": "MENTEE",
      "currentLevel": "Mid-level Developer",
      "targetLevel": "Senior Developer"
    },

    "goals": [
      {
        "goalId": "GOAL-001",
        "title": "시스템 설계 역량 강화",
        "goalType": "LEARNING_GOAL",
        "category": "TECHNICAL",
        "targetDate": "2026-06-30",
        "progress": 40,
        "status": "IN_PROGRESS",
        "measurableCriteria": [
          "설계 문서 3개 이상 작성",
          "코드 리뷰 피드백 반영",
          "아키텍처 발표 1회"
        ]
      },
      {
        "goalId": "GOAL-002",
        "title": "리더십 경험 쌓기",
        "goalType": "BEHAVIOR_GOAL",
        "category": "LEADERSHIP",
        "targetDate": "2026-08-31",
        "progress": 20,
        "status": "IN_PROGRESS"
      }
    ],

    "progressTracking": {
      "overallProgress": 35,
      "goalsAchieved": 0,
      "totalGoals": 2,
      "sessionsCompleted": 4,
      "totalSessions": 12,
      "actionItemsCompleted": 8,
      "totalActionItems": 15,
      "currentPhase": "DEVELOPMENT",
      "healthStatus": "GOOD"
    },

    "recentSession": {
      "sessionNumber": 4,
      "sessionObjective": "설계 패턴 리뷰 및 적용 방안 논의",
      "topicsDiscussed": [
        "현재 프로젝트 아키텍처 리뷰",
        "SOLID 원칙 적용 사례"
      ],
      "keyInsights": [
        "의존성 역전 원칙 적용 필요",
        "모듈 분리 전략 수립"
      ],
      "actionItemsCreated": 3,
      "sessionEffectiveness": 4
    }
  }
}
```

---

## 문서 정보

- **작성일**: 2026-02-27
- **버전**: 1.0
- **의존 문서**: domain.md, core_v2.md
