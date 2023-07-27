#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import inscriptis
from bs4 import BeautifulSoup


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


def html_2_text2(html_file):
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

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_object, 'html.parser')

    # Remove unwanted elements from the HTML document

    for element in soup(['figure', 'figcaption', 'meta', 'author', 'affiliation', 'abstract',
                         'cite', 'table', 'references', 'acronym']):
        element.extract()

    # Extract the text from the modified HTML document
    text = inscriptis.get_text(str(soup))
    return text
