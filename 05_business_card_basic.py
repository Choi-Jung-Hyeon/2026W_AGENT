# 05_business_card_basic.py
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()
client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# 명함 이미지 경로
card_image = "business_card.jpg"
card_base64 = encode_image(card_image)

# 🔹 입력 메시지(프롬프트) 구성 – 호출 밖
input_data = [
    {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": "이 명함에서 이름, 회사, 직책, 전화번호, 이메일을 추출해주세요."
            },
            {
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{card_base64}"
            }
        ]
    }
]

# 🔹 API 호출
response = client.responses.create(
    model="gpt-4.1-mini",
    input=input_data
)

print("명함 정보:")
print(response.output_text)
