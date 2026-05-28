"""앱 전체에 적용하는 커스텀 디자인.

참고: sample.dreamitbiz.com 의 personal-02 "카드형 이력서(Resume)" 디자인.
- 웜 페이퍼 배경(#f4f1ec) + 테라코타 액센트(#b34a2a)
- 다크 사이드바(#1d1c1a) + 밝은 텍스트 (이력서의 좌측 사이드바 컨셉)
- Pretendard 폰트, 8~12px 둥근 모서리, 종이 카드 + 부드러운 그림자
"""

import streamlit as st

# 디자인 토큰 (personal-02 :root 변수에서 차용)
ACCENT = "#b34a2a"   # 테라코타
BG = "#f4f1ec"       # 웜 페이퍼
PAPER = "#ffffff"
INK = "#1d1c1a"      # 웜 잉크 (텍스트 & 사이드바 배경)
MUTED = "#6e6a64"
LINE = "#e5dfd4"
SIDE_TEXT = "#ece6da"

CUSTOM_CSS = f"""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css');

/* ── 전역 폰트 ───────────────────────────────────────────── */
html, body, [class*="st-"], .stApp {{
    font-family: 'Pretendard', 'Noto Sans KR', -apple-system, BlinkMacSystemFont,
                 'Segoe UI', sans-serif !important;
    color: {INK};
    line-height: 1.55;
}}
.stApp {{ background: {BG}; }}

/* 머티리얼 아이콘은 폰트 오버라이드에서 제외(아이콘이 글자로 깨지는 것 방지) */
[data-testid="stIconMaterial"],
span[class*="material-symbols"],
.material-icons, .material-icons-outlined, .material-icons-round {{
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined',
                 'Material Icons' !important;
}}

/* ── 히어로 헤더 (종이 카드 + 테라코타 아바타) ───────────── */
.hero {{
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 24px 28px;
    border-radius: 12px;
    background: {PAPER};
    border: 1px solid {LINE};
    border-bottom: 3px solid {ACCENT};
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    margin-bottom: 22px;
}}
.hero-icon {{
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: {ACCENT};
    color: #fff;
    display: grid;
    place-items: center;
    font-size: 30px;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(179, 74, 42, 0.30);
}}
.hero-title {{
    color: {INK};
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0;
}}
.hero-sub {{
    color: {MUTED};
    font-size: 14px;
    margin-top: 4px;
}}

/* ── 다크 사이드바 (이력서 좌측 컬럼 컨셉) ─────────────────── */
[data-testid="stSidebar"] {{
    background: {INK};
    border-right: 1px solid #000;
}}
/* 사이드바 기본 텍스트는 밝게 */
[data-testid="stSidebar"],
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
    color: {SIDE_TEXT} !important;
}}
/* 사이드바 섹션 헤더는 테라코타 강조 (이력서 side-title 느낌) */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    color: {ACCENT} !important;
    letter-spacing: 1px;
    font-size: 18px;
}}
/* 입력 위젯은 흰 종이 + 어두운 글자로 가독성 유지 */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background: {PAPER} !important;
    color: {INK} !important;
    border-radius: 8px !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] * {{ color: {INK} !important; }}

/* ── 채팅 말풍선 (종이 카드) ───────────────────────────────── */
[data-testid="stChatMessage"] {{
    background: {PAPER};
    border: 1px solid {LINE};
    border-radius: 10px;
    padding: 6px 16px;
    margin-bottom: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}}
/* 사용자 말풍선: 페이퍼 톤 + 테라코타 좌측 보더 */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
    background: {BG};
    border-left: 3px solid {ACCENT};
}}

/* ── 버튼 (테라코타) ───────────────────────────────────────── */
.stButton > button {{
    background: {ACCENT};
    color: #fff;
    border: 0;
    border-radius: 8px;
    font-weight: 600;
    transition: filter 0.2s ease, transform 0.12s ease;
}}
.stButton > button:hover {{
    filter: brightness(1.08);
    transform: translateY(-1px);
    color: #fff;
}}

/* ── 입력 위젯 ─────────────────────────────────────────────── */
[data-testid="stChatInput"] {{
    background: {PAPER};
    border: 1px solid {LINE};
    border-radius: 10px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}}
[data-baseweb="select"] > div {{ border-radius: 8px !important; }}
[data-testid="stAlert"] {{ border-radius: 10px; }}
</style>
"""


def apply_design():
    """커스텀 CSS를 페이지에 주입한다. set_page_config 직후 한 번 호출."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero(title: str, subtitle: str, icon: str = "🛡️"):
    """히어로 헤더를 렌더링한다(기존 st.title 대체)."""
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
