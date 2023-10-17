#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import os
import string
import random
import pandas as pd
import nltk
from sklearn import model_selection
import spacy
from spacy.matcher import Matcher
from spacy.util import minibatch, compounding
from spacy.training.example import Example
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from mofsyncondition.doc import convert_html_to_text
from mofsyncondition.doc import doc_parser
from mofsyncondition.io.filetyper import load_data, save_pickle, append_pickle
from mofsyncondition.synparagraph import model_evaluation
from mofsyncondition.synparagraph import ml_models
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def custom_tokenizer(nlp):
    # Add a rule to the tokenizer to treat words enclosed within brackets as a single token
    infixes = nlp.Defaults.infixes + [r'\[[^\]]+\]|\([^\)]+\)']
    infix_regex = spacy.util.compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_regex.finditer


def get_entities(doc):
    """
    code to find relation in sentences
    borrowed from 
    https://www.kaggle.com/code/pavansanagapati/knowledge-graph-nlp-tutorial-bert-spacy-nltk 
    """
    # chunk 1
    nlp = spacy.load('en_core_web_sm')
    ent1 = ""
    ent2 = ""

    prv_tok_dep = ""    # dependency tag of previous token in the sentence
    prv_tok_text = ""   # previous token in the sentence

    prefix = ""
    modifier = ""
    doc = nlp(doc)
    for sent in doc.sents:
        for tok in nlp(sent.text):
            # chunk 2
            # if token is a punctuation mark then move on to the next token
            if tok.dep_ != "punct":
                # check: token is a compound word or not
                if tok.dep_ == "compound":
                    prefix = tok.text
                    # if the previous word was also a 'compound' then add the current word to it
                    if prv_tok_dep == "compound":
                        prefix = prv_tok_text + " " + tok.text

            # check: token is a modifier or not
            if tok.dep_.endswith("mod") == True:
                modifier = tok.text
                # if the previous word was also a 'compound' then add the current word to it
                if prv_tok_dep == "compound":
                    modifier = prv_tok_text + " " + tok.text

            # chunk 3
            if tok.dep_.find("subj") == True:
                ent1 = modifier + " " + prefix + " " + tok.text
                prefix = ""
                modifier = ""
                prv_tok_dep = ""
                prv_tok_text = ""

            # chunk 4
            if tok.dep_.find("obj") == True:
                ent2 = modifier + " " + prefix + " " + tok.text

            # chunk 5
            # update variables
            prv_tok_dep = tok.dep_
            prv_tok_text = tok.text

    return [ent1.strip(), ent2.strip()]


def get_relation(doc):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(doc)

    # Matcher class object
    matcher = Matcher(nlp.vocab)

    # define the pattern
    pattern = [{'DEP': 'ROOT'},
               {'DEP': 'prep', 'OP': "?"},
               {'DEP': 'agent', 'OP': "?"},
               {'POS': 'ADJ', 'OP': "?"}]

    matcher.add("matching_1", [pattern])

    matches = matcher(doc)
    k = len(matches) - 1

    span = doc[matches[k][1]:matches[k][2]]

    return (span.text)


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


def preselected_data(plain_text):
    seen_keys = []
    selected_paragraphs = {}
    name_of_chemicals, _, _ = doc_parser.chemdata_extractor(plain_text)
    paragraphs = doc_parser.text_2_paragraphs(plain_text)
    # metal_precursors = synthesis_condition_extraction.metal_precursors_in_text(
    #     name_of_chemicals)
    # mofs = synthesis_condition_extraction.mof_alias_in_text(name_of_chemicals)
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
    _, spacy_doc = doc_parser.tokenize_doc(data)
    return selected_paragraphs


def create_paragraph_training_data(encoded_paragraph, path_to_save, format='xlsx'):
    """
    Function to create training data of paragraphs for
    sentiment analysis
    Parameters
    ----------
    encoded_paragraph: json file containing encoded paragraphs 
    path_2_csv: folder to save dataframe

    """
    training_data = {}
    path_to_data = '../db/html'
    json_data = load_data(encoded_paragraph)
    refcodes = list(json_data.keys())
    for refcode in refcodes:
        par_encoder = json_data[refcode]
        all_par_keys = list(par_encoder.keys())
        full_path = os.path.join(path_to_data, refcode+'.html')
        paragraphs = doc_parser.text_2_paragraphs(
            convert_html_to_text.html_2_text2(full_path))
        for index, paragraph in enumerate(paragraphs):
            if str(index) in all_par_keys:
                par_value = par_encoder[str(index)]
                if par_value == 1:
                    training_data[paragraph] = par_value
                else:
                    training_data[paragraph] = 0
            else:
                training_data[paragraph] = 0
    par_df = pd.DataFrame.from_dict(
        training_data, orient='index', columns=['sentiment'])
    par_df.index.name = 'paragraph'
    if format == 'xlsx':
        par_df.to_excel(path_to_save+'/' +
                        'Training_data_for_sentiment_analysis.xlsx')
    elif format == 'csv':
        par_df.to_csv(path_to_save+'/' +
                      'Training_data_for_sentiment_analysis.csv')
    elif format == 'json':
        par_df.to_json(path_to_save+'/' +
                       'Training_data_for_sentiment_analysis.json')

    return


