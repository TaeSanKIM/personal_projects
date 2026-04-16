"""주식 시세 조회 → 카카오 메시지 전송."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime

from common.stock_fetcher import fetch_all
from common.kakao_sender import send_message
from common.config import BASE_DATE


def _format_message(stocks: list[dict]) -> str:
    base_display = f"{BASE_DATE[:4]}-{BASE_DATE[4:6]}-{BASE_DATE[6:]}"
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"📊 주식현황 {today}", f"(기준일: {base_display})", ""]

    ok = sorted([s for s in stocks if "error" not in s], key=lambda s: s["change_pct"], reverse=True)
    failed = [s for s in stocks if "error" in s]
    stocks = ok + failed

    for s in stocks:
        if "error" in s:
            lines.append(f"{s['name']} ({s['ticker']}): 조회 실패")
            lines.append("")
            continue

        arrow = "▲" if s["change"] >= 0 else "▼"
        sign = "+" if s["change"] >= 0 else ""

        if s["currency"] == "KRW":
            cur = lambda p: f"{int(p):,}원"
        else:
            cur = lambda p: f"${p:,.2f}"

        lines.append(f"{s['name']} ({s['ticker']})")
        lines.append(f"현재 {cur(s['current_price'])}")
        lines.append(f"기준 {cur(s['base_price'])}")
        lines.append(f"{arrow} {cur(abs(s['change']))} ({sign}{s['change_pct']:.2f}%)")
        lines.append("")

    return "\n".join(lines).strip()


def run() -> None:
    print("주식 데이터 조회 중...")
    stocks = fetch_all()

    for s in stocks:
        if "error" in s:
            print(f"  [{s['name']}] 오류: {s['error']}")
        else:
            print(f"  [{s['name']}] 현재 {s['current_price']:.2f} / 기준 {s['base_price']:.2f} / 등락 {s['change_pct']:+.2f}%")

    message = _format_message(stocks)
    print("\n--- 전송 메시지 ---")
    print(message)
    print("-------------------\n")

    send_message(message)
    print("카카오톡 전송 완료.")


if __name__ == "__main__":
    run()
