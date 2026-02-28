# Phase 7: 문서 분석 레이어 설계

---

## 1. 문서 분석 레이어 개요

### 1.1 목적
사용자가 업로드한 **비정형 사업계획서**를 분석하여 **구조화된 프로젝트 데이터**로 변환

### 1.2 처리 흐름

```
[입력]
사업계획서 (PDF, DOCX, TXT)
         │
         ▼
┌─────────────────────┐
│  Document Parsing   │  파일 형식별 텍스트 추출
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Text Preprocessing │  텍스트 정제 및 전처리
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Information        │  LLM 기반 정보 추출
│  Extraction         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Schema Mapping     │  온톨로지 스키마 매핑
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Validation         │  데이터 검증 및 보완
└──────────┬──────────┘
           │
           ▼
[출력]
구조화된 프로젝트 JSON
```

---

## 2. 입력 형식 지원

### 2.1 지원 파일 형식

| 형식 | 확장자 | 처리 방법 | 비고 |
|------|--------|----------|------|
| PDF | .pdf | PyPDF2, pdfplumber | OCR 지원 포함 |
| Word | .docx, .doc | python-docx | 표, 이미지 처리 |
| Text | .txt | 직접 읽기 | UTF-8 인코딩 |
| HTML | .html | BeautifulSoup | 웹 콘텐츠 |

### 2.2 문서 파싱 로직

```python
def parse_document(file_path: str) -> str:
    """
    파일 형식에 따른 텍스트 추출
    """
    extension = file_path.split('.')[-1].lower()

    if extension == 'pdf':
        return parse_pdf(file_path)
    elif extension in ['docx', 'doc']:
        return parse_word(file_path)
    elif extension == 'txt':
        return parse_text(file_path)
    elif extension == 'html':
        return parse_html(file_path)
    else:
        raise UnsupportedFormatError(f"지원하지 않는 형식: {extension}")


def parse_pdf(file_path: str) -> str:
    """PDF 파일 파싱"""
    import pdfplumber

    text_content = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)

            # 표 추출
            tables = page.extract_tables()
            for table in tables:
                text_content.append(format_table(table))

    return '\n\n'.join(text_content)
```

---

## 3. 추출 대상 정보

### 3.1 추출 항목 정의

| 카테고리 | 추출 항목 | 필수 여부 | 데이터 타입 |
|----------|----------|:--------:|------------|
| **프로젝트 기본** | 프로젝트명 | 필수 | String |
| | 프로젝트 유형 | 필수 | Enum |
| | 프로젝트 목적 | 필수 | String |
| **기능 요구사항** | 기능 목록 | 필수 | List |
| | 기능별 설명 | 권장 | String |
| | 기능 우선순위 | 권장 | Enum |
| **비기능 요구사항** | 예상 사용자 수 | 권장 | Number |
| | 데이터 규모 | 권장 | Enum |
| | 성능 요구사항 | 선택 | String |
| | 보안 요구사항 | 선택 | String |
| **일정/예산** | 희망 일정 | 권장 | Duration |
| | 예산 범위 | 선택 | Money |
| | 마일스톤 | 선택 | List |
| **기술 요구사항** | 기술 스택 | 권장 | List |
| | 연동 시스템 | 권장 | List |
| | 기존 시스템 | 선택 | String |
| **고객 정보** | 산업 분야 | 권장 | String |
| | 회사 규모 | 선택 | Enum |

### 3.2 추출 스키마

