import fitz  # Import PyMuPDF
import re
import json
import os

class GuidelinesParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_instructions_text(self):
        document = fitz.open(self.pdf_path)
        instructions = []
        capture = False
        
        for page_num, page in enumerate(document):
            text = page.get_text()
            print(f"Page {page_num + 1} text:\n{text}\n")  # Debug print
            
            if "INSTRUCTIONS:" in text:
                capture = True  # Start capturing text from here
                print(f"--- Start capture on page {page_num + 1} ---")  # Debug print
            if "Reference" in text and capture:
                capture = False  # Stop capturing text at "Reference"
                print(f"--- End capture on page {page_num + 1} ---")  # Debug print
            
            if capture:
                instructions.append(text)
                
            if not capture and instructions:  # If we have captured and just hit "Reference"
                break  # We can stop looking through the rest of the pages
        
        instructions_text = '\n'.join(instructions)
        print(f"Captured Instructions text:\n{instructions_text}")  # Debug print
        return instructions_text

    def parse_questions_and_options(self, captured_text):
        questions = re.findall(r'(?:(\d+)\.\s(.*?)\n((?:\s*[A-Z]\)\s.*?\n(?:\s*•.*?\n)*)+))+', captured_text, re.DOTALL)
        steps = []

        for step_number, step_data in enumerate(questions):
            step_key, step_text, options_text = step_data
            
            options = re.findall(r'([A-Z])\)\s(.*?)\n((?:\s*•.*?\n)*)', options_text)
            options_list = []
            logic_list = []
            
            for option_key, option_text, logic_text in options:
                options_list.append({"key": option_key, "text": option_text.strip(), "selected": False})
                logic_list.append({"text": logic_text.strip(), "selected": False})
            
            step = {
                "key": str(step_number),
                "question": step_text.strip(),
                "options": options_list,
                "logic": logic_list
            }
            steps.append(step)

        return steps

    def to_json(self):
        text = self.extract_instructions_text()
        steps = self.parse_questions_and_options(text)
        return json.dumps({"steps": steps}, indent=4)

    def write_json(self, output_dir, filename='parsed_guidelines.json'):
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
        
        json_data = self.to_json()
        
        with open(file_path, 'w') as f:
            f.write(json_data)
        print(f"JSON file written to {file_path}")