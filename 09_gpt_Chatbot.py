import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# [수정] 강사님 코드는 .env지만, 사용자님은 key.env를 쓰시므로 수정했습니다.
load_dotenv("key.env")
client = OpenAI()

# Streamlit 버전 호환성을 위한 rerun 함수
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.warning("현재 Streamlit 버전에서 rerun 함수가 지원되지 않습니다.")

# LLM 호출 함수 (최신 Responses API 사용)
def chatbot(messages, temperature=0.7, max_tokens=1000, model="gpt-4.1-mini"):
    try:
        # [최신 문법] client.responses.create 사용
        response = client.responses.create(
            model=model,
            input=messages,           # messages -> input
            temperature=temperature,
            max_output_tokens=max_tokens # max_tokens -> max_output_tokens
        )
        return response.output_text.strip() # content -> output_text

    except Exception as e:
        return f"❌ API 호출 실패: {str(e)}"

# -------------------------------------------------------------------
# Streamlit UI 설정
# -------------------------------------------------------------------

# 1. 페이지 기본 설정 (탭 제목, 아이콘)
st.set_page_config(page_title="나만의 GPT 챗봇", page_icon="🤖")
st.title("🤖 GPT 챗봇 (Responses API)")

# 2. 사이드바 설정 (옵션 조절)
with st.sidebar:
    st.header("⚙️ 설정")

    # 모델 선택 (gpt-4.1-mini 기본)
    model = st.selectbox(
        "모델 선택",
        ["gpt-4.1-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0
    )

    # Temperature 조절 슬라이더
    temperature = st.slider(
        "Temperature (창의성)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="값이 높을수록 더 창의적이고 다양한 답변을 합니다."
    )

    st.divider()

    # 🔄 대화 다시 시작 버튼
    if st.button("🔄 대화 초기화"):
        st.session_state.messages = [
            {
                "role": "developer",
                "content": "You are a helpful assistant. Respond in Korean."
            }
        ]
        safe_rerun() # 화면 새로고침

# 3. 세션 상태 초기화 (대화 기록 저장소)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "developer",
            "content": "You are a helpful assistant. Respond in Korean."
        }
    ]

# 4. 이전 대화 내용 화면에 출력
for msg in st.session_state.messages:
    # 시스템(developer) 메시지는 화면에 안 보여줌
    if msg["role"] == "developer":
        continue
    
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. 사용자 입력 처리
user_input = st.chat_input("메시지를 입력하세요...")

if user_input:
    # (1) 사용자 메시지를 화면에 표시하고 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # (2) GPT 응답 생성 및 표시
    with st.chat_message("assistant"):
        with st.spinner("생각하는 중..."):
            answer = chatbot(
                messages=st.session_state.messages,
                temperature=temperature,
                model=model
            )
            st.markdown(answer)

    # (3) GPT 응답 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )