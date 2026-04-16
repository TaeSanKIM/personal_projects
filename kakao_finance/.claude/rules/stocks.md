# 주식 종목 선택 규칙

## 종목 목록 관리

- 모든 추적 종목은 `config.py`의 `STOCKS` 리스트에서만 관리한다.
- 각 종목은 반드시 `name`, `ticker`, `market` 세 필드를 포함해야 한다.

```python
{"name": "종목명", "ticker": "티커코드", "market": "KRX" | "US"}
```

## 시장 구분

| market | 데이터 소스 | 통화 | ticker 형식 |
|--------|------------|------|-------------|
| `"KRX"` | `pykrx` | KRW | 6자리 숫자 (예: `"082640"`) |
| `"US"`  | `yfinance` | USD | 알파벳 대문자 (예: `"COP"`) |

- `market` 값은 반드시 `"KRX"` 또는 `"US"` 중 하나여야 한다.
- 그 외 시장(도쿄, 홍콩 등)을 추가할 경우, `stock_fetcher.py`에 해당 분기와 데이터 소스를 함께 구현해야 한다.

## 기준일 (BASE_DATE)

- `config.py`의 `BASE_DATE`는 `"YYYYMMDD"` 형식의 문자열이다.
- 등락률은 `BASE_DATE` 시점의 종가 대비 현재가로 계산한다.
- `BASE_DATE`를 변경하면 모든 종목의 등락 기준이 동시에 바뀌므로 신중히 수정한다.

## 종목 추가/제거 시 체크리스트

1. `config.py`의 `STOCKS`에 항목 추가 또는 제거
2. KRX 종목이면 ticker가 6자리 숫자인지 확인
3. US 종목이면 yfinance에서 유효한 ticker인지 확인 (`yf.Ticker("XXX").history(period="1d")`)
4. `python main.py`로 종단 테스트 (전역 원칙 참고)
