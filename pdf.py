import PyPDF2
import re


import http.client
import mimetypes
from codecs import encode


def XXXX(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        markdown_text = ""

        # Iterate through all pages
        for page in reader.pages:
            text = page.extract_text()

            # Process the text to create markdown
            # This is a basic conversion and may need adjustment based on your PDF structure

            # Convert headers (assuming they are in larger font or bold)
            # text = re.sub(r'^(.+)$', r'# \1', text, flags=re.MULTILINE)

            # Convert bullet points
            text = re.sub(r'^\s*•\s*(.+)$', r'* \1', text, flags=re.MULTILINE)

            # Add two spaces at the end of each line for markdown line breaks
            text = re.sub(r'$', '  ', text, flags=re.MULTILINE)

            markdown_text += text + "\n\n"

    return markdown_text


def convert_pdf_to_text(file_path):
    conn = http.client.HTTPSConnection("pdf-to-text-converter.p.rapidapi.com")
    api_key = "58e43ba440msh4f5cd6acbf0dffep13414ajsnf6383c0f71ef"
    # Read the PDF file
    with open(file_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()

    # Prepare the form data
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode(
        'Content-Disposition: form-data; name=file; filename={0}'.format(file_path)))

    fileType = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
    dataList.append(encode('Content-Type: {}'.format(fileType)))
    dataList.append(encode(''))
    dataList.append(pdf_content)
    dataList.append(encode('--' + boundary + '--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)

    # Prepare headers
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "pdf-to-text-converter.p.rapidapi.com",
        'Content-Type': 'multipart/form-data; boundary={}'.format(boundary)
    }

    # Make the API request
    conn.request("POST", "/api/pdf-to-text/convert", body, headers)
    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")


if __name__ == "__main__":

    pdf_file_path = "trial.pdf"

    try:
        result = convert_pdf_to_text(pdf_file_path, api_key)
        print("Converted Text:")
        print(result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
