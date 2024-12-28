from PIL import Image, ImageDraw, ImageFont

# 이미지 생성
width, height = 800, 600
image = Image.new('RGB', (width, height), color=(255, 255, 255))

# 텍스트 추가
draw = ImageDraw.Draw(image)
text = "Placeholder Image"
font = ImageFont.load_default()
text_width, text_height = draw.textsize(text, font=font)
draw.text(((width - text_width) / 2, (height - text_height) / 2), text, fill="black", font=font)

# 저장
image.save("placeholder_white.png")