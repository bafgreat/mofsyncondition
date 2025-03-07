#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"

import requests
import pandas
from elsapy.elsclient import ElsClient
from elsapy.elsdoc import FullDoc
from crossref.restful import Works
from bs4 import BeautifulSoup
import urllib.request
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from mofsyncondition.io import filetyper


def find_doi_url(doi):
    'A function that searches for the url of any doi'
    works = Works()
    result = works.doi(doi)
    return result['URL']


def url_format(url):
    return re.sub(r'%\d', '/',  url)


def find_documentation_url(doi):
    url = 'https://api.crossref.org/works/' + doi
    response = requests.get(url)
    data = response.json()

    if 'message' in data and 'URL' in data['message']:
        return data['message']['URL']
    else:
        return 'Downloadable URL not found'


def pdf_to_html(pdf_tmp):
    from io import BytesIO
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import HTMLConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, laparams=laparams)
    # Use with statement for file handling
    with open(path, 'rb') as fp:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, check_extractable=True):
            interpreter.process_page(page)
        text = retstr.getvalue()
    device.close()
    retstr.close()
    return


def read_html_from_chrome(url):
    # Set up Chrome options for headless mode
    chrome_options = webdriver.ChromeOptions()
    # Run Chrome in headless mode (without a GUI)
    chrome_options.add_argument('--headless')

    # Initialize the Chrome browser with the specified options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the specified URL in Chrome
        driver.get(url)

        # Wait for a few seconds to ensure the page is loaded (you may need to adjust this)
        driver.implicitly_wait(5)

        # Get the HTML content of the page
        html_content = driver.page_source

        return html_content
    finally:
        # Close the Chrome browser
        driver.quit()


def download_from_springer(doi, outfile, api_key="ae6fdabb9fe31cb397ed9b96fb23d2e1"):
    """
    Download html files from springer publisher using the api key.
    We use try to check whether the doi can be found. If it is found then
    the html page is downloaded.
    Parameters
    ----------
    doi: the doi for the journal
    outfile: the output file
    api_key: your api key, it can be obtained freely by registrying

    Returns
    -------
    Nothing is return. If the doi is found, the html content is written in
    the outfile
    """
    return_value = False
    data_url = f'https://api.springernature.com/metadata/json?q=doi:{doi}&api_key={api_key}'
    response = requests.get(data_url)
    if response.status_code == 200:
        data = response.json()
        try:
            html_url = data['records'][0]['url'][0]['value']
            html_response = requests.get(html_url)
            if type(outfile) == str:
                filetyper.put_contents(outfile, html_response.text)
            elif type(outfile) == list:
                for filename in outfile:
                    filetyper.put_contents(filename, html_response.text)
            return_value = True
        except:
            pass
    return return_value


def download_from_acs(doi, outfile, api_key="0a4e80aee3b130d6d9c342b09dfac8b8780f66c2"):
    """
    Download html files from acs. acs requires using the census module
    Parameters
    ----------
    doi: the doi for the journal
    outfile: the output file
    api_key: your api key, it can be obtained freely by registrying

    Returns
    -------
    Nothing is return. If the doi is found, the html content is written in
    the outfile
    """
    # autheticate = Census(api_key)

    # html_content = autheticate.acs5.get(('NAME', 'B25034_010E'), {'for': 'zip code tabulation area:10.1021/acs.accounts.0c00178'})
    # print(html_content)
    return_value = False
    try:
        url = f"https://pubs.acs.org/doi/{doi}"
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(2)
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        html_content = driver.page_source
        # Check if "Page Not Found" is present in the HTML content
        if "Page Not Found" not in html_content:
            if type(outfile) == str:
                filetyper.put_contents(outfile, html_content)
            elif type(outfile) == list:
                for filename in outfile:
                    filetyper.put_contents(filename, html_content)
            # filetyper.put_contents(outfile, html_content)
            return_value = True
        driver.quit()
    except Exception as e:
        # print(f"An error occurred: {e}")
        pass
    return return_value


