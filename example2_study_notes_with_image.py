# example2_study_notes_with_image.py
"""
[기능] 학습 노트 관리 (이미지 지원)
- 이미지에서 문제 읽기
- 과목별 노트 저장
- 키워드 검색
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import json
import os
import base64

load_dotenv("key.env")

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
vision_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # 이미지용

@tool
def read_image_problem(image_path: str) -> str:
    """이미지 파일에서 문제를 읽어냅니다"""
    try:
        # 이미지를 base64로 인코딩
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        # 이미지 분석
        message = HumanMessage(
            content=[
                {"type": "text", "text": "이 이미지에 있는 문제나 내용을 한글로 정확하게 읽어주세요."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                }
            ]
        )

        response = vision_llm.invoke([message])
        return response.content

    except Exception as e:
        return f"이미지 읽기 실패: {str(e)}"

@tool
def save_note(subject: str, content: str) -> str:
    """과목별로 학습 노트를 저장합니다"""
    notes = {}
    if os.path.exists("notes.json"):
        with open("notes.json", "r", encoding="utf-8") as f:
            notes = json.load(f)

    if subject not in notes:
        notes[subject] = []
    notes[subject].append(content)

    with open("notes.json", "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

    return f"{subject} 노트 저장 완료 ({len(notes[subject])}번째)"

@tool
def search_notes(keyword: str) -> str:
    """키워드로 노트를 검색합니다"""
    if not os.path.exists("notes.json"):
        return "노트 없음"

    with open("notes.json", "r", encoding="utf-8") as f:
        notes = json.load(f)

    results = []
    for subject, contents in notes.items():
        for i, content in enumerate(contents, 1):
            if keyword in content:
                results.append(f"[{subject}#{i}] {content[:100]}...")

    return "\n".join(results) if results else "검색 결과 없음"

@tool
def list_notes() -> str:
    """모든 노트 목록을 보여줍니다"""
    if not os.path.exists("notes.json"):
        return "노트 없음"

    with open("notes.json", "r", encoding="utf-8") as f:
        notes = json.load(f)

    result = []
    for subject, contents in notes.items():
        result.append(f"\n[{subject}] ({len(contents)}개)")
        for i, c in enumerate(contents, 1):
            result.append(f"  {i}. {c[:50]}...")

    return "\n".join(result) if result else "노트 없음"

tools = [read_image_problem, save_note, search_notes, list_notes]
llm_with_tools = llm.bind_tools(tools)

print("="*60)
print("학습 노트 관리 (이미지 지원)")
print("="*60)
print("\n사용법:")
print("  - '수학 이미지 problem.jpg 읽어서 저장해줘'")
print("  - '영어 노트에 저장: 현재완료 용법'")
print("  - '미적분 검색해줘'")
print("  - '노트 목록 보여줘'")
print("\n종료: quit, exit, q, 종료, 끝")
print("="*60)

while True:
    user_input = input("\n> ").strip()

    if user_input.lower() in ['quit', 'exit', 'q', '종료', '끝']:
        print("종료합니다")
        break

    if not user_input:
        continue

    messages = [{"role": "user", "content": user_input}]
    response = llm_with_tools.invoke(messages)

    if response.tool_calls:
        for tc in response.tool_calls:
            for tool in tools:
                if tool.name == tc["name"]:
                    result = tool.invoke(tc["args"])
                    print(f"\n{result}")
                    break
    else:
        print(f"\n{response.content}")
