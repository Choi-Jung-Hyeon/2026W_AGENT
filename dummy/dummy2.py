from openai import OpenAI
from dotenv import load_dotenv
import base64
import os

load_dotenv()
client = OpenAI()

image_path = "배경사진.jpg"

ext = os.path.splitext(image_path)[1].lower()
mime_types = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}
mime_type = mime_types.get(ext, "image/jpeg")

with open(image_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "이 이미지에 대해 설명해주세요."},
                {
                    "type": "input_image",
                    "image_url": f"data:{mime_type};base64,{b64}"
                }
            ]
        }
    ]
)

print(response.output_text)
