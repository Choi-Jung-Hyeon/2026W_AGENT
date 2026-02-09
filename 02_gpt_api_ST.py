import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# [설정] .env 파일에서 API 키 로드 (보안을 위해 환경변수 사용)
load_dotenv("key.env")

# [설정] OpenAI 클라이언트 초기화
client = OpenAI()

# [UI] 애플리케이션 제목 설정
st.title("🤖 나만의 AI 챗봇")

# [로직] 4. 세션 상태(session_state)를 활용하여 대화 기록 유지
# 'messages'라는 키가 없으면 빈 리스트로 초기화합니다.
if "messages" not in st.session_state:
    st.session_state.messages = []

# [UI] 기존 대화 내용 출력
# 세션에 저장된 모든 메시지를 순서대로 화면에 표시합니다.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# [UI/로직] 1. 사용자 입력 받기 (chat_input 사용)
if prompt := st.chat_input("질문을 입력하세요..."):
    # 사용자가 입력한 내용을 화면에 표시
    with st.chat_message("user"):
        st.write(prompt)
    
    # 대화 기록(세션)에 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})

    # [로직] 2. OpenAI API로 질문 전달 및 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("답변 생성 중..."):
            try:
                # 3. 모델의 응답을 받아옴 (전체 대화 기록 전달하여 문맥 유지)
                response = client.chat.completions.create(
                    model="gpt-4o",  # 사용 가능한 모델명 (gpt-3.5-turbo 등)
                    messages=st.session_state.messages
                )
                assistant_response = response.choices[0].message.content
                st.write(assistant_response)
                
                # [로직] 대화 기록(세션)에 AI 응답 추가
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")