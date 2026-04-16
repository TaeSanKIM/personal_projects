# AI 분석 규칙

## 동작 방식

`analyzer/`는 전일 대비 5% 이상 급등한 종목을 Anthropic API + `web_search` 툴로 원인을 분석해 카카오톡으로 전송한다.

## 프롬프트 관리

- 분석에 사용하는 프롬프트는 코드에 하드코딩하지 않는다.
- 프롬프트 파일은 `analyzer/prompts/` 에서 관리한다.
- 파일 형식은 frontmatter(model, max_tokens) + 본문으로 구성한다.

@../../analyzer/prompts/surge_analysis.md

## 프롬프트 수정 시 체크리스트

1. `analyzer/prompts/surge_analysis.md` 수정
2. `model` / `max_tokens` 변경이 있으면 frontmatter에 반영
3. 변수 자리표시자(`{name}`, `{ticker}`, `{pct}`)는 반드시 유지

## 급등 기준

- 전일 대비 등락률 기준: `SURGE_THRESHOLD = 5.0` (`analyzer/stock_analyzer.py`)
- 기준값 변경 시 `stock_analyzer.py`의 `SURGE_THRESHOLD` 상수만 수정
