# 01_basic_tokenization.py
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
client = OpenAI()

print("=" * 60)
print("Step 1: 기본 토큰화 - 텍스트를 숫자(토큰 ID)로 변환")
print("=" * 60)

# 1. 인코더 로드
encoding = tiktoken.encoding_for_model("gpt-4.1-nano")
print(f"인코더 로드 완료: {encoding.name}")

# 2. 텍스트를 토큰 ID로 변환
text = "Hello World!"
token_ids = encoding.encode(text)

# 3. 출력해서 확인하기 
print(type(token_ids))

print(f"원본 텍스트: {text}")
print(f"총 토큰 수: {len(token_ids)}\n")

tokens = [encoding.decode([token_id]) for token_id in token_ids]

print("토큰 분해:")
for i, (token_id, token) in enumerate(zip(token_ids, tokens), 1):
    # 토큰을 보기 좋게 표시 (공백, 줄바꿈 등 특수문자 표시)
    token_display = token.replace(' ', '/')
    print(f"  [{i}] ID: {token_id:6d} | Token: '{token_display}'")
    
    
    
    