import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# [설정] 환경 변수 로드 (API 키 확인)
load_dotenv("key.env")

# [설정] OpenAI 클라이언트 초기화
client = OpenAI()

# [UI] 애플리케이션 제목
st.title("🎛️ GPT 텍스트 생성기 (설정 가능)")

# [UI/로직] 4. 시스템 프롬프트와 Temperature 설정 (사이드바 또는 Expander 활용)
with st.expander("🛠️ 모델 설정 (System Prompt & Temperature)", expanded=True):
    # 시스템 프롬프트 입력 (기본값 설정)
    system_prompt = st.text_input(
        "시스템 프롬프트 (AI의 역할)",
        value="You are a helpful assistant.",
        help="AI에게 부여할 역할이나 성격을 정의하세요."
    )
    
    # Temperature 조절 (슬라이더 사용)
    temperature = st.slider(
        "Temperature (창의성 조절)",
        min_value=0.0,
        max_value=2.0, # GPT-4o 기준 최대 2.0 (일반적으로 0~1 사용)
        value=0.7,
        step=0.1,
        help="낮을수록 사실적이고, 높을수록 창의적인 답변이 나옵니다."
    )

# [UI] 1. 사용자 질문 입력창 구성
st.subheader("질문 입력")
user_input = st.text_area("GPT에게 물어볼 내용을 입력하세요:", height=150)

# [UI/로직] 5. 버튼 클릭 시 실행
if st.button("🚀 답변 생성하기"):
    if not user_input:
        st.warning("⚠️ 질문 내용을 입력해주세요!")
    else:
        # 답변 생성 중임을 알리는 스피너 표시
        with st.spinner("AI가 답변을 생각하는 중입니다..."):
            try:
                # [로직] 2. OpenAI API로 질문 전달 및 응답 생성
                response = client.chat.completions.create(
                    model="gpt-4o", # 또는 "gpt-3.5-turbo"
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=temperature
                )
                
                answer = response.choices[0].message.content
                
                # [UI] 3. 생성된 응답 화면 출력
                st.subheader("💡 AI의 답변")
                st.markdown(answer) # 마크다운 형식 지원
                
            except Exception as e:
                st.error(f"❌ 에러가 발생했습니다: {e}")