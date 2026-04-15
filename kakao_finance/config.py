import os
from dotenv import load_dotenv

load_dotenv()

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
KAKAO_REFRESH_TOKEN = os.getenv("KAKAO_REFRESH_TOKEN")
SEND_TIME = os.getenv("SEND_TIME", "09:00")

# 등락 기준일 (YYYYMMDD)
BASE_DATE = "20260301"

STOCKS = [
    {"name": "동양생명",     "ticker": "082640", "market": "KRX"},
    {"name": "코노코필립스", "ticker": "COP",    "market": "US"},
]
