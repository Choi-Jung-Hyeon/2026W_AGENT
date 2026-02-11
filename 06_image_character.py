# 06_image_character.py
from openai import OpenAI
from dotenv import load_dotenv
import base64
import requests

load_dotenv()
client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

def analyze_photo(image_path):
    base64_image = encode_image(image_path)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "이 사진의 특징을 설명해주세요."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ]
    )
    return response.choices[0].message.content

def create_character(description, style):
    prompt = f"{description}, {style}"
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    
    image_data = requests.get(response.data[0].url).content
    return image_data

# 메인
print("="*60)
print("사진 → 캐릭터 변환기 (프리셋)")
print("="*60)

photo_path = input("\n사진 경로: ").strip()

print("\n사진 분석 중...")
description = analyze_photo(photo_path)
print("✓ 분석 완료")

# 스타일 프리셋
styles = {
    "1": ("치비 캐릭터 스타일, 큰 머리, 작은 몸, 귀여운", "chibi.png"),
    "2": ("애니메이션 캐릭터 스타일, 일본 애니메이션 스타일", "anime.png"),
    "3": ("3D 게임 캐릭터, 언리얼 엔진 스타일, 고품질 렌더링", "3d_game.png"),
    "4": ("픽셀아트 캐릭터, 16비트 스타일, 레트로 게임", "pixel_art.png"),
    "5": ("판타지 RPG 캐릭터, 던전 앤 드래곤 스타일", "fantasy_rpg.png"),
    "6": ("귀여운 스티커 스타일, 카카오톡 캐릭터 스타일", "sticker.png"),
}

while True:
    print("\n" + "="*60)
    print("스타일 선택:")
    print("="*60)
    print("1. 치비 캐릭터")
    print("2. 애니메이션")
    print("3. 3D 게임")
    print("4. 픽셀아트")
    print("5. 판타지 RPG")
    print("6. 스티커")
    print("7. 직접 입력")
    print("q. 종료")
    
    choice = input("\n선택: ").strip()
    
    if choice == 'q':
        break
    
    if choice == '7':
        custom_style = input("\n원하는 스타일 입력: ").strip()
        filename = input("파일명 (예: my_character.png): ").strip()
        
        if not filename.endswith('.png'):
            filename += '.png'
        
        print("\n생성 중...")
        image_data = create_character(description, custom_style)
        
    elif choice in styles:
        style_desc, filename = styles[choice]
        
        print(f"\n생성 중...")
        image_data = create_character(description, style_desc)
    else:
        print("잘못된 선택입니다.")
        continue
    
    with open(filename, "wb") as f:
        f.write(image_data)
    
    print(f"✓ {filename} 저장 완료!")

print("\n종료!")