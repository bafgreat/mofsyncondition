#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import inscriptis
import fitz
import re
from bs4 import BeautifulSoup
from mofsyncondition.doc import doc_parser


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


def file_2_list_of_paragraphs(markup_file):
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

    # with open(html_file, 'r', encoding="utf-8") as file_object:
    #     html_object = file_object.read()
    # # headings = []
    # # Parse the HTML content with BeautifulSoup
    # soup = BeautifulSoup(html_object, 'html.parser')
    # # for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5']):
    # #     headings.append(heading.text.strip())

    # # Remove unwanted elements from the HTML document

    # for element in soup(['figure', 'figcaption', 'meta', 'author', 'affiliation', 'abstract',
    #                      'cite', 'table', 'references', 'acronym']):
    #     element.extract()

    # # Extract the text from the modified HTML document
    # text = inscriptis.get_text(str(soup))
    # return text

    text = []
    ext = markup_file[markup_file.rindex('.')+1:]
    if ext == 'html':
        plain_text = html_2_text(markup_file)
        text = doc_parser.text_2_paragraphs(plain_text)

        # with open(markup_file, 'r', encoding="utf-8") as file_object:
        #     file_object = file_object.read()
        # soup = BeautifulSoup(file_object, 'html.parser')
        # extract = soup(['title', 'h2', 'h1', 'h3', 'h4', 'p'])
        # for element in extract:
        #     text.append(inscriptis.get_text(str(element)).strip())

    elif ext == 'xml':
        with open(markup_file, 'r', encoding="utf-8") as file_object:
            file_object = file_object.read()
        soup = BeautifulSoup(file_object, 'xml')
        extract = soup(['para', 'section-title'])
        for element in extract:
            text.append(inscriptis.get_text(str(element)))
    elif ext == 'pdf':
        text = text = extract_pdf_paragraphs(markup_file)
    return text


def _clean_line(s: str) -> str:
    s = s.replace("\u00ad", "")  # soft hyphen
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _dehyphenate(prev: str, nxt: str) -> str:
    """
    If previous line ends with hyphen and next starts with a letter,
    join them: "examp-" + "le" -> "example"
    """
    if prev.endswith("-") and nxt and nxt[0].isalpha():
        return prev[:-1] + nxt
    return prev + " " + nxt


def extract_pdf_paragraphs(
    pdf_path: str,
    *,
    min_chars: int = 30,
    header_footer_margin_ratio: float = 0.08,
    para_gap_multiplier: float = 1.25
    ) -> list[str]:
    """
    Extract paragraphs from a PDF using layout blocks + heuristics.

    Parameters
    ----------
    min_chars:
        drop very short blocks (often page numbers, running headers)
    header_footer_margin_ratio:
        treat top/bottom X% of page as header/footer region and ignore text there
    para_gap_multiplier:
        bigger -> fewer paragraph breaks; smaller -> more breaks

    Returns
    -------
    paragraphs : list[str]
    """
    doc = fitz.open(pdf_path)
    all_paras: list[str] = []

    for page in doc:
        page_h = page.rect.height
        header_y = page_h * header_footer_margin_ratio
        footer_y = page_h * (1 - header_footer_margin_ratio)

        blocks = page.get_text("blocks")
        text_blocks = []
        for (x0, y0, x1, y1, text, *_rest) in blocks:
            if y1 < header_y or y0 > footer_y:
                continue
            text = text.strip()
            if len(text) < min_chars:
                continue
            text_blocks.append((x0, y0, x1, y1, text))
        text_blocks.sort(key=lambda b: (round(b[1], 1), round(b[0], 1)))

        for (x0, y0, x1, y1, block_text) in text_blocks:
            raw_lines = [ln.strip() for ln in block_text.splitlines()]
            lines = [_clean_line(ln) for ln in raw_lines if _clean_line(ln)]

            if not lines:
                continue

            # est_line_h = max((y1 - y0) / max(len(lines), 1), 1.0)
            # para_gap = est_line_h * para_gap_multiplier

            paras_in_block = []
            buf = ""

            for ln in lines:
                if not ln:
                    if buf:
                        paras_in_block.append(buf.strip())
                        buf = ""
                    continue

                if not buf:
                    buf = ln
                else:
                    if buf.endswith("-"):
                        buf = _dehyphenate(buf, ln)
                    else:
                        buf = buf + " " + ln

            if buf:
                paras_in_block.append(buf.strip())

            paras_in_block = [re.sub(r"\s+", " ", p).strip() for p in paras_in_block]
            all_paras.extend([p for p in paras_in_block if p])

    cleaned = []
    seen = set()
    for p in all_paras:
        key = p.strip()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(key)

    return cleaned
