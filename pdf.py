import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

marker_key = os.getenv("MARKER_API_KEY")
url = "https://www.datalab.to/api/v1/marker"

headers = {"X-Api-Key": f"{marker_key}"}


def convert_pdf_to_markdown(filename, pdf_content):

    form_data = {
       'file': (filename, pdf_content, 'application/pdf'),
       "langs": (None, "en"),
       "force_ocr": (None, False),
       "paginate": (None, False),
       "extract_images": (None, False)
    }

    response = requests.post(url, files=form_data, headers=headers)

    data = response.json()

    max_polls = 300
    check_url = data["request_check_url"]

    for i in range(max_polls):
        time.sleep(2)
        # Don't forget to send the auth headers
        response = requests.get(check_url, headers=headers)
        data = response.json()

        if data["status"] == "complete":
            break

    json_response = response.json()

    markdown = json_response['markdown']

    return markdown

    
if __name__ == "__main__":
    with open("trial.pdf", "rb") as f:
        pdf_content = f.read()
        markdown = convert_pdf_to_markdown(pdf_content)
        print(markdown)
