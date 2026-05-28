"""Anthropic(Claude) 호출 래퍼. 응답을 스트리밍으로 흘려준다.

OpenAI와 다른 점:
- 시스템 프롬프트를 messages가 아닌 별도 `system` 파라미터로 전달
- messages는 user/assistant 역할만 포함 (system 역할 없음)
"""

from __future__ import annotations  # 타입 힌트 지연 평가 (Python 3.9 호환)

from anthropic import Anthropic, AuthenticationError, APIConnectionError


def stream_claude(api_key: str, model: str, system: str, messages: list[dict], max_tokens: int):
    """Claude 응답을 토큰 단위로 yield 하는 제너레이터.

    Args:
        api_key: Anthropic API 키 (sk-ant-...)
        model:   모델명 (예: "claude-opus-4-7")
        system:  시스템 프롬프트 (별도 파라미터로 전달)
        messages: [{"role": "user"|"assistant", "content": str}, ...]
        max_tokens: 응답 토큰 상한 (Anthropic은 필수)

    Yields:
        응답 텍스트 조각(str). 오류 시 사용자 친화 메시지를 한 번 yield 한다.
    """
    try:
        client = Anthropic(api_key=api_key)
        with client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield text
    except AuthenticationError:
        yield "⚠️ Anthropic API 키가 올바르지 않습니다. 사이드바에서 키를 다시 확인해 주세요."
    except APIConnectionError:
        yield "⚠️ Anthropic 서버에 연결하지 못했습니다. 네트워크 상태를 확인해 주세요."
    except Exception as e:
        # 스트리밍 도중 끊김 등 예기치 못한 오류도 앱이 죽지 않도록 처리한다.
        yield f"⚠️ 요청 처리 중 오류가 발생했습니다: {e}"
