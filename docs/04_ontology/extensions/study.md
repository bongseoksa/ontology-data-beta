# Extension: Learning Study

---

## 1. 개요

### 1.1 목적
Domain Ontology의 `Study`를 학습 스터디 맥락으로 확장하여
커리큘럼, 과제, 발표, 평가 체계를 상세하게 모델링

### 1.2 확장 구조

```
Domain:Study (domain.md)
    └── extends → LearningStudy
                      ├── hasCurriculum → Curriculum (core_v2.md)
                      ├── hasAssignment → Assignment
                      ├── hasPresentation → Presentation
                      ├── hasLearningObjective → LearningObjective
                      └── hasAssessment → Assessment
```

---

## 2. LearningStudy

### 2.1 Class 정의

```yaml
Class: LearningStudy
  Extends: Domain:Study

  Properties:
    - learningFormat: LearningFormat (enum)
    - assessmentMethod: AssessmentMethod (enum)
    - completionCriteria: CompletionCriteria (embedded)
    - certificateIssued: Boolean
    - recordingAvailable: Boolean

  Enums:
    LearningFormat:
      - LECTURE_BASED        # 강의 중심
      - DISCUSSION_BASED     # 토론 중심
      - PROJECT_BASED        # 프로젝트 중심
      - HANDS_ON             # 실습 중심
      - SELF_PACED           # 자기주도형
      - BLENDED              # 혼합형

    AssessmentMethod:
      - PRESENTATION         # 발표
      - QUIZ                 # 퀴즈
      - ASSIGNMENT           # 과제
      - PEER_REVIEW          # 피어 리뷰
      - PROJECT_DEMO         # 프로젝트 시연
      - NONE                 # 평가 없음

  Embedded:
    CompletionCriteria:
      minAttendance: Percentage     # 최소 출석률 (예: 80%)
      minAssignmentSubmission: Percentage  # 최소 과제 제출률
      minScore: Integer (nullable)  # 최소 점수 (평가 있는 경우)
      requiredPresentation: Boolean # 발표 필수 여부

  Relationships:
    - hasCurriculum: Curriculum (1:1)
    - hasAssignment: Assignment (1:N)
    - hasPresentation: Presentation (1:N)
    - hasLearningObjective: LearningObjective (1:N)
    - hasAssessment: Assessment (0:N)
```

---

## 3. LearningObjective (학습 목표)

### 3.1 Class 정의

```yaml
Class: LearningObjective
  Description: 스터디의 학습 목표

  Properties:
    - objectiveId: String (PK)
    - order: Integer
    - title: String
    - description: String
    - category: ObjectiveCategory (enum)
    - measurable: Boolean
    - successCriteria: String

  Enums:
    ObjectiveCategory:
      - KNOWLEDGE            # 지식 습득
      - SKILL                # 기술 습득
      - APPLICATION          # 적용 능력
      - ANALYSIS             # 분석 능력
      - SYNTHESIS            # 종합 능력
      - EVALUATION           # 평가 능력

  Relationships:
    - belongsTo: LearningStudy (N:1)
    - mappedTo: CurriculumItem (N:N)
```

---

## 4. Assignment (과제)

### 4.1 Class 정의

