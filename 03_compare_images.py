# 03_compare_images.py
from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()
client = OpenAI()

def encode_image(image_path):
    """이미지를 base64로 인코딩"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_mime_type(image_path):
    """파일 확장자로 MIME 타입 결정"""
    ext = os.path.splitext(image_path)[1].lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    return mime_types.get(ext, 'image/jpeg')

# 비교할 이미지 경로
image1_path = "image1.jpg"
image2_path = "image2.jpg"

# base64 인코딩
image1_base64 = encode_image(image1_path)
image2_base64 = encode_image(image2_path)

# MIME 타입 자동 결정
mime_type1 = get_mime_type(image1_path)
mime_type2 = get_mime_type(image2_path)

# 메시지 구성
messages = [
    {
        "role": "user",
        "content": [
            {"type": "input_text", "text": "두 이미지의 차이점을 설명해주세요."},
            {
                "type": "input_image",
                "image_url": f"data:{mime_type1};base64,{image1_base64}"
            },
            {
                "type": "input_image",
                "image_url": f"data:{mime_type2};base64,{image2_base64}"
            },
        ],
    }
]

# ✅ 최신 OpenAI API 호출
response = client.responses.create(
    model="gpt-4.1-mini",
    input=messages
)

print("두 이미지 비교 결과:")
print(response.output_text)
