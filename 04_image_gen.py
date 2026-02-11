# 04_image_gen.py
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()
client = OpenAI()

# 이미지 생성
response = client.images.generate(
    model="gpt-image-1.5",
    prompt="귀여운 고양이가 커피를 마시는 모습, 따뜻한 카페",
    size="1024x1024",
    n=1
)

# base64 이미지 디코딩 후 저장
image_base64 = response.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

with open("cat_coffee.png", "wb") as f:
    f.write(image_bytes)

print("이미지 저장 완료: cat_coffee.png")
