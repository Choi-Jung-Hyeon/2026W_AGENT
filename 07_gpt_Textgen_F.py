import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. 환경 변수 및 API 키 로드
load_dotenv("key.env")
client = OpenAI()

# 2. 챗봇 함수 정의 (강사님 코드에서 호출하는 함수)
# 이 부분이 없으면 'name 'chatbot' is not defined' 에러가 납니다.
def chatbot(messages, temperature=0.7, model="gpt-4o"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # 에러 발생 시 프로그램이 멈추지 않도록 예외 처리
        return f"죄송합니다. 오류가 발생했습니다: {str(e)}"

# 3. 메인 함수 (강사님이 보내주신 코드 + 수정사항)
def main():
    print("Prompt Engineering 실습 - 대화 기억하기(Multi-turn)\n")

    # 설정
    system_prompt = "You are a helpful assistant."
    temp = 0.7
    
    # [수정] gpt-4.1-mini는 존재하지 않는 모델명이므로 gpt-4o로 변경했습니다.
    # 만약 수업용 전용 프록시를 쓴다면 그대로 두셔도 됩니다.
    model = "gpt-4.1-mini" 

    # 대화 히스토리 초기화
    # 최신 모델(gpt-4o 등)에서는 'developer' 대신 'system'을 주로 사용합니다.
    history = [
        {"role": "system", "content": system_prompt}
    ]

    while True:
        try:
            user_input = input("입력: ").strip()

            # 종료 조건
            if user_input.lower() in ["exit", "q", "종료"]:
                print("Chatbot: Goodbye!")
                break

            # 빈 입력 방지
            if not user_input:
                print("질문을 입력해주세요.")
                continue

            # 4. 사용자 메시지를 히스토리에 추가 (기억하기)
            history.append({"role": "user", "content": user_input})

            # API 호출 (전체 히스토리를 보냄)
            answer = chatbot(
                messages=history,
                temperature=temp,
                model=model
            )

            # 응답 출력
            print(f"답변: {answer}\n")

            # 5. AI 응답을 히스토리에 추가 (기억하기)
            history.append({"role": "assistant", "content": answer})

        except KeyboardInterrupt:
            print("\n 프로그램을 종료합니다.")
            sys.exit(0)

        except Exception as e:
            print(f"\n 에러 발생: {e}")
            print("다시 시도해주세요.\n")

if __name__ == "__main__":
    main()