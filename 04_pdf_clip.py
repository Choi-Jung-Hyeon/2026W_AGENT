# 04_pdf_clip.py
import pymupdf
import os

pdf_file_path = "pdf_ai/생성형AI트렌드및활용사례분석.pdf"
doc = pymupdf.open(pdf_file_path)

header_height = 80
footer_height = 80
full_text = ''

for page in doc:
    rect = page.rect
    text = page.get_text(clip=(0, header_height, rect.width, rect.height - footer_height))#왼쪽 위,오른쪽, 아래
    full_text += text + '\n' + '-'*50 + '\n'

doc.close()

# 파일명 추출
pdf_file_name = os.path.splitext(os.path.basename(pdf_file_path))[0]

# 현재 폴더에 저장
txt_file_path = f'pdf_ai/{pdf_file_name}_clean.txt'


with open(txt_file_path, 'w', encoding='utf-8') as f:
    f.write(full_text)

print(f"저장 완료: {txt_file_path}")


