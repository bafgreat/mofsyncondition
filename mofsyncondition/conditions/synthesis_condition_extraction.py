#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import os
import re
import glob
import spacy
from spacy.matcher import PhraseMatcher
import en_core_web_sm
from mofsyncondition.conditions import conditions_extraction
from mofsyncondition.conditions import chemical_entity_regex
from mofsyncondition.doc.convert_html_to_text import html_2_text2
from mofsyncondition.doc import doc_parser
from mofsyncondition.synparagraph import extract_synthesis_paragraphs
from mofsyncondition.io import filetyper
nlp = spacy.load("en_core_web_sm")


def regex_content(all_tokens, pattern):
    contents = []
    for id, token in enumerate(all_tokens):
        match = re.search(pattern, token)
        if match:
            if token == 'evaporation' or token == 'Evaporation':
                if 'slow' or 'Slow' in [all_tokens[id-1], all_tokens[id-2], all_tokens[id-3]]:
                    contents.append('slow evaporation')
            else:
                contents.append(token)
    return list(set(contents))


def select_content(all_tokens, list_content):
    '''
    '''
    content = []
    for token in all_tokens:
        if token in list_content:
            content.append(token)
    return content


def synthetic_method(tokens):
    """
    A function that converts a document into document into 
    token using spacy
     Parameters
    ----------
    plain_text: str.type 

    Returns
    -------
    token : list of words
    """
    # solvents_regex = chemical_entity_regex.solvents_regex()
    method_pattern = chemical_entity_regex.synthetic_method_re()
    synthesis_method = regex_content(tokens, method_pattern)
    synthesis_method = [method.capitalize() for method in synthesis_method]
    synthesis_method = [chemical_entity_regex.method_abbreviation(
        method) for method in synthesis_method]
    return list(set(synthesis_method))


def solvents_in_text(tokens):
    """
    A function that converts a document into document into 
    token using spacy
     Parameters
    ----------
    plain_text: str.type 

    Returns
    -------
    token : list of words
    """
    # solvents_regex = chemical_entity_regex.solvents_regex()
    solvents_pattern = chemical_entity_regex.solvents_regex()
    solvents = select_content(tokens, solvents_pattern)
    solvents = [chemical_entity_regex.solvent_abbreviation(
        solvent) for solvent in solvents]
    return list(set(solvents))


def metal_precursors_in_text(tokens):
    """
    A function that converts a document into document into 
    token using spacy
     Parameters
    ----------
    plain_text: str.type 

    Returns
    -------
    token : list of words
    """
    metal_salt = []
    # print(tokens)
    pattern = chemical_entity_regex.metal_salts_formular()
    for chemical in tokens:
        matches = re.findall(pattern, chemical)
        if matches:
            metal_salt.append(chemical)
    return metal_salt


def mof_alias_in_text(tokens):
    alias_mof = chemical_entity_regex.mof_regex()
    return regex_content(tokens, alias_mof)


def all_reaction_temperature(token, par_doc):
    """
    A function that extract time from tokens
    Parameters
    ----------
    token: str.type 

    Returns
    -------
    list: containing temperature
    """
    temperature = conditions_extraction.get_temperatures_toks(token)
    # reaction_temp, stability_temp, drying_temp, melting_temp = chemical_entity_regex.reaction_temperature_breakdown(temperature, par_doc)
    # reaction_temp, stability_temp, drying_temp
    return chemical_entity_regex.reaction_temperature_breakdown(temperature, par_doc)


def all_reaction_time(token, par_doc):
    """
    A function that extract reaction time from tokens
    Parameters
    ----------
    token: str.type 

    Returns
    -------
    dictionary: containing time, token number and units
    """
    time_in_token = conditions_extraction.get_times_toks(token)
    for time in time_in_token:
        if time['value'] == 'more':
            time['value'] = token[time['tok_id']-1]
    # reaction_time, stability_time, drying_time, crystalization_time = chemical_entity_regex.reaction_time_breakdown(time_in_token, par_doc)
    return chemical_entity_regex.reaction_time_breakdown(time_in_token, par_doc)


