# 03_token_visualization.py
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
client = OpenAI()

print("=" * 60)
print("Step 3: 토큰 분해 시각화")
print("=" * 60)

encoding = tiktoken.encoding_for_model("gpt-4o")

def visualize_tokens(text):
    """토큰 분해를 시각적으로 표시"""
    token_ids = encoding.encode(text)
    
    print(f"원본: {text}")
    print(f"총 {len(token_ids)}개 토큰\n")
    print("토큰 분해:")
    print("-" * 50)
    
    for i, token_id in enumerate(token_ids, 1):
        token_text = encoding.decode([token_id])
        # 공백을 시각화
        display_text = token_text.replace(' ', '␣').replace('\n', '↵')
        print(f"  [{i:2d}] ID: {token_id:6d} → '{display_text}'")
    
    print("-" * 50)
    return len(token_ids)

# 영어 예시
print("\n 영어 토큰화:")
english_tokens = visualize_tokens("Explain the data analysis process!")

# 한글 예시
print("\n 한글 토큰화:")
korean_tokens = visualize_tokens("데이터 분석 프로세스를 설명해주세요!")

# 비교
print(f"\n 토큰 효율성 비교:")
print(f"   영어: {english_tokens}개 토큰")
print(f"   한글: {korean_tokens}개 토큰")


