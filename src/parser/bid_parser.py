"""
입찰공고 파서

나라장터 입찰공고 HTML 및 첨부 PDF 파싱
"""

import re
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ParsedBid:
    """파싱된 입찰공고 데이터"""
    bidId: str
    title: str
    description: Optional[str] = None
    organization: Optional[str] = None
    estimatedPrice: Optional[int] = None
    duration: Optional[Dict[str, Any]] = None
    deadline: Optional[str] = None
    announcementDate: Optional[str] = None
    contractType: Optional[str] = None
    category: Optional[str] = None
    techStack: Optional[List[str]] = None
    scope: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def to_jsonl(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


class BidHTMLParser:
    """입찰공고 HTML 파서"""

    # 금액 패턴
    PRICE_PATTERNS = [
        r'예정가격[:\s]*([0-9,]+)\s*원',
        r'추정가격[:\s]*([0-9,]+)\s*원',
        r'예산금액[:\s]*([0-9,]+)\s*원',
        r'사업비[:\s]*([0-9,]+)\s*원',
    ]

    # 기간 패턴
    DURATION_PATTERNS = [
        r'사업기간[:\s]*(\d+)\s*(개월|월)',
        r'계약기간[:\s]*(\d+)\s*(개월|월)',
        r'수행기간[:\s]*(\d+)\s*(개월|월)',
        r'(\d+)\s*(개월|월)\s*간',
    ]

    # 기술스택 키워드
    TECH_KEYWORDS = [
        "Java", "Python", "JavaScript", "TypeScript",
        "Spring", "Spring Boot", "Django", "FastAPI", "Node.js",
        "React", "Vue", "Angular", "Flutter",
        "PostgreSQL", "MySQL", "Oracle", "MongoDB", "Redis",
        "AWS", "GCP", "Azure", "Docker", "Kubernetes",
        "Kafka", "Elasticsearch", "Grafana",
    ]

    # 프로젝트 유형 키워드
    PROJECT_TYPE_KEYWORDS = {
        "WEB_APPLICATION": ["웹", "홈페이지", "포털", "웹시스템"],
        "MOBILE_APPLICATION": ["모바일", "앱", "어플리케이션", "iOS", "Android"],
        "DATA_PLATFORM": ["데이터", "분석", "빅데이터", "BI", "DW", "데이터레이크"],
        "API_PLATFORM": ["API", "연동", "인터페이스", "게이트웨이"],
        "AI_ML_SYSTEM": ["AI", "인공지능", "머신러닝", "딥러닝", "ML"],
    }

    def parse_html(self, html_content: str, bid_id: str) -> ParsedBid:
        """HTML에서 입찰공고 정보 추출"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
        except ImportError:
            # BeautifulSoup 없이 정규식으로 파싱
            return self._parse_with_regex(html_content, bid_id)

        # TODO: 실제 나라장터 HTML 구조에 맞게 구현
        # 현재는 정규식 기반 파싱 사용
        return self._parse_with_regex(html_content, bid_id)

    def _parse_with_regex(self, text: str, bid_id: str) -> ParsedBid:
        """정규식으로 텍스트에서 정보 추출"""

        # 금액 추출
        estimated_price = None
        for pattern in self.PRICE_PATTERNS:
            match = re.search(pattern, text)
            if match:
                price_str = match.group(1).replace(',', '')
                estimated_price = int(price_str)
                break

        # 기간 추출
        duration = None
        for pattern in self.DURATION_PATTERNS:
            match = re.search(pattern, text)
            if match:
                duration = {
                    "value": int(match.group(1)),
                    "unit": "MONTH"
                }
                break

        # 기술스택 추출
        tech_stack = []
        text_upper = text.upper()
        for tech in self.TECH_KEYWORDS:
            if tech.upper() in text_upper:
                tech_stack.append(tech)

        # 프로젝트 유형 추출
        category = None
        for cat, keywords in self.PROJECT_TYPE_KEYWORDS.items():
            for kw in keywords:
                if kw in text:
                    category = cat
                    break
            if category:
                break

        return ParsedBid(
            bidId=bid_id,
            title="",  # 별도 추출 필요
            estimatedPrice=estimated_price,
            duration=duration,
            techStack=tech_stack if tech_stack else None,
            category=category,
        )


class RFPParser:
    """RFP/과업지시서 PDF 파서"""

    # FP 관련 패턴
    FP_PATTERNS = [
        r'기능점수[:\s]*(\d+)\s*FP',
        r'총\s*FP[:\s]*(\d+)',
        r'(\d+)\s*FP',
    ]

    # 화면 수 패턴
    SCREEN_PATTERNS = [
        r'화면\s*수[:\s]*(\d+)',
        r'(\d+)\s*개\s*화면',
    ]

    # 모듈 수 패턴
    MODULE_PATTERNS = [
        r'모듈\s*수[:\s]*(\d+)',
        r'(\d+)\s*개\s*모듈',
    ]

    def parse_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """PDF에서 프로젝트 범위 정보 추출

        Note: pdfplumber 또는 PyPDF2 필요
        """
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return self._extract_scope(text)
        except ImportError:
            pass

        try:
            import PyPDF2
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() or ""
                return self._extract_scope(text)
        except ImportError:
            pass

        return {}

    def parse_text(self, text: str) -> Dict[str, Any]:
        """텍스트에서 범위 정보 추출"""
        return self._extract_scope(text)

    def _extract_scope(self, text: str) -> Dict[str, Any]:
        """텍스트에서 Scope 정보 추출"""
        scope = {}

        # FP 추출
        for pattern in self.FP_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                scope["totalFP"] = int(match.group(1))
                break

        # 화면 수 추출
        for pattern in self.SCREEN_PATTERNS:
            match = re.search(pattern, text)
            if match:
                scope["screenCount"] = int(match.group(1))
                break

        # 모듈 수 추출
        for pattern in self.MODULE_PATTERNS:
            match = re.search(pattern, text)
            if match:
                scope["moduleCount"] = int(match.group(1))
                break

        return scope


class CostCalculator:
    """비용 계산기

    수집된 참조 데이터를 기반으로 비용 계산
    """

    def __init__(self, data_dir: str = "../../data/cost"):
        self.data_dir = Path(data_dir)
        self.labor_rates = {}
        self.indirect_rates = {}
        self.fp_rates = {}
        self.adjustment_factors = {}
        self._load_reference_data()

    def _load_reference_data(self):
        """참조 데이터 로드"""
        # 노임단가
        labor_file = self.data_dir / "labor_rates.jsonl"
        if labor_file.exists():
            with open(labor_file, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    self.labor_rates[data["gradeCode"]] = data

        # 간접비율
        indirect_file = self.data_dir / "indirect_rates.jsonl"
        if indirect_file.exists():
            with open(indirect_file, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    self.indirect_rates[data["categoryCode"]] = data

        # FP단가
        fp_file = self.data_dir / "fp_rates.jsonl"
        if fp_file.exists():
            with open(fp_file, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    self.fp_rates[data["methodCode"]] = data

    def calculate_labor_cost(
        self,
        roles: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """인건비 계산

        Args:
            roles: [{"roleType": "PM", "skillLevel": "SENIOR", "headcount": 1, "manMonth": 6}]

        Returns:
            {"totalLaborCost": 금액, "breakdown": [...]}
        """
        breakdown = []
        total = 0

        for role in roles:
            skill_level = role.get("skillLevel", "MID")
            man_month = role.get("manMonth", 0)

            # 등급별 노임단가 조회
            rate_info = self.labor_rates.get(skill_level, {})
            monthly_rate = rate_info.get("monthlyRate", 8000000)  # 기본값

            cost = monthly_rate * man_month
            total += cost

            breakdown.append({
                "roleType": role.get("roleType"),
                "skillLevel": skill_level,
                "manMonth": man_month,
                "monthlyRate": monthly_rate,
                "cost": cost,
            })

        return {
            "totalLaborCost": total,
            "breakdown": breakdown,
        }

    def calculate_total_cost(
        self,
        labor_cost: int,
        direct_expense: int = 0,
        overhead_rate: float = 110,
        tech_fee_rate: float = 25,
    ) -> Dict[str, Any]:
        """총 비용 계산 (공공사업 기준)

        공식:
        - 제경비 = 직접인건비 × (제경비율/100)
        - 기술료 = (직접인건비 + 제경비) × (기술료율/100)
        - 총원가 = 직접인건비 + 제경비 + 기술료 + 직접경비
        """
        overhead = labor_cost * (overhead_rate / 100)
        tech_fee = (labor_cost + overhead) * (tech_fee_rate / 100)
        total = labor_cost + overhead + tech_fee + direct_expense

        return {
            "directLaborCost": labor_cost,
            "overhead": int(overhead),
            "overheadRate": overhead_rate,
            "technicalFee": int(tech_fee),
            "technicalFeeRate": tech_fee_rate,
            "directExpense": direct_expense,
            "totalCost": int(total),
        }

    def calculate_fp_based_cost(
        self,
        total_fp: int,
        method: str = "FP",
        size_adjustment: bool = True,
    ) -> Dict[str, Any]:
        """FP 기반 비용 계산

        Args:
            total_fp: 총 기능점수
            method: FP, FP_SIMPLE, FP_FULL
            size_adjustment: 규모 보정 적용 여부
        """
        rate_info = self.fp_rates.get(method, {})
        unit_cost = rate_info.get("unitCost", 553000)

        base_cost = total_fp * unit_cost

        # 규모 보정
        adjustment_factor = 1.0
        if size_adjustment:
            for factor_data in self.adjustment_factors.values():
                if factor_data.get("categoryCode") == "SIZE_ADJUSTMENT":
                    fp_range = factor_data.get("fpRange", {})
                    min_fp = fp_range.get("min", 0)
                    max_fp = fp_range.get("max")

                    if min_fp <= total_fp and (max_fp is None or total_fp < max_fp):
                        adjustment_factor = factor_data.get("factor", 1.0)
                        break

        adjusted_cost = base_cost * adjustment_factor

        return {
            "totalFP": total_fp,
            "unitCost": unit_cost,
            "baseCost": base_cost,
            "adjustmentFactor": adjustment_factor,
            "adjustedCost": int(adjusted_cost),
        }


if __name__ == "__main__":
    # 테스트
    parser = BidHTMLParser()

    sample_text = """
    사업명: 스마트 관리시스템 구축
    예정가격: 500,000,000원
    사업기간: 6개월
    주요 기술: Java, Spring Boot, PostgreSQL, React
    """

    result = parser._parse_with_regex(sample_text, "TEST-001")
    print("Parsed result:")
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))

    # 비용 계산 테스트
    calculator = CostCalculator()

    roles = [
        {"roleType": "PM", "skillLevel": "SENIOR", "manMonth": 6},
        {"roleType": "DEVELOPER", "skillLevel": "MID", "manMonth": 20},
    ]

    labor_result = calculator.calculate_labor_cost(roles)
    print("\nLabor cost:")
    print(json.dumps(labor_result, ensure_ascii=False, indent=2))

    total_result = calculator.calculate_total_cost(
        labor_cost=labor_result["totalLaborCost"]
    )
    print("\nTotal cost:")
    print(json.dumps(total_result, ensure_ascii=False, indent=2))
