import pdfkit
import requests
from bs4 import BeautifulSoup
import os
import re

# Configure pdfkit to use this path
path_to_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'  # Replace with your actual path to wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# Base URLs
root_url = 'https://www.sapiens.com.ua/en/publications'
base_url = 'https://www.sapiens.com.ua/en'

def fetch_publication_links():
    """Fetches all publication links from the main page."""
    response = requests.get(root_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    elements = soup.find_all(class_="single-blog-post")
    publication_links = []
    
    # Loop through each post and gather URLs
    for element in elements:
        h2_tag = element.find('h2', class_='title')
        if h2_tag:
            a_tag = h2_tag.find('a')
            if a_tag and 'href' in a_tag.attrs:
                href_url = a_tag['href']
                each_post_url = f'{base_url}/{href_url}'
                publication_links.append(each_post_url)
    
    return publication_links

def download_pdf(url, pdf_path):
    if url[:3] == '../':
        pdf_download_url = f"https://www.sapiens.com.ua/{url[3:]}"
    else:
        pdf_download_url = url
    
    response = requests.get(pdf_download_url)
    if response.status_code == 200:
        with open(pdf_path, "wb") as pdf_file:
            pdf_file.write(response.content)
        return True
    return False
       
def generate_pdf_from_content(content_html, output_pdf):
    # Define a style for fonts supporting Cyrillic text
    style = """
    <!-- Reset CSS -->
		<link rel="stylesheet" type="text/css" href="https://www.sapiens.com.ua/css/reset.css">

		<!-- Bootstrap CSS -->
		<link rel="stylesheet" type="text/css" href="https://www.sapiens.com.ua/css/bootstrap/bootstrap.css" media="screen">


		<!-- Fonts -->
		<link href='https://fonts.googleapis.com/css?family=Roboto:400,300,300italic,400italic,500italic,500,700,700italic' rel='stylesheet' type='text/css'>
		<link href='https://fonts.googleapis.com/css?family=Raleway:400,500,300,600,700,800,900' rel='stylesheet' type='text/css'>
		<link href='https://fonts.googleapis.com/css?family=Open+Sans:400,400italic,600,600italic,700,700italic,800,300,300italic' rel='stylesheet' type='text/css'>
		<link href='https://fonts.googleapis.com/css?family=PT+Serif:400,400italic,700,700italic' rel='stylesheet' type='text/css'>


		<!-- Font Awesome -->
		<link rel="stylesheet" href="https://www.sapiens.com.ua/fonts/font-awesome/css/font-awesome.min.css">
		

		<!-- Stroke Gap Icon -->
		<link rel="stylesheet" href="https://www.sapiens.com.ua/fonts/stroke-gap/style.css">
		

		<!-- owl-carousel css -->
		<link rel="stylesheet" href="https://www.sapiens.com.ua/css/owl.carousel.css">
		<link rel="stylesheet" href="https://www.sapiens.com.ua/css/owl.theme.css">
		

		<!-- owl-carousel css -->
		<link rel="stylesheet" href="https://www.sapiens.com.ua/css/owl.carousel.css">
		<link rel="stylesheet" href="https://www.sapiens.com.ua/css/owl.theme.css">


		<!-- CSS -->
		<link rel="stylesheet" type="text/css" href="https://www.sapiens.com.ua/css/custom/style.css">
		<link rel="stylesheet" type="text/css" href="https://www.sapiens.com.ua/css/media/media.css">
        <style>
            
            img {
                max-width: 100% !important; 
                margin: auto; 
                display: block;
            }
        </style>
    """
    
    # Add the style to the HTML content
    content_html = style + content_html

    options = {
        'encoding': "UTF-8",
        'enable-local-file-access': True, 
        'margin-top': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'margin-right': '10mm',
    }
    
    pdfkit.from_string(content_html, "output_content/temp_generated.pdf", options=options, configuration=config)
    if os.path.exists(output_pdf):
        os.remove(output_pdf)
    os.rename( "output_content/temp_generated.pdf", output_pdf)

def sanitize_filename(filename):
    # Remove any characters that are not alphanumeric, dashes, or underscores
    return re.sub(r'[^\w\-_.]', '_', filename)
                                         
def process_each_post(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        whole_post_content = soup.find(class_="single-blog-post")
        meta_element = soup.find(class_="post-meta")
        # Extract the title
        title = meta_element.find('h2', class_='title').text
        clean_title = sanitize_filename(title)[:100]
        # Extract the date
        date = meta_element.find('li').text.strip()

        short_name_format = f"{date}_{clean_title}_short.pdf"
        

        # Check if there's a downloadable PDF link
        # Find all <a> tags that contain ".pdf" in their href and have an href attribute
        pdf_links = [
            a_tag for a_tag in whole_post_content.find_all("a", href=True)
            if ".pdf" in a_tag['href'].lower()
        ]
        
        for i, pdf_link in enumerate(pdf_links, start=1):
            if pdf_link:
                full_name_format = f"{date}_{clean_title}_{i}_full.pdf"
                pdf_url = pdf_link['href']
                pdf_path = f"output_reports/{full_name_format}"
                if download_pdf(pdf_url, pdf_path):
                    print(f"    Downloaded PDF directly from {pdf_url}")
                else:
                    print("    Failed to download PDF.")

    except Exception as e:
        print(f" error happned while processing the pdf report: {url} - {e}")
        
        
    try:    
        # Fix relative URLs for images if necessary
        for img in whole_post_content.find_all("img"):
            if img['src'].startswith("../"):
                img['src'] = f"https://www.sapiens.com.ua/{img['src'][3:]}"
            
            if 'height' in img.attrs:
                del img['height']
            

        # Loop through all <p> tags within content and remove youtube iframe
        for p_tag in whole_post_content.find_all("p"):
            if p_tag.find("iframe"):
                p_tag.decompose()

        # Extract and structure HTML content for PDF conversion
        
        content_html = str(whole_post_content)
        
        # Generate PDF from the extracted HTML content
        output_pdf = f"output_content/{short_name_format}"
        generate_pdf_from_content(content_html, output_pdf)
        print(f"    Generated PDF from content and saved as {output_pdf}")
    
    except Exception as e:
        print(f" error happned while saving the content of the post: {url} - {e}")
      
    

def main():
    # Create a directory for storing PDFs if it doesn't exist
    os.makedirs("output_content", exist_ok=True)
    os.makedirs("output_reports", exist_ok=True)

    # Fetch all publication links
    publication_links = fetch_publication_links()
    # Generate PDF for each publication
    for i, url in enumerate(publication_links, start=1):    
        print(f" - {i}th URL processing: {url}")
        try:
            process_each_post(url)
            
        except Exception as e:
            print(f"Failed to save {url} as PDF: {e}")

if __name__ == "__main__":
    main()
