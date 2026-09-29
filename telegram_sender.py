"""
📤 텔레그램 전송 모듈
- 나(의원님)에게 알림 전송
- 카카오톡 대체
- parse_mode 제거로 특수문자 문제 해결
"""
import os
import requests

# ─────────────────────────────────────────
# 시크릿 로딩: Streamlit Cloud → .env 순서로 시도
# ─────────────────────────────────────────
def _get_secret(key: str) -> str:
    # 1) Streamlit Secrets (배포 환경)
    try:
        import streamlit as st
        if key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass

    # 2) 환경변수 (.env, 로컬)
    return os.getenv(key, "").strip()

TELEGRAM_BOT_TOKEN = _get_secret("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = _get_secret("TELEGRAM_CHAT_ID")
def send_to_me(text: str):
    """
    텔레그램으로 메시지 전송
    반환: (성공 여부, 메시지)
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False, ".env 파일에 TELEGRAM_BOT_TOKEN 또는 TELEGRAM_CHAT_ID가 없습니다."

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text[:4000],   # 텔레그램 텍스트 제한 4096자
        # parse_mode 제거 → 특수문자 문제 없음
    }

    try:
        res = requests.post(url, data=data, timeout=10)
        if res.status_code == 200:
            return True, "텔레그램 전송 완료!"
        else:
            return False, f"전송 실패 ({res.status_code}): {res.text}"
    except Exception as e:
        return False, f"오류: {e}"


def send_test():
    """테스트 메시지 전송"""
    message = """🌸 나유경 춘천시의원 AI 보좌관

[테스트 메시지]
텔레그램 전송이 정상 작동합니다!

이 메시지는 telegram_sender.py 로 발송되었습니다.
"""
    return send_to_me(message)