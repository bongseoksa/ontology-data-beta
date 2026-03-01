"""
온톨로지 매핑 스키마

JSONL 데이터를 Core/Extension Ontology 구조로 변환합니다.
RAG 시스템에서 사용할 수 있는 형태로 데이터를 구조화합니다.
"""

import json
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime, timezone
from pathlib import Path


# =============================================================================
# Enumerations (Core Ontology)
# =============================================================================

class ActivityType(str, Enum):
    PROJECT = "PROJECT"
    STUDY = "STUDY"
    MENTORING = "MENTORING"
    CONSULTING = "CONSULTING"


class ActivityStatus(str, Enum):
    DRAFT = "DRAFT"
    PLANNING = "PLANNING"
    RECRUITING = "RECRUITING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"
    CANCELLED = "CANCELLED"


class CostType(str, Enum):
    LABOR = "LABOR"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    TOOL = "TOOL"
    EXTERNAL = "EXTERNAL"
    OVERHEAD = "OVERHEAD"
    TECHNICAL_FEE = "TECHNICAL_FEE"


class RoleType(str, Enum):
    PROJECT_MANAGER = "PROJECT_MANAGER"
    ARCHITECT = "ARCHITECT"
    BACKEND_DEVELOPER = "BACKEND_DEVELOPER"
    FRONTEND_DEVELOPER = "FRONTEND_DEVELOPER"
    MOBILE_DEVELOPER = "MOBILE_DEVELOPER"
    DEVOPS_ENGINEER = "DEVOPS_ENGINEER"
    QA_ENGINEER = "QA_ENGINEER"
    UI_UX_DESIGNER = "UI_UX_DESIGNER"
    DATA_ENGINEER = "DATA_ENGINEER"
    ML_ENGINEER = "ML_ENGINEER"


class SkillLevel(str, Enum):
    JUNIOR = "JUNIOR"
    MID = "MID"
    SENIOR = "SENIOR"
    EXPERT = "EXPERT"


class CompetitionLevel(str, Enum):
    MONOPOLY = "MONOPOLY"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    INTENSE = "INTENSE"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# =============================================================================
# Data Classes (Core Ontology Mapping)
# =============================================================================

@dataclass
class Money:
    """금액 타입"""
    amount: int
    currency: str = "KRW"


@dataclass
class Duration:
    """기간 타입"""
    value: int
    unit: str = "MONTH"  # MONTH, WEEK, DAY


@dataclass
class Role:
    """인력 역할 (Extension: SoftwareProject)"""
    roleType: RoleType
    skillLevel: SkillLevel
    headcount: int
    manMonth: float
    allocation: float = 100.0


@dataclass
class Scope:
    """프로젝트 범위 (Extension: SoftwareProject)"""
    totalFP: Optional[int] = None
    moduleCount: Optional[int] = None
    screenCount: Optional[int] = None
    reportCount: Optional[int] = None
    interfaceCount: Optional[int] = None


@dataclass
class Timeline:
    """프로젝트 일정"""
    duration: Duration
    startDate: Optional[str] = None
    endDate: Optional[str] = None