```yaml
Class: Assignment
  Description: 스터디 과제

  Properties:
    - assignmentId: String (PK)
    - order: Integer
    - title: String
    - description: String
    - assignmentType: AssignmentType (enum)
    - dueDate: DateTime
    - duration: Duration (nullable)  # 예상 소요 시간
    - submissionType: SubmissionType (enum)
    - maxScore: Integer (nullable)
    - isRequired: Boolean
    - rubric: Rubric (embedded, nullable)

  Enums:
    AssignmentType:
      - READING              # 읽기 과제
      - WRITING              # 작성 과제 (블로그, 정리 등)
      - CODING               # 코딩 과제
      - RESEARCH             # 리서치/조사
      - PRACTICE             # 실습/연습
      - PROJECT              # 미니 프로젝트
      - REVIEW               # 코드/문서 리뷰

    SubmissionType:
      - DOCUMENT             # 문서 (PDF, Word)
      - CODE                 # 코드 (GitHub 링크, 파일)
      - PRESENTATION         # 발표 자료
      - LINK                 # URL 링크
      - VIDEO                # 영상
      - MULTIPLE             # 복합

  Embedded:
    Rubric:
      criteria: RubricCriteria[]

    RubricCriteria:
      name: String
      description: String
      maxPoints: Integer
      levels: RubricLevel[]

    RubricLevel:
      level: String          # 예: "Excellent", "Good", "Needs Improvement"
      points: Integer
      description: String

  Relationships:
    - belongsTo: LearningStudy (N:1)
    - linkedToSession: Session (N:1, nullable)
    - coversObjective: LearningObjective (N:N)
    - hasSubmission: AssignmentSubmission (1:N)
```

### 4.2 AssignmentSubmission (과제 제출)

```yaml
Class: AssignmentSubmission
  Description: 참여자의 과제 제출

  Properties:
    - submissionId: String (PK)
    - submittedAt: DateTime
    - content: String (nullable)     # 텍스트 내용
    - attachments: Attachment[]      # 첨부 파일
    - linkUrl: String (nullable)     # 제출 링크
    - status: SubmissionStatus (enum)
    - score: Integer (nullable)
    - feedback: String (nullable)
    - reviewedAt: DateTime (nullable)
    - reviewedBy: String (nullable)  # 리뷰어 ID

  Enums:
    SubmissionStatus:
      - NOT_SUBMITTED        # 미제출
      - SUBMITTED            # 제출됨
      - LATE                 # 지각 제출
      - REVIEWED             # 리뷰 완료
      - NEEDS_REVISION       # 수정 필요
      - ACCEPTED             # 승인됨

  Embedded:
    Attachment:
      fileName: String
      fileType: String
      fileSize: Integer
      fileUrl: String

  Relationships:
    - forAssignment: Assignment (N:1)
    - submittedBy: Participant (N:1)
    - hasPeerReview: PeerReview (1:N)
```

---

## 5. Presentation (발표)

### 5.1 Class 정의

```yaml
Class: Presentation
  Description: 스터디 발표

  Properties:
    - presentationId: String (PK)
    - title: String
    - description: String (nullable)
    - presentationType: PresentationType (enum)
    - scheduledDate: DateTime
    - duration: Duration             # 발표 시간
    - status: PresentationStatus (enum)
    - materials: Material[]          # 발표 자료
    - recordingUrl: String (nullable)

  Enums:
    PresentationType:
      - TOPIC_PRESENTATION   # 주제 발표
      - PAPER_REVIEW         # 논문/아티클 리뷰
      - PROJECT_DEMO         # 프로젝트 시연
      - LIVE_CODING          # 라이브 코딩
      - LIGHTNING_TALK       # 라이트닝 토크 (5-10분)
      - DISCUSSION_LEAD      # 토론 리딩

    PresentationStatus:
      - SCHEDULED            # 예정
      - IN_PROGRESS          # 진행 중
      - COMPLETED            # 완료
      - CANCELLED            # 취소
      - RESCHEDULED          # 일정 변경

  Embedded:
    Material:
      materialType: MaterialType (SLIDE, DOCUMENT, CODE, VIDEO, LINK)
      title: String
      url: String
      description: String (nullable)

  Relationships:
    - belongsTo: LearningStudy (N:1)
    - presentedIn: Session (N:1)
    - presentedBy: Participant (N:N)  # 공동 발표 가능
    - coversContent: CurriculumItem (N:N)
    - hasFeedback: PresentationFeedback (1:N)
```

### 5.2 PresentationFeedback

```yaml
Class: PresentationFeedback
  Description: 발표에 대한 피드백

  Properties:
    - feedbackId: String (PK)
    - overallRating: Integer (1-5)
    - contentRating: Integer (1-5)
    - deliveryRating: Integer (1-5)
    - comment: String
    - isAnonymous: Boolean
    - createdAt: DateTime

  Relationships:
    - forPresentation: Presentation (N:1)
    - givenBy: Participant (N:1)
```

