from openai import OpenAI
from dotenv import load_dotenv
import sys
import os

# [수정] 사용자 환경에 맞춰 key.env 파일 로드
load_dotenv("key.env")
client = OpenAI()

# LLM 호출 함수
def chatbot(messages, temperature=0.7, max_tokens=1000, model="gpt-4.1-mini"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens # 최신 라이브러리 버전에 따라 max_completion_tokens로 변경 가능
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"API 호출 실패: {str(e)}")

def main():
    print("Prompt Engineering 실습 - Multi-turn Conversation\n")

    system = "You are a helpful assistant."
    temp = 0.7
    
    # [요청사항 반영] 모델명을 gpt-4.1-mini로 설정
    model = "gpt-4.1-mini" 

    # [수정] 대화 히스토리 초기화
    # 원본 텍스트에는 system_prompt 변수가 정의되지 않아 system으로 변경했습니다.
    history = [{"role": "system", "content": system}] 

    while True:
        try:
            user_input = input("입력: ").strip()

            if user_input.lower() in ["exit", "q", "종료"]:
                print("Chatbot: Goodbye!")
                break

            if not user_input:
                print("질문을 입력해주세요.")
                continue

            # 1. 사용자 입력을 히스토리에 추가 (기억하기)
            history.append({"role": "user", "content": user_input})

            # 2. 전체 히스토리를 AI에게 전달
            answer = chatbot(
                messages=history,
                temperature=temp,
                model=model
            )
            
            print(f"답변: {answer}\n")

            # 3. AI의 답변도 히스토리에 추가 (기억하기)
            history.append({"role": "assistant", "content": answer})

        except KeyboardInterrupt:
            print("\n 프로그램을 종료합니다.")
            sys.exit(0)
            
        except Exception as e:
            print(f"\n 에러 발생: {e}")
            print("다시 시도해주세요.\n")

if __name__ == "__main__":
    main()