def creat_spacy_data_for_textcat(raw_data):
    '''
    A function tha creates a spacy data set for text classification
    Load training data and split it into 80/20
    Parameters
    ----------
    raw_data: list of lists or tuples containing (text, labels)

    return
    ----------
    spacy_data: The data arrange in format that spacy recognises for 
                text classification
    '''
    spacy_data = []
    random.shuffle(raw_data)
    nlp = spacy.load('en_core_web_sm')
    for text, label in raw_data:
        doc = nlp.make_doc(text)
        if label == 1:
            annotation = {"cats": {"synthesis par": label}}
        else:
            annotation = {"cats": {"non synthesis par": label}}
        spacy_data.append(Example.from_dict(doc,  annotation))
    random.shuffle(raw_data)
    return spacy_data


def load_training_data(file_path, split: float = 0.8, limit: int = 0):
    """
    Load training data and split it into 80/20
    Parameters
    ----------
    file_path: path to the file containing the training data
    return
    ----------
    training_data: training data,
    test_data: testing data for evaluation
    """
    data = load_data(file_path)
    x_train, x_test, y_train, y_test = train_test_split(
        data['paragraph'], data['sentiment'], test_size=0.2, random_state=42, shuffle=True)
    training_data = list(map(list, list(zip(x_train, y_train))))
    test_data = list(map(list, zip(x_test, y_test)))

    return training_data, test_data


def model_evaluator(tokenizer, textcat, test_data):
    '''
    Evaluating ML model
    Parameters
    ----------
    tokenizer: npl.tokenizer to tokenize sentences
    textcat: trained model
    test_data: test data

    return
    ----------
    '''
    paragraphs, labels = zip(*test_data)
    paragraphs = (tokenizer(paragraph) for paragraph in paragraphs)
    true_positives = 0
    false_positives = 1e-8  # Can't be 0 because of presence in denominator
    true_negatives = 0
    false_negatives = 1e-8
    for i, paragraph in enumerate(textcat.pipe(paragraphs)):
        true_label = labels[i]
        for predicted_label, score in paragraph.cats.items():
            print(predicted_label, score, true_label)
            # Every cats dictionary includes both labels. You can get all
            # the info you need with just the pos label.
            if (
                predicted_label == "non synthesis par"
            ):
                continue
            if score >= 0.5 and true_label == 1:
                true_positives += 1
            elif score >= 0.5 and true_label == 0:
                false_positives += 1
            elif score < 0.5 and true_label == 0:
                true_negatives += 1
            elif score < 0.5 and true_label == 1:
                false_negatives += 1
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)

    if precision + recall == 0:
        f_score = 0
    else:
        f_score = 2 * (precision * recall) / (precision + recall)
    return {"precision": precision, "recall": recall, "f-score": f_score}


def spacy_synethesis_model(training_data, test_data, number_of_iteration=40):
    """
    classification model
    Parameters
    ----------
    training_data: training data,
    test_data: testing data for evaluatio
    ----------
    model
    """
    nlp = spacy.load("en_core_web_sm")
    if "textcat" not in nlp.pipe_names:
        textcat = nlp.add_pipe("textcat", last=True)
    else:
        textcat = nlp.get_pipe("textcat")
    textcat.add_label("synthesis par")
    textcat.add_label("non synthesis par")
    # Train only textcat
    training_excluded_pipes = list([
        pipe for pipe in nlp.pipe_names if pipe != "textcat"
    ])
    for pipe in training_excluded_pipes:
        nlp.disable_pipe(pipe)
    optimizer = nlp.begin_training()
    print('Training started!!!')
    batch_sizes = compounding(4.0, 32.0, 1.001)
    for _ in range(number_of_iteration):
        loss = {}
        random.shuffle(training_data)
        batches = minibatch(training_data, size=batch_sizes)
        for batch in batches:
            spacy_data = creat_spacy_data_for_textcat(batch)
            nlp.update(spacy_data, drop=0.2, sgd=optimizer, losses=loss)
        with textcat.model.use_params(optimizer.averages):
            evaluation_results = model_evaluator(
                tokenizer=nlp.tokenizer,
                textcat=textcat,
                test_data=test_data
            )
            with open('syn_model_evaluator.txt', 'w', encoding='utf-8') as f_writer:
                print(
                    f"{loss['textcat']}\t{evaluation_results['precision']}"
                    f"\t{evaluation_results['recall']}"
                    f"\t{evaluation_results['f-score']}",
                    file=f_writer)
    # Save model
    with nlp.use_params(optimizer.averages):
        nlp.to_disk("../models/model_syn_paragraph")
    return


def bow_paragraph_classifier(text_data_path, model_key, vectorize_key):
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
    data = {f'{model_key}_{vectorize_key}': vectorizer}
    append_pickle(data, f'../models/vectorizers/{model_key}_{vectorize_key}.pkl')
    model_evaluation.confusion_matrix(
        y_true, prediction,  model_key, vectorize_key)
    save_pickle(
        model, f'../models/ml_models/{model_key}_{vectorize_key}_model.pkl')
    return


file_path = '../db/csv/Training_data_for_sentiment_analysis.xlsx'
bow_paragraph_classifier(file_path, 'LR', "tfv")
bow_paragraph_classifier(file_path, 'LR', "CV")
bow_paragraph_classifier(file_path, 'NB', "tfv")
bow_paragraph_classifier(file_path, 'NB', "CV")
bow_paragraph_classifier(file_path, 'SVM', "tfv")
bow_paragraph_classifier(file_path, 'SVM', "CV")
bow_paragraph_classifier(file_path, 'DT', "tfv")
bow_paragraph_classifier(file_path, 'DT', "CV")
bow_paragraph_classifier(file_path, 'RF', "tfv")
bow_paragraph_classifier(file_path, 'RF', "CV")
bow_paragraph_classifier(file_path, 'NN', "tfv")
bow_paragraph_classifier(file_path,'NN', "CV")
