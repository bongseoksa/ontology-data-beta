"""
나라장터(G2B) 입찰공고 크롤러

공공 입찰 정보를 수집하여 JSONL 형식으로 저장합니다.
SW개발/SI 관련 입찰공고와 낙찰정보를 수집합니다.

Usage:
    python g2b_crawler.py --mode bid --keyword "소프트웨어개발" --pages 10
    python g2b_crawler.py --mode result --days 30
"""

import json
import time
import logging
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from urllib.parse import urljoin, urlencode

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Required packages: pip install requests beautifulsoup4")
    raise

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class BidAnnouncement:
    """입찰공고 데이터 클래스"""
    bidId: str
    title: str
    description: Optional[str] = None
    announcementDate: Optional[str] = None
    deadline: Optional[str] = None
    estimatedPrice: Optional[int] = None
    organization: Optional[str] = None
    category: Optional[str] = None
    contractType: Optional[str] = None
    duration: Optional[Dict[str, Any]] = None
    attachments: Optional[List[str]] = None
    sourceUrl: Optional[str] = None
    crawledAt: Optional[str] = None

    def to_jsonl(self) -> str:
        """JSONL 형식 문자열 반환"""
        data = {k: v for k, v in asdict(self).items() if v is not None}
        return json.dumps(data, ensure_ascii=False)


@dataclass
class BidResult:
    """낙찰결과 데이터 클래스"""
    bidId: str
    title: str
    estimatedPrice: Optional[int] = None
    winningPrice: Optional[int] = None
    winningRate: Optional[float] = None
    competitorCount: Optional[int] = None
    winnerName: Optional[str] = None
    bidDate: Optional[str] = None
    contractType: Optional[str] = None
    sourceUrl: Optional[str] = None
    crawledAt: Optional[str] = None

    def to_jsonl(self) -> str:
        """JSONL 형식 문자열 반환"""
        data = {k: v for k, v in asdict(self).items() if v is not None}
        # 낙찰률 계산
        if data.get('estimatedPrice') and data.get('winningPrice'):
            data['winningRate'] = round(
                data['winningPrice'] / data['estimatedPrice'] * 100, 2
            )
        return json.dumps(data, ensure_ascii=False)


class G2BCrawler:
    """나라장터 크롤러"""

    BASE_URL = "https://www.g2b.go.kr"

    # 검색 키워드
    SEARCH_KEYWORDS = [
        "소프트웨어개발",
        "시스템구축",
        "정보시스템",
        "SI",
        "정보화",
        "웹개발",
        "앱개발",
    ]

    def __init__(self, output_dir: str = "../../data"):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        })
        self.output_dir = Path(output_dir)
        self.delay = 1.0  # 요청 간 지연 시간 (초)

    def _request(self, url: str, params: Optional[Dict] = None) -> Optional[BeautifulSoup]:
        """HTTP 요청 및 파싱"""
        try:
            time.sleep(self.delay)  # Rate limiting
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Request failed: {url} - {e}")
            return None

    def search_bid_announcements(
        self,
        keyword: str,
        pages: int = 10
    ) -> List[BidAnnouncement]:
        """입찰공고 검색

        Note: 실제 나라장터 URL 구조에 맞게 수정 필요
        현재는 데모용 구조입니다.
        """
        results = []
        logger.info(f"Searching bid announcements: keyword='{keyword}', pages={pages}")

        # TODO: 실제 나라장터 검색 페이지 구현
        # 현재는 데모용으로 빈 결과 반환
        # 실제 구현 시 다음 단계 필요:
        # 1. 나라장터 검색 페이지 URL 확인
        # 2. 검색 폼 파라미터 분석
        # 3. 결과 테이블 HTML 구조 분석
        # 4. 상세 페이지 링크 추출 및 파싱

        logger.warning(
            "Demo mode: 나라장터 실제 크롤링은 사이트 구조 분석 후 구현 필요. "
            "현재는 샘플 데이터를 사용하세요."
        )

        return results

    def search_bid_results(
        self,
        days: int = 30
    ) -> List[BidResult]:
        """낙찰결과 검색

        Note: 실제 나라장터 URL 구조에 맞게 수정 필요
        """
        results = []
        logger.info(f"Searching bid results: last {days} days")

        # TODO: 실제 나라장터 낙찰정보 페이지 구현

        logger.warning(
            "Demo mode: 나라장터 실제 크롤링은 사이트 구조 분석 후 구현 필요. "
            "현재는 샘플 데이터를 사용하세요."
        )

        return results

    def parse_bid_detail(self, url: str) -> Optional[BidAnnouncement]:
        """입찰공고 상세 페이지 파싱"""
        soup = self._request(url)
        if not soup:
            return None

        # TODO: 실제 HTML 구조에 맞게 파싱 로직 구현
        # 예시:
        # title = soup.select_one('.bid-title').text.strip()
        # estimated_price = soup.select_one('.estimated-price').text

        return None

    def save_to_jsonl(
        self,
        data: List[Any],
        filename: str,
        subdir: str = "project"
    ):
        """JSONL 파일로 저장"""
        output_path = self.output_dir / subdir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'a', encoding='utf-8') as f:
            for item in data:
                f.write(item.to_jsonl() + '\n')

        logger.info(f"Saved {len(data)} items to {output_path}")

    def run_bid_crawler(self, keywords: List[str], pages: int = 10):
        """입찰공고 크롤링 실행"""
        all_announcements = []

        for keyword in keywords:
            announcements = self.search_bid_announcements(keyword, pages)
            all_announcements.extend(announcements)
            logger.info(f"Found {len(announcements)} announcements for '{keyword}'")

        if all_announcements:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.save_to_jsonl(
                all_announcements,
                f'g2b_bids_{timestamp}.jsonl',
                'project'
            )

        return all_announcements

    def run_result_crawler(self, days: int = 30):
        """낙찰결과 크롤링 실행"""
        results = self.search_bid_results(days)

        if results:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.save_to_jsonl(
                results,
                f'g2b_results_{timestamp}.jsonl',
                'pricing'
            )

        return results


