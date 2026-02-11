# 01_1_pdf_extract.py
import pdfplumber

# PDF 경로
pdf_path = "자율주행로봇의 최소경로계획을 위한 그래프 탐색 방법.pdf"

full_text = ""

# PDF 열기
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:  # 페이지에 텍스트가 있는 경우만
            full_text += text + "\n"

print(f"추출 완료: {len(full_text)} 문자")
print(full_text[:500])  # 처음 500자 확인
