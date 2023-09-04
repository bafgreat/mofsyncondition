#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
from nltk.tokenize import word_tokenize
import numpy as np 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from mofsyncondition.doc import convert_html_to_text
from mofsyncondition.doc import doc_parser
from mofsyncondition.io.filetyper import load_data


def all_synthesis_paragraphs(plain_text, model='LR_CV'):
    '''
    Function to extract paragraphs describing synthesis 
    Parameters
    ----------
    plain_text: plain text, which could be a full article 

    Returns
    -------
    list of paragraphs discribing sythensis conditions
    '''
    paragraphs = doc_parser.text_2_paragraphs(plain_text)
    vectorizer_loader = load_data('../models/vectorizer.pkl')
    if model == 'LR_CV':
        model_name = 'synpar_LR_CV_model'
    elif model == 'LR_tfv':
        model_name = 'synpar_LR_tfv_model'
    elif model == 'NB_CV':
        model_name = 'synpar_NB_CV_model'
    elif model == 'NB_tfv':
        model_name = 'synpar_NB_tfv_model'
    
    model = load_data(f'../models/{model_name}.pkl')
    vectorizer = vectorizer_loader[f'{model_name}']
    text_vectors = vectorizer.transform(paragraphs)
    prediction = model.predict(text_vectors)
    n_indices = np.where(prediction == 1)[0]
    synthesis_paragraphs = [paragraphs[i] for i in n_indices]
    return  synthesis_paragraphs 
    
# plain_text = convert_html_to_text.html_2_text2('../test/Test3.html')

# print (all_synthesis_paragraphs(plain_text))
