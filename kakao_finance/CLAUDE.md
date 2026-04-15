# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

매일 지정한 주식들의 가격을 조회하고, 그 결과를 카카오톡 메시지로 자동 전송하는 Python 앱.

- **주식 데이터**: `yfinance` (해외 주식) + `pykrx` (한국 주식)
- **메시지 전송**: Kakao REST API ("나에게 보내기")
- **자동 실행**: Python 스케줄러 (`schedule` 라이브러리) or cron

## 주요 명령어

```bash
# 의존성 설치
pip install -r requirements.txt

# 앱 실행 (1회)
python main.py

# 스케줄러 시작 (매일 자동 실행)
python scheduler.py

# 카카오 토큰 초기 발급 (최초 1회)
python kakao_auth.py
```

## 환경 변수 설정

`.env` 파일을 루트에 생성해야 한다 (`.env.example` 참고):

```
KAKAO_REST_API_KEY=...       # Kakao Developers 앱의 REST API 키
KAKAO_REFRESH_TOKEN=...      # 최초 인증 후 발급되는 리프레시 토큰
SEND_TIME=09:00              # 매일 메시지를 보낼 시각 (HH:MM)
```

## 아키텍처

```
main.py           진입점. 주식 조회 → 메시지 포맷 → 카카오 전송 순서로 실행
scheduler.py      main.py를 매일 지정 시각에 자동 호출
kakao_auth.py     OAuth 인증 흐름 처리 및 토큰 갱신 유틸리티
stock_fetcher.py  yfinance / pykrx를 이용해 주식 시세 조회 및 전일 대비 등락 계산
kakao_sender.py   Kakao REST API를 호출해 나에게 메시지 전송
config.py         .env 로드 및 추적할 주식 목록(종목 코드/티커) 관리
```

## 카카오 API 인증 흐름

Kakao "나에게 보내기"는 사용자 토큰(access token)이 필요하다.

1. `kakao_auth.py`를 실행해 브라우저 인증 → 최초 `access_token` + `refresh_token` 발급
2. `refresh_token`을 `.env`에 저장
3. 이후 매 실행 시 `refresh_token`으로 `access_token`을 자동 갱신

토큰 유효기간: `access_token` 6시간 / `refresh_token` 60일 (갱신 시 재발급)

## 주식 종목 설정

`config.py`의 `STOCKS` 리스트에서 관리:

```python
STOCKS = [
    {"name": "동양생명",      "ticker": "082640", "market": "KRX"},
    {"name": "코노코필립스",  "ticker": "COP",    "market": "US"},
]
```

- 한국 주식: `market="KRX"` → `pykrx` 사용
- 해외 주식: `market="US"` → `yfinance` 사용