---

## 6. Assessment (평가)

### 6.1 Class 정의

```yaml
Class: Assessment
  Description: 스터디 평가 (퀴즈, 테스트 등)

  Properties:
    - assessmentId: String (PK)
    - title: String
    - assessmentType: AssessmentType (enum)
    - description: String
    - scheduledAt: DateTime
    - duration: Duration
    - totalPoints: Integer
    - passingScore: Integer
    - isRequired: Boolean
    - questions: Question[]

  Enums:
    AssessmentType:
      - QUIZ                 # 퀴즈
      - MIDTERM_TEST         # 중간 테스트
      - FINAL_TEST           # 최종 테스트
      - SELF_ASSESSMENT      # 자가 평가
      - PEER_ASSESSMENT      # 피어 평가

  Embedded:
    Question:
      questionId: String
      questionType: QuestionType (MULTIPLE_CHOICE, SHORT_ANSWER, ESSAY, CODING)
      content: String
      points: Integer
      options: String[] (nullable)    # 객관식의 경우
      correctAnswer: String (nullable) # 자동 채점용

  Relationships:
    - belongsTo: LearningStudy (N:1)
    - linkedToSession: Session (N:1, nullable)
    - hasResult: AssessmentResult (1:N)
```

### 6.2 AssessmentResult

```yaml
Class: AssessmentResult
  Description: 평가 결과

  Properties:
    - resultId: String (PK)
    - score: Integer
    - percentage: Percentage
    - passed: Boolean
    - completedAt: DateTime
    - timeSpent: Duration
    - answers: Answer[]

  Embedded:
    Answer:
      questionId: String
      answer: String
      isCorrect: Boolean (nullable)
      points: Integer

  Relationships:
    - forAssessment: Assessment (N:1)
    - takenBy: Participant (N:1)
```

---

## 7. PeerReview (피어 리뷰)

### 7.1 Class 정의

```yaml
Class: PeerReview
  Description: 참여자 간 상호 리뷰

  Properties:
    - reviewId: String (PK)
    - reviewType: ReviewType (enum)
    - overallRating: Integer (1-5)
    - content: String
    - strengths: String[]
    - improvements: String[]
    - isAnonymous: Boolean
    - createdAt: DateTime

  Enums:
    ReviewType:
      - ASSIGNMENT_REVIEW    # 과제 리뷰
      - CODE_REVIEW          # 코드 리뷰
      - PRESENTATION_REVIEW  # 발표 리뷰

  Relationships:
    - forSubmission: AssignmentSubmission (N:1, nullable)
    - forPresentation: Presentation (N:1, nullable)
    - reviewedBy: Participant (N:1)
    - reviewee: Participant (N:1)
```

---

## 8. StudyProgress (학습 진행 현황)

### 8.1 Class 정의

```yaml
Class: StudyProgress
  Description: 참여자별 학습 진행 현황

  Properties:
    - progressId: String (PK)
    - overallProgress: Percentage
    - attendanceRate: Percentage
    - assignmentCompletionRate: Percentage
    - averageScore: Decimal (nullable)
    - status: ProgressStatus (enum)
    - lastActivityAt: DateTime
    - completedAt: DateTime (nullable)
    - certificateIssuedAt: DateTime (nullable)

  Enums:
    ProgressStatus:
      - ON_TRACK             # 정상 진행
      - AT_RISK              # 주의 필요
      - BEHIND               # 뒤처짐
      - COMPLETED            # 완료
      - DROPPED              # 중도 포기

  Derived Properties:
    - completedSessions: Integer
    - totalSessions: Integer
    - submittedAssignments: Integer
    - totalAssignments: Integer
    - completedPresentations: Integer

  Relationships:
    - forStudy: LearningStudy (N:1)
    - forParticipant: Participant (N:1)
```

---

## 9. 관계 다이어그램

