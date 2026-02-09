#01_gpt_api.py
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("key.env")
client = OpenAI()

prompt = input("Enter your prompt: ")

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "developer",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("Response: ")
print(response.output_text)