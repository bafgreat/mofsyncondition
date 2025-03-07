#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import inscriptis
import PyPDF2
import fitz
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from pdfdataextractor import Reader


def find_xml_namespace(markup_file, name_pattern):
    """
    a simple function to find xml name space
    """
    namespace = {}
    all_name_list = []
    if type(name_pattern) == str:
        all_name_list.append(name_pattern)
    elif type(name_pattern) == list:
        all_name_list.extend(name_pattern)

    with open(markup_file, 'r', encoding="utf-8") as file_object:
        file_object = file_object.read()
        for n_pattern in all_name_list:
            pattern = r'xmlns:'+n_pattern+r'[^\s]+'
            match = re.search(pattern, file_object)
            if match:
                found_name_space = re.search(
                    r'"(.*?)"',  match.group()).group(1)
                namespace[n_pattern] = found_name_space
    return namespace


def html_2_text(html_file):
    """
    A function that uses inscriptis to convert
    html files to plain text.
    Parameters
    ----------
    html_file: html file name or path: str.type

    Returns
    -------
    plain text : str.type
    """
    with open(html_file, 'r', encoding="utf-8") as file_object:
        html_object = file_object.read()

    return inscriptis.get_text(html_object)


def html_2_text2(markup_file):
    """
    A function that uses inscriptis to convert
    html files to plain text.
    Parameters
    ----------
    html_file: html file name or path: str.type

    Returns
    -------
    plain text : str.type
    """
<<<<<<< HEAD
    with open(html_file, 'r', encoding="utf-8") as file_object:
        html_object = file_object.read()
    # headings = []
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_object, 'html.parser')
    # for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5']):
    #     headings.append(heading.text.strip())

    # Remove unwanted elements from the HTML document

    for element in soup(['figure', 'figcaption', 'meta', 'author', 'affiliation', 'abstract',
                         'cite', 'table', 'references', 'acronym']):
        element.extract()

    # Extract the text from the modified HTML document
    text = inscriptis.get_text(str(soup))
    return text

=======
    text = []
    ext = markup_file[markup_file.rindex('.')+1:]
    if ext == 'html':
        with open(markup_file, 'r', encoding="utf-8") as file_object:
            file_object = file_object.read()
        soup = BeautifulSoup(file_object, 'html.parser')
        extract = soup(['title', 'h2', 'h1', 'h3', 'h4', 'p'])
        for element in extract:
            text.append(inscriptis.get_text(str(element)).strip())
    elif ext == 'xml':
        with open(markup_file, 'r', encoding="utf-8") as file_object:
            file_object = file_object.read()
        soup = BeautifulSoup(file_object, 'xml')
        extract = soup(['para', 'section-title'])
        for element in extract:
            text.append(inscriptis.get_text(str(element)))
    elif ext == 'pdf':
        text = pdfataextractor(markup_file)
    return text


def convert_pdf_to_text(pdf_path):
    """
    A function that uses PyPDF2 to convert
    pdf files to plain text.
    Parameters
    ----------
    pdf_path: pdf file name or path: str.type

    Returns
    -------
    """
    text_content = ""

    try:
        with open(pdf_path, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # Iterate through each page and extract text
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                print(page.extract_text())
                text_content += page.extract_text()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return text_content


def convert_pdf_to_plaintext(pdf_path):
    """
    A function that uses PyPDF2 to convert
    pdf files to plain text.
    Parameters
    ----------
    pdf_path: pdf file name or path: str.type

    Returns
    -------
    """
    text_content = ""
    doc = fitz.open(pdf_path)
    paragraph_spacing = "\n\n"
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text("text")
        # Split paragraphs and add spacing
        paragraphs = text.split("\n")
        formatted_text = paragraph_spacing.join(paragraphs)
        text_content += text
    return text_content


def pdfataextractor(pdf_path):
    all_text = []
    file = Reader()
    pdf = file.read_file(pdf_path)
    plain_text = pdf.plaintext()
    for text in plain_text.split('\n'):
        all_text.append(inscriptis.get_text(text))
    return all_text
>>>>>>> 9253cec (fixed)
