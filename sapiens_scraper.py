import pdfkit
import requests
from bs4 import BeautifulSoup
import base64
import re

# URL of the webpage you want to capture
root_url = 'https://www.sapiens.com.ua/en/publications'


# Configure pdfkit to use this path
path_to_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'  # Replace with actual path
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# Define PDF options for better formatting
pdf_options = {
    'enable-local-file-access': None,  # Allow local resources if needed
    'page-size': 'A4',
    'encoding': 'UTF-8',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in'
}


# Fetch the main page
response = requests.get(root_url)
soup = BeautifulSoup(response.text, 'html.parser')

elements = soup.find_all(class_="single-blog-post")

# Print each element
for element in elements:
    print(element)


# Generate PDF directly from the URL
# url = 'https://www.sapiens.com.ua/en/publication-single-page?id=299'
# pdfkit.from_url(url, 'output.pdf', options=pdf_options, configuration=config)
