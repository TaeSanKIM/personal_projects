import os
from dotenv import load_dotenv

# common/의 부모(kakao_finance/) 에 있는 .env 로드
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
KAKAO_REFRESH_TOKEN = os.getenv("KAKAO_REFRESH_TOKEN")
SEND_TIME = os.getenv("SEND_TIME", "09:00")

# 등락 기준일 (YYYYMMDD)
BASE_DATE = "20260301"

STOCKS = [
    {"name": "동양생명",     "ticker": "082640", "market": "KRX"},
    {"name": "삼성전자",     "ticker": "005930", "market": "KRX"},
    {"name": "SK하이닉스",   "ticker": "000660", "market": "KRX"},
    {"name": "SK텔레콤",     "ticker": "017670", "market": "KRX"},
    {"name": "코노코필립스", "ticker": "COP",    "market": "US"},
    {"name": "퀀텀컴퓨팅",  "ticker": "QUBT",   "market": "US"},
    {"name": "디웨이브퀀텀", "ticker": "QBTS",   "market": "US"},
    {"name": "블룸에너지",   "ticker": "BE",     "market": "US"},
]
