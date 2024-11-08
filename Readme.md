# Scraper for info sapiens.

Development of a Python-based automated system for collecting and organizing publications from the specified website's publication section, including both web page content and associated PDF reports.
Website: https://www.sapiens.com.ua/en/publications

## installation

 - Need to install python3.10 or over and pip
 - Must install ```wkhtmltopdf``` on your windows to convert the PDF files. and add the file path into the system variables. 
     ```eg: C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe```
    And replace with your actual path to wkhtmltopdf in the code, at line 8

 - make the virtual env

 ```
 python -m venv myvenv
 ```

 - Activate the virtual 
 In the command prompt or PowerShell, run the following command:
 ```
 myenv\Scripts\activate
 ```

 - Install Packages from requirements.
 ```
pip install -r requirements.txt
 ```

 - run the scraper
 ```
python sapiens_scraper.py
 ```