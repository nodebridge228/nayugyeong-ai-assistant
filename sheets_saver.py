"""
📊 Google Sheets 저장 모듈
- 민원 접수 내용을 스프레드시트에 자동 저장
- Streamlit Cloud: st.secrets에서 서비스 계정 정보 읽기
- 로컬: gcp_key.json 파일에서 읽기
"""
import json
import os
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials


# ─────────────────────────────────────────
# 설정
# ─────────────────────────────────────────
SHEET_NAME = "나유경_AI보좌관_민원이력"   # 스프레드시트 이름
WORKSHEET_NAME = "Sheet1"                 # 시트 탭 이름 (없으면 첫 번째 시트)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


# ─────────────────────────────────────────
# 서비스 계정 정보 로딩
# ─────────────────────────────────────────
def _load_credentials():
    """
    Streamlit Cloud → st.secrets
    로컬 → gcp_key.json 파일
    """
    # 1) Streamlit Cloud Secrets 시도
    try:
        import streamlit as st
        if "gcp_service_account" in st.secrets:
            info = dict(st.secrets["gcp_service_account"])
            return Credentials.from_service_account_info(info, scopes=SCOPES)
    except Exception:
        pass

    # 2) 로컬 파일 시도
    key_path = os.path.join(os.path.dirname(__file__), "gcp_key.json")
    if os.path.exists(key_path):
        return Credentials.from_service_account_file(key_path, scopes=SCOPES)

    raise FileNotFoundError(
        "서비스 계정 정보를 찾을 수 없습니다. "
        "Streamlit Secrets(gcp_service_account) 또는 gcp_key.json 파일을 확인하세요."
    )


# ─────────────────────────────────────────
# 시트 연결 (캐싱)
# ─────────────────────────────────────────
_sheet_cache = None

def _get_worksheet():
    """워크시트 객체 반환 (한 번만 연결)"""
    global _sheet_cache
    if _sheet_cache is not None:
        return _sheet_cache

    creds = _load_credentials()
    client = gspread.authorize(creds)
    spreadsheet = client.open(SHEET_NAME)

    # 시트 탭 찾기 (없으면 첫 번째 시트)
    try:
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.sheet1

    _sheet_cache = worksheet
    return worksheet


# ─────────────────────────────────────────
# 메인 저장 함수
# ─────────────────────────────────────────
def save_to_sheet(
    name: str,
    contact: str,
    content: str,
    staff_report: str = "",
    telegram_sent: bool = False,
) -> tuple[bool, str]:
    """
    민원 내용을 Google Sheets에 한 행으로 저장

    반환: (성공여부, 메시지)
    """
    try:
        worksheet = _get_worksheet()

        # 헤더 순서: 접수시각 | 성함 | 연락처 | 민원내용 | 내부보고서 | 텔레그램전송
        row = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name or "(미입력)",
            contact or "(미입력)",
            content[:1000],                     # 1000자 제한
            staff_report[:2000],                # 2000자 제한
            "✅" if telegram_sent else "❌",
        ]

        worksheet.append_row(row, value_input_option="USER_ENTERED")
        return True, "📊 스프레드시트 저장 완료"

    except Exception as e:
        return False, f"시트 저장 실패: {e}"