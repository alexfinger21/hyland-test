import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
image = Image.open("p3.png")
text = pytesseract.image_to_string(image)

print("Extracted Text:")
print(text)