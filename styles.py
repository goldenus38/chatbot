"""앱 전체에 적용하는 커스텀 디자인.

참고 사이트(sample.dreamitbiz.com)의 디자인 시스템을 차용:
- 인디고 액센트(#6366f1) + 로열블루(#0046c8) 135° 그라데이션
- Pretendard 폰트, 둥근 모서리(12~16px), 부드러운 그림자, 카드형 레이아웃
"""

import streamlit as st

# 디자인 토큰
ACCENT = "#6366f1"
ACCENT_DEEP = "#0046c8"
TEXT = "#0f172a"

CUSTOM_CSS = f"""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css');

/* ── 전역 폰트 ───────────────────────────────────────────── */
html, body, [class*="st-"], .stApp {{
    font-family: 'Pretendard', 'Noto Sans KR', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', sans-serif !important;
    color: {TEXT};
}}

/* 머티리얼 아이콘은 폰트 오버라이드에서 제외(아이콘이 글자로 깨지는 것 방지) */
[data-testid="stIconMaterial"],
span[class*="material-symbols"],
.material-icons, .material-icons-outlined, .material-icons-round {{
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined',
                 'Material Icons' !important;
}}

/* ── 그라데이션 히어로 헤더 ─────────────────────────────── */
.hero {{
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 26px 30px;
    border-radius: 16px;
    background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_DEEP} 100%);
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.30);
    margin-bottom: 22px;
}}
.hero-icon {{
    font-size: 40px;
    line-height: 1;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}}
.hero-title {{
    color: #ffffff;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
}}
.hero-sub {{
    color: rgba(255,255,255,0.88);
    font-size: 14px;
    margin-top: 4px;
}}

/* ── 채팅 말풍선 (카드형) ───────────────────────────────── */
[data-testid="stChatMessage"] {{
    border-radius: 16px;
    padding: 6px 16px;
    margin-bottom: 12px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
    background: #ffffff;
}}
/* 사용자 말풍선: 인디고 톤 */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
    background: rgba(99, 102, 241, 0.07);
    border-color: rgba(99, 102, 241, 0.25);
}}

/* ── 버튼 (그라데이션 + 호버 리프트) ───────────────────── */
.stButton > button {{
    border-radius: 999px;
    border: none;
    background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_DEEP} 100%);
    color: #ffffff;
    font-weight: 600;
    transition: transform 0.12s ease, box-shadow 0.12s ease;
}}
.stButton > button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(99, 102, 241, 0.35);
    color: #ffffff;
}}

/* ── 입력 위젯 둥글게 ───────────────────────────────────── */
[data-testid="stChatInput"], .stTextInput input, [data-baseweb="select"] > div {{
    border-radius: 12px !important;
}}
[data-testid="stChatInput"] {{
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
}}

/* ── 사이드바 ───────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: #f8fafc;
    border-right: 1px solid #e5e7eb;
}}

/* ── 안내 박스(info/warning) 둥글게 ────────────────────── */
[data-testid="stAlert"] {{
    border-radius: 12px;
}}
</style>
"""


def apply_design():
    """커스텀 CSS를 페이지에 주입한다. set_page_config 직후 한 번 호출."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str, icon: str = "🛡️"):
    """그라데이션 히어로 헤더를 렌더링한다(기존 st.title 대체)."""
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-icon">{icon}</div>
            <div>
                <div class="hero-title">{title}</div>
                <div class="hero-sub">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
