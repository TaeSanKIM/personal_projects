"""매일 지정 시각에 main.run()을 자동 실행."""

import time

import schedule

from config import SEND_TIME
from main import run


def start() -> None:
    schedule.every().day.at(SEND_TIME).do(run)
    print(f"스케줄러 시작 — 매일 {SEND_TIME}에 실행합니다. (종료: Ctrl+C)")

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    start()
