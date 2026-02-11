# 02_Local_img.py
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv(".env")
client = OpenAI()

# 이미지 경로
image_path = "배경사진.jpg"

# 이미지를 base64로 변환
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# API 요청
# API 요청 (최신 OpenAI Responses API)
response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "이 이미지에 대해 설명해주세요."},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        }
    ]
)

print(response.output_text)