class PublicDataAPIClient:
    """공공데이터포털 API 클라이언트

    조달청 입찰공고 정보 API 활용
    API Key 필요: https://www.data.go.kr/
    """

    # 조달청 입찰공고 API
    BID_API_URL = "https://apis.data.go.kr/1230000/BidPublicInfoService"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    def get_bid_list(
        self,
        start_date: str,
        end_date: str,
        keyword: Optional[str] = None,
        page: int = 1,
        rows: int = 100
    ) -> Dict:
        """입찰공고 목록 조회

        Args:
            start_date: 검색 시작일 (YYYYMMDD)
            end_date: 검색 종료일 (YYYYMMDD)
            keyword: 검색어
            page: 페이지 번호
            rows: 페이지당 건수
        """
        endpoint = f"{self.BID_API_URL}/getBidPblancListInfoServc"

        params = {
            'serviceKey': self.api_key,
            'pageNo': page,
            'numOfRows': rows,
            'inqryDiv': '1',  # 검색구분 (1: 공고)
            'inqryBgnDt': start_date,
            'inqryEndDt': end_date,
            'type': 'json',
        }

        if keyword:
            params['bidNtceNm'] = keyword

        try:
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {}

    def get_bid_result(
        self,
        start_date: str,
        end_date: str,
        page: int = 1,
        rows: int = 100
    ) -> Dict:
        """낙찰결과 조회"""
        endpoint = f"{self.BID_API_URL}/getOpengResultListInfoServc"

        params = {
            'serviceKey': self.api_key,
            'pageNo': page,
            'numOfRows': rows,
            'inqryBgnDt': start_date,
            'inqryEndDt': end_date,
            'type': 'json',
        }

        try:
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return {}


def main():
    parser = argparse.ArgumentParser(description='나라장터 입찰정보 크롤러')
    parser.add_argument(
        '--mode',
        choices=['bid', 'result', 'api'],
        default='bid',
        help='크롤링 모드 (bid: 입찰공고, result: 낙찰결과, api: 공공API)'
    )
    parser.add_argument(
        '--keyword',
        default='소프트웨어개발',
        help='검색 키워드'
    )
    parser.add_argument(
        '--pages',
        type=int,
        default=10,
        help='검색 페이지 수'
    )
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='최근 N일 데이터 검색'
    )
    parser.add_argument(
        '--api-key',
        help='공공데이터포털 API Key'
    )
    parser.add_argument(
        '--output-dir',
        default='../../data',
        help='출력 디렉토리'
    )

    args = parser.parse_args()

    if args.mode == 'api':
        if not args.api_key:
            logger.error("API mode requires --api-key")
            return

        client = PublicDataAPIClient(args.api_key)
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=args.days)).strftime('%Y%m%d')

        result = client.get_bid_list(start_date, end_date, args.keyword)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        crawler = G2BCrawler(output_dir=args.output_dir)

        if args.mode == 'bid':
            keywords = [args.keyword] if args.keyword else crawler.SEARCH_KEYWORDS
            crawler.run_bid_crawler(keywords, args.pages)
        elif args.mode == 'result':
            crawler.run_result_crawler(args.days)


if __name__ == '__main__':
    main()
