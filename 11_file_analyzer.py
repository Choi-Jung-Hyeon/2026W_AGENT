# 11_file_analyzer.py
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv("key.env")
client = OpenAI()

def analyze_local_file(file_path: str, question: str) -> str:
    """
    로컬 파일을 업로드한 뒤,
    질문을 기반으로 내용을 분석한다.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

    # 1️⃣ 로컬 파일 업로드
    uploaded_file = client.files.create(
        file=open(file_path, "rb"),
        purpose="assistants"
    )

    # 2️⃣ 업로드한 파일을 기반으로 분석
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": question
                    },
                    {
                        "type": "input_file",
                        "file_id": uploaded_file.id
                    }
                ]
            }
        ]
    )

    return response.output_text


# -----------------------------
# 실행부
# -----------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("📄 로컬 파일 분석기")
    print("=" * 60)

    file_path = input("분석할 파일 경로 (예: 2024ltr.pdf): ").strip()
    question = input("파일에 대해 물어볼 질문: ").strip()

    try:
        print("\n⏳ 파일 분석 중...\n")
        result = analyze_local_file(file_path, question)

        print("✅ 분석 결과:")
        print("-" * 60)
        print(result)
        print("-" * 60)

    except Exception as e:
        print("\n❌ 오류 발생:")
        print(e)
