from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("key.env")
client = OpenAI()

# LLM 호출 함수
def chatbot( user_prompt,
             system_prompt="You are a helpful assistant.",
             temperature=0.7,
             max_tokens=1000):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # 실행 시 gpt-4o-mini 등으로 수정 필요
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt} ],
        temperature=temperature,
        max_completion_tokens=max_tokens ) # openai 최신 버전에서는 max_completion_tokens 권장
    
    return response.choices[0].message.content.strip()

print("Prompt Engineering 실습 - Roleplay 입력 버전\n")

# System Prompt (롤플레이) 입력
system_prompt = input(
    "롤플레이(System Prompt)를 입력하세요\n"
    "(엔터만 누르면 기본값 사용):\n " ).strip()

if not system_prompt:
    system_prompt = "You are a helpful assistant."

print(f"\n[사용 중인 역할]\n→ {system_prompt}\n")

# Temperature 입력 (0~1)
while True:
    temp_input = input("Temperature 입력 (0.0 ~ 1.0, 기본0.7):").strip()
    if temp_input == "":
        temperature = 0.7
        break
    try:
        temperature = float(temp_input)
        if 0.0 <= temperature <= 1.0:
            break
    except ValueError:
        pass
    print("0.0 ~ 1.0 사이의 숫자를 입력하세요.")

# 사용자 질문 입력
user_input = input("\n질문을 입력하세요:\n> ").strip()

if not user_input:
    print("⚠ 질문이 입력되지 않아 프로그램을 종료합니다.")
    exit()

# GPT 호출
answer = chatbot(
    user_input,
    system_prompt=system_prompt,
    temperature=temperature
)

# 결과 출력
print("\n 답변:")
print(answer)