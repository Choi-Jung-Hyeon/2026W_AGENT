import os
from getpass import getpass

# API 키 입력 받기
if 'OPENAI_API_KEY' not in os.environ:
    os.environ['OPENAI_API_KEY'] = getpass('OpenAI API Key: ')

print("✅ 설정 완료!")