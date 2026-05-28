"""피싱 분석 챗봇 — Streamlit 메인 앱.

실행: streamlit run app.py
"""

import streamlit as st

from config import (
    PROVIDERS, PHISHING_SYSTEM_PROMPT, WELCOME_MESSAGE, PHISHING_SAMPLES,
    MAX_OUTPUT_TOKENS, MAX_INPUT_CHARS,
)
from chat_client import stream_chat
from styles import apply_design, render_hero

st.set_page_config(page_title="피싱 분석 챗봇", page_icon="🛡️")
apply_design()


def get_secret_key() -> str:
    """Streamlit Secrets에 저장된 기본 API 키를 읽는다(배포 환경용).

    로컬에서 secrets가 없으면 빈 문자열을 반환한다.
    """
    try:
        return st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        return ""


SECRET_KEY = get_secret_key()

# --- 세션 상태 초기화 ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{"role": ..., "content": ...}]
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# --- 사이드바: 설정 -----------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 설정")

    provider = st.selectbox("제공사", list(PROVIDERS.keys()))
    model = st.selectbox("모델", PROVIDERS[provider]["models"])

    st.session_state.api_key = st.text_input(
        "OpenAI API 키",
        type="password",
        value=st.session_state.api_key,
        placeholder="sk-... (비워두면 서버 기본 키 사용)" if SECRET_KEY else "sk-...",
    )
    if SECRET_KEY:
        st.caption("🔑 서버에 기본 키가 설정되어 있어 바로 사용할 수 있습니다. "
                   "직접 입력하면 입력한 키를 우선 사용합니다.")
    else:
        st.caption("🔒 키는 이 세션에만 보관되며 디스크에 저장되지 않습니다. "
                   "앱을 재시작하면 다시 입력해야 합니다.")

    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 사이드바 입력이 있으면 그것을, 없으면 서버 기본 키(Secrets)를 사용한다.
effective_key = st.session_state.api_key.strip() or SECRET_KEY

# --- 메인 헤더 ---------------------------------------------------------------
render_hero("피싱 분석 챗봇", "의심스러운 이메일·문자·URL을 분석해 드립니다", icon="🛡️")

# --- 사용 가능 여부 판단(게이트) ----------------------------------------------
provider_enabled = PROVIDERS[provider]["enabled"]
has_key = bool(effective_key)

if not provider_enabled:
    st.warning(
        f"**{provider}** 는 아직 API 키가 설정되지 않았습니다. "
        "사이드바에서 제공사를 **ChatGPT** 로 선택해 주세요."
    )
elif not has_key:
    st.info("👈 사이드바 설정에서 **OpenAI API 키**를 먼저 등록해 주세요.")
else:
    st.caption(WELCOME_MESSAGE)

ready = provider_enabled and has_key

# --- 시작 도우미: 샘플 예시 (대화가 비어있을 때만 노출) ----------------------
if ready and not st.session_state.messages:
    st.markdown("##### 👇 예시를 눌러 바로 체험해 보세요")
    cols = st.columns(len(PHISHING_SAMPLES))
    for col, sample in zip(cols, PHISHING_SAMPLES):
        if col.button(sample["label"], use_container_width=True):
            st.session_state.pending_sample = sample["text"]
            st.rerun()

# --- 기존 대화 렌더링 ---------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 입력 처리 ---------------------------------------------------------------
prompt = st.chat_input(
    "의심스러운 이메일·문자·URL을 붙여넣으세요" if ready else "먼저 API 키를 등록하세요",
    disabled=not ready,
    max_chars=MAX_INPUT_CHARS,  # 위젯 레벨 입력 길이 제한
)

# 샘플 버튼으로 선택한 내용이 있으면 직접 입력한 것처럼 처리한다.
if st.session_state.get("pending_sample"):
    prompt = st.session_state.pop("pending_sample")

if prompt:
    # 처리 전 입력 길이 검증 (비용·토큰 초과 방지)
    if len(prompt) > MAX_INPUT_CHARS:
        st.warning(
            f"⚠️ 입력이 너무 깁니다 ({len(prompt):,}자). "
            f"{MAX_INPUT_CHARS:,}자 이내로 줄여 주세요."
        )
    else:
        # 사용자 메시지 표시 및 저장
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 모델에 보낼 메시지: 시스템 프롬프트 + 대화 기록
        api_messages = [{"role": "system", "content": PHISHING_SYSTEM_PROMPT}]
        api_messages += st.session_state.messages

        # 어시스턴트 응답 스트리밍 (응답 토큰 상한으로 비용 제어)
        with st.chat_message("assistant"):
            response = st.write_stream(
                stream_chat(effective_key, model, api_messages, max_tokens=MAX_OUTPUT_TOKENS)
            )

        st.session_state.messages.append({"role": "assistant", "content": response})