def synthesis_condition(plain_text):
    """
    """
    experimental_condition = {}
    paragraphs = doc_parser.text_2_paragraphs(plain_text)
    warning = chemical_entity_regex.synthetic_warning(paragraphs)
    synthetic_paragraphs = extract_synthesis_paragraphs.all_synthesis_paragraphs(
        plain_text)
    dic_synthetic_paragraphs = indices_of_sentetic_paragraphs(
        paragraphs, synthetic_paragraphs)
    elements_symbols = chemical_entity_regex.all_elements()
    for steps, par_index in enumerate(list(dic_synthetic_paragraphs.keys())):
        par_text = dic_synthetic_paragraphs[par_index]
        chemical_names, _, abb = doc_parser.chemdata_extractor(par_text)
        chemical_names = [
            i for i in chemical_names if i not in elements_symbols]
        quantites = chemical_entity_regex.extract_chemical_quantities(
            par_text, chemical_names)
        all_mofs = mof_alias_in_text(chemical_names)
        conditions = {}
        par_tokens, par_doc = doc_parser.tokenize_doc(par_text)
        all_solvents = solvents_in_text(chemical_names)
        reaction_temp, stability_temp, drying_temp, melting_temp, crystalization_temp = all_reaction_temperature(
            par_tokens, par_doc)
        reaction_time, stability_time, drying_time, crystalization_time = all_reaction_time(
            par_tokens, par_doc)
        # mof_names = mof_alias_in_text(par_tokens)
        metal_salt = metal_precursors_in_text(chemical_names)
        metal_salt = [
            salts for salts in metal_salt if not salts in all_solvents]
        tmp_metal_reagent = [
            salts for salts in metal_salt if not salts in all_mofs]
        method_synthetic = synthetic_method(par_tokens)
        conditions['metal precursor'] = [i for i in list(
            set(tmp_metal_reagent)) if i in list(quantites.keys())]
        conditions['solvent'] = list(set(all_solvents))
        conditions['reaction temperature'] = list(set(reaction_temp))
        conditions['melting temperature'] = list(set(melting_temp))
        conditions['crystalization temperature'] = list(set(crystalization_temp))
        conditions['stability temperature'] = list(set(stability_temp))
        conditions['drying temperature'] = list(set(drying_temp))
        conditions['reaction time'] = chemical_entity_regex.get_unique(reaction_time)
        conditions['stability time'] = chemical_entity_regex.get_unique(stability_time)
        conditions['crystalization time'] = chemical_entity_regex.get_unique(crystalization_time)
        conditions['alias'] = list(set(all_mofs))
        if len(method_synthetic) == 0:
            if 'water' in all_solvents or 'H2O' in all_solvents:
                method_synthetic.append('hydrothermal')
            elif len(all_solvents) > 0:
                method_synthetic.append('solvothermal')
        conditions['synthetic method'] = [method.lower()
                                          for method in list(set(method_synthetic))]
        warning_value = [i for i in list(warning.keys()) if i > par_index]

        if len(warning_value) > 0:
            conditions['warning'] = warning[warning_value[0]].strip()
        else:
            conditions['warning'] = 'no warning'
        conditions['quanties'] = quantites
        # conditions['meta_info'] = record
        if len(conditions) > 0:
            experimental_condition['step_'+str(steps)] = conditions
    return experimental_condition


def indices_of_sentetic_paragraphs(paragraphs, synthetic_paragraphs):
    '''
    script to match
    '''
    # nlp = spacy.load("en_core_web_sm")
    patterns = [nlp(text) for text in synthetic_paragraphs]
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    matcher.add("MatchPhrase", None, *patterns)
    matching_paragraphs = {}
    for i, paragraph in enumerate(paragraphs):
        doc = nlp(paragraph)
        matches = matcher(doc)
        if matches:
            matching_paragraphs[i] = paragraph
    return matching_paragraphs

# html_files = glob.glob('../test/EDUSIF.html')


def compile_synthesis_condition(html_file):
    name = html_file.split('/')[-1].split('.')[0]
    print(name)
    plain_text = html_2_text2(html_file)
    experimental_condition = synthesis_condition(plain_text)
    return name, experimental_condition


def run_condition_extraction(html_files):
    '''
    function that takes an html file and create a database containing 
    extracted synthesis conditions
    '''
    synthesis_data = {}
    for html_file in html_files:
        # try:
        name, experimental_condition = compile_synthesis_condition(
            html_file)
      
        #     print(experimental_condition)
        # except:
        #     pass
        synthesis_data[name] = experimental_condition

        filetyper.append_json(synthesis_data, '../db/json/all_synthesis_data.json')
    return

def run(html_files):
    outfile = '../db/json/all_synthesis_data.json'
    if os.path.exists(outfile):
        json_data = filetyper.load_data(outfile)

        done_keys = json_data.keys()
        all_html_refcodes = [i.split('/')[-1].split('.')[0] for i in html_files]
        unfinished_refcodes = [i for i in all_html_refcodes if not i in done_keys]
        all_html_files = [external_drive_path + '/'+refcode +
                    '.html' for refcode in unfinished_refcodes]
        all_html_files = [
        file_path for file_path in all_html_files if os.path.getsize(file_path) > 500]
    else:
        all_html_files = [file_path for file_path in html_files if os.path.getsize(file_path) > 500]

    run_condition_extraction(all_html_files)
    
# external_drive_path = os.path.abspath('/Volumes/My Passport/All_HTML')
# html_files = sorted(glob.glob(external_drive_path+'/*.html'))
run(html_files)
# # check = [os.path.getsize(file_path) for file_path in all_html_files]
# # print (check)
