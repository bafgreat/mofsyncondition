#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import numpy as np
from mofsyncondition.doc import doc_parser
from mofsyncondition.io.filetyper import load_model


def all_synthesis_paragraphs(plain_text, model='NN_tfv'):
    '''
    Function to extract paragraphs describing synthesis
    Parameters
    ----------
    paragraphs: list of paragraphs

    Returns
    -------
    list of paragraphs discribing sythensis conditions
    '''

    vectorizer_loader, ml_model = load_model(model)

    paragraphs = plain_text

    vectorizer = vectorizer_loader[f'{model}']
    text_vectors = vectorizer.transform(paragraphs)
    prediction = ml_model.predict(text_vectors)
    n_indices = np.where(prediction == 1)[0]
    synthesis_paragraphs = [paragraphs[i] for i in n_indices]
    return synthesis_paragraphs
