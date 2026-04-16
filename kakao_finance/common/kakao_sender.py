"""카카오 '나에게 보내기' API를 통해 메시지를 전송."""

import json
import os

import requests
from dotenv import set_key

from .kakao_auth import refresh_access_token
from .config import KAKAO_REST_API_KEY, KAKAO_REFRESH_TOKEN

MEMO_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")


def _get_access_token() -> str:
    if not KAKAO_REST_API_KEY or not KAKAO_REFRESH_TOKEN:
        raise ValueError(".env에 KAKAO_REST_API_KEY와 KAKAO_REFRESH_TOKEN을 설정하세요.")

    access_token, new_refresh = refresh_access_token(KAKAO_REST_API_KEY, KAKAO_REFRESH_TOKEN)

    # refresh_token이 재발급된 경우 .env 업데이트
    if new_refresh != KAKAO_REFRESH_TOKEN:
        set_key(ENV_PATH, "KAKAO_REFRESH_TOKEN", new_refresh)

    return access_token


def send_message(text: str) -> None:
    """text를 카카오 나에게 보내기로 전송."""
    access_token = _get_access_token()

    template = json.dumps({
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://finance.naver.com",
            "mobile_web_url": "https://m.finance.naver.com",
        },
        "button_title": "네이버 금융",
    }, ensure_ascii=False)

    resp = requests.post(
        MEMO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        data={"template_object": template},
        timeout=10,
    )
    resp.raise_for_status()

    result = resp.json()
    if result.get("result_code") != 0:
        raise RuntimeError(f"카카오 전송 실패: {result}")
