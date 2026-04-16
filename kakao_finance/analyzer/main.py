"""주식 시세 조회 → 급등 종목 AI 분석 → 카카오 메시지 전송."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.stock_fetcher import fetch_all
from common.kakao_sender import send_message
from common.config import BASE_DATE
from common.formatter import format_message
from stock_analyzer import analyze_surges


def run() -> None:
    print("주식 데이터 조회 중...")
    stocks = fetch_all()

    for s in stocks:
        if "error" in s:
            print(f"  [{s['name']}] 오류: {s['error']}")
        else:
            daily = f" / 전일대비 {s['daily_change_pct']:+.2f}%" if s.get("daily_change_pct") is not None else ""
            print(f"  [{s['name']}] 현재 {s['current_price']:.2f} / 기준 {s['base_price']:.2f} / 등락 {s['change_pct']:+.2f}%{daily}")

    print("\n급등 종목 AI 분석 중...")
    analyses = analyze_surges(stocks)
    if analyses:
        for ticker, text in analyses.items():
            print(f"  [{ticker}] {text[:80]}...")
    else:
        print("  급등 종목 없음 (분석 건너뜀)")

    message = format_message(stocks, BASE_DATE, analyses)
    print("\n--- 전송 메시지 ---")
    print(message)
    print("-------------------\n")

    send_message(message)
    print("카카오톡 전송 완료.")


if __name__ == "__main__":
    run()