```json
{
  "project_basic": {
    "project_name": "string",
    "project_type": "NEW_DEVELOPMENT | ENHANCEMENT | MIGRATION | INTEGRATION",
    "project_purpose": "string",
    "project_description": "string"
  },

  "functional_requirements": {
    "features": [
      {
        "feature_name": "string",
        "description": "string",
        "priority": "HIGH | MEDIUM | LOW",
        "category": "string"
      }
    ],
    "modules": ["string"]
  },

  "non_functional_requirements": {
    "expected_users": "number",
    "peak_users": "number",
    "data_volume": "SMALL | MEDIUM | LARGE | VERY_LARGE",
    "performance": {
      "response_time": "string",
      "throughput": "string"
    },
    "security": {
      "level": "STANDARD | ENHANCED | HIGH",
      "requirements": ["string"]
    },
    "availability": "percentage"
  },

  "schedule_budget": {
    "desired_start_date": "date",
    "desired_end_date": "date",
    "desired_duration": {
      "value": "number",
      "unit": "MONTH | WEEK"
    },
    "budget_range": {
      "min": "number",
      "max": "number",
      "currency": "string"
    },
    "milestones": [
      {
        "name": "string",
        "target_date": "date"
      }
    ],
    "hard_deadline": "date | null"
  },

  "technical_requirements": {
    "preferred_tech_stack": ["string"],
    "required_integrations": [
      {
        "system_name": "string",
        "integration_type": "API | DB | FILE",
        "description": "string"
      }
    ],
    "existing_systems": {
      "has_legacy": "boolean",
      "legacy_description": "string"
    },
    "deployment": {
      "environment": "CLOUD | ON_PREMISE | HYBRID",
      "cloud_provider": "string"
    }
  },

  "client_context": {
    "industry": "string",
    "company_size": "STARTUP | SMB | ENTERPRISE | PUBLIC",
    "it_maturity": "LOW | MEDIUM | HIGH",
    "stakeholders": ["string"]
  },

  "constraints": {
    "regulatory": ["string"],
    "technical": ["string"],
    "resource": ["string"]
  },

  "metadata": {
    "extraction_timestamp": "datetime",
    "extraction_confidence": "float",
    "source_document": "string",
    "missing_fields": ["string"]
  }
}
```

---

## 4. LLM 기반 정보 추출

### 4.1 추출 프롬프트 설계

```
[System Prompt]
당신은 사업계획서 분석 전문가입니다.
제공된 문서에서 소프트웨어 프로젝트 관련 정보를 추출합니다.

추출 원칙:
1. 문서에 명시된 정보만 추출 (추론 금지)
2. 불확실한 정보는 confidence 표시
3. 누락된 정보는 null로 표시
4. 지정된 JSON 스키마 엄격 준수

[User Prompt]
## 사업계획서 내용
{document_text}

## 추출 요청
위 문서에서 다음 정보를 추출해주세요:
1. 프로젝트 기본 정보 (이름, 유형, 목적)
2. 기능 요구사항 (기능 목록, 설명, 우선순위)
3. 비기능 요구사항 (사용자 수, 성능, 보안)
4. 일정 및 예산
5. 기술 요구사항 (기술 스택, 연동 시스템)
6. 고객/산업 정보

결과를 지정된 JSON 스키마로 출력해주세요.
```

### 4.2 추출 파이프라인

```python
def extract_information(document_text: str) -> dict:
    """
    LLM 기반 정보 추출 함수
    """
    # 1. 문서 분할 (긴 문서의 경우)
    chunks = split_document(document_text, max_tokens=4000)

    # 2. 각 청크에서 정보 추출
    extracted_parts = []
    for chunk in chunks:
        prompt = build_extraction_prompt(chunk)
        response = llm.generate(prompt, schema=EXTRACTION_SCHEMA)
        extracted_parts.append(response)

    # 3. 추출 결과 병합
    merged_result = merge_extractions(extracted_parts)

    # 4. 후처리 및 정규화
    normalized_result = normalize_extraction(merged_result)

    # 5. 신뢰도 점수 계산
    normalized_result['metadata']['extraction_confidence'] = (
        calculate_confidence(normalized_result)
    )

    return normalized_result


def calculate_confidence(extracted_data: dict) -> float:
    """
    추출 신뢰도 계산
    """
    required_fields = [
        'project_basic.project_name',
        'project_basic.project_type',
        'functional_requirements.features'
    ]

    filled_required = sum(
        1 for field in required_fields
        if get_nested_value(extracted_data, field) is not None
    )

    recommended_fields = [
        'non_functional_requirements.expected_users',
        'schedule_budget.desired_duration',
        'technical_requirements.preferred_tech_stack'
    ]

    filled_recommended = sum(
        1 for field in recommended_fields
        if get_nested_value(extracted_data, field) is not None
    )

    # 가중 평균 신뢰도
    required_score = filled_required / len(required_fields) * 0.7
    recommended_score = filled_recommended / len(recommended_fields) * 0.3

    return round(required_score + recommended_score, 2)
```

---

## 5. 스키마 매핑

### 5.1 추출 데이터 → 온톨로지 매핑

