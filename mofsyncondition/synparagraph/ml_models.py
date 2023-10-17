#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
from sklearn import linear_model, naive_bayes, svm, tree, ensemble, neural_network
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def sklearn_model(key):
    """
    Machine learning model selection
    """
    if key == 'LR':
        # initialize logistic regression
        # model = linear_model.LogisticRegression(max_iter=1000)
        return linear_model.LogisticRegression(max_iter=10000)
    elif key == 'NB':
        return naive_bayes.MultinomialNB()
    elif key == 'SVM':
        return svm.SVC(kernel='linear')
    elif key == 'GNB':
        return naive_bayes.GaussianNB()
    elif key == 'DT':
        return tree.DecisionTreeClassifier()
    elif key == 'RF':
        return ensemble.RandomForestClassifier()
    elif key == 'NN':
        return neural_network.MLPClassifier()


def vectorizer(train_text, key):
    """
    model to vectorize data
    """
    if key == 'tfv':
        #  initialize TfidfVectorizer
        # Term Frequency and Inverse Document Frequency
        tfidf_vec = TfidfVectorizer(
            tokenizer=word_tokenize, token_pattern=None)
        # fit tfidf_vec on training data

        return tfidf_vec.fit(train_text)
    elif key == 'CV':
        #  initialize CounterVectorizer
        count_vec = CountVectorizer(
            tokenizer=word_tokenize, token_pattern=None)
        # fit count_vec on training data
        return count_vec.fit(train_text)
