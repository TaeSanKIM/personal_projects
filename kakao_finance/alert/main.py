"""주식 시세 조회 → 카카오 메시지 전송."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.stock_fetcher import fetch_all
from common.kakao_sender import send_message
from common.config import BASE_DATE
from common.formatter import format_message

ALERT_THRESHOLD = 5.0  # 전일대비 등락률 기준 (%)


def run() -> None:
    print("주식 데이터 조회 중...")
    stocks = fetch_all()

    for s in stocks:
        if "error" in s:
            print(f"  [{s['name']}] 오류: {s['error']}")
        else:
            print(f"  [{s['name']}] 현재 {s['current_price']:.2f} / 기준 {s['base_price']:.2f} / 등락 {s['change_pct']:+.2f}%")

    filtered = [
        s for s in stocks
        if "error" not in s and abs(s.get("daily_change_pct") or 0) >= ALERT_THRESHOLD
    ]

    if not filtered:
        print(f"  전일대비 ±{ALERT_THRESHOLD}% 이상 종목 없음 — 전송 건너뜀")
        return

    message = format_message(filtered, BASE_DATE)
    print("\n--- 전송 메시지 ---")
    print(message)
    print("-------------------\n")

    send_message(message)
    print("카카오톡 전송 완료.")


if __name__ == "__main__":
    run()
