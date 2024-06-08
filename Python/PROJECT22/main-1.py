from PIL import Image
import pytesseract

image_path = r"22. 이미지에서 글자 추출하기\한글이미지.png"

pytesseract.pytesseract.tesseract_cmd = r'<path>'
text = pytesseract.image_to_string(Image.open(image_path), lang="kor")

print(text)