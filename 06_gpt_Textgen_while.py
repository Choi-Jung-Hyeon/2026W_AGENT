import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

# [설정] 환경 변수 로드 (key.env 파일이 같은 폴더에 있어야 함)
load_dotenv("key.env")
client = OpenAI()

# [함수] LLM 호출 함수 (표준 API 문법으로 수정됨)
def chatbot(user_prompt,
            system_prompt="You are a helpful assistant.",
            temperature=0.7,
            max_tokens=1000,
            model="gpt-4.1-mini"): # gpt-4.1-mini는 존재하지 않으므로 gpt-4o로 변경
    
    try:
        # 수정됨: client.responses.create -> client.chat.completions.create
        response = client.chat.completions.create(
            model=model,
            messages=[  # input -> messages
                {"role": "system", "content": system_prompt}, # developer -> system
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens # max_output_tokens -> max_tokens
        )
        # 수정됨: response.output_text -> response.choices[0].message.content
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        # 에러 발생 시 호출한 곳으로 에러 메시지 전달
        raise Exception(f"API 호출 실패: {str(e)}")


# [메인] 프로그램 실행 로직
def main():
    print("Prompt Engineering 실습 - Interactive Loop\n")

    system = "You are a helpful assistant."
    temp = 0.7
    model = "gpt-4o"  # 사용 가능한 모델명으로 설정

    while True:
        try:
            # 사용자 입력 받기
            user_input = input("입력: ").strip()

            # 종료 조건 확인
            if user_input.lower() in ["exit", "q", "종료"]:
                print("Chatbot: Goodbye!")
                break

            # 빈 입력 방지
            if not user_input:
                print("⚠️ 질문을 입력해주세요.\n")
                continue

            # 챗봇 함수 호출
            answer = chatbot(
                user_prompt=user_input,
                system_prompt=system,
                temperature=temp,
                model=model
            )
            
            # 결과 출력
            print(f"답변: {answer}\n")

        except KeyboardInterrupt:
            # Ctrl+C 입력 시 종료
            print("\n\n👋 프로그램을 종료합니다.")
            sys.exit(0)

        except Exception as e:
            # 에러 발생 시 처리
            print(f"\n❌ 에러 발생: {e}")
            print("다시 시도해주세요.\n")


if __name__ == "__main__":
    main()