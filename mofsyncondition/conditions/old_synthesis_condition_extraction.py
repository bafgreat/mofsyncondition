#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import re
import glob
import spacy
import en_core_web_sm
from mofsyncondition.conditions import conditions_extraction
from  mofsyncondition.conditions import chemical_entity_regex
from mofsyncondition.doc.convert_html_to_text import html_2_text2
from mofsyncondition.doc import doc_parser

def regex_content(all_tokens, pattern):
    contents = []
    for id, token in enumerate(all_tokens):
        match = re.search(pattern, token)
        if match:
            if token == 'evaporation' or token == 'Evaporation':
                if 'slow' or 'Slow' in [all_tokens[id-1], all_tokens[id-2], all_tokens[id-3]]:
                    contents.append('Slow evaporation')
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
    
    pattern = chemical_entity_regex.metal_salts_formular()
    metal_ = regex_content(tokens, pattern)
    metal_salt = [text for text in metal_ if len(doc_parser.unclosed_brackets(text)) == 0]
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
    token_temp = []
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
    reaction_time, stability_time, drying_time = chemical_entity_regex.reaction_time_breakdown(
        time_in_token, par_doc)
    return reaction_time, stability_time, drying_time
    
def synthesis_condition(plain_text, paragraphs):
    """
    """
    experimental_condition = {}
    chemical_name, records, cde_doc = doc_parser.chemdata_extractor(plain_text)
    stability_pattern, analysis_pattern = chemical_entity_regex.key_words_regex()
    metal_precursors = metal_precursors_in_text(chemical_name)
    all_mofs = mof_alias_in_text(chemical_name)
    metal_precursors = [i for i in metal_precursors if not i in all_mofs]
    seen = []
    i = 0
    for metal_formular in metal_precursors:
        if not metal_formular.startswith('[') and not metal_formular.endswith(']'):
            metal_salt_paragraph = doc_parser.paragraph_containing_word(
                paragraphs, metal_formular)
            for par_index in list(metal_salt_paragraph.keys()):
                if not par_index in seen:
                    par_text = metal_salt_paragraph[par_index]
                    chemical_entity_regex.get_ph(par_text)
                    par_tokens, par_doc = doc_parser.tokenize_doc(par_text)
                    all_solvents = solvents_in_text(par_tokens)
                    reaction_temp, stability_temp, drying_temp, melting_temp = all_reaction_temperature(par_tokens, par_doc)
                    reaction_time, stability_time, drying_time = all_reaction_time(
                        par_tokens, par_doc)
                    mof_names = mof_alias_in_text(par_tokens)
                    metal_salt = metal_precursors_in_text(par_tokens)
                    method_synthetic = synthetic_method(par_tokens)
                    conditions = {}
                    react_temp = []
                    stab_temp = []
                    dry_temp = []
                    react_time = []
                    stab_time = []
                    degas_time = []
                    tmp_solvent = []
                    mof_name = []
                    methods = []
                    melt_temp = []
                    tmp_metal_reagent = []
                    for solvent in all_solvents:
                        tmp_solvent.append(solvent)
                    for time in reaction_time:
                        react_time.append(time)
                    for time in stability_time:
                        stab_time.append(time)
                    for time in drying_time:
                        degas_time.append(time)
                    for temp in reaction_temp:
                        react_temp.append(temp)
                    for temp in stability_temp:
                        stab_temp.append(temp)
                    for temp in drying_temp:
                        dry_temp.append(temp)
                    for temp in melting_temp:
                        melt_temp.append(temp)
                    for mofs in mof_names:
                        mof_name.append(mofs)
                    for method in method_synthetic:
                        methods.append(method)
                    for salts in metal_salt:
                        if not salts in all_mofs:
                            tmp_metal_reagent.append(salts)
                    sentence = chemical_entity_regex.sentence_containing_word(par_doc, metal_formular)
                    match = re.search(analysis_pattern, sentence)
                    match2 = re.search(stability_pattern, sentence)
                    if not (match and match2): 
                        conditions['metal precursor'] = list(set(tmp_metal_reagent))
                        conditions['solvent'] = list(set(tmp_solvent))
                        conditions['reaction temperature'] = list(set(react_temp))
                        conditions['stability temperature'] = list(set(stab_temp))
                        conditions['analysis temperature'] = list(set(dry_temp))
                        conditions['melting temperature'] = list(set(melt_temp))
                        conditions['reaction time'] = list(set(react_time))
                        conditions['stability time'] = list(set(stab_time))
                        conditions['drying time'] = list(set(degas_time))
                        conditions['alias'] = list(set(mof_name))
                        if len(methods) == 0:
                            if 'water' in all_solvents or 'H2O' in all_solvents:
                                methods.append('Hydrothermal')
                            elif len(all_solvents) > 0:
                                methods.append('Solvothermal')
                        conditions['synthetic method'] = list(set(methods))
                    if len(conditions) > 0:
                        if len(mof_name)>0:
                            experimental_condition['step'+str(i)] = conditions
                        i += 1
                    seen.append(par_index)
    
    return synthesis_condition2(experimental_condition, paragraphs)

def synthesis_condition2(experimental_condition, paragraphs):
    seen_mofs = []
    seen_par = []
    for steps in experimental_condition:
        conditions = experimental_condition[steps]
        mofs = conditions['alias']
        for mof in mofs:
            paragraph = doc_parser.paragraph_containing_word(paragraphs, mof)
            for index in paragraph:
                if not index in seen_par:
                    par_text = paragraph[index]
                    par_tokens, par_doc = doc_parser.tokenize_doc(par_text)
                    reaction_temp, stability_temp, drying_temp, melting_temp = all_reaction_temperature(par_tokens, par_doc)
                    reaction_time, stability_time, drying_time = all_reaction_time(par_tokens, par_doc)
                    if len(conditions['reaction temperature']) == 0:
                        conditions['reaction temperature'] = reaction_temp
                    if len(conditions['stability temperature']) == 0:
                        conditions['stability temperature'] = stability_temp
                    if len(conditions['analysis temperature']) == 0:
                        conditions['analysis temperature'] = drying_temp
                    if len(conditions['melting temperature']) == 0:
                        conditions['melting temperature'] = melting_temp 
                    if len(conditions['reaction time']) == 0:
                        conditions['reaction time'] = reaction_time
                    if len(conditions['stability time']) == 0:
                        conditions['stability time'] = stability_time
                    if len(conditions['drying time']) == 0:
                        conditions['drying time'] = drying_time
                    if not mof in seen_mofs:
                        if len(conditions['metal precursor']) == 0:
                            conditions['metal precursor'] = list(set([i for i in metal_precursors_in_text(par_tokens) if not i in mofs]))
                        if len(conditions['solvent']) == 0:
                            conditions['solvent'] = solvents_in_text(par_tokens)
                seen_par.append(index)
            seen_mofs.append(mof)
        experimental_condition[steps] = conditions
    return experimental_condition
        
html_files = glob.glob('../../MOF_structures/data/htmls/*html')
#html_files = glob.glob('../test/EDUSIF.html')



def compile_synthesis_condition(html_file):
    name = html_file.split('/')[-1].split('.')[0]
    print(name)
    plain_text = html_2_text2(html_file)
    tokens, _ = doc_parser.tokenize_doc(plain_text)
    paragraphs = doc_parser.text_2_paragraphs(plain_text)
    experimental_condition = synthesis_condition(plain_text, paragraphs)
    print (experimental_condition)
    # print(text_2_paragraphs(plain_text))


# for html_file in html_files:
#     compile_synthesis_condition(html_file)


# # condition_extraction(tokens, doc)
# # print(solvents_in_text(tokens))
# # print(metals_in_text(tokens))
