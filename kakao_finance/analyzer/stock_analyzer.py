"""전일 대비 급등 종목을 AI로 분석해 원인을 반환."""

import os

import anthropic

SURGE_THRESHOLD = 5.0  # 전일 대비 등락률 기준 (%)


def analyze_surges(stocks: list[dict]) -> dict[str, str]:
    """급등 종목(전일 대비 SURGE_THRESHOLD% 이상)의 원인을 AI로 분석.

    Returns:
        ticker → 분석 텍스트 매핑 (급등 종목이 없으면 빈 dict)
    """
    surged = [
        s for s in stocks
        if "error" not in s and (s.get("daily_change_pct") or 0) >= SURGE_THRESHOLD
    ]
    if not surged:
        return {}

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("  ANTHROPIC_API_KEY가 설정되지 않아 분석을 건너뜁니다.")
        return {}

    client = anthropic.Anthropic(api_key=api_key)
    results = {}

    for s in surged:
        name, ticker, pct = s["name"], s["ticker"], s["daily_change_pct"]
        print(f"  [{name}] 급등 분석 중 ({pct:+.2f}%)...")
        try:
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"오늘 {name}({ticker}) 주식이 전일 대비 {pct:+.2f}% 급등했습니다. "
                        "최근 뉴스를 검색해서 급등 원인을 한국어로 2-3문장으로 간결하게 설명해주세요."
                    ),
                }
            ]

            while True:
                response = client.messages.create(
                    model="claude-opus-4-6",
                    max_tokens=512,
                    tools=[{"type": "web_search_20260209", "name": "web_search"}],
                    messages=messages,
                )

                if response.stop_reason == "end_turn":
                    for block in response.content:
                        if hasattr(block, "text") and block.text.strip():
                            results[ticker] = block.text.strip()
                            break
                    break
                elif response.stop_reason == "pause_turn":
                    messages.append({"role": "assistant", "content": response.content})
                else:
                    break

        except Exception as e:
            print(f"  [{name}] 분석 실패: {e}")

    return results
