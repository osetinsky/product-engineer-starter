import openai
import json
import os

def generate_json_from_ocr(ocr_text, schema_path):
    # Setup your OpenAI API key here
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Read the JSON schema from the specified path
    with open(schema_path, 'r') as file:
        json_schema = json.load(file)

    # Define the prompt using the unstructured OCR text and the desired JSON output structure
    prompt = f"""Given the unstructured text extracted via OCR from a medical procedure document, convert the section labeled 'INSTRUCTIONS' into a structured JSON format focusing on decision-making steps. Each step should include a unique key, a question, a list of options (with keys and descriptions), and any logic that directs the flow based on option selections. The text involves different types of medical injections and decision paths based on diagnostic criteria. Ensure that each option is marked as 'selected: false' by default, and include logic that clearly outlines the progression from one question to the next based on selected options. The text provided is:

{ocr_text}

Using the JSON schema provided below, format the output:
{json.dumps(json_schema, indent=2)}
"""

    # Call the OpenAI API to generate the response
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=1000,  # You can adjust this based on the expected length of the output
        n=1,
        stop=None,
        temperature=0.5  # A lower temperature value for more deterministic output
    )

    # Print the generated JSON output
    print(response.choices[0].text.strip())

# Example unstructured OCR text
unstructured_ocr_text = """
GlobalQual
INSTRUCTIONS: Choose one of the following options and continue to the appropriate section
10. Diagnostic facet joint injection
20. Therapeutic facet joint injection
...
"""

# Example JSON schema file path
schema_path = 'path_to_your_schema_file.json'

# Generate the JSON
generate_json_from_ocr(unstructured_ocr_text, schema_path)
