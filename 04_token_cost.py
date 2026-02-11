# 04_token_cost.py
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
client = OpenAI()

print("=" * 60)
print("Step 6: 토큰 기반 비용 계산")
print("=" * 60)

# GPT-4o 가격
PRICE_PER_1M_INPUT = 2.50  # $2.50 per 1M input tokens
PRICE_PER_1M_OUTPUT = 10.00  # $10.00 per 1M output tokens

encoding = tiktoken.encoding_for_model("gpt-4.1-mini")

# API 호출
input_text = "Explain the data analysis process!"
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": input_text}],
    max_tokens=500
)

# 토큰 사용량
input_tokens = response.usage.prompt_tokens
output_tokens = response.usage.completion_tokens
total_tokens = response.usage.total_tokens

# 비용 계산
input_cost = (input_tokens / 1_000_000) * PRICE_PER_1M_INPUT
output_cost = (output_tokens / 1_000_000) * PRICE_PER_1M_OUTPUT
total_cost = input_cost + output_cost

print(f"토큰 사용량:")
print(f"   입력:  {input_tokens:4d} 토큰")
print(f"   출력:  {output_tokens:4d} 토큰")
print(f"   총합:  {total_tokens:4d} 토큰")

print(f"\n 비용 계산:")
print(f"   입력:  ${input_cost:.6f}")
print(f"   출력:  ${output_cost:.6f}")
print(f"   총합:  ${total_cost:.6f}")

# 1,000번 호출 시 예상 비용
print(f"\n 스케일 예측 (1,000번 호출):")
print(f"   예상 비용: ${total_cost * 1000:.2f}")

# 월 예산 시뮬레이션
monthly_budget = 100  # $100 예산
calls_per_budget = int(monthly_budget / total_cost)
print(f"\n 예산 ${monthly_budget}로 가능한 호출:")
print(f"   약 {calls_per_budget:,}번 호출 가능")


