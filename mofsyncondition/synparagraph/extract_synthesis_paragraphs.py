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


<<<<<<< HEAD
def all_synthesis_paragraphs(plain_text, model='NN_tfv'):
=======
def all_synthesis_paragraphs(paragraphs, model='NN_tfv'):
>>>>>>> 9253cec (fixed)
    '''
    Function to extract paragraphs describing synthesis 
    Parameters
    ----------
    paragraphs: list of paragraphs

    Returns
    -------
    list of paragraphs discribing sythensis conditions
    '''
<<<<<<< HEAD
    paragraphs = doc_parser.text_2_paragraphs(plain_text)
=======
>>>>>>> 9253cec (fixed)
    vectorizer_loader = load_data(f'../models/vectorizers/{model}.pkl')
    ml_model = load_data(f'../models/ml_models/{model}_model.pkl')
    vectorizer = vectorizer_loader[f'{model}']
    text_vectors = vectorizer.transform(paragraphs)
    prediction = ml_model.predict(text_vectors)
    n_indices = np.where(prediction == 1)[0]
    synthesis_paragraphs = [paragraphs[i] for i in n_indices]
    return  synthesis_paragraphs 
