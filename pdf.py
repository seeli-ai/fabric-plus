import requests
import os

def convert_pdf_to_markdown(pdf_content):
    url = "http://marker:8000/convert"
    files = {'pdf_file': ("file.pdf", pdf_content, 'application/pdf')}

    response = requests.post(url, files=files)

    json_response = response.json()[0]

    markdown = json_response['markdown']

    return markdown

    
if __name__ == "__main__":
    with open("trial.pdf", "rb") as f:
        pdf_content = f.read()
        markdown = convert_pdf_to_markdown(pdf_content)
        print(markdown)
