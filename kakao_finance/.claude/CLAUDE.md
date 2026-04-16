# Rules

이 파일은 프로젝트 작업 규칙의 진입점이다.
각 도메인별 상세 규칙은 아래 파일에서 관리한다.

## 전역 원칙

### 설정값 하드코딩 금지
모든 설정값은 코드에 직접 넣지 않는다.

| 설정 종류 | 저장 위치 |
|-----------|-----------|
| 주식 종목, 기준일 | `config.py` |
| 발송 시각, API 키, 토큰 | `.env` |

### 변경 후 검증
코드나 설정을 변경한 뒤에는 반드시 `python main.py`로 종단 테스트를 실행해 오류가 없는지 확인한다.

---

### 주식 종목 선택 (`rules/stocks.md`)
추적 종목 추가/제거 방법, KRX·US 시장 구분 기준, BASE_DATE 사용 원칙, 종목 변경 시 체크리스트.

@rules/stocks.md

### 스케줄러 (`rules/scheduler.md`)
1회 실행 vs 자동 실행 구분, SEND_TIME 관리, 운영 환경 백그라운드 실행, 수정 시 주의사항.

@rules/scheduler.md

### 보안 (`rules/security.md`)
환경 변수 설정, 카카오 OAuth 인증 흐름, 토큰 관리, 외부 API 호출 규칙, .env 파일 보호.

@rules/security.md
