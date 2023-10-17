#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import pandas as pd 
from mofsyncondition.io.filetyper import load_data

def collect_data(data, ml_model):
    '''
    Collect evaluation from every metrix and take average
    '''
    averages = {}
    acc, auc, score, recall, precision = [],[],[],[],[]
    for index, lines in enumerate(data):
        line = lines.split()
        if line == ml_model:
            acc.append(float(data[index+2].split()[2]))
            auc.append(float(data[index+3].split()[2]))
            score.append(float(data[index+4].split()[2]))
            recall.append(float(data[index+5].split()[2]))
            precision.append(float(data[index+6].split()[2]))
    
    if ml_model[1] == 'tfv':
        vectorizer = 'TF-IDF'
    else:
        vectorizer = ml_model[1]
    averages['model']=ml_model[0] + '-' + vectorizer
    averages['accuracy']=round(sum(acc)/len(acc),3)
    averages['roc-auc']=round(sum(auc)/len(auc),3)
    averages['f-score']=round(sum(score)/len(score),3)
    averages['recall']=round(sum(recall)/len(recall),3)
    averages['precision']=round(sum(precision)/len(precision),3)
    return averages
    
    print (averages)
def extract_models(data):
    '''
    script to extract all models in file
    '''
    ml_models = []
    for lines in data:
        line = lines.split()
        if len(line) == 2:
            if not line in ml_models:
                ml_models.append(line)
    return ml_models
 
def create_tabular_average(data):
    all_averages = []
    all_models = extract_models(data)
    for models in all_models:
        averages = collect_data(data, models)
        all_averages.append(averages)
    df = pd.DataFrame(all_averages)
    df.to_latex('evaluation.tex')
        
            
data = load_data('paragraph_model_evaluator.txt')
create_tabular_average(data)

