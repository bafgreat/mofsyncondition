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
    metals = chemical_entity_regex.metal_atom_dic()
    metals = list(metals.items())
    all_metals = '|'.join([metal for metal_tuple in metals for metal in metal_tuple])
    multiplicity = chemical_entity_regex._multiplicity()
    pattern = r'\b'+multiplicity+all_metals+r'\b'
    pattern = re.compile( pattern)
    
    for chemical in tokens:
        if isinstance(chemical, tuple) or isinstance(chemical, list) or isinstance(chemical, dict):
            for chem in chemical: 
                match = re.match(pattern, chem)
                metal_salt.append(chemical)
        else:
            matches = re.match(pattern, chemical)
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

def find_organic_reagents(quantity, all_solvents):
    '''
    guest organic reagens
    '''
    organic_precursors = []
    metals = chemical_entity_regex.metal_atom_dic()
    metals = list(metals.items())
    all_metals = '|'.join([metal for metal_tuple in metals for metal in metal_tuple])
    multiplicity = chemical_entity_regex._multiplicity()
    pattern = r'\b'+multiplicity+all_metals+r'\b'
    pattern = re.compile( pattern)
    for element in list(quantity.keys()):
        if isinstance(element, tuple) or isinstance(element, list) or isinstance(element, dict):
            for chem in element:         
                match = re.match(pattern, chem)
                if not match:
                    organic_precursors.append(chem)
        else:
            match = re.match(pattern, element)
            if not match:
                organic_precursors.append(element)
    return[element for element in organic_precursors if not element in all_solvents]


def find_organic_reagents2(quantity, name_from_json, all_solvents):
    '''
    guest organic reagens
    '''
    organic_precursors1 = []
    seen = []
    for elements in quantity:
        try:
            doc_elt = nlp(elements)
            for org_name in name_from_json:
                doc_org = nlp(org_name)
                similarity =  doc_elt.similarity(doc_org)
                if similarity*100 >= 90:
                    organic_precursors1.append(org_name)
                    seen.append(elements)
        except ValueError:
            pass 
    new_quantities = {k: v for k, v in quantity.items() if k not in seen}
    organic_precursors2 = find_organic_reagents(new_quantities, all_solvents)
    return list(set(organic_precursors1))+ organic_precursors2 

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
    return chemical_entity_regex.reaction_time_breakdown(time_in_token, par_doc)


def correct_abbreviations(substrates, abbreviation, chemical_list):
    '''
    check whether there are any abbreviatons in the list of chemicals and fix it
    '''
    if isinstance(substrates, list):
        for i, chemical in enumerate(substrates):
            for abb in list(abbreviation.keys()):
                if isinstance(chemical, tuple) or isinstance(chemical, list) or isinstance(chemical, dict):
                    for chem in chemical:
                        if re.search(abb, chem, re.IGNORECASE) and abbreviation[abb] in chemical_list:
                            substrates[i] = abbreviation[abb]
                            break
                else:
                    if re.match(abb, chemical, re.IGNORECASE) and abbreviation[abb] in chemical_list:
                        substrates[i] = abbreviation[abb]
                        break
               
    elif isinstance(substrates, dict):
        for chemical in list(substrates.keys()):
            if isinstance(chemical, tuple) or isinstance(chemical, list) or isinstance(chemical, dict):
                chem = chemical[0]
                substrates[chem]= substrates.pop(chemical)
            else:
                for abb in list(abbreviation.keys()):
                    if re.search(abb, chemical, re.IGNORECASE) and abbreviation[abb] in chemical_list:
                        renamed_chemical = abbreviation[abb]
                        substrates[renamed_chemical]= substrates.pop(chemical)
                        break
    return substrates

