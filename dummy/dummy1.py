from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
client = OpenAI()

image_url = "https://upload.wikimedia.org/wikipedia/commons/5/56/Tiger.50.jpg"

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "이 이미지에 대해 설명해주세요."},
                {
                    "type": "input_image",
                    "image_url": image_url
                }
            ]
        }
    ]
)

print(response.output_text.strip())


