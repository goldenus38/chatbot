"""OpenAI(ChatGPT) 호출 래퍼. 응답을 스트리밍으로 흘려준다."""

from openai import OpenAI, AuthenticationError, APIConnectionError


def stream_chat(api_key: str, model: str, messages: list[dict]):
    """ChatGPT 응답을 토큰 단위로 yield 하는 제너레이터.

    Args:
        api_key: OpenAI API 키
        model:   사용할 모델명 (예: "gpt-4o-mini")
        messages: [{"role": "system"|"user"|"assistant", "content": str}, ...]

    Yields:
        응답 텍스트 조각(str). 오류 발생 시 사용자 친화 메시지를 한 번 yield 한다.
    """
    try:
        client = OpenAI(api_key=api_key)
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
    except AuthenticationError:
        yield "⚠️ API 키가 올바르지 않습니다. 사이드바에서 키를 다시 확인해 주세요."
    except APIConnectionError:
        yield "⚠️ OpenAI 서버에 연결하지 못했습니다. 네트워크 상태를 확인해 주세요."
    except Exception as e:
        # 스트리밍 도중 연결 끊김 등 예기치 못한 오류도 앱이 죽지 않도록 처리한다.
        yield f"⚠️ 요청 처리 중 오류가 발생했습니다: {e}"