def synthesis_condition(plain_text, name_from_json=None):
    """
    """
    experimental_condition = {}
    paragraphs = doc_parser.text_2_paragraphs(plain_text)
    all_chemical_names, _, abbreviation = doc_parser.chemdata_extractor(plain_text)
    warning = chemical_entity_regex.synthetic_warning(paragraphs)
    synthetic_paragraphs = extract_synthesis_paragraphs.all_synthesis_paragraphs(
        plain_text)
    dic_synthetic_paragraphs = indices_of_senthetic_paragraphs(
        paragraphs, synthetic_paragraphs)
    elements_symbols = chemical_entity_regex.all_elements()
    for steps, par_index in enumerate(list(dic_synthetic_paragraphs.keys())):
        par_text = dic_synthetic_paragraphs[par_index]
        chemical_names, _, _ = doc_parser.chemdata_extractor(par_text)
        chemical_names = [
            i for i in chemical_names if i not in elements_symbols]
        quantities = chemical_entity_regex.extract_chemical_quantities(
            par_text, chemical_names)
        all_mofs = mof_alias_in_text(chemical_names)
        conditions = {}
        par_tokens, par_doc = doc_parser.tokenize_doc(par_text)
        all_solvents = solvents_in_text(chemical_names)
        if name_from_json is not None:
            organic_reagents = find_organic_reagents2(quantities, name_from_json, all_solvents )
        else:
            organic_reagents = find_organic_reagents(quantities, all_solvents)
        reaction_temp, stability_temp, drying_temp, melting_temp, crystalization_temp = all_reaction_temperature(
            par_tokens, par_doc)
        reaction_time, stability_time, _, crystalization_time = all_reaction_time(
            par_tokens, par_doc)
        # mof_names = mof_alias_in_text(par_tokens)
        metal_salt = metal_precursors_in_text(chemical_names) + all_mofs
        metal_salt = [
            salts for salts in metal_salt if not salts in all_solvents]
        tmp_metal_reagent = [salts for salts in metal_salt if salts in list(quantities.keys())]
        method_synthetic = synthetic_method(par_tokens)
        metal_precursor = [i for i in list(set(tmp_metal_reagent)) if not i in all_solvents]
        organic_reagents = [i for i in list(set(organic_reagents)) if not i in metal_salt]
        solvents = [i for i in list(set(all_solvents)) if i in list(quantities.keys())]
        conditions['mof_metal_precursor'] = list(set(correct_abbreviations(metal_precursor, abbreviation, all_chemical_names)))
        conditions['mof_organic_linker_reagent'] = [i for i in list(set(correct_abbreviations(organic_reagents, abbreviation, all_chemical_names))) if i not in ['water','Water']]
        conditions['mof_solvent'] = list(set(correct_abbreviations(solvents, abbreviation, all_chemical_names)))
        conditions['mof_reaction_temperature'] = list(set(reaction_temp))
        conditions['mof_melting_temperature'] = list(set(melting_temp))
        conditions['mof_crystallization_temperature'] = list(set(crystalization_temp))
        conditions['mof_stability_temperature'] = list(set(stability_temp))
        conditions['mof_drying_temperature'] = list(set(drying_temp))
        conditions['mof_reaction_time'] = chemical_entity_regex.get_unique(reaction_time)
        conditions['stability time'] = chemical_entity_regex.get_unique(stability_time)
        conditions['mof_crystallization_time'] = chemical_entity_regex.get_unique(crystalization_time)
        conditions['alias'] = list(set([mof for mof in all_mofs if not mof in tmp_metal_reagent ]))
        if len(method_synthetic) == 0:
            if 'water' in all_solvents or 'H2O' in all_solvents:
                method_synthetic.append('hydrothermal')
            elif len(all_solvents) > 0:
                method_synthetic.append('solvothermal')
        conditions['mof_synthesis_method'] = [method.lower()
                                          for method in list(set(method_synthetic))]
        warning_value = [i for i in list(warning.keys()) if i > par_index]

        if len(warning_value) > 0:
            conditions['mof_synthesis_precaution'] = warning[warning_value[0]].strip()
        else:
            conditions['mof_synthesis_precaution'] = 'no warning'
        conditions['mof_reaction_quanties'] = correct_abbreviations(quantities, abbreviation, all_chemical_names)
        if len(conditions['mof_metal_precursor']) > 0 and len(conditions['mof_reaction_quanties'])>0:
            experimental_condition['step_'+str(steps)] = conditions
    return experimental_condition


def indices_of_senthetic_paragraphs(paragraphs, synthetic_paragraphs):
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

def indices_of_headings(paragraphs, headings):
    '''
    script to match
    '''
    # nlp = spacy.load("en_core_web_sm")
    all_headings = {}
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp(heading) for heading in headings]
    matcher.add("Headings", None, *patterns)
    for i, paragraph in enumerate(paragraphs):
        doc = nlp(paragraph)
        matches = matcher(doc)
        if matches:
            all_headings[i] = paragraph
    return all_headings


def compile_synthesis_condition(html_file, ligan_data):
    name = html_file.split('/')[-1].split('.')[0]
    print(name)
    plain_text = html_2_text2(html_file)
    if name in list(ligan_data.keys()):
        name_from_json = ligan_data[name]
        print (name_from_json)
    else:
        name_from_json = 'None'
    experimental_condition = synthesis_condition(plain_text, name_from_json)
    return name, experimental_condition


def run_condition_extraction(html_files):
    '''
    function that takes an html file and create a database containing 
    extracted synthesis conditions
    '''
    synthesis_data = {}
    for html_file in html_files:
        # try:
        ligand_data = filetyper.load_data('../db/json/Organic_reagents.json')
        name, experimental_condition = compile_synthesis_condition(
            html_file, ligand_data)

        synthesis_data[name] = experimental_condition

        filetyper.append_json(synthesis_data, '../db/json/second_synthesis_data.json')
    return

def run(path_to_file):
    html_files = sorted(glob.glob(path_to_file+'/*.html'))
    outfile = '../db/json/second_synthesis_data.json'
    if os.path.exists(outfile):
        json_data = filetyper.load_data(outfile)

        done_keys = json_data.keys()
        all_html_refcodes = [i.split('/')[-1].split('.')[0] for i in html_files]
        unfinished_refcodes = [i for i in all_html_refcodes if not i in done_keys]
        all_html_files = [path_to_file + '/'+refcode +
                    '.html' for refcode in unfinished_refcodes]
        all_html_files = [
        file_path for file_path in all_html_files if os.path.getsize(file_path) > 500]
    else:
        all_html_files = [file_path for file_path in html_files if os.path.getsize(file_path) > 500]

    run_condition_extraction(all_html_files)
    
# external_drive_path = os.path.abspath('/Volumes/My Passport/All_HTML')
external_drive_path = os.path.abspath('/Volumes/X9 Pro/All_HTML')
# html_files = sorted(glob.glob(external_drive_path+'/*.html'))
# html_files = sorted(glob.glob('../db/html/*html'))
path_to_html = '../db/html'
# run(path_to_html)
run(external_drive_path)