```
┌────────────────────────────────────────────────────────────────┐
│                      LearningStudy                              │
│  (extends Domain:Study)                                         │
│                                                                 │
│  ┌────────────────┐    ┌────────────────┐                      │
│  │LearningObjective│    │   Curriculum   │ (from core_v2.md)   │
│  │                │    │                │                      │
│  │ - category     │    │ - items        │                      │
│  │ - criteria     │    │ - duration     │                      │
│  └───────┬────────┘    └───────┬────────┘                      │
│          │                     │                                │
│          │ maps to             │ covers                        │
│          ▼                     ▼                                │
│  ┌────────────────┐    ┌────────────────┐    ┌──────────────┐ │
│  │   Assignment   │    │  Presentation  │    │  Assessment  │ │
│  │                │    │                │    │              │ │
│  │ - dueDate      │    │ - scheduledDate│    │ - totalPoints│ │
│  │ - rubric       │    │ - duration     │    │ - questions  │ │
│  └───────┬────────┘    └───────┬────────┘    └──────┬───────┘ │
│          │                     │                     │         │
│          │ has                 │ has                 │ has     │
│          ▼                     ▼                     ▼         │
│  ┌────────────────┐    ┌────────────────┐    ┌──────────────┐ │
│  │   Submission   │    │   Feedback     │    │    Result    │ │
│  │                │    │                │    │              │ │
│  │ - score        │    │ - rating       │    │ - score      │ │
│  │ - status       │    │ - comment      │    │ - passed     │ │
│  └───────┬────────┘    └────────────────┘    └──────────────┘ │
│          │                                                      │
│          │ reviewed by                                          │
│          ▼                                                      │
│  ┌────────────────┐                        ┌──────────────────┐│
│  │   PeerReview   │                        │  StudyProgress   ││
│  │                │                        │                  ││
│  │ - strengths    │                        │ - attendance %   ││
│  │ - improvements │                        │ - completion %   ││
│  └────────────────┘                        └──────────────────┘│
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 10. JSON 예시

```json
{
  "learningStudy": {
    "activityId": "STUDY-2026-001",
    "activityName": "Claude API 심화 스터디",
    "activityType": "STUDY",
    "studyType": "TECH_STUDY",
    "learningFormat": "HANDS_ON",
    "assessmentMethod": "ASSIGNMENT",
    "maxParticipants": 15,
    "isRecurring": true,
    "recurringPattern": "WEEKLY",

    "completionCriteria": {
      "minAttendance": 80,
      "minAssignmentSubmission": 70,
      "requiredPresentation": true
    },

    "learningObjectives": [
      {
        "order": 1,
        "title": "Claude API 기본 개념 이해",
        "category": "KNOWLEDGE",
        "measurable": true
      },
      {
        "order": 2,
        "title": "Tool Use 구현 능력",
        "category": "SKILL",
        "measurable": true
      }
    ],

    "assignments": [
      {
        "order": 1,
        "title": "첫 번째 Claude API 호출",
        "assignmentType": "CODING",
        "dueDate": "2026-03-15T23:59:00",
        "submissionType": "CODE",
        "isRequired": true
      },
      {
        "order": 2,
        "title": "Tool Use 실습",
        "assignmentType": "PROJECT",
        "dueDate": "2026-03-22T23:59:00",
        "submissionType": "MULTIPLE",
        "isRequired": true
      }
    ],

    "presentations": [
      {
        "title": "Claude API 활용 사례 발표",
        "presentationType": "TOPIC_PRESENTATION",
        "duration": { "value": 15, "unit": "MINUTE" }
      }
    ]
  },

  "participantProgress": {
    "participantId": "PART-001",
    "overallProgress": 65,
    "attendanceRate": 87.5,
    "assignmentCompletionRate": 75,
    "status": "ON_TRACK",
    "completedSessions": 7,
    "totalSessions": 8
  }
}
```

---

## 문서 정보

- **작성일**: 2026-02-27
- **버전**: 1.0
- **의존 문서**: domain.md, core_v2.md
