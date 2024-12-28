
from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder(width=800, height=600, text="Placeholder", bg_color=(240, 240, 240), text_color=(80, 80, 80)):
    # 이미지 생성
    image = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)
    
    # 테두리 그리기 (20px)
    border_color = (220, 220, 220)
    draw.rectangle([(0, 0), (width-1, height-1)], outline=border_color, width=20)
    
    # 기본 폰트 사용
    font = ImageFont.load_default()
    
    # 텍스트 크기 계산
    text_width, text_height = draw.textsize(text, font=font)
    
    # 텍스트 위치 계산 (중앙)
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    # 텍스트 그리기
    draw.text((text_x, text_y), text, fill=text_color, font=font)
    
    # 크기 표시 추가
    size_text = f"{width}x{height}"
    size_width, size_height = draw.textsize(size_text, font=font)
    draw.text(
        (width - size_width - 30, height - size_height - 30),
        size_text,
        fill=text_color,
        font=font
    )
    
    # 저장
    image.save("placeholder.png")
    print(f"생성된 이미지: placeholder.png ({width}x{height})")

if __name__ == "__main__":
    create_placeholder(800, 600, "Placeholder Image")
