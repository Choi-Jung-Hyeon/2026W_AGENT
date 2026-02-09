import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 1. 환경 변수 및 API 키 로드
load_dotenv("key.env")
client = OpenAI()

# [설정] 모델 및 시스템 프롬프트 정의
MODEL_NAME = "gpt-4.1-mini"
SYSTEM_PROMPT = "You are a helpful assistant."

# 2. 챗봇 함수 정의 (API 호출 담당)
def get_response(messages, temperature=0.7, model=MODEL_NAME):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"죄송합니다. 오류가 발생했습니다: {str(e)}"

# 3. Streamlit 앱 메인 로직
def main():
    st.title("💬 Streamlit AI 챗봇 (Multi-turn)")
    st.caption(f"현재 사용 중인 모델: {MODEL_NAME}")

    # [세션 상태 초기화] 대화 히스토리가 없으면 생성 및 시스템 프롬프트 추가
    if "history" not in st.session_state:
        st.session_state.history = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    # [화면 출력] 기존 대화 내용 표시 (시스템 메시지는 제외)
    for message in st.session_state.history:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # [사용자 입력] 채팅창에 입력이 들어오면 실행
    if prompt := st.chat_input("메시지를 입력하세요..."):
        
        # 1. 사용자 메시지 화면 표시 및 히스토리에 추가
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.history.append({"role": "user", "content": prompt})

        # 2. AI 응답 생성 (스피너 표시)
        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                answer = get_response(
                    messages=st.session_state.history,
                    temperature=0.7,
                    model=MODEL_NAME
                )
                st.markdown(answer)

        # 3. AI 응답 히스토리에 추가
        st.session_state.history.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()