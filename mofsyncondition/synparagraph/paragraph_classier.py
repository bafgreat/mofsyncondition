#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import re
import string
import chemdataextractor as cde
import spacy
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from mofsyncondition.doc import convert_html_to_text
from mofsyncondition.doc import doc_parser
from mofsyncondition.conditions import synthesis_condition_extraction
from mofsyncondition.conditions import chemical_entity_regex


def spacy_tokenizer(plain_text):
    '''
    Remove stop words from a list of tokens. 
    Parameters
    ----------
    token list   

    Returns
    -------
    cleaned token
    '''
    nlp = spacy.load('en_core_web_sm')
    spacy_stopwords = nlp.Defaults.stop_words
    punctuations = string.punctuation
    spacy_doc = nlp(plain_text)
    mytokens = [word.lemma_.lower().strip() if word.lemma_ !=
                "-PRON-" else word.lower_ for word in spacy_doc]
    mytokens = [
        word for word in mytokens if word not in spacy_stopwords and word not in punctuations]
    # Removing spaces and converting text into lowercase
    mytokens = [clean_text(text) for text in mytokens]
    return mytokens


def clean_text(text):
    # Removing spaces and converting text into lowercase
    return text.strip().lower()


def mode_builder():
    bow_vector = CountVectorizer(tokenizer=spacy_tokenizer, ngram_range=(1, 1))
    tfidf_vector = TfidfVectorizer(tokenizer=spacy_tokenizer)
    return


def preselected_data(plain_text):
    seen_keys = []
    selected_paragraphs = {}
    name_of_chemicals, _, _ = doc_parser.chemdata_extractor(plain_text)
    paragraphs = doc_parser.text_2_paragraphs(plain_text)
    metal_precursors = synthesis_condition_extraction.metal_precursors_in_text(
        name_of_chemicals)
    mofs = synthesis_condition_extraction.mof_alias_in_text(name_of_chemicals)
    chem_data_to_select = name_of_chemicals  # metal_precursors + mofs
    for chem in chem_data_to_select:
        paragraph = doc_parser.paragraph_containing_word(paragraphs, chem)
        all_keys = paragraph.keys()
        unseen_keys = [keys for keys in all_keys if keys not in seen_keys]
        if len(unseen_keys) > 0:
            for key in paragraph:
                selected_paragraphs[key] = paragraph[key]
            seen_keys.extend(unseen_keys)
    for key in sorted(selected_paragraphs.keys()):
        print('')
        print(key)
        print('')
        print(selected_paragraphs[key])
    ccdc_paragraph = doc_parser.paragraph_containing_word(paragraphs, 'CCDC')
    data = ''.join(list(ccdc_paragraph.values()))
    _, spacy_doc = doc_parser.tokenize_doc(data )
    print('ccdc_number: ', chemical_entity_regex.find_ccdc_number(spacy_doc))
    return selected_paragraphs


test = convert_html_to_text.html_2_text2('../db/html/FAXQIH.html')
preselected_data(test)
# selected_par = [par for par in doc_parser.paragraph_containing_word(
#     paragraphs, 'Zn(NO3)2·4H2O')

# clean = spacy_tokenizer(selected_par[119])
# mode_builder( )
# print (clean)
