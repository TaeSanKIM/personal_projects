# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

매일 지정한 주식들의 가격을 조회하고, 그 결과를 카카오톡 메시지로 자동 전송하는 Python 앱.

- **주식 데이터**: `yfinance` (해외 주식) + `pykrx` (한국 주식)
- **메시지 전송**: Kakao REST API ("나에게 보내기")
- **자동 실행**: Python 스케줄러 (`schedule` 라이브러리) or cron

## 파일 구조 및 로드 경로

```
kakao_finance/
├── CLAUDE.md                           # 현재 파일 (프로젝트 진입점)
├── .env                                # 환경변수 (alert/analyzer 공유)
├── requirements.txt                    # 모든 의존성 통합
├── .claude/
│   ├── CLAUDE.md                       # Rules 진입점 (@import)
│   └── rules/
│       ├── stocks.md                   # 주식 선택 규칙
│       ├── scheduler.md                # 스케줄러 규칙
│       └── security.md                 # 보안 규칙
├── .github/
│   └── workflows/
│       └── kakao_finance.yml           # GitHub Actions 워크플로우
├── common/                             # 공유 모듈
│   ├── config.py                       # 환경변수 로드 및 종목 목록 관리
│   ├── kakao_auth.py                   # OAuth 인증 및 토큰 갱신
│   ├── kakao_sender.py                 # 카카오 나에게 보내기 전송
│   └── stock_fetcher.py                # yfinance / pykrx 시세 조회 (전일대비 포함)
├── alert/                              # 주식 시세 알림 기능
│   ├── main.py                         # 진입점. 주식 조회 → 포맷 → 카카오 전송
│   └── scheduler.py                    # 로컬 스케줄러 (선택적 사용)
└── analyzer/                           # 급등 종목 AI 분석 기능
    ├── main.py                         # 진입점. 조회 → AI 분석 → 카카오 전송
    └── stock_analyzer.py               # Anthropic API + web_search로 급등 원인 분석
```

## 아키텍처

### common/ — 공유 모듈
```
config.py         .env 로드, STOCKS 목록, BASE_DATE 관리
kakao_auth.py     OAuth 인증 흐름 처리 및 토큰 갱신 유틸리티
kakao_sender.py   Kakao REST API를 호출해 나에게 메시지 전송
stock_fetcher.py  yfinance / pykrx 시세 조회 (기준가 대비 + 전일 대비 등락 포함)
```

### alert/ — 주식 시세 알림
```
main.py           진입점. 주식 조회 → 메시지 포맷 → 카카오 전송
scheduler.py      main.py를 매일 지정 시각에 자동 호출
```

### analyzer/ — 급등 종목 AI 분석
```
main.py           진입점. 주식 조회 → AI 분석 → 메시지 포맷 → 카카오 전송
stock_analyzer.py 전일 대비 5% 이상 급등 종목을 Anthropic API + web_search로 원인 분석
```

## Rules

도메인별 작업 규칙을 정의한다. 종목 관리, 스케줄러 운영, 보안 정책에 대한 세부 지침을 포함한다.

@.claude/CLAUDE.md

## 주요 명령어

```bash
# 의존성 설치
pip install -r requirements.txt

# 주식 알림 실행 (1회)
python alert/main.py

# 급등 분석 실행 (1회)
python analyzer/main.py

# 스케줄러 시작 (매일 자동 실행)
python alert/scheduler.py

# 카카오 토큰 초기 발급 (최초 1회)
python common/kakao_auth.py
```

## 환경 변수 설정

각 폴더에 `.env` 파일을 생성해야 한다:

```
KAKAO_REST_API_KEY=...       # Kakao Developers 앱의 REST API 키
KAKAO_REFRESH_TOKEN=...      # 최초 인증 후 발급되는 리프레시 토큰
SEND_TIME=16:00              # 매일 메시지를 보낼 시각 (HH:MM)
ANTHROPIC_API_KEY=...        # analyzer/ 전용. Anthropic API 키
```