@dataclass
class SoftwareProject:
    """소프트웨어 프로젝트 (Extension)

    Core:Activity + Extension:SoftwareProject 매핑
    """
    # Core: Activity
    activityId: str
    activityName: str
    activityType: ActivityType = ActivityType.PROJECT
    status: ActivityStatus = ActivityStatus.DRAFT
    description: Optional[str] = None

    # Extension: SoftwareProject
    category: Optional[str] = None  # WEB, MOBILE, DATA
    systemType: Optional[str] = None  # ERP, CRM, CUSTOM
    securityLevel: Optional[str] = None
    techStack: List[str] = field(default_factory=list)

    # Scope
    scope: Optional[Scope] = None

    # Timeline
    timeline: Optional[Timeline] = None

    # Roles
    roles: List[Role] = field(default_factory=list)

    # Cost
    estimatedCost: Optional[Money] = None

    # Metadata
    source: Optional[str] = None
    sourceUrl: Optional[str] = None
    crawledAt: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리 변환"""
        result = {
            "activityId": self.activityId,
            "activityName": self.activityName,
            "activityType": self.activityType.value,
            "status": self.status.value,
        }

        if self.description:
            result["description"] = self.description
        if self.category:
            result["category"] = self.category
        if self.systemType:
            result["systemType"] = self.systemType
        if self.techStack:
            result["techStack"] = self.techStack

        if self.scope:
            result["scope"] = {
                k: v for k, v in self.scope.__dict__.items() if v is not None
            }

        if self.timeline:
            result["timeline"] = {
                "duration": {
                    "value": self.timeline.duration.value,
                    "unit": self.timeline.duration.unit,
                },
            }
            if self.timeline.startDate:
                result["timeline"]["startDate"] = self.timeline.startDate
            if self.timeline.endDate:
                result["timeline"]["endDate"] = self.timeline.endDate

        if self.roles:
            result["roles"] = [
                {
                    "roleType": r.roleType.value,
                    "skillLevel": r.skillLevel.value,
                    "headcount": r.headcount,
                    "manMonth": r.manMonth,
                }
                for r in self.roles
            ]

        if self.estimatedCost:
            result["estimatedCost"] = {
                "amount": self.estimatedCost.amount,
                "currency": self.estimatedCost.currency,
            }

        if self.source:
            result["source"] = self.source
        if self.crawledAt:
            result["crawledAt"] = self.crawledAt

        return result

    def to_jsonl(self) -> str:
        """JSONL 형식 문자열"""
        return json.dumps(self.to_dict(), ensure_ascii=False)


@dataclass
class Pricing:
    """가격 산정 결과 (Pricing Ontology)"""
    pricingId: str
    bidId: str

    # 가격 정보
    baseCost: Optional[Money] = None
    estimatedPrice: Optional[Money] = None
    winningPrice: Optional[Money] = None
    winningRate: Optional[float] = None

    # 경쟁 정보
    competitorCount: Optional[int] = None
    competitionLevel: Optional[CompetitionLevel] = None

    # 계약 정보
    contractType: Optional[str] = None
    winnerName: Optional[str] = None
    bidDate: Optional[str] = None

    # 분석 정보
    impliedMargin: Optional[float] = None
    riskLevel: Optional[RiskLevel] = None

    # Metadata
    source: Optional[str] = None
    crawledAt: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "pricingId": self.pricingId,
            "bidId": self.bidId,
        }

        if self.estimatedPrice:
            result["estimatedPrice"] = self.estimatedPrice.__dict__
        if self.winningPrice:
            result["winningPrice"] = self.winningPrice.__dict__
        if self.winningRate is not None:
            result["winningRate"] = self.winningRate
        if self.competitorCount is not None:
            result["competitorCount"] = self.competitorCount
        if self.competitionLevel:
            result["competitionLevel"] = self.competitionLevel.value
        if self.contractType:
            result["contractType"] = self.contractType
        if self.winnerName:
            result["winnerName"] = self.winnerName
        if self.bidDate:
            result["bidDate"] = self.bidDate
        if self.impliedMargin is not None:
            result["impliedMargin"] = self.impliedMargin
        if self.riskLevel:
            result["riskLevel"] = self.riskLevel.value
        if self.source:
            result["source"] = self.source
        if self.crawledAt:
            result["crawledAt"] = self.crawledAt

        return result

    def to_jsonl(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def to_quote_version_jsonld(
        self,
        requirement_set_id: str,
        evidence_urls: List[str],
        version_no: int = 1,
        assumptions: Optional[List[str]] = None,
        context_uri: Optional[str] = None,
        quote_id: Optional[str] = None,
        estimate_range: Optional["EstimateRange"] = None,
    ) -> Dict[str, Any]:
        """Pricing 인스턴스를 견적 JSON-LD(QuoteVersion + EstimateRange)로 변환"""
        graph = build_quote_version_graph_from_pricing(
            pricing=self,
            requirement_set_id=requirement_set_id,
            evidence_urls=evidence_urls,
            version_no=version_no,
            assumptions=assumptions,
            context_uri=context_uri,
            quote_id=quote_id,
            estimate_range=estimate_range,
        )
        return graph.to_dict()


@dataclass
class EstimateRange:
    """견적 범위 결과"""
    min: int
    p50: int
    p80: int
    max: int
    pointEstimate: Optional[int] = None

    def __post_init__(self):
        if self.pointEstimate is None:
            self.pointEstimate = self.p50
        if not (self.min <= self.p50 <= self.p80 <= self.max):
            raise ValueError("Invalid estimate range ordering: min <= p50 <= p80 <= max")

    def to_jsonld_node(self, node_id: str) -> Dict[str, Any]:
        return {
            "id": node_id,
            "type": "quote:EstimateRange",
            "min": self.min,
            "p50": self.p50,
            "p80": self.p80,
            "max": self.max,
            "quote:pointEstimate": self.pointEstimate,
        }


@dataclass
class QuoteVersionGraph:
    """JSON-LD 계약을 따르는 견적 버전 그래프"""
    quoteId: str
    versionNo: int
    requirementSetId: str
    estimateRange: EstimateRange
    evidenceUrls: List[str]
    assumptions: List[str] = field(default_factory=list)
    generatedAt: Optional[str] = None
    contextUri: Optional[str] = None

    def __post_init__(self):
        if not self.evidenceUrls:
            raise ValueError("evidenceUrls must contain at least one source URL")
        if self.generatedAt is None:
            self.generatedAt = _utc_now_iso()
        if self.contextUri is None:
            self.contextUri = _default_jsonld_context_uri()

    def _quote_node_id(self) -> str:
        return _ensure_node_id(self.quoteId, "quote")

    def _version_node_id(self) -> str:
        return f"{self._quote_node_id()}-v{self.versionNo}"

    def _range_node_id(self) -> str:
        return f"{self._quote_node_id()}-range-v{self.versionNo}"

    def to_dict(self) -> Dict[str, Any]:
        version_node: Dict[str, Any] = {
            "id": self._version_node_id(),
            "type": "quote:QuoteVersion",
            "versionNo": self.versionNo,
            "generatedAt": self.generatedAt,
            "derivedFromRequirementSet": _ensure_node_id(self.requirementSetId, "req"),
            "wasDerivedFrom": self.evidenceUrls,
            "quote:hasEstimateRange": self._range_node_id(),
        }

        if self.assumptions:
            version_node["usesAssumption"] = [
                _ensure_node_id(assumption, "base") for assumption in self.assumptions
            ]

        return {
            "@context": self.contextUri,
            "@graph": [
                {
                    "id": self._quote_node_id(),
                    "type": "quote:Quote",
                    "quoteId": self.quoteId,
                    "quote:hasVersion": self._version_node_id(),
                },
                version_node,
                self.estimateRange.to_jsonld_node(self._range_node_id()),
            ],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


@dataclass
class CostReference:
    """비용 참조 데이터 (Cost Ontology)"""
    type: str  # labor_rate, indirect_rate, fp_rate, adjustment_factor
    category: Optional[str] = None
    categoryCode: Optional[str] = None

    # 노임단가
    grade: Optional[str] = None
    gradeCode: Optional[str] = None
    monthlyRate: Optional[int] = None
    dailyRate: Optional[int] = None
    hourlyRate: Optional[int] = None
    minExperience: Optional[int] = None

    # 간접비율
    minRate: Optional[float] = None
    maxRate: Optional[float] = None
    defaultRate: Optional[float] = None
    baseOn: Optional[str] = None
    formula: Optional[str] = None

    # FP단가
    method: Optional[str] = None
    methodCode: Optional[str] = None
    unitName: Optional[str] = None
    unitCost: Optional[int] = None
    currency: str = "KRW"

    # 보정계수
    fpRange: Optional[Dict[str, Any]] = None
    level: Optional[str] = None
    language: Optional[str] = None
    factor: Optional[float] = None

    # 메타
    year: int = 2026
    source: Optional[str] = None
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def to_jsonl(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


# =============================================================================
# Mapping Functions
# =============================================================================

def _utc_now_iso() -> str:
    """UTC now in ISO-8601 with Z suffix"""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _default_jsonld_context_uri() -> str:
    """프로젝트 내 JSON-LD context 경로를 문자열 URI로 반환"""
    project_root = Path(__file__).resolve().parents[2]
    context_path = project_root / "sh" / "estimation-ontology-improvement" / "schemas" / "context.json"
    return str(context_path)


def _ensure_node_id(value: str, default_prefix: str) -> str:
    """프리픽스가 없는 식별자에 기본 프리픽스를 부여"""
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if ":" in value:
        return value
    return f"{default_prefix}:{value}"


def derive_estimate_range_from_pricing(pricing: Pricing) -> EstimateRange:
    """Pricing 정보로 최소 범위 견적을 생성"""
    candidates = []
    if pricing.estimatedPrice:
        candidates.append(pricing.estimatedPrice.amount)
    if pricing.winningPrice:
        candidates.append(pricing.winningPrice.amount)
    if pricing.baseCost:
        candidates.append(pricing.baseCost.amount)

    if not candidates:
        raise ValueError("Cannot derive estimate range: no pricing amount available")

    base_value = candidates[0]

    if len(candidates) == 1:
        min_value = int(base_value * 0.90)
        p50_value = base_value
        p80_value = int(base_value * 1.10)
        max_value = int(base_value * 1.20)
    else:
        low = min(candidates)
        high = max(candidates)
        min_value = int(low * 0.90)
        p50_value = low
        p80_value = high
        max_value = int(high * 1.15)

    return EstimateRange(
        min=min_value,
        p50=p50_value,
        p80=p80_value,
        max=max_value,
        pointEstimate=p50_value,
    )


def build_quote_version_graph_from_pricing(
    pricing: Pricing,
    requirement_set_id: str,
    evidence_urls: List[str],
    version_no: int = 1,
    assumptions: Optional[List[str]] = None,
    context_uri: Optional[str] = None,
    quote_id: Optional[str] = None,
    estimate_range: Optional[EstimateRange] = None,
) -> QuoteVersionGraph:
    """Pricing에서 QuoteVersion JSON-LD 그래프를 생성"""
    if estimate_range is None:
        estimate_range = derive_estimate_range_from_pricing(pricing)

    resolved_quote_id = quote_id if quote_id else pricing.bidId
    if not resolved_quote_id:
        raise ValueError("quote_id or pricing.bidId is required")

    return QuoteVersionGraph(
        quoteId=resolved_quote_id,
        versionNo=version_no,
        requirementSetId=requirement_set_id,
        estimateRange=estimate_range,
        evidenceUrls=evidence_urls,
        assumptions=assumptions or [],
        contextUri=context_uri,
    )


def map_g2b_project_to_ontology(raw_data: Dict[str, Any]) -> SoftwareProject:
    """나라장터 프로젝트 데이터를 온톨로지 구조로 변환"""

    # Scope 매핑
    scope = None
    if "scope" in raw_data:
        scope = Scope(
            totalFP=raw_data["scope"].get("totalFP"),
            moduleCount=raw_data["scope"].get("moduleCount"),
            screenCount=raw_data["scope"].get("screenCount"),
            reportCount=raw_data["scope"].get("reportCount"),
            interfaceCount=raw_data["scope"].get("interfaceCount"),
        )

    # Timeline 매핑
    timeline = None
    if "timeline" in raw_data:
        tl = raw_data["timeline"]
        timeline = Timeline(
            duration=Duration(
                value=tl.get("duration", 0),
                unit=tl.get("unit", "MONTH"),
            ),
            startDate=tl.get("startDate"),
            endDate=tl.get("endDate"),
        )

    # Roles 매핑
    roles = []
    if "roles" in raw_data:
        for r in raw_data["roles"]:
            roles.append(Role(
                roleType=RoleType(r["roleType"]),
                skillLevel=SkillLevel(r["skillLevel"]),
                headcount=r["headcount"],
                manMonth=r["manMonth"],
            ))

    # Cost 매핑
    estimated_cost = None
    if "estimatedPrice" in raw_data:
        estimated_cost = Money(amount=raw_data["estimatedPrice"])

    return SoftwareProject(
        activityId=raw_data.get("bidId", ""),
        activityName=raw_data.get("title", ""),
        description=raw_data.get("description"),
        category=raw_data.get("category"),
        systemType=raw_data.get("systemType"),
        securityLevel=raw_data.get("securityLevel"),
        techStack=raw_data.get("techStack", []),
        scope=scope,
        timeline=timeline,
        roles=roles,
        estimatedCost=estimated_cost,
        source=raw_data.get("source"),
        crawledAt=raw_data.get("crawledAt"),
    )


def map_g2b_pricing_to_ontology(raw_data: Dict[str, Any]) -> Pricing:
    """나라장터 낙찰정보를 Pricing 온톨로지로 변환"""

    # Competition Level 매핑
    competition_level = None
    if "competitionLevel" in raw_data:
        competition_level = CompetitionLevel(raw_data["competitionLevel"])
    elif "competitorCount" in raw_data:
        count = raw_data["competitorCount"]
        if count <= 1:
            competition_level = CompetitionLevel.MONOPOLY
        elif count <= 3:
            competition_level = CompetitionLevel.LOW
        elif count <= 5:
            competition_level = CompetitionLevel.MEDIUM
        elif count <= 7:
            competition_level = CompetitionLevel.HIGH
        else:
            competition_level = CompetitionLevel.INTENSE

    # Risk Level 매핑
    risk_level = None
    if "riskLevel" in raw_data:
        risk_level = RiskLevel(raw_data["riskLevel"])

    return Pricing(
        pricingId=f"PRC-{raw_data.get('bidId', '')}",
        bidId=raw_data.get("bidId", ""),
        estimatedPrice=Money(amount=raw_data["estimatedPrice"]) if "estimatedPrice" in raw_data else None,
        winningPrice=Money(amount=raw_data["winningPrice"]) if "winningPrice" in raw_data else None,
        winningRate=raw_data.get("winningRate"),
        competitorCount=raw_data.get("competitorCount"),
        competitionLevel=competition_level,
        contractType=raw_data.get("contractType"),
        winnerName=raw_data.get("winnerName"),
        bidDate=raw_data.get("bidDate"),
        impliedMargin=raw_data.get("impliedMargin"),
        riskLevel=risk_level,
        source=raw_data.get("source"),
        crawledAt=raw_data.get("crawledAt"),
    )


# =============================================================================
# Utility Functions
# =============================================================================

def load_jsonl(filepath: str) -> List[Dict[str, Any]]:
    """JSONL 파일 로드"""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def save_jsonl(data: List[Any], filepath: str):
    """JSONL 파일 저장"""
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in data:
            if hasattr(item, 'to_jsonl'):
                f.write(item.to_jsonl() + '\n')
            else:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')


def save_json(data: Dict[str, Any], filepath: str):
    """JSON 파일 저장"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 테스트: 샘플 데이터 변환
    sample_project = {
        "bidId": "G2B-2026-001",
        "title": "테스트 시스템 구축",
        "description": "테스트 프로젝트입니다.",
        "scope": {"totalFP": 500, "moduleCount": 5},
        "timeline": {"duration": 6, "unit": "MONTH"},
        "roles": [
            {"roleType": "PROJECT_MANAGER", "skillLevel": "SENIOR", "headcount": 1, "manMonth": 6}
        ],
        "estimatedPrice": 300000000,
        "category": "WEB_APPLICATION",
        "source": "테스트",
    }

    project = map_g2b_project_to_ontology(sample_project)
    print("Project JSONL:")
    print(project.to_jsonl())
    print()

    sample_pricing = {
        "bidId": "G2B-2026-001",
        "estimatedPrice": 300000000,
        "winningPrice": 270000000,
        "winningRate": 90.0,
        "competitorCount": 4,
        "contractType": "협상에의한계약",
    }

    pricing = map_g2b_pricing_to_ontology(sample_pricing)
    print("Pricing JSONL:")
    print(pricing.to_jsonl())
    print()

    quote_jsonld = pricing.to_quote_version_jsonld(
        requirement_set_id="REQSET-2026-0001",
        evidence_urls=[
            "https://www.sw.or.kr/site/sw/ex/board/View.do?cbIdx=276&bcIdx=63607",
            "https://www.sw.or.kr/site/sw/ex/board/View.do?cbIdx=304&bcIdx=64717",
        ],
        version_no=1,
        assumptions=["ASM-01"],
    )
    print("QuoteVersion JSON-LD:")
    print(json.dumps(quote_jsonld, ensure_ascii=False, indent=2))
