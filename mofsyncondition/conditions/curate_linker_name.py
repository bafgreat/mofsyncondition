#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import os
import re
import glob
import cirpy
import requests
from mofsyncondition.conditions import chemical_entity_regex
from mofsyncondition.doc import doc_parser
from mofsyncondition.io import filetyper
import pubchempy as pcp

def opsin_name_to_smile(chemical_name, key_type):
    opsin_url = 'https://opsin.ch.cam.ac.uk/opsin/'
    response = requests.get(opsin_url + chemical_name)
    smiles = response.json()
    if key_type in list(smiles.keys()):
        return smiles[key_type]
    else:
        return None

def pubchem_to_inchikey(identifier):
    pubchem = pcp.get_compounds(identifier, 'name')
    if len(pubchem) > 0:
        return pubchem[0].inchikey, pubchem[0].canonical_smiles
    else:
        return None

def cheminfor (chemical_name):
    value = opsin_name_to_smile(chemical_name, 'inchikey')
    if value is not None:
        return value
    else:
        value = pubchem_to_inchikey(chemical_name)
        if value is not None:
            return value


def index_data(refcode, data):
    if isinstance(data, dict):
        return data[refcode]
    else:
        return data.loc[data['Refcode'] == refcode]


def _multiplicity():
    mult = ['mono', 'di', 'tri', 'tetra', 'penta', 'hexa', 'hepta', 'octa', 'nona',
            'deca', 'undeca', 'dodeca', 'trideca', 'tetradeca', 'pentadeca', 'hexadeca', 'heptadeca',
            'octadeca', 'nonadeca', 'icosa', 'cosa', 'henicosa', 'docoasa', 'tricosa', 'tetracosa', 'pentacosa',
            'hexacosa', 'heptacosa', 'octacosa', 'nonacosa']
    return mult

def compute_lcs(string_1, string_2):
    len_string_1 = len(string_1)
    len_string_2 = len(string_2)
    n_array = [[0 for i in range(len_string_2+1)]
               for j in range(len_string_1+1)]
    for i in range(1, len_string_1+1):
        for j in range(1, len_string_2+1):
            if string_1[i-1] == string_2[j-1]:
                n_array[i][j] = n_array[i-1][j-1]+1
            else:
                n_array[i][j] = max(n_array[i-1][j], n_array[i][j-1])
    return n_array[len_string_1][len_string_2]

def remove_metal(word):
    metals = chemical_entity_regex.metal_atom_dic()
    name = list(metals.keys()) + list(metals.value())
    pattern = r'\b('+'|'.join(name) + r')\b'
    # if re.search(pattern, word, re.IGNORECASE):

def correct_name(word):
    if isinstance(word, tuple):
        word = word[0]

    if re.findall(r'trate-?', word, re.IGNORECASE):
        group = re.finditer(r'trate-?', word, re.IGNORECASE)
        spans = [i.span() for i in group]
        span = spans[-1][0]
        word = word[:span]+'taric acid'
    elif re.findall(r'dato-?', word, re.IGNORECASE):
        group = re.finditer(r'dato-?', word, re.IGNORECASE)
        spans = [i.span() for i in group]
        span = spans[-1][0]
        word = word[:span]+'nic acid'
    elif re.findall(r'(?!water)\w+ate|ato-?', word, re.IGNORECASE):
        group = re.finditer(r'ate|ato-?', word, re.IGNORECASE)
        spans = [i.span() for i in group]
        span = spans[-1][0]
        word = word[:span]+'ic acid'
    elif re.search('-?isonico', word, re.IGNORECASE):
        word = 'isonicotinic acid'
    elif word == 'bipyridyl':
        word = "2,2'-bipyridine"
    return word

def to_remove():
    mult = _multiplicity()
    remove = ['water', 'oxo', 'oxide', 'cyano', 'γ-pentakis(oxo)', '', 'deca', '(chloro)',
              'methoxy', 'methanol', 'tetracyanic acid', 'bromo', 'floro', 'iodo', 'chloro',
              '2-oxide', 'carbonyl', 'ammine', '4-oxide', '5-oxide', 'hydroxy', 'ethanol', 'nico',  'deuterium oxide',
              '+-', 'cyano', 'chloro-oxo', 'conta', 'trans-cyano', 'trans', 'cis', 'hemikis']
    return remove + mult


def get_metals():
    metals = chemical_entity_regex.metal_atom_dic()
    metal_list = list(metals.keys()) + list(metals.values())
    return metal_list