def download_from_taylor_and_francis(doi, outfile):
    """
    Download html files from acs. acs requires using the census module
    Parameters
    ----------
    doi: the doi for the journal
    outfile: the output file
    api_key: your api key, it can be obtained freely by registrying

    Returns
    -------
    Nothing is return. If the doi is found, the html content is written in
    the outfile
    """
    # autheticate = Census(api_key)

    # html_content = autheticate.acs5.get(('NAME', 'B25034_010E'), {'for': 'zip code tabulation area:10.1021/acs.accounts.0c00178'})
    # print(html_content)
    return_value = False
    try:
        url = f"https://www.tandfonline.com/doi/full/{doi}"
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(2)
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        html_content = driver.page_source
        # Check if "Page Not Found" is present in the HTML content
        if 'Error 404' not in html_content:
            if type(outfile) == str:
                filetyper.put_contents(outfile, html_content)
            elif type(outfile) == list:
                for filename in outfile:
                    filetyper.put_contents(filename, html_content)
            # filetyper.put_contents(outfile, html_content)
            return_value = True
        driver.quit()
    except Exception as e:
        # print(f"An error occurred: {e}")
        pass
    return return_value


def download_from_elsevier(doi, outfile, api_key="f84870d93502edadf7a412cb7faf5cca"):
    """
    Download html files from acs. acs requires using the census module
    Parameters
    ----------
    doi: the doi for the journal
    outfile: the output file
    api_key: your api key, it can be obtained freely by registrying

    Returns
    -------
    Nothing is return. If the doi is found, the html content is written in
    the outfile
    """
    return_value = False
    url = f'https://api.elsevier.com/content/article/doi/{doi}?apiKey={api_key}&httpAccept=text%2Fxml'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            if type(outfile) == str:
                base_name = outfile[:outfile.rindex('.')]
                text_name = base_name + '.xml'
                filetyper.put_contents(text_name, response.text)
            elif type(outfile) == list:
                for filename in outfile:
                    base_name = filename[:filename.rindex('.')]
                    text_name = base_name + '.xml'
                    filetyper.put_contents(text_name, response.text)
            # filetyper.put_contents(text_name, response.text)
            return_value = True
        except:
            pass
    return return_value


def download_from_wiley(doi, outfile, api_key="7dad2ef6-e69f-4b26-a521-8be8d9e5d872"):
    """
    Download html files from acs. acs requires using the census module
    Parameters
    ----------
    doi: the doi for the journal
    outfile: the output file
    api_key: your api key, it can be obtained freely by registrying

    Returns
    -------
    Nothing is return. If the doi is found, the html content is written in
    the outfile
    """
    return_value = False

    # try:
    #     url = f"https://onlinelibrary.wiley.com/doi/full/{doi}"
    #     driver = webdriver.Chrome()
    #     driver.get(url)
    #     time.sleep(1.5)
    #     body = driver.find_element(By.TAG_NAME, 'body')
    #     body.send_keys(Keys.PAGE_DOWN)
    #     time.sleep(1.5)
    #     html_content = driver.page_source
    #     # Check if "Page Not Found" is present in the HTML content
    #     if 'Error 404' not in html_content:
    #         if type(outfile) == str:
    #             filetyper.put_contents(outfile, html_content)
    #         elif type(outfile) == list:
    #             for filename in outfile:
    #                 filetyper.put_contents(filename, html_content)
    #         # filetyper.put_contents(outfile, html_content)
    #         return_value = True
    #     driver.quit()
    # except Exception as e:
    #     # print(f"An error occurred: {e}")
    #     pass
    headers = {'Accept': 'application/vnd.crossref.unixsd+xml',
               'Wiley-TDM-Client-Token': api_key
               }
    # opener = urllib.request.build_opener()
    # opener.addheaders = [
    #     ('Accept', 'application/vnd.crossref.unixsd+xml'), ('Wiley-TDM-Client-Token', api_key)]
    # doc_request = opener.open(find_doi_url(doi))
    # if doc_request.status == 200:
    #     print (doc_request.headers)

    #     head = doc_request.headers['link']
    #     # pattern = r'<(https://onlinelibrary.wiley.com/doi/full-xml/[^>]*)>'
    #     pattern = r'<(https://api.wiley.com/onlinelibrary/tdm[^>]*)>'
    #     url_path = re.search(pattern, head).group(1)
    #     response1 = requests.get(url=url_path, headers=headers, allow_redirects=True)
    #     print (response1)

    # pattern = r'(https://api.wiley.com/onlinelibrary/tdm[^>]*)'
    # pattern = r'(https://onlinelibrary.wiley.com/doi/10*?)'
    # pattern = r'(https://onlinelibrary.wiley.com/doi/pdf/*?)'
    # response = requests.get(find_doi_url(doi), headers=headers)
    # if response.status_code == 200:
    #     soup = BeautifulSoup(response.text, 'xml')
    #     head = [value.text for value in soup(['resource'])]
    #     url_path = [url for url in head if re.match(pattern, url)][0]
    #     if len(url_path) > 0:
    #         url_path = url_format(url_path)
    #         print (url_path)
    #         header = {'CR-Clickthrough-Client-Token': api_key}
    #         response1 = requests.get(url=url_path, headers=header, allow_redirects=True)
    #         print (response1)

    #     # head = response.headers['link']
    #     pattern = r'(https://api.wiley.com/onlinelibrary/tdm[^>]*)'
    #     # pattern = r'(https://onlinelibrary.wiley.com/doi/full[^>]*)'
    #     # pattern = r'(https://onlinelibrary.wiley.com/doi/10*?)'

    #     header2 = {
    #         'Wiley-TDM-Client-Token': api_key
    #     }
    #     url_path = [url for url in head if re.match(pattern, url)][0]
    #     print (url_path )
    #     if len(url_path) > 0:
    #         response1 = requests.get(url=url_path, headers=headers, allow_redirects=True)
    #         print (response1)
    #         try:
    #             base_name = outfile.split('.h')[0]
    #             text_name = base_name + '.pdf'
    #             with open(text_name, "wb") as pdf_file:
    #                 pdf_file.write(response.content)
    #             return_value = True
    #         except:
    #             pass
    return return_value


def download_from_rsc(doi, outfile):
    """
    Download html files from rsc.
    Parameters
    ----------
    doi: the doi for the journal
    outfile: the output file

    Returns
    -------
    Nothing is return. If the doi is found, the html content is written in
    the outfile
    """
    return_value = False
    find_url = requests.get(find_doi_url(doi),  headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'})
    if find_url.status_code == 200:
        try:
            url_path = re.findall(
                r'https://pubs.rsc.org/en/content/articlehtml/.*?"',
                find_url.text)[0][:-1]
        except:
            url_path = []
            pass
        if len(url_path) > 0:
            try:
                html_content = read_html_from_chrome(url_path)
                if type(outfile) == str:
                    filetyper.put_contents(outfile, html_content)
                elif type(outfile) == list:
                    for filename in outfile:
                        filetyper.put_contents(filename, html_content)
                # filetyper.put_contents(outfile, html_content)
                return_value = True
            except:
                pass
    return return_value


def overall_download(doi, outfile):
    url = find_documentation_url(doi)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    return_value = False
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            with open(outfile, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            return_value = False
    except:
        pass


# # download_from_elsevier('10.1016/j.poly.2016.09.043', 'test.hml')
# overall_download('10.1016/j.poly.2016.09.043', 'test6.html')

# download_from_acs('10.1021/cg0342258', 'test8.html')
# download_from_taylor_and_francis(, outfile)

# download_from_wiley(
#     '10.1002/1521-3773(20010903)40:17<3211::AID-ANIE3211>3.0.CO;2-X', 'willey.html')
