"""공통 메시지 포맷터."""

from datetime import datetime


def _cur(value: float, currency: str) -> str:
    if currency == "KRW":
        return f"{int(value):,}원"
    return f"${value:,.2f}"


def format_message(stocks: list[dict], base_date: str) -> str:
    """전체 종목 현황 메시지."""
    base_display = f"{base_date[:4]}-{base_date[4:6]}-{base_date[6:]}"
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"📊 주식현황 {today}", f"(기준일: {base_display})", ""]

    ok = sorted(
        [s for s in stocks if "error" not in s],
        key=lambda s: s["daily_change_pct"] or 0,
        reverse=True,
    )
    failed = [s for s in stocks if "error" in s]

    for s in ok + failed:
        if "error" in s:
            lines.append(f"{s['name']} ({s['ticker']}): 조회 실패")
            lines.append("")
            continue

        currency = s["currency"]
        arrow = "▲" if s["change"] >= 0 else "▼"
        sign = "+" if s["change"] >= 0 else ""

        lines.append(f"{s['name']} ({s['ticker']})")
        lines.append(f"현재 {_cur(s['current_price'], currency)}")
        lines.append(f"기준 {_cur(s['base_price'], currency)}")
        lines.append(f"기준대비 {arrow} {_cur(abs(s['change']), currency)} ({sign}{s['change_pct']:.2f}%)")

        if s.get("daily_change_pct") is not None:
            d_arrow = "▲" if s["daily_change"] >= 0 else "▼"
            d_sign = "+" if s["daily_change"] >= 0 else ""
            lines.append(f"전일대비 {d_arrow} {_cur(abs(s['daily_change']), currency)} ({d_sign}{s['daily_change_pct']:.2f}%)")

        lines.append("")

    return "\n".join(lines).strip()


def format_analysis_message(sector_analyses: list[dict]) -> str:
    """섹터별 AI 분석 결과 메시지."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"🔍 급등 분석 {today}", ""]

    for item in sector_analyses:
        sector = item["sector"]
        stocks_str = " · ".join(
            f"{s['name']}({s['daily_change_pct']:+.2f}%)"
            for s in item["stocks"]
        )
        lines.append(f"[{sector}] {stocks_str}")
        lines.append(item["analysis"])
        lines.append("")

    return "\n".join(lines).strip()
