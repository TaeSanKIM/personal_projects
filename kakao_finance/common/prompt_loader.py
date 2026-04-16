"""계층적 프롬프트 로더.

탐색 순서:
  1. caller_prompts_dir/<name>.md  (모듈 전용 프롬프트)
  2. common/prompts/<name>.md      (공통 기본 프롬프트)

같은 파일은 프로세스 내에서 한 번만 읽는다 (lru_cache).
"""

import os
from functools import lru_cache

_COMMON_PROMPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")


def load(name: str, caller_dir: str) -> dict:
    """프롬프트 파일을 계층 순서로 탐색해 로드.

    Args:
        name:       파일명 (확장자 제외, 예: "surge_analysis")
        caller_dir: 모듈 전용 prompts/ 의 부모 디렉터리 (__file__ 기준)

    Returns:
        {"model": ..., "max_tokens": ..., "prompt": ...}
    """
    candidates = [
        os.path.join(caller_dir, "prompts", f"{name}.md"),
        os.path.join(_COMMON_PROMPTS_DIR, f"{name}.md"),
    ]

    for path in candidates:
        if os.path.exists(path):
            return _load_file(path)

    searched = "\n  ".join(candidates)
    raise FileNotFoundError(f"프롬프트 '{name}'을 찾을 수 없습니다. 탐색 경로:\n  {searched}")


@lru_cache(maxsize=None)
def _load_file(path: str) -> dict:
    """파일을 파싱해 반환. 결과는 캐싱되어 재읽기 없음."""
    with open(path, encoding="utf-8") as f:
        raw = f.read()

    parts = raw.split("---", 2)
    if len(parts) < 3:
        return {"model": "claude-opus-4-6", "max_tokens": 512, "prompt": raw.strip()}

    meta, body = parts[1], parts[2].strip()

    result: dict = {"model": "claude-opus-4-6", "max_tokens": 512, "prompt": body}
    for line in meta.strip().splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        if key == "max_tokens":
            result[key] = int(val)
        else:
            result[key] = val

    return result