```python
def map_to_ontology(extracted_data: dict) -> dict:
    """
    추출된 데이터를 온톨로지 스키마로 매핑
    """
    return {
        "softwareProject": {
            "projectName": extracted_data['project_basic']['project_name'],
            "projectType": map_project_type(
                extracted_data['project_basic']['project_type']
            ),
            "applicationType": infer_application_type(
                extracted_data['functional_requirements']['features']
            )
        },

        "scope": {
            "features": [
                {
                    "featureName": f['feature_name'],
                    "description": f['description'],
                    "priority": f['priority'],
                    "estimatedFP": estimate_fp(f)  # FP 추정
                }
                for f in extracted_data['functional_requirements']['features']
            ],
            "totalEstimatedFP": sum(
                estimate_fp(f)
                for f in extracted_data['functional_requirements']['features']
            )
        },

        "timeline": {
            "desiredDuration": extracted_data['schedule_budget']['desired_duration'],
            "hardDeadline": extracted_data['schedule_budget'].get('hard_deadline')
        },

        "constraints": {
            "techStack": extracted_data['technical_requirements']['preferred_tech_stack'],
            "integrations": extracted_data['technical_requirements']['required_integrations'],
            "budget": extracted_data['schedule_budget'].get('budget_range')
        },

        "clientInfo": {
            "industry": extracted_data['client_context']['industry'],
            "clientType": map_company_size(
                extracted_data['client_context']['company_size']
            )
        }
    }
```

---

## 6. 검증 및 보완

### 6.1 데이터 검증 규칙

```yaml
ValidationRules:
  Required:
    - field: "project_basic.project_name"
      rule: "not_empty"
      message: "프로젝트명은 필수입니다"

    - field: "functional_requirements.features"
      rule: "array_min_length: 1"
      message: "최소 1개 이상의 기능이 필요합니다"

  Consistency:
    - rule: "start_date < end_date"
      fields: ["schedule_budget.desired_start_date", "schedule_budget.desired_end_date"]
      message: "시작일이 종료일보다 앞서야 합니다"

    - rule: "budget_min <= budget_max"
      fields: ["schedule_budget.budget_range.min", "schedule_budget.budget_range.max"]
      message: "최소 예산이 최대 예산보다 작아야 합니다"

  Reasonability:
    - rule: "duration_reasonable"
      field: "schedule_budget.desired_duration"
      range: [1, 36]
      unit: "MONTH"
      message: "프로젝트 기간이 합리적 범위를 벗어납니다"
```

### 6.2 누락 정보 처리

```python
def handle_missing_fields(extracted_data: dict) -> dict:
    """
    누락된 필드 처리 및 기본값 설정
    """
    missing_fields = []

    # 필수 필드 확인
    if not extracted_data['project_basic'].get('project_type'):
        extracted_data['project_basic']['project_type'] = 'NEW_DEVELOPMENT'
        missing_fields.append('project_type (기본값 적용)')

    # 비기능 요구사항 기본값
    if not extracted_data['non_functional_requirements'].get('expected_users'):
        # 기능 수 기반 추정
        feature_count = len(extracted_data['functional_requirements']['features'])
        if feature_count <= 10:
            extracted_data['non_functional_requirements']['expected_users'] = 100
        elif feature_count <= 30:
            extracted_data['non_functional_requirements']['expected_users'] = 500
        else:
            extracted_data['non_functional_requirements']['expected_users'] = 1000
        missing_fields.append('expected_users (기능 수 기반 추정)')

    extracted_data['metadata']['missing_fields'] = missing_fields
    return extracted_data
```

---

## 7. 출력 스키마

### 7.1 최종 출력 형식

```json
{
  "extraction_result": {
    "project": {...},
    "scope": {...},
    "timeline": {...},
    "constraints": {...},
    "clientInfo": {...}
  },

  "extraction_metadata": {
    "timestamp": "datetime",
    "confidence": "float (0-1)",
    "source_document": {
      "filename": "string",
      "format": "string",
      "pages": "number",
      "characters": "number"
    },
    "processing_info": {
      "chunks_processed": "number",
      "llm_calls": "number",
      "processing_time_ms": "number"
    },
    "quality_flags": {
      "missing_required": ["string"],
      "low_confidence_fields": ["string"],
      "inferred_values": ["string"]
    }
  },

  "validation_result": {
    "is_valid": "boolean",
    "errors": [...],
    "warnings": [...]
  }
}
```

---

## 문서 정보

- **작성일**: 2026-02-25
- **상태**: Phase 7 완료
- **다음 단계**: Phase 8 - RAG 설계
