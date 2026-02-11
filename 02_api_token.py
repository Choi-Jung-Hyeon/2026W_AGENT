# 02_API_token.py
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# 순수 텍스트만의 토큰 수
encoding = tiktoken.encoding_for_model("gpt-4.1-mini")
text = "안녕하세요!"
pure_tokens = len(encoding.encode(text))
print(f"순수 텍스트 토큰: {pure_tokens}")

# 실제 API 호출 시 소비되는 토큰
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "안녕하세요!"}],
    max_tokens=1  # 응답을 최소화 
    )

actual_tokens = response.usage.prompt_tokens
print(f"실제 API 입력 토큰: {actual_tokens}")
print(f"차이 (포맷팅 오버헤드): {actual_tokens - pure_tokens}")


