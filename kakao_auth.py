"""
카카오 OAuth 인증 유틸리티.

최초 1회: `python kakao_auth.py` 실행 → 브라우저 로그인 → .env에 토큰 저장
이후 매 실행: refresh_access_token()으로 access_token 자동 갱신
"""

import webbrowser
from urllib.parse import parse_qs, urlparse

import requests
from dotenv import set_key

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
REDIRECT_URI = "http://localhost:4000/redirect"


def _request_auth_code(rest_api_key: str) -> str:
    url = (
        f"{KAKAO_AUTH_URL}"
        f"?client_id={rest_api_key}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
    )
    print(f"\n아래 URL로 카카오 로그인을 완료하세요:\n{url}\n")
    webbrowser.open(url)

    redirect_url = input("로그인 후 브라우저 주소창의 URL을 붙여넣으세요: ").strip()
    code = parse_qs(urlparse(redirect_url).query).get("code", [None])[0]
    if not code:
        raise ValueError("URL에서 code를 찾지 못했습니다. 올바른 리디렉션 URL을 붙여넣으세요.")
    return code


def _exchange_code_for_tokens(rest_api_key: str, code: str) -> dict:
    resp = requests.post(KAKAO_TOKEN_URL, data={
        "grant_type": "authorization_code",
        "client_id": rest_api_key,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }, timeout=10)
    resp.raise_for_status()
    return resp.json()


def refresh_access_token(rest_api_key: str, refresh_token: str) -> tuple[str, str]:
    """access_token을 갱신하고 (new_access_token, new_refresh_token)을 반환.
    refresh_token이 재발급되지 않은 경우 기존 값을 그대로 반환.
    """
    resp = requests.post(KAKAO_TOKEN_URL, data={
        "grant_type": "refresh_token",
        "client_id": rest_api_key,
        "refresh_token": refresh_token,
    }, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    new_refresh = data.get("refresh_token", refresh_token)
    return data["access_token"], new_refresh


if __name__ == "__main__":
    import os
    from config import KAKAO_REST_API_KEY

    if not KAKAO_REST_API_KEY:
        raise SystemExit(".env에 KAKAO_REST_API_KEY를 먼저 설정하세요.")

    code = _request_auth_code(KAKAO_REST_API_KEY)
    tokens = _exchange_code_for_tokens(KAKAO_REST_API_KEY, code)

    env_path = os.path.join(os.path.dirname(__file__), ".env")
    set_key(env_path, "KAKAO_REFRESH_TOKEN", tokens["refresh_token"])

    print(f"\naccess_token : {tokens['access_token']}")
    print(f"refresh_token: {tokens['refresh_token']}")
    print("\n.env에 KAKAO_REFRESH_TOKEN이 저장되었습니다.")
