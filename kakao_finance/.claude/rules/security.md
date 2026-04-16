# 보안 규칙

## 환경 변수 설정

`.env` 파일을 프로젝트 루트에 생성해야 한다:

```
KAKAO_REST_API_KEY=...       # Kakao Developers 앱의 REST API 키
KAKAO_REFRESH_TOKEN=...      # 최초 인증 후 발급되는 리프레시 토큰
SEND_TIME=16:00              # 매일 메시지를 보낼 시각 (HH:MM)
ANTHROPIC_API_KEY=...        # analyzer/ 전용. Anthropic API 키
```

## 카카오 API 인증 흐름

Kakao "나에게 보내기"는 사용자 토큰(access token)이 필요하다.

1. `kakao_auth.py`를 실행해 브라우저 인증 → 최초 `access_token` + `refresh_token` 발급
2. `refresh_token`을 `.env`에 저장
3. 이후 매 실행 시 `refresh_token`으로 `access_token`을 자동 갱신

토큰 유효기간: `access_token` 6시간 / `refresh_token` 60일 (갱신 시 재발급)

## 민감 정보 관리

- `KAKAO_REST_API_KEY`, `KAKAO_REFRESH_TOKEN` 등 모든 시크릿은 반드시 `.env` 파일에만 저장한다.
- `.env` 파일은 절대 git에 커밋하지 않는다. `.gitignore`에 포함되어 있는지 항상 확인한다.
- 코드 내에 API 키, 토큰, 비밀번호를 하드코딩하지 않는다 (전역 원칙 참고).
- 로그나 print 출력에 토큰 값이 노출되지 않도록 한다.

## 토큰 관리

- `access_token`은 파일이나 DB에 저장하지 않는다. 매 실행 시 `refresh_token`으로 새로 발급받는다.
- `refresh_token`이 재발급된 경우에만 `.env`를 갱신한다 (`kakao_sender.py` 참고).
- `refresh_token` 유효기간은 60일이다. 만료 전에 앱을 1회 이상 실행해 자동 갱신되도록 한다.
- `refresh_token`이 만료된 경우 `python kakao_auth.py`를 실행해 재인증한다.

## 외부 API 호출

- 카카오 API 호출 시 `timeout=10`을 반드시 설정한다 (무한 대기 방지).
- HTTP 응답은 `resp.raise_for_status()`로 오류를 즉시 감지한다.
- 카카오 API의 `result_code`가 `0`이 아닌 경우 예외를 발생시킨다.

## .env 파일 보호

- `.env`에는 최소한의 키만 저장한다: `KAKAO_REST_API_KEY`, `KAKAO_REFRESH_TOKEN`, `SEND_TIME`.
- 팀 공유 시 `.env` 대신 `.env.example`(실제 값 없이 키 이름만)을 사용한다.
- `.env` 파일 권한을 `600`으로 설정하는 것을 권장한다:
  ```bash
  chmod 600 .env
  ```
