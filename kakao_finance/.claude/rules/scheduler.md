# 스케줄러 규칙

## 실행 방식

이 프로젝트는 두 가지 실행 방식을 지원한다.

| 방식 | 명령어 | 용도 |
|------|--------|------|
| 1회 즉시 실행 | `python main.py` | 수동 테스트, 디버깅 |
| 매일 자동 실행 | `python scheduler.py` | 운영 환경 |

## 발송 시각 설정

- 발송 시각은 `.env`의 `SEND_TIME`으로 관리한다 (형식: `HH:MM`, 기본값 `09:00`).
- `SEND_TIME`은 코드에 하드코딩하지 않는다 (전역 원칙 참고).
- 시각 변경 시 `scheduler.py`를 재시작해야 반영된다.

## scheduler.py 동작 원리

- `schedule` 라이브러리를 사용해 `main.run()`을 매일 `SEND_TIME`에 1회 실행한다.
- 메인 루프는 30초 간격으로 `schedule.run_pending()`을 호출한다.
- 프로세스가 살아있는 동안만 동작하므로, 서버 재시작 시 재실행이 필요하다.

## 운영 환경 권장 사항

- 장기 운영 시 `python scheduler.py`를 백그라운드 프로세스나 시스템 서비스로 등록하는 것을 권장한다.
  ```bash
  # 예: nohup으로 백그라운드 실행
  nohup python scheduler.py &
  ```
- cron을 사용할 경우 `scheduler.py` 대신 `main.py`를 직접 cron에 등록한다.
  ```cron
  0 9 * * 1-5  /usr/bin/python3 /path/to/main.py
  ```

## 수정 시 주의사항

- `scheduler.py`를 수정할 때 `main.run()`의 인터페이스(시그니처)가 바뀌지 않았는지 확인한다.
- 스케줄 로직을 변경하면 `python scheduler.py`를 실행해 "스케줄러 시작" 메시지와 시각이 올바른지 확인한다.
