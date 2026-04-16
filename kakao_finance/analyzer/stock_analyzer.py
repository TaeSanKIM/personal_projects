"""전일 대비 급등 종목을 AI로 분석해 원인을 반환."""

import os

import anthropic

SURGE_THRESHOLD = 5.0  # 전일 대비 등락률 기준 (%)

_PROMPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts", "surge_analysis.md")


def _load_prompt() -> tuple[str, str, int]:
    """surge_analysis.md에서 model, max_tokens, prompt 텍스트를 파싱해 반환."""
    with open(_PROMPT_PATH, encoding="utf-8") as f:
        raw = f.read()

    # frontmatter 파싱
    parts = raw.split("---", 2)
    meta, body = parts[1], parts[2].strip()

    model = "claude-opus-4-6"
    max_tokens = 512
    for line in meta.strip().splitlines():
        if line.startswith("model:"):
            model = line.split(":", 1)[1].strip()
        elif line.startswith("max_tokens:"):
            max_tokens = int(line.split(":", 1)[1].strip())

    return model, max_tokens, body


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
    model, max_tokens, prompt_template = _load_prompt()
    results = {}

    for s in surged:
        name, ticker, pct = s["name"], s["ticker"], s["daily_change_pct"]
        print(f"  [{name}] 급등 분석 중 ({pct:+.2f}%)...")
        try:
            messages = [
                {
                    "role": "user",
                    "content": prompt_template.format(name=name, ticker=ticker, pct=pct),
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
