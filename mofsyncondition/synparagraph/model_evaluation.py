#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def accuracy(y_true, y_pred, standard=True):
    '''
    Function to compute the accuracy of a machine learning model
    Parameters
    ----------
    y_true: list of true values
    y_predict: list of predicted values
    standard: Boolen that determines whether to us
              method from sklean.metrics or implemented method
    return correct prediction/
    ----------
    '''
    if standard:
        return metrics.accuracy_score(y_true, y_pred)
    else:
        correct_counter = 0
        for y_t, y_p in zip(y_true, y_pred):
            if y_t == y_p:
                correct_counter += 1
        return correct_counter/float(len(y_true))


def true_positive(y_true, y_pred):
    '''
    Function to compute the true positive predictions
    from a machine learning model
    y_true: list of true values
    y_predict: list of predicted values
    '''
    t_p = 0

    for y_t, y_p in zip(y_true, y_pred):
        if y_t == 1 and y_p == 1:
            t_p += 1
    return t_p


def true_negative(y_true, y_pred):
    '''
    Function to compute the true negative predictions
    from a machine learning model
    y_true: list of true values
    y_predict: list of predicted values
    '''
    t_n = 0

    for y_t, y_p in zip(y_true, y_pred):
        if y_t == 0 and y_p == 0:
            t_n += 0
    return t_n


def false_positive(y_true, y_pred):
    '''
    Function to compute the false positive predictions
    from a machine learning model
    y_true: list of true values
    y_predict: list of predicted values
    '''
    f_p = 0

    for y_t, y_p in zip(y_true, y_pred):
        if y_t == 1 and y_p == 0:
            f_p += 1
    return f_p


def false_negative(y_true, y_pred):
    '''
    Function to compute the true negative predictions
    from a machine learning model
    y_true: list of true values
    y_predict: list of predicted values
    '''
    f_n = 0

    for y_t, y_p in zip(y_true, y_pred):
        if y_t == 0 and y_p == 1:
            f_n += 0
    return f_n


def precision(y_true, y_pred):
    '''
    Function to compute the precision of a machine learning model
    y_true: list of true values
    y_predict: list of predicted values

    return t_p/(t_p + f_p)
    '''
    t_p = true_positive(y_true, y_pred)
    f_p = false_positive(y_true, y_pred)
    return t_p/float((t_p + f_p))


def recall(y_true, y_pred):
    '''
    Function to compute the Recall from a machine learning model. 
    This give the percentage by how much our model correctly predicts
    the true positive
    y_true: list of true values
    y_predict: list of predicted values
    returns t_p/(t_p+f_n)
    '''
    t_p = true_positive(y_true, y_pred)
    f_n = false_negative(y_true, y_pred)
    return t_p/float((t_p + f_n))


def f_score(y_true, y_pred, standard=True):
    '''
    Function to compute the f1 score of a machine learning model. 
    It is a the weighted average of precision and recall
    y_true: list of true values
    y_predict: list of predicted values
    standard: Boolen that determines whether to us
              method from sklean.metrics or implemented method
    returns 2PR/(P+R)
    '''
    if standard:
        return metrics.f1_score(y_true, y_pred)
    else:
        p_value = precision(y_true, y_pred)
        r_value = recall(y_true, y_pred)
        return 2*p_value*r_value/float((p_value + r_value))


def roc_auc(y_true, y_pred):
    '''
    Function to compute the area under curve also known as the 
    receiver operating characteristics. 
    y_true: list of true values
    y_predict: list of predicted values

    '''
    return metrics.roc_auc_score(y_true, y_pred)


def confusion_matrix(y_true, y_pred, model_key='LR', vector_key='CV'):
    '''
    Function to plot the confusion metrix. 
    y_true: list of true values
    y_predict: list of predicted values
    '''
    c_m = metrics.confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(np.eye(2), annot=c_m, fmt='g', annot_kws={'size': 50},
            cmap=sns.color_palette(['#F1C40F', '#2E86C1'], as_cmap=True), cbar=False,
            yticklabels=['True', 'False'], xticklabels=['False', 'True'], ax=ax)
    sns.set(font_scale=2.5)
    ax.tick_params(axis='both', which='major', labelsize=20)
    plt.ylabel('Actual Labels', fontsize=20)
    plt.xlabel('Predicted Labels', fontsize=20)
    additional_texts = ['(True Negative)', '(False Positive)', '(False Negative)', '(True Positive)']
    for text_elt, additional_text in zip(ax.texts, additional_texts):
        ax.text(*text_elt.get_position(), '\n' + additional_text, color=text_elt.get_color(),
                ha='center', va='top', size=24)
    plt.tight_layout()
    plt.savefig(
        f'../evaluation/confusion-matrix_{model_key}-{vector_key}.png',  dpi=800, bbox_inches='tight')
