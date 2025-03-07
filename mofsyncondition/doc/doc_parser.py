#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import re
import chemdataextractor as cde
import spacy
from mofsyncondition.doc import convert_html_to_text
from mofsyncondition.conditions.organic_reagents_from_iupac_name import find_parentheses, find_square_brackets


def unclosed_brackets(text):
    """
    A simple algorithm to remove unbalanced brackets
    Algorithm
    1) Search for all balanced brackets
    2) Seacrh for all bra and kets
    3) loop through the list of bra and kets and find indices that are not present in the 
    list of all balanced brackets
    4) Remove all characters at the identified indices
    """
    new_list_1 = list(find_parentheses(text).keys()) + \
        list(find_parentheses(text).values())
    new_list_2 = list(find_square_brackets(text).keys()) + \
        list(find_square_brackets(text).values())
    new_list_3 = list(find_square_brackets(text).keys()) + \
        list(find_square_brackets(text).values())
    all_brackets = new_list_1 + new_list_2 + new_list_3
    brackets = [i for i in range(len(text)) if text[i] == '(' or text[i] == ')' or text[i]
                == '{' or text[i] == '}' or text[i] == '[' or text[i] == '}']
    unbalanced_bracket = [i for i in brackets if not i in all_brackets]

    return unbalanced_bracket


def tokenize_doc(plain_text):
    """
    A function that converts a document into document into 
    token using spacy
     Parameters
    ----------
    plain_text: str.type 

    Returns
    -------
    token : list of words, ponctuationlist.type
    """
    nlp = spacy.load("en_core_web_sm")
    spacy_doc = nlp(plain_text)
    tokens = [token.text for token in spacy_doc]
    return tokens, spacy_doc


def are_words_in_same_sentence(spacy_doc, word1, word2):
    """
    A function that checks whether two words in a document are 
    found in the same sentence.
     Parameters
    ----------
    spacy_doc: npl(text)
    word1 : string text 
    word2 : string text  

    Returns
    -------
    Bolean 
    """
    for token in spacy_doc:
        if token.text == word1:
            if token.sent.text.find(word2) != -1:
                return True
        elif token.text == word2:
            if token.sent.text.find(word1) != -1:
                return True
    return False


def text_2_paragraphs(plain_text):
    """
    A function that splits a text file into 
    paragrphs and return a list of paragrphs. 
    Parameters
    ----------
    plain_text  

    Returns
    -------
    list of paragraphs
    """
    # regular expression pattern to match paragraph boundaries
    # pattern = r"(?<=\n\n|^)(?:\t| {4}).*?(?=\n\n|$)"
    paragraphs = []
    # pattern = r"(\n\n|\n|^)(?:\t|\s{2,}).*?(?=\n\n|\n|$)"
    pattern = r"(\n{2,}|\n)(\t|\s{2,}).*?(?=\n{2,}|\n|$)"
    paragraph_match_patern = re.finditer(pattern, plain_text, flags=re.DOTALL)
    for match in paragraph_match_patern:
        text_span = match.span()
        paragraph = plain_text[text_span[0]:text_span[1]]
        paragraphs.append(paragraph)
    return paragraphs


def paragraph_containing_word(paragraphs, specific_word):
    """
    A function to extract paragraph containing 
    a specific text
    Parameters
    ----------
    paragraphs : list of paragraphs 
    specific_word : word   

    Returns
    -------
    list of paragraphs containing specific word
    """
    word_paragraphs = {}
    for i, paragraph in enumerate(paragraphs):
        tmp = []
        if specific_word in paragraph:
            tmp.append(paragraph)
        if len(tmp) > 0:
            word_paragraphs[i] = ','.join(tmp)
    return word_paragraphs


def join_text(list_of_words):
    '''
    Function to join list of words to form a single word
    '''
    new_word = ' '.join(list_of_words)
    new_word = new_word.split(' - ')
    new_word = '-'.join(new_word)
    return new_word


def chemdata_extractor(plain_text):
    '''
    Extraction of neccessary information from plain texts using
    chemdataextractor.
    Parameters
    ----------
    plain_text  

    Returns
    -------
    name_of_chemicals: list of chemical names  
    records : cde records 
    abbreviations : dictionary containing abbreviation
    '''
    cde_doc = cde.Document(plain_text)
    name_of_chemicals = list(set([cem.text for cem in cde_doc.cems]))
    doc_records = [record for record in cde_doc.records.serialize()]
    abbreviations = dict([(','.join(name[0]), join_text(name[1]))
                          for name in cde_doc.abbreviation_definitions])
    return name_of_chemicals, doc_records, abbreviations
