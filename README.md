# 🛡️ 피싱 분석 챗봇

의심스러운 **이메일 · 문자 · URL**을 붙여넣으면 피싱 위험 신호를 분석해 주는 챗봇입니다.
바이브코딩 교육 과정 실습 과제로, **Streamlit + OpenAI(ChatGPT)** 로 구현했습니다.

## 주요 기능

- 챗봇 사용 전 **제공사(ChatGPT / Claude)** 와 **모델** 선택
- 설정 화면에서 **API 키 등록** (세션에만 보관, 디스크 미저장)
- 피싱 분석: **위험도 → 위험 신호 → 판단 근거 → 권장 대응** 구조로 응답
- 후속 질문도 대화로 이어가는 채팅 인터페이스

> 이번 실습에서는 OpenAI 키만 등록합니다. Claude는 선택지로 보이지만 비활성 상태입니다.

## 실행 방법

```bash
# 1) 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2) 의존성 설치
pip install -r requirements.txt

# 3) 앱 실행
streamlit run app.py
```

브라우저가 열리면 사이드바에 **OpenAI API 키**(`sk-...`)를 입력한 뒤 채팅을 시작하세요.

## 파일 구조

| 파일 | 설명 |
|---|---|
| `app.py` | 메인 앱 — 사이드바 설정 + 채팅 UI |
| `config.py` | 제공사·모델 목록, 피싱 분석 시스템 프롬프트 |
| `chat_client.py` | OpenAI 호출 래퍼 (스트리밍) |
| `requirements.txt` | 의존성 |

## 보안 참고

- API 키는 `st.session_state`에만 저장되어 **브라우저나 디스크에 노출되지 않습니다**.
- 앱을 재시작하면 키를 다시 입력해야 합니다(의도된 동작).
- 본 챗봇은 **방어 목적**(피싱 식별·예방)으로만 사용하세요. 분석 결과는 참고용입니다.
