"""전일 대비 급등 종목을 섹터별로 묶어 AI로 분석."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import anthropic
from common.prompt_loader import load as load_prompt

SURGE_THRESHOLD = 5.0  # 전일 대비 등락률 기준 (%)
_DIR = os.path.dirname(os.path.abspath(__file__))


def analyze_surges(stocks: list[dict]) -> list[dict]:
    """급등 종목을 섹터별로 그룹화해 AI 분석.

    Returns:
        [{"sector": ..., "stocks": [...], "analysis": ...}, ...]
        급등 종목이 없으면 빈 리스트
    """
    surged = [
        s for s in stocks
        if "error" not in s and (s.get("daily_change_pct") or 0) >= SURGE_THRESHOLD
    ]
    if not surged:
        return []

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("  ANTHROPIC_API_KEY가 설정되지 않아 분석을 건너뜁니다.")
        return []

    # 섹터별 그룹화
    by_sector: dict[str, list[dict]] = {}
    for s in surged:
        by_sector.setdefault(s.get("sector", "기타"), []).append(s)

    client = anthropic.Anthropic(api_key=api_key)
    prompt_cfg = load_prompt("surge_analysis", _DIR)
    model = prompt_cfg["model"]
    max_tokens = prompt_cfg["max_tokens"]
    prompt_template = prompt_cfg["prompt"]

    results = []
    for sector, sector_stocks in by_sector.items():
        stocks_desc = ", ".join(
            f"{s['name']}({s['ticker']}, {s['daily_change_pct']:+.2f}%)"
            for s in sector_stocks
        )
        print(f"  [{sector}] 분석 중: {stocks_desc}")
        try:
            messages = [
                {
                    "role": "user",
                    "content": prompt_template.format(sector=sector, stocks=stocks_desc),
                }
            ]

            while True:
                response = client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    tools=[{"type": "web_search_20260209", "name": "web_search"}],
                    messages=messages,
                )

                if response.stop_reason == "end_turn":
                    text_parts = [
                        block.text.strip()
                        for block in response.content
                        if hasattr(block, "text") and block.text.strip()
                    ]
                    if text_parts:
                        results.append({
                            "sector": sector,
                            "stocks": sector_stocks,
                            "analysis": "\n".join(text_parts),
                        })
                    break
                elif response.stop_reason == "pause_turn":
                    messages.append({"role": "assistant", "content": response.content})
                else:
                    break

        except Exception as e:
            print(f"  [{sector}] 분석 실패: {e}")

    return results
