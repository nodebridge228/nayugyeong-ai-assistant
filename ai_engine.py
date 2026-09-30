"""
AI 연결 모듈
- Claude(Anthropic)로 먼저 분석하고, 실패하면 Gemini로 대체
- 키는 Streamlit Secrets → .env 순서로 읽는다
"""
import os

import anthropic
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

CLAUDE_MODELS = ["claude-sonnet-5-5", "claude-sonnet-5"]
GEMINI_MODELS = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite"]


def _get_secret(name: str) -> str:
    try:
        import streamlit as st
        if name in st.secrets:
            return str(st.secrets[name]).strip()
    except Exception:
        pass
    return os.getenv(name, "").strip()


def _claude(system: str, prompt: str) -> tuple[str, str]:
    client = anthropic.Anthropic(api_key=_get_secret("ANTHROPIC_API_KEY"), timeout=120, max_retries=1)
    last_error = None
    for model in CLAUDE_MODELS:
        try:
            response = client.messages.create(
                model=model,
                max_tokens=4000,
                system=system,
                messages=[{"role": "user", "content": prompt}],
            )
        except (anthropic.AuthenticationError, anthropic.PermissionDeniedError):
            raise
        except anthropic.APIError as e:
            last_error = e
            continue
        text = "".join(b.text for b in response.content if b.type == "text")
        if text.strip():
            return text, f"Claude ({model})"
    raise last_error or RuntimeError("Claude 응답이 비어 있습니다.")


def _gemini(system: str, prompt: str) -> tuple[str, str]:
    client = genai.Client(
        api_key=_get_secret("GEMINI_API_KEY"),
        http_options=types.HttpOptions(timeout=60_000, retry_options=types.HttpRetryOptions(attempts=1)),
    )
    config = types.GenerateContentConfig(system_instruction=system)
    last_error = None
    for model in GEMINI_MODELS:
        try:
            text = client.models.generate_content(model=model, contents=prompt, config=config).text or ""
        except Exception as e:
            last_error = e
            continue
        if text.strip():
            return text, f"Gemini ({model})"
    raise last_error or RuntimeError("Gemini 응답이 비어 있습니다.")


def generate(system: str, prompt: str) -> tuple[str, str]:
    """(AI 응답, 사용한 AI 이름). 모두 실패하면 마지막 오류를 올린다."""
    last_error = None
    if _get_secret("ANTHROPIC_API_KEY"):
        try:
            return _claude(system, prompt)
        except Exception as e:
            last_error = e
    if _get_secret("GEMINI_API_KEY"):
        try:
            return _gemini(system, prompt)
        except Exception as e:
            last_error = e
    raise last_error or RuntimeError("AI 키(ANTHROPIC_API_KEY 또는 GEMINI_API_KEY)가 설정되지 않았습니다.")
