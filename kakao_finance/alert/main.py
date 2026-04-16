"""주식 시세 조회 → 카카오 메시지 전송 (가격 + 급등 AI 분석 2개 메시지)."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "analyzer"))

from common.stock_fetcher import fetch_all
from common.kakao_sender import send_message
from common.config import BASE_DATE
from common.formatter import format_message, format_analysis_message
from stock_analyzer import analyze_surges


def run() -> None:
    print("주식 데이터 조회 중...")
    stocks = fetch_all()

    for s in stocks:
        if "error" in s:
            print(f"  [{s['name']}] 오류: {s['error']}")
        else:
            print(f"  [{s['name']}] 현재 {s['current_price']:.2f} / 기준 {s['base_price']:.2f} / 등락 {s['change_pct']:+.2f}%")

    # 메시지 1: 전체 종목 현황
    price_message = format_message(stocks, BASE_DATE)
    send_message(price_message)
    print("주식현황 전송 완료.")

    # 메시지 2: 급등 종목 AI 분석 (±5% 이상만)
    print("\n급등 종목 AI 분석 중...")
    sector_analyses = analyze_surges(stocks)

    if sector_analyses:
        analysis_message = format_analysis_message(sector_analyses)
        print("\n--- 분석 메시지 ---")
        print(analysis_message)
        print("-------------------\n")
        send_message(analysis_message)
        print("급등 분석 전송 완료.")
    else:
        print("  급등 종목 없음 — 분석 메시지 건너뜀")


if __name__ == "__main__":
    run()
