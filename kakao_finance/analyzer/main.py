"""주식 시세 조회 → 급등 종목 AI 분석 → 카카오 메시지 전송."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime

from common.stock_fetcher import fetch_all
from common.kakao_sender import send_message
from common.config import BASE_DATE
from stock_analyzer import analyze_surges


def _format_message(stocks: list[dict], analyses: dict[str, str]) -> str:
    base_display = f"{BASE_DATE[:4]}-{BASE_DATE[4:6]}-{BASE_DATE[6:]}"
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"📊 주식현황 {today}", f"(기준일: {base_display})", ""]

    ok = sorted([s for s in stocks if "error" not in s], key=lambda s: s["change_pct"], reverse=True)
    failed = [s for s in stocks if "error" in s]

    for s in ok + failed:
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

        # 전일 대비
        if s.get("daily_change_pct") is not None:
            d_arrow = "▲" if s["daily_change"] >= 0 else "▼"
            d_sign = "+" if s["daily_change"] >= 0 else ""
            lines.append(f"전일대비 {d_arrow} {cur(abs(s['daily_change']))} ({d_sign}{s['daily_change_pct']:.2f}%)")

        # AI 분석 결과
        if s["ticker"] in analyses:
            lines.append(f"[AI 분석] {analyses[s['ticker']]}")

        lines.append("")

    return "\n".join(lines).strip()


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

    message = _format_message(stocks, analyses)
    print("\n--- 전송 메시지 ---")
    print(message)
    print("-------------------\n")

    send_message(message)
    print("카카오톡 전송 완료.")


if __name__ == "__main__":
    run()
