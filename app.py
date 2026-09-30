"""
🌸 나유경 춘천시의원 AI 보좌관 (v7)
- 더불어민주당 파랑 + 의원님 사진
- Claude AI(예비: Gemini) + 텔레그램 자동 전송
- Google Sheets 민원 이력 저장 ⭐ NEW
- Civic Atelier 스타일
"""
import os
import re
import html
import base64
from pathlib import Path
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
import ai_engine
import departments
import telegram_sender
import sheets_saver

# ═══════════════════════════════════════════════════
# 1) 페이지 설정
# ═══════════════════════════════════════════════════
st.set_page_config(
    page_title="나유경 춘천시의원 AI 보좌관",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════
# 2) 🎨 Civic Atelier 스타일 CSS
# ═══════════════════════════════════════════════════
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Malgun Gothic', sans-serif !important;
        color: #1b2c32;
        word-break: keep-all;
    }

    .stApp { background: #f6f7f3; }

    .main .block-container {
        max-width: 1360px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ── 🎯 히어로 헤더 ── */
    .civic-hero {
        position: relative;
        isolation: isolate;
        overflow: hidden;
        border-radius: 32px;
        background: linear-gradient(135deg, #002A6B 0%, #0047A0 50%, #1560BC 100%);
        color: #d2dfdb;
        padding: 56px 58px 0;
        margin-bottom: 2rem;
        border: 1px solid #1a4a8f;
        box-shadow: 0 24px 60px -40px rgba(0, 42, 107, 0.7);
    }

    .civic-hero::before {
        content: "";
        position: absolute;
        inset: 0;
        z-index: -1;
        background: 
            radial-gradient(ellipse at 83% 20%, rgba(30, 95, 187, 0.5) 0%, transparent 50%),
            radial-gradient(ellipse at 10% 90%, rgba(255, 255, 255, 0.08), transparent 40%);
        pointer-events: none;
    }

    .civic-hero-inner {
        display: grid;
        grid-template-columns: 1.3fr 1fr;
        gap: 40px;
        align-items: end;
        min-height: 340px;
    }

    .civic-hero-copy { padding-bottom: 40px; }

    .civic-hero-visual {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end;
        position: relative;
        align-self: stretch;
    }

    .civic-photo-wrap {
        position: relative;
        width: 260px;
        height: 320px;
        align-self: flex-end;
        margin-top: auto;
    }

    .civic-photo {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center top;
        border-radius: 20px 20px 0 0;
        position: relative;
        z-index: 2;
        box-shadow: 0 -10px 40px -15px rgba(0, 0, 0, 0.4);
    }

    .civic-photo-fallback {
        display: grid;
        place-items: center;
        font-size: 80px;
        background: linear-gradient(135deg, #1E5FBB, #0047A0);
        color: white;
        border-radius: 20px 20px 0 0;
    }

    .civic-photo-glow {
        position: absolute;
        inset: -20px;
        background: radial-gradient(circle at center, rgba(189, 155, 86, 0.35) 0%, transparent 70%);
        z-index: 1;
        filter: blur(30px);
        animation: halo-breathe 4s ease-in-out infinite;
    }

    @keyframes halo-breathe {
        0%, 100% { opacity: 0.5; transform: scale(0.95); }
        50% { opacity: 1; transform: scale(1.05); }
    }

    .civic-photo-label {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2px;
        padding: 12px 22px;
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-top: -8px;
        margin-bottom: 24px;
        z-index: 3;
    }

    .civic-photo-label small {
        font-size: 10px;
        color: #b8c9c4;
        letter-spacing: 0.15em;
        font-weight: 500;
    }

    .civic-photo-label strong {
        font-size: 20px;
        color: #ffffff;
        letter-spacing: 0.2em;
        font-weight: 700;
    }

    .civic-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 9px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.12em;
        color: #d8c89f;
        margin-bottom: 23px;
    }

    .civic-eyebrow-dot {
        width: 6px;
        height: 6px;
        background: #d8c89f;
        border-radius: 50%;
        box-shadow: 0 0 0 5px rgba(216, 200, 159, 0.06);
    }

    .civic-hero h1 {
        font-size: clamp(42px, 4.5vw, 68px);
        line-height: 1.19;
        letter-spacing: -0.055em;
        font-weight: 750;
        color: #f8f8f0 !important;
        margin: 0 !important;
    }

    .civic-emphasis {
        background: linear-gradient(100deg, #f2e0ad 6%, #cfb575 49%, #f5ecd3 75%, #cfb575);
        background-size: 220% auto;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }

    .civic-hero-desc {
        font-size: 16px;
        line-height: 1.95;
        max-width: 550px;
        color: #c5d5e5;
        margin-top: 22px;
        letter-spacing: -0.01em;
    }

    .civic-hero-note {
        display: flex;
        align-items: center;
        gap: 7px;
        font-size: 11px;
        color: #b8c9c4;
        margin-top: 22px;
    }

    .civic-hero-steps {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        padding: 21px 58px;
        background: rgba(0, 0, 0, 0.2);
        margin: 0 -58px;
        gap: 30px;
    }

    .civic-step {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .civic-step + .civic-step {
        border-left: 1px solid rgba(255, 255, 255, 0.15);
        padding-left: 28px;
    }

    .civic-step-num {
        font-family: Georgia, serif;
        font-style: italic;
        font-size: 31px;
        line-height: 1;
        color: #e0c487;
    }

    .civic-step-title {
        color: #ffffff;
        font-size: 13px;
        font-weight: 650;
        display: block;
    }

    .civic-step-desc {
        color: #b8c9d4;
        font-size: 11px;
        display: block;
        margin-top: 3px;
    }

    /* ── 섹션 제목 ── */
    .civic-section-head {
        display: flex;
        align-items: flex-end;
        justify-content: space-between;
        gap: 24px;
        margin: 2.5rem 0 1.5rem 0;
    }

    .civic-kicker {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #0047A0;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.16em;
        margin-bottom: 14px;
    }

    .civic-kicker::before {
        content: "";
        width: 23px;
        height: 1px;
        background: #0047A0;
    }

    .civic-section-head h2 {
        font-size: 32px;
        font-weight: 720;
        line-height: 1.4;
        letter-spacing: -0.045em;
        color: #1b2c32 !important;
        margin: 0 !important;
    }

    .civic-section-head .soft {
        font-weight: 400;
        color: #687976;
    }

    /* ── 폼 입력창 ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #fafaf6 !important;
        border: 1px solid #dde3db !important;
        border-radius: 11px !important;
        font-size: 15px !important;
        padding: 12px 14px !important;
        color: #1b2c32 !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #0047A0 !important;
        box-shadow: 0 0 0 4px rgba(0, 71, 160, 0.1) !important;
        background: #ffffff !important;
    }

    .stTextInput label,
    .stTextArea label {
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #1b2c32 !important;
    }

    /* ── 제출 버튼 ── */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #0047A0 0%, #1560BC 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 11px !important;
        padding: 0.85rem 2rem !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 22px -12px rgba(0, 71, 160, 0.5) !important;
        min-height: 50px !important;
    }

    .stFormSubmitButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 14px 28px -14px rgba(0, 71, 160, 0.6) !important;
    }

    /* ── 탭 ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #edf1eb;
        padding: 4px;
        border-radius: 11px;
        border: 1px solid #dde3db;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 7px;
        padding: 8px 16px;
        font-weight: 650;
        font-size: 12px;
        color: #687976;
        height: auto;
    }

    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #0047A0 !important;
        box-shadow: 0 2px 5px rgba(20, 39, 51, 0.04);
    }

    /* ── 성공 배지 ── */
    .civic-success-badge {
        border: 1px solid #c7dbcc;
        border-radius: 16px;
        background: #eaf3ec;
        padding: 17px 20px;
        margin-bottom: 18px;
    }

    .civic-success-top {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .civic-success-icon {
        display: grid;
        place-items: center;
        width: 36px;
        height: 36px;
        border: 1px solid #a9c4ad;
        border-radius: 50%;
        color: #466d60;
        font-size: 18px;
    }

    .civic-success-top strong {
        font-size: 15px;
        font-weight: 700;
        color: #1b2c32;
        display: block;
    }

    .civic-success-caption {
        display: block;
        font-size: 10px;
        color: #466d60;
        margin-bottom: 3px;
    }

    .civic-success-badge p {
        font-size: 12px;
        line-height: 1.85;
        color: #466d60;
        margin: 9px 0 0 48px;
    }

    .civic-next {
        margin: 16px 0 0 48px;
        padding-top: 14px;
        border-top: 1px solid #c7dbcc;
    }

    .civic-next + .civic-next { margin-top: 12px; }

    .civic-next-label {
        display: block;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #466d60;
        margin-bottom: 6px;
    }

    .civic-next-dept {
        display: block;
        font-size: 15px;
        font-weight: 700;
        color: #1b2c32;
    }

    .civic-next-partner {
        display: block;
        font-size: 13px;
        font-weight: 600;
        color: #2d4d6b;
        margin-top: 4px;
    }

    .civic-next-note {
        display: block;
        font-size: 11px;
        color: #687976;
        margin-top: 3px;
    }

    .civic-next ol {
        margin: 4px 0 0 18px;
        padding: 0;
        font-size: 13px;
        line-height: 1.85;
        color: #1b2c32;
    }

    @media (max-width: 820px) {
        .civic-next, .civic-success-badge p { margin-left: 0; }
    }

    /* ── 텔레그램 상태 ── */
    .civic-telegram-ok {
        background: linear-gradient(135deg, #e8f4ec, #d4ecd9);
        border: 1px solid #a9d4b3;
        border-radius: 14px;
        padding: 14px 20px;
        color: #2d6b40;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* ── 시트 저장 상태 ── */
    .civic-sheet-ok {
        background: linear-gradient(135deg, #e8eef4, #d4e2ec);
        border: 1px solid #a9c1d4;
        border-radius: 14px;
        padding: 14px 20px;
        color: #2d4d6b;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* ── 편지지 스타일 ── */
    .civic-letter {
        background: #ffffff;
        border: 1px solid #dde3db;
        border-radius: 24px;
        padding: 2rem 2rem 1.5rem;
        box-shadow: 0 12px 40px -24px rgba(24, 49, 40, 0.27);
        position: relative;
        overflow: hidden;
        margin-bottom: 1.5rem;
    }

    .civic-letter::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background: linear-gradient(#0047A0, rgba(21, 96, 188, 0) 75%);
    }

    .civic-letter-head {
        padding-bottom: 22px;
        border-bottom: 1px solid #dde3db;
        margin-bottom: 25px;
    }

    .civic-letter-eyebrow {
        font-size: 10px;
        color: #0047A0;
        font-weight: 650;
        letter-spacing: 0.18em;
        margin-bottom: 9px;
    }

    .civic-letter-head h3 {
        font-size: 21px;
        line-height: 1.6;
        letter-spacing: -0.04em;
        font-weight: 750;
        color: #1b2c32;
        margin: 0;
    }

    .civic-letter-signature {
        border-top: 1px solid #dde3db;
        margin-top: 24px;
        padding-top: 18px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 12px;
    }

    .civic-letter-signature small {
        font-size: 12px;
        color: #687976;
    }

    .civic-letter-signature strong {
        font-size: 22px;
        letter-spacing: 0.19em;
        font-weight: 650;
        color: #0047A0;
    }

    /* ── 애니메이션 ── */
    @keyframes fade-in-up {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .civic-fade-in {
        animation: fade-in-up 0.6s cubic-bezier(0.22, 1, 0.36, 1);
    }

    /* ── 반응형 ── */
    @media (max-width: 820px) {
        .civic-hero { padding: 40px 28px 0; border-radius: 24px; }
        .civic-hero h1 { font-size: 42px; }
        .civic-hero-inner { grid-template-columns: 1fr; gap: 20px; text-align: center; }
        .civic-hero-copy { padding-bottom: 20px; }
        .civic-photo-wrap { width: 200px; height: 250px; margin-inline: auto; }
        .civic-hero-steps {
            grid-template-columns: 1fr;
            gap: 14px;
            padding: 21px 28px;
            margin: 30px -28px 0;
        }
        .civic-step + .civic-step {
            border-left: 0;
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            padding-left: 0;
            padding-top: 14px;
        }
        .civic-section-head h2 { font-size: 26px; }
        .main .block-container { padding-inline: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# 3) 환경 설정
# ═══════════════════════════════════════════════════
load_dotenv()
COOLDOWN_SECONDS = 60

# ═══════════════════════════════════════════════════
# 4) AI 프롬프트
# ═══════════════════════════════════════════════════
SYSTEM_PROMPT = """너는 춘천시의회에서 20년 동안 근무한 '베테랑 수석보좌관'이야.
나유경 춘천시의원실에 접수된 민원을 분석해서 두 가지를 만들어줘.

반드시 아래 형식으로 출력해:

===STAFF_VIEW===
(의원님 내부 보고용)
1. 민원 요약 및 핵심 쟁점
2. 구체적 경위
3. 관련 소관 부처 및 현행 법률
4. 의원실 대응 가이드라인

===CITIZEN_VIEW===
(민원인 회신 초안 - 의원실이 검토·수정한 뒤 직접 보낸다. 정중한 존댓말, "안녕하십니까, 나유경 춘천시의원실입니다"로 시작)
1. 접수 확인
2. 민원 요약
3. 앞으로의 절차 (의원실에서 내용을 확인한 뒤 연락드린다는 수준으로만)

회신 초안 작성 규칙:
- 해결 여부, 예산, 일정, 처리 결과를 약속하거나 단정하지 않는다.
- 민원 내용에 없는 사실, 기관 답변, 수치를 지어내지 않는다.

===PUBLIC_VIEW===
(접수 직후 민원인 화면에 바로 보여 줄 안내. 아래 형식 그대로, 다른 말은 쓰지 않는다)
담당부서: 아래 [부서 목록]에서 이 민원을 주로 맡는 부서 하나를 기관명까지 목록 그대로 (예: 춘천시 교통과)
협조부서: 함께 확인이 필요한 다른 부서 하나를 기관명까지 목록 그대로, 없으면 "없음" (예: 강원특별자치도 도로관리사업소)
진행: 첫 번째 진행 단계
진행: 두 번째 진행 단계
진행: 세 번째 진행 단계

안내 작성 규칙:
- 담당부서·협조부서는 반드시 [부서 목록]에 있는 이름만 쓴다. 목록에 없는 부서명을 지어내지 않는다.
- 춘천 시민의 생활 민원은 대부분 춘천시 부서가 담당한다. 지방도·지방하천·도립시설·도 인허가·소방·자치경찰처럼 강원특별자치도 소관이면 강원특별자치도 부서를 담당부서로 쓴다.
- 협조부서는 춘천시와 강원특별자치도가 함께 관여하는 등 실제로 협조가 필요할 때만 쓴다. 억지로 채우지 않는다.
- 내부 보고서의 "관련 소관 부처"도 이 목록의 부서명을 쓴다.
- 진행 단계는 의원실이 실제로 하는 일(내용 확인, 담당 부서에 사실 확인·조치 요청, 현장 확인 검토 등)을 이 민원에 맞게 한 문장씩, 존댓말(~합니다)로 쓴다.
- 해결 여부, 일정, 결과를 약속하지 않는다. 연락·회신 이야기는 쓰지 않는다(따로 안내한다).

[부서 목록] (기관 부서명: 주요 업무)
""" + departments.guide_text()

# ═══════════════════════════════════════════════════
# 5) 🎯 히어로 헤더
# ═══════════════════════════════════════════════════
def get_photo_base64():
    for ext in ['.png', '.jpg', '.jpeg']:
        for name in ['나유경', 'nayugyeong']:
            p = Path(f"images/{name}{ext}")
            if p.exists():
                with open(p, "rb") as f:
                    return base64.b64encode(f.read()).decode(), ext.replace('.', '')
    return None, None

photo_b64, photo_ext = get_photo_base64()

if photo_b64:
    photo_html = f'<img src="data:image/{photo_ext};base64,{photo_b64}" alt="나유경 의원" class="civic-photo">'
else:
    photo_html = '<div class="civic-photo civic-photo-fallback">🌸</div>'

st.markdown(f"""
<div class="civic-hero civic-fade-in">
    <div class="civic-hero-inner">
        <div class="civic-hero-copy">
            <div class="civic-eyebrow">
                <span class="civic-eyebrow-dot"></span>
                시민과 의원실을 잇는 AI 보좌관
            </div>
            <h1>젊고 확실한<br><span class="civic-emphasis">소통.</span></h1>
            <p class="civic-hero-desc">
                소중한 민원을 남겨주시면 AI 보좌관이<br>
                신속하게 분석하여 의원님께 전달드립니다.
            </p>
            <p class="civic-hero-note">
                🌸 실제 접수 · AI 분석 · 텔레그램 전송이 이루어집니다.
            </p>
        </div>
        <div class="civic-hero-visual">
            <div class="civic-photo-wrap">
                {photo_html}
                <div class="civic-photo-glow"></div>
            </div>
            <div class="civic-photo-label">
                <small>춘천시의원</small>
                <strong>나유경</strong>
            </div>
        </div>
    </div>
    <div class="civic-hero-steps">
        <div class="civic-step">
            <span class="civic-step-num">01</span>
            <span>
                <strong class="civic-step-title">이야기를 듣고</strong>
                <span class="civic-step-desc">소중한 민원 접수</span>
            </span>
        </div>
        <div class="civic-step">
            <span class="civic-step-num">02</span>
            <span>
                <strong class="civic-step-title">핵심을 정리하고</strong>
                <span class="civic-step-desc">AI 보좌관의 내용 분석</span>
            </span>
        </div>
        <div class="civic-step">
            <span class="civic-step-num">03</span>
            <span>
                <strong class="civic-step-title">의원실에 전합니다</strong>
                <span class="civic-step-desc">확인 후 소통으로 연결</span>
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# 6) 섹션 제목
# ═══════════════════════════════════════════════════
st.markdown("""
<div class="civic-section-head">
    <div>
        <p class="civic-kicker">01 — YOUR VOICE</p>
        <h2>어떤 이야기를<br><span class="soft">전하고 싶으신가요?</span></h2>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# 7) 민원 입력 폼
# ═══════════════════════════════════════════════════
with st.form("민원_입력"):
    col1, col2 = st.columns(2)
    with col1:
        이름 = st.text_input("성함 (선택)", placeholder="홍길동")
    with col2:
        연락처 = st.text_input("연락처 (선택)", placeholder="010-1234-5678")

    민원_원문 = st.text_area(
        "📝 민원 내용을 입력해주세요",
        height=200,
        placeholder="예: 어제 새벽 3시부터 공사 소음 때문에 잠을 못 잤습니다. 시청에 여러 번 항의했는데도 해결이 안 됩니다...",
    )

    with st.expander("개인정보 수집·이용 안내 (성함·연락처를 적으실 때 꼭 읽어 주세요)"):
        st.markdown(
            "- **수집 항목**: 성함, 연락처, 민원 내용\n"
            "- **이용 목적**: 민원 확인 및 회신\n"
            "- **보유 기간**: 민원 처리 완료 후 파기\n"
            "- **처리 방식**: 민원 내용은 정리를 위해 AI 서비스(Anthropic Claude, Google Gemini)로 전송되며, "
            "접수 내용은 의원실 텔레그램과 구글 스프레드시트에 기록됩니다.\n"
            "- 동의하지 않으셔도 됩니다. 이 경우 성함·연락처 칸을 비우고 익명으로 접수해 주세요. "
            "익명 접수는 회신이 어렵습니다."
        )
    동의 = st.checkbox("위 개인정보 수집·이용에 동의합니다. (성함·연락처를 적으신 경우 필수)")

    submitted = st.form_submit_button("🌸 민원 접수하기", width="stretch", type="primary")

# ═══════════════════════════════════════════════════
# 8) 분석 · 전달
# ═══════════════════════════════════════════════════
DEFAULT_STEPS = [
    "의원실에서 접수된 민원 내용을 꼼꼼히 확인합니다.",
    "필요한 경우 춘천시 담당 부서에 사실 확인과 조치를 요청합니다.",
    "확인 결과에 따라 의원실에서 후속 활동을 이어 갑니다.",
]


def _section(raw: str, name: str) -> str:
    m = re.search(rf"==={name}===(.*?)(?====[A-Z_]+===|\Z)", raw, re.DOTALL)
    return m.group(1).strip() if m else ""


def _public_info(block: str) -> dict:
    department, partner, steps = "", "", []
    for line in block.replace("**", "").splitlines():
        line = line.strip().lstrip("-•· ").strip()
        if line.startswith("담당부서:"):
            department = departments.match(line.split(":", 1)[1])
        elif line.startswith("협조부서:"):
            partner = departments.match(line.split(":", 1)[1])
        elif line.startswith("진행:"):
            step = line.split(":", 1)[1].strip()
            if step:
                steps.append(step)
    if partner == department:
        partner = ""
    return {"department": department, "partner": partner, "steps": steps[:4] or DEFAULT_STEPS}


def analyze(name: str, contact: str, text: str) -> tuple[str, str, dict, str]:
    """(내부 보고서, 회신 초안, 민원인 안내, 사용 AI). AI가 실패해도 원문은 전달되도록 빈 값 대신 안내문을 돌려준다."""
    user_prompt = f"""
[민원인 정보]
- 성함: {name or "(미입력)"}
- 연락처: {contact or "(미입력)"}

[민원 내용]
{text}
"""
    try:
        raw, engine = ai_engine.generate(SYSTEM_PROMPT, user_prompt)
    except Exception as e:
        print(f"[AI 분석 실패] {e}")
        return "(AI 분석 실패 - 민원 원문을 직접 확인해 주세요)", "", _public_info(""), "없음"

    staff = _section(raw, "STAFF_VIEW") or raw
    citizen = _section(raw, "CITIZEN_VIEW")
    public = _public_info(_section(raw, "PUBLIC_VIEW"))
    return staff.replace("**", ""), citizen.replace("**", ""), public, engine


def deliver(name: str, contact: str, text: str) -> tuple[bool, dict]:
    """의원실(텔레그램·시트)에 전달. (한 곳이라도 성공했는지, 민원인 안내)"""
    staff, citizen, public, engine = analyze(name, contact, text)
    received_at = datetime.now().strftime('%Y-%m-%d %H:%M')

    report = f"""🌸 나유경 춘천시의원 AI 보좌관
🔔 새 민원이 접수되었습니다

━━━━━━━━━━━━━━━━━━━━
👤 민원인: {name or "(미입력)"}
📞 연락처: {contact or "(미입력)"}
━━━━━━━━━━━━━━━━━━━━

[민원 원문]
{text[:1500]}

━━━━━━━━━━━━━━━━━━━━
[내부 보고서] (작성 AI: {engine})
{staff}

━━━━━━━━━━━━━━━━━━━━
⏰ 접수 시각: {received_at}
"""
    tg_ok, tg_msg = telegram_sender.send_to_me(report)
    if not tg_ok:
        print(f"[텔레그램 전송 실패] {tg_msg}")
    elif citizen:
        telegram_sender.send_to_me(
            "✉️ 민원인 회신 초안 (검토·수정 후 직접 보내 주세요. 자동 발송되지 않았습니다)\n\n" + citizen
        )

    try:
        sheet_ok, sheet_msg = sheets_saver.save_to_sheet(
            name=name,
            contact=contact,
            content=text,
            staff_report=staff,
            telegram_sent=tg_ok,
        )
    except Exception as e:
        sheet_ok, sheet_msg = False, str(e)
    if not sheet_ok:
        print(f"[시트 저장 실패] {sheet_msg}")

    return tg_ok or sheet_ok, public


if submitted:
    last = st.session_state.get("last_submit_at")
    wait = COOLDOWN_SECONDS - (datetime.now() - last).total_seconds() if last else 0

    if not 민원_원문.strip():
        st.warning("⚠️ 민원 내용을 입력해주세요.")
    elif (이름.strip() or 연락처.strip()) and not 동의:
        st.warning(
            "⚠️ 성함이나 연락처를 적으셨다면 개인정보 수집·이용에 동의해 주세요. "
            "동의하지 않으시면 성함·연락처 칸을 비우고 익명으로 접수하실 수 있습니다."
        )
    elif wait > 0:
        st.warning(f"⚠️ 방금 접수하셨습니다. {int(wait) + 1}초 뒤에 다시 접수해 주세요.")
    else:
        with st.spinner("🌸 민원을 정리해 의원실로 전달하고 있습니다..."):
            delivered, public = deliver(이름.strip(), 연락처.strip(), 민원_원문.strip())
        st.session_state.receipt = {
            "delivered": delivered,
            "department": public["department"],
            "partner": public["partner"],
            "steps": public["steps"],
            "time": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "has_contact": bool(연락처.strip()),
        }
        if delivered:
            st.session_state.last_submit_at = datetime.now()

# ═══════════════════════════════════════════════════
# 9) 접수 결과 (민원인에게는 접수 여부만 보여 준다)
# ═══════════════════════════════════════════════════
receipt = st.session_state.get("receipt")
if receipt:
    st.markdown("---")
    if receipt["delivered"]:
        follow_up = (
            "의원실에서 내용을 확인한 뒤 남겨 주신 연락처로 연락드리겠습니다."
            if receipt["has_contact"]
            else "연락처를 남기지 않으셔서 따로 회신드리기는 어렵습니다. 소중한 의견은 의원실에서 꼭 확인하겠습니다."
        )
        department = receipt.get("department") or "의원실에서 확인한 뒤 안내드립니다"
        steps = "".join(f"<li>{html.escape(s)}</li>" for s in receipt.get("steps", []))
        st.markdown(
            '<div class="civic-success-badge civic-fade-in">'
            '<div class="civic-success-top">'
            '<span class="civic-success-icon">✓</span>'
            f'<div><span class="civic-success-caption">접수 시각 {receipt["time"]}</span>'
            '<strong>민원이 의원실에 전달되었습니다</strong></div>'
            '</div>'
            '<div class="civic-next">'
            '<span class="civic-next-label">담당 부서</span>'
            f'<span class="civic-next-dept">{html.escape(department)}</span>'
            + (f'<span class="civic-next-partner">협조 부서: {html.escape(receipt["partner"])}</span>'
               if receipt.get("partner") else "")
            + '<span class="civic-next-note">처리 과정에서 협조 부서가 추가될 수 있습니다.</span>'
            '</div>'
            '<div class="civic-next">'
            '<span class="civic-next-label">앞으로 이렇게 진행됩니다</span>'
            f'<ol>{steps}</ol>'
            '</div>'
            f'<p>{follow_up}</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.error(
            "죄송합니다. 지금 민원이 의원실에 전달되지 않았습니다. "
            "입력하신 내용은 그대로 남아 있으니 잠시 뒤 다시 접수해 주세요."
        )
