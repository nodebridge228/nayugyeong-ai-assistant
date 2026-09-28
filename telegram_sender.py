"""
📨 텔레그램 전송 모듈
- Streamlit Cloud Secrets와 로컬 .env 모두 지원
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def _get_secret(key: str, default: str = "") -> str:
    """Streamlit Secrets 우선, 없으면 .env에서 읽기"""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    return os.getenv(key, default).strip()


TELEGRAM_BOT_TOKEN = _get_secret("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = _get_secret("TELEGRAM_CHAT_ID")


def send_to_me(text: str):
    """텔레그램으로 메시지 전송 - (성공여부, 메시지) 반환"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False, "Secrets에 TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID가 없습니다."

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text[:4000],
    }

    try:
        res = requests.post(url, data=data, timeout=10)
        if res.status_code == 200:
            return True, "텔레그램 전송 완료!"
        return False, f"전송 실패 ({res.status_code}): {res.text}"
    except Exception as e:
        return False, f"오류: {e}"


def send_test():
    """테스트 메시지 전송"""
    message = "🌸 나유경 춘천시의원 AI 보좌관\n\n[테스트] 텔레그램 전송 정상 작동!"
    return send_to_me(message)
