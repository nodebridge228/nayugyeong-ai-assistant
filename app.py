"""
🌸 나유경 춘천시의원 AI 보좌관 (v6)
- 더불어민주당 파랑 + 의원님 사진
- Gemini 3.8-flash + 텔레그램 자동 전송
- Civic Atelier 스타일
"""
import os
import re
import base64
from pathlib import Path
from datetime import datetime
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import telegram_sender

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

    .stApp {
        background: #f6f7f3;
    }

    .main .block-container {
        max-width: 1360px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ── 🎯 히어로 헤더 (민주당 파랑 + 사진) ── */
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

    .civic-hero-copy {
        padding-bottom: 40px;
    }

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

    /* ── 제출 버튼 (민주당 파랑) ── */
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
        .civic-hero {
            padding: 40px 28px 0;
            border-radius: 24px;
        }
        .civic-hero h1 {
            font-size: 42px;
        }
        .civic-hero-inner {
            grid-template-columns: 1fr;
            gap: 20px;
            text-align: center;
        }
        .civic-hero-copy {
            padding-bottom: 20px;
        }
        .civic-photo-wrap {
            width: 200px;
            height: 250px;
            margin-inline: auto;
        }
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
        .civic-section-head h2 {
            font-size: 26px;
        }
        .main .block-container {
            padding-inline: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# 3) 환경 설정
# ═══════════════════════════════════════════════════
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

if not API_KEY:
    st.error("⚠️ .env 파일에 GEMINI_API_KEY를 설정해주세요.")
    st.stop()

genai.configure(api_key=API_KEY)

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
(민원인에게 보여줄 안내문 - 정중한 존댓말, "안녕하십니까, 나유경 춘천시의원입니다"로 시작)
1. 접수 확인
2. 민원 요약
3. 향후 처리 계획
"""

# ═══════════════════════════════════════════════════
# 5) 🎯 히어로 헤더 (민주당 파랑 + 의원 사진)
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
    submitted = st.form_submit_button("🌸 민원 접수하기", use_container_width=True, type="primary")

# ═══════════════════════════════════════════════════
# 8) 분석 실행
# ═══════════════════════════════════════════════════
if submitted:
    if not 민원_원문.strip():
        st.warning("⚠️ 민원 내용을 입력해주세요.")
    else:
        with st.spinner("🌸 AI 보좌관이 민원을 분석 중입니다..."):
            try:
                user_prompt = f"""
[민원인 정보]
- 성함: {이름 if 이름 else "(미입력)"}
- 연락처: {연락처 if 연락처 else "(미입력)"}

[민원 내용]
{민원_원문}
"""
                model = genai.GenerativeModel(
                    model_name="gemini-3.8-flash",
                    system_instruction=SYSTEM_PROMPT,
                )
                response = model.generate_content(user_prompt)
                raw = response.text

                staff_match = re.search(r"===STAFF_VIEW===(.*?)===CITIZEN_VIEW===", raw, re.DOTALL)
                citizen_match = re.search(r"===CITIZEN_VIEW===(.*?)$", raw, re.DOTALL)

                staff = staff_match.group(1).strip() if staff_match else raw
                citizen = citizen_match.group(1).strip() if citizen_match else raw

                st.session_state.staff = staff
                st.session_state.citizen = citizen
                st.session_state.raw = raw

                telegram_msg = f"""🌸 나유경 춘천시의원 AI 보좌관
🔔 새 민원이 접수되었습니다

━━━━━━━━━━━━━━━━━━━━
👤 민원인: {이름 if 이름 else "(미입력)"}
📞 연락처: {연락처 if 연락처 else "(미입력)"}
━━━━━━━━━━━━━━━━━━━━

[민원 원문]
{민원_원문[:500]}

━━━━━━━━━━━━━━━━━━━━
[내부 보고서]
{staff}

━━━━━━━━━━━━━━━━━━━━
⏰ 접수 시각: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
                ok, tg_msg = telegram_sender.send_to_me(telegram_msg)

                st.session_state.telegram_sent = ok
                st.session_state.telegram_msg = "📱 의원님께 텔레그램 전송 완료!" if ok else tg_msg

            except Exception as e:
                st.error(f"❌ 분석 실패: {e}")
                st.exception(e)

# ═══════════════════════════════════════════════════
# 9) 결과 표시
# ═══════════════════════════════════════════════════
if "citizen" in st.session_state:
    st.markdown("---")
    st.markdown("""
    <div class="civic-section-head">
        <div>
            <p class="civic-kicker">02 — A THOUGHTFUL RESPONSE</p>
            <h2>확인부터 다음 단계까지,<br><span class="soft">정성스럽게 안내합니다.</span></h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("telegram_sent"):
        st.markdown(f"""
        <div class="civic-telegram-ok">
            {st.session_state.get('telegram_msg', '텔레그램 전송 완료!')}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ {st.session_state.get('telegram_msg', '전송 실패')}")

    st.markdown("""
    <div class="civic-success-badge">
        <div class="civic-success-top">
            <span class="civic-success-icon">✓</span>
            <div>
                <span class="civic-success-caption">민원이 정상적으로 접수되었습니다</span>
                <strong>접수 완료 안내</strong>
            </div>
        </div>
        <p>아래 내용은 담당자에게 전달되었습니다.<br>의원실에서 확인 후 연락드리겠습니다.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📄 의원실 내부 보고서",
        "💬 시민 전송용 문자",
        "🔎 AI 원본 출력",
    ])

    with tab1:
        st.markdown("#### 🔒 내부 보고 (외부 유출 금지)")
        st.markdown(st.session_state.staff)

    with tab2:
        st.markdown("""
        <div class="civic-letter">
            <div class="civic-letter-head">
                <p class="civic-letter-eyebrow">A LETTER FROM THE OFFICE</p>
                <h3>🌸 나유경 춘천시의원실 안내문</h3>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(st.session_state.citizen)

        st.markdown("""
            <div class="civic-letter-signature">
                <small>춘천시의원</small>
                <strong>나유경</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.text_area(
            "📋 복사용 텍스트",
            value=st.session_state.citizen,
            height=150,
            key="citizen_copy",
        )

    with tab3:
        with st.expander("AI 원본 텍스트 보기"):
            st.text(st.session_state.raw)