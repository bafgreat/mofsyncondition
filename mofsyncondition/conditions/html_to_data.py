#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import ast
import re
import json
import os
import sys
import glob
from mofsyncondition.doc.convert_html_to_text import html_2_text2
from mofsyncondition.io import filetyper

from mofsyncondition.conditions import synthesis_condition_extraction
from mofsyncondition.conditions import conditions_extraction
from mofsyncondition.conditions import chemical_entity_regex
from mofsyncondition.synparagraph import extract_synthesis_paragraphs
from mofsyncondition.doc import doc_parser
elements_symbols = chemical_entity_regex.all_elements()


def append_json(new_data, filename):
    '''
    append a new data in an existing json file
    '''
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('{}')
    elif os.path.getsize(filename) == 0:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('{}')
    with open(filename, 'r+', encoding='utf-8') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Overwrite existing keys with new_data
        file_data.update(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4, sort_keys=False)

def regex_content(all_tokens, pattern):
    contents = []
    for idx, token in enumerate(all_tokens):
        match = re.search(pattern, token)
        if match:
            if token == 'evaporation' or token == 'Evaporation':
                if 'slow' or 'Slow' in [all_tokens[idx-1], all_tokens[idx-2], all_tokens[idx-3]]:
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

def check_local_html(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            if content:
                print("Local HTML file contains data.")
                return True
            else:
                print("Local HTML file is empty.")
                return False
    except FileNotFoundError:
        print("File not found.")
        return False

def get_refcodes_to_doi(csv_filename):
    """
    Reads a CSV file and returns a dictionary where the keys are Refcodes
    and the values are the corresponding DOI.

    Rows with empty, NaN, or 'None' (case-insensitive) DOIs are excluded.
    """
    # Read the CSV file into a DataFrame
    df = filetyper.load_data(csv_filename)

    # Remove rows with NaN, empty strings, or 'None' (case-insensitive) in the DOI column
    df = df[df['DOI'].notna()]
    df = df[df['DOI'].astype(str).str.strip() != '']
    df = df[df['DOI'].astype(str).str.lower() != 'none']

    # Create a dictionary mapping each Refcode to its DOI.
    # Note: If the same Refcode appears multiple times, the last DOI encountered will be used.
    refcode_to_doi = df.set_index('Refcode')['DOI'].to_dict()

    return refcode_to_doi


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
    all_metals = '|'.join(
        [metal for metal_tuple in metals for metal in metal_tuple])
    multiplicity = chemical_entity_regex.iupac_multiplicity()
    pattern = r'\b'+multiplicity+all_metals+r'\b'
    pattern = re.compile(pattern)

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


def compile_synthesis_condition(html_file):
    """
    Compile synthesis condition
    """
    paragraphs = html_2_text2(html_file)
    _, _, abbreviations =  doc_parser.chemdata_extractor(" ".join(paragraphs))
    synthetic_paragraphs = extract_synthesis_paragraphs.all_synthesis_paragraphs(
        paragraphs)
    all_paragraphs = {}
    chemical_data = {}
    for steps, paragraph in enumerate(synthetic_paragraphs):
        all_paragraphs[steps] = {}
        chemical_data[steps] = {}
        all_paragraphs[steps]['paragraph'] = paragraph
        name_of_chemicals, _, _ = doc_parser.chemdata_extractor(paragraph)
        chemical_names = [i for i in name_of_chemicals if i not in elements_symbols]
        quantities = chemical_entity_regex.extract_chemical_quantities(
            paragraph, chemical_names)

        metal_salt = metal_precursors_in_text(chemical_names)
        mofs = mof_alias_in_text(chemical_names)
        metal_salt = [i for i in metal_salt if i not in mofs]

        all_paragraphs[steps]['paragraph'] = paragraph
        all_paragraphs[steps]['chemicals'] = chemical_names
        all_paragraphs[steps]['abbreviations'] = abbreviations
        all_paragraphs[steps]['quantities'] = quantities
        all_paragraphs[steps]['metal_salt'] = metal_salt
        all_paragraphs[steps]['mofs'] = mofs



        new_quantities = {}
        chemical_names = [abbreviations.get(i, i) for i in chemical_names]
        for name in quantities:
            fix_abbreviation = abbreviations.get(name, name)
            new_quantities[fix_abbreviation] = quantities[name]
        chemical_data[steps]['quantities'] = new_quantities
        solvents = solvents_in_text(chemical_names)
        chemical_data[steps]['solvents'] = solvents

        chemical_data[steps]['metal_salt'] = metal_salt
        chemical_data[steps]['mofs'] = mofs
        chemical_data[steps]['chemicals'] = [i for i in chemical_names if i not in solvents+mofs+metal_salt]
    return chemical_data, all_paragraphs



# path_to_chemicals = os.path.abspath("/Volumes/X9/src/Python/fairmofsyncondition/data/json_data/all_chemical_data.json")
# path_to_paragraphs = os.path.abspath("/Volumes/X9/src/Python/fairmofsyncondition/data/json_data/path_to_paragraphs.json")

refcode_doi = get_refcodes_to_doi("../db/csv/DIO_2021_and_other_properties.csv")

paragraphs_folder = os.path.abspath('/Volumes/X9/src/Python/fairmofsyncondition/data/paragraphs')
chemical_folder = os.path.abspath('/Volumes/X9/src/Python/fairmofsyncondition/data/chemicals')

seen = glob.glob(f"{paragraphs_folder}/*json")
seen = [os.path.basename(i).split('.')[0] for i in seen]
print(seen)

alpha = ["J", "K", "L", "M", "N", "O", "P", "Q", "R"]
# data_chemicals = filetyper.load_data(path_to_chemicals)
# data_paragraphs = filetyper.load_data(path_to_paragraphs)
print('Writing')
# print (len(data_chemicals),  len(data_paragraphs))
# for alp in alpha:
alpha = sys.argv[1]
path_to_html = sorted(glob.glob(os.path.abspath(f'/Volumes/X9/All_HTML/{alpha}*html')))
for html_file in path_to_html:
    data_chemicals = {}
    data_paragraphs = {}
    try:
        refcode = os.path.basename(html_file).split('.')[0]
        if refcode not in seen:
            print(refcode)
            doi = refcode_doi.get(refcode, refcode)
        # if doi not in data_chemicals:
            chemical_data, all_paragraphs = compile_synthesis_condition(html_file)
            if len(chemical_data) > 0:
                data_chemicals[doi] = chemical_data
                data_paragraphs[doi] = all_paragraphs

                path_to_chemicals = os.path.join(chemical_folder, f'{refcode}.json')
                path_to_paragraphs = os.path.join(paragraphs_folder, f'{refcode}.json')
                filetyper.write_json(data_chemicals, path_to_chemicals)
                filetyper.write_json(data_paragraphs ,path_to_paragraphs)
    except Exception as e:
        print(f"Error in {html_file}: {e}")

