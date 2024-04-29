import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

class OCRUtility:
    def __init__(self):
        pass  # Tesseract path is already set by the package in Linux

    def process_file(self, file_path, output_file):
        text = ''
        if file_path.lower().endswith('.pdf'):
            text = self.process_pdf(file_path)
        elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            text = self.process_image(file_path)
        else:
            raise ValueError("Unsupported file format. Please use PDF or PNG.")
        self.save_text_to_file(text, output_file)

    def process_pdf(self, pdf_path):
        images = convert_from_path(pdf_path)
        text_results = []
        for i, image in enumerate(images):
            text = self.extract_text(image)
            text_results.append(f'Page {i+1}:\n{text}\n')
        return "\n".join(text_results)

    def process_image(self, image_path):
        image = Image.open(image_path)
        return self.extract_text(image)

    def extract_text(self, image):
        text = pytesseract.image_to_string(image)
        return text

    def save_text_to_file(self, text, output_file):
        with open(output_file, 'w') as file:
            file.write(text)