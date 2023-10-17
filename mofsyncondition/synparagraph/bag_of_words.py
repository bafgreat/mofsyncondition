#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import nltk
from sklearn import model_selection
from mofsyncondition.io.filetyper import load_data, save_pickle, append_pickle
from mofsyncondition.synparagraph import model_evaluation
from mofsyncondition.synparagraph import ml_models
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def paragraph_classifier(text_data_path, model_key='LR', vectorize_key="CV"):
    '''
    A simple function for sentoiment analysis to extract the paragraphs that
    are describing the synthesis conditions.

    '''
    df = load_data(text_data_path)

    # Create new column called kfolf and fill with -1
    df['kfold'] = -1

    # The next step is to randomize the rows of the data

    df = df.sample(frac=1).reset_index(drop=True)

    # extract labels
    y_label = df.sentiment.values

    # initiate the kfold class from model_selection
    k_f = model_selection.StratifiedKFold(n_splits=5)
    # fille new kfold class from model selection
    for f, (t_, v_) in enumerate(k_f.split(X=df, y=y_label)):
        df.loc[v_, 'kfold'] = f
    # we go over folds created
    for fold_ in range(5):
        # tmp df for training and testing
        train_df = df[df.kfold != fold_].reset_index(drop=True)
        test_df = df[df.kfold == fold_].reset_index(drop=True)

        train_text = train_df.paragraph
        test_text = test_df.paragraph

        # transforming training and validation
        vectorizer = ml_models.vectorizer(train_text, vectorize_key)

        # transform training and validation data
        xtrain = vectorizer.transform(train_text)
        xtest = vectorizer.transform(test_text)

        model = ml_models.sklearn_model(model_key)

        # fit the model
        model.fit(xtrain, train_df.sentiment)

        # make prediction on test data
        # threshold for prediction
        prediction = model.predict(xtest)
        y_true = test_df.sentiment
        # print (prediction)

        # calculate accuracy
        # accuracy = metrics.accuracy_score(test_df.sentiment, prediction)
        with open('../evaluation/paragraph_model_evaluator.txt', 'a', encoding='utf-8') as f_writer:
            print(f"{model_key}\t{''}\t{vectorize_key}", file=f_writer)
            print(f"Fold_:{fold_}", file=f_writer)
            print(
                f"Accuracy = {model_evaluation.accuracy( y_true, prediction)}", file=f_writer)
            print(
                f"roc_auc = {model_evaluation.roc_auc( y_true, prediction)}", file=f_writer)
            print(
                f"f_score = {model_evaluation.f_score( y_true, prediction)}", file=f_writer)
            print(
                f"recall = {model_evaluation.recall( y_true, prediction)}", file=f_writer)
            print(
                f"precision = {model_evaluation.precision( y_true, prediction)}", file=f_writer)
            print('', file=f_writer)
    data = {f'synpar_{model_key}_{vectorize_key}_model': vectorizer}
    append_pickle(data, '../models/vectorizer.pkl')
    model_evaluation.confusion_matrix(
        y_true, prediction,  model_key, vectorize_key)
    save_pickle(
        model, f'../models/synpar_{model_key}_{vectorize_key}_model.pkl')
    return


file_path = '../db/csv/Training_data_for_sentiment_analysis.xlsx'
# paragraph_classifier(file_path, model_key='LR', vectorize_key="CV")
# paragraph_classifier(file_path, model_key='NB', vectorize_key="tfv")
# paragraph_classifier(file_path, model_key='LR', vectorize_key="tfv")
# paragraph_classifier(file_path, model_key='NB', vectorize_key="CV")
df = load_data(file_path)
y_label = df.sentiment.values
positive = df[df['sentiment'] == 1]
print (len(positive))

print(len(y_label))

print((len(positive)/len(y_label))*100)