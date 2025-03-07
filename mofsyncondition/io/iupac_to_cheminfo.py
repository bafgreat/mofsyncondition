#!/usr/bin/python                                              #
# A script that converts IUPAC name to cheminformatics         #
# like smiles strings, inchi keys and inchi                    #
# This is to faciliate the mapping of chemical names to their  #
# cheminformatic indentifiers                                  #
################################################################


from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import requests
from mofsyncondition.io import filetyper
from mofsyncondition.conditions import chemical_entity_regex
import pubchempy as pcp

import time
def opsin_name_to_smile(chemical_name):
    '''
    Function that uses opsin api to convert iupac names
    to cheminformatic identifiers
    '''
    opsin_url = 'https://opsin.ch.cam.ac.uk/opsin/'
    response = requests.get(opsin_url + chemical_name)
    output = response.json()
    if output['status'] == 'SUCCESS':
        return output
    else:
        return None

def pubchem_to_inchikey(identifier):
    pubchem = pcp.get_compounds(identifier, 'name')
    if len(pubchem) > 0:
        return pubchem[0].inchikey, pubchem[0].canonical_smiles
    else:
        return None



def json_full_search(lookup_key, json_dict, search_result = []):
    if type(json_dict) == dict:
        for key, value in  json_dict.items():
            if key == lookup_key:
                search_result.append(value)
            json_full_search(lookup_key, value, search_result)
    elif type(json_dict) == list:
        for element in json_dict:
            json_full_search(lookup_key, element, search_result)
    return search_result

def write_unique_names():
    organic_reagents = filetyper.load_data(
        '../db/json/curate_organic_reagents.json')
    unique_names = list(set(sum(list(organic_reagents.values()), [])))
    to_write = {}
    to_write['first'] = unique_names
    filetyper.write_json(to_write, '../db/json/unique2_iupac_names.json')

def write_unique_reagent():
    organic_reagents = filetyper.load_data(
        '../db/json/third_synthesis_data.json')
    seen_chemicals = filetyper.load_data(
    '../db/json/unique2_iupac_names.json')
    chemical_name = sorted(seen_chemicals['first'])
    reagents = list(set(sum(json_full_search("mof_organic_linker_reagent", organic_reagents, search_result = []), [])))
    reagents = [i for i in reagents if not i in chemical_name]
    seen_chemicals['second'] = reagents
    print (seen_chemicals)
    filetyper.write_json(seen_chemicals, '../db/json/unique2_iupac_names.json')


def name_to_cheminfo(chemical_names, seen_names):
    """
        Function to convert list names to cheminfo
    """
    chemifo = filetyper.load_data('../db/json/inchi_to_name_and_smile.json')
    chemifo2 = filetyper.load_data('../db/json/inchi_to_cheminformatics.json')
    done = {}
    for name in chemical_names:
        if name not in seen_names:
            try:
                tmp = {}
                tmp2 = {}
                data = opsin_name_to_smile(name)
                if data is not None:
                    print(name)
                    inchikey = data['stdinchikey']
                    tmp['name'] = name
                    tmp['inchikey'] = data['stdinchikey']
                    tmp['smiles'] = data['smiles']
                    tmp2['name'] = name
                    tmp2['inchikey'] = data['stdinchikey']
                    tmp2['smiles'] = data['smiles']
                    tmp2['cml'] = data['cml']
                    tmp2['stdinchi'] = data['stdinchi']
                    if len(tmp) > 0:
                        chemifo[inchikey] = tmp
                        filetyper.write_json(
                            chemifo, '../db/json/inchi_to_name_and_smile.json')
                    if len(tmp2) > 0:
                        chemifo2[inchikey] = tmp2
                        filetyper.write_json(
                            chemifo2, '../db/json/inchi_to_cheminformatics.json')
                    seen_names.append(name)
                    done['seen'] = seen_names
                filetyper.append_json(done, 'seen_names.json')
            except:
                pass


def name_to_cheminfo2(chemical_names, seen_names):
    """
        Function to convert list names to cheminfo
    """
    chemifo = filetyper.load_data('../db/json/chemical_name_to_inchi.json')
    done = {}
    for name in chemical_names:
        if name not in seen_names:
            try:
                tmp = {}
                print(name)
                data = opsin_name_to_smile(name)
                if data is not None:
                    print(name)
                    tmp['inchikey'] = data['stdinchikey']
                    tmp['smiles'] = data['smiles']
                else:
                    data = pubchem_to_inchikey(name)
                    if data is not None:
                        tmp['inchikey'] = data[0]
                        tmp['smiles'] = data[1]
                if len(tmp) > 0:
                    chemifo[name] = tmp
                    filetyper.write_json(
                        chemifo, '../db/json/chemical_name_to_inchi.json')
                    seen_names.append(name)
                    done['seen'] = seen_names
                filetyper.append_json(done, 'seen_names2.json')
            except:
                pass


def solvents_to_inchi_smile():
    solvent_chem = filetyper.load_data('../db/json/solvent_to_inchi_and_smile.json')
    solvents_list = chemical_entity_regex.solvent_chemical_names()
    for solvent in solvents_list:
        tmp = {}
        data = opsin_name_to_smile(solvent)
        if data is not None:
            tmp['inchikey'] = data['stdinchikey']
            tmp['smiles'] = data['smiles']
        else:
            data = pubchem_to_inchikey(solvent)
            if data is not None:
                tmp['inchikey'] = data[0]
                tmp['smiles'] = data[1]
        if len(tmp)> 0:
            solvent_chem[solvent]=tmp
        filetyper.write_json(solvent_chem, '../db/json/solvent_to_inchi_and_smile.json')
    return





def organic_chemicals():
    all_chemical


    # write_unique_names()
    # chemical_name1 = sorted(filetyper.load_data(
    #     '../db/json/unique2_iupac_names.json')['first'])

    # chemical_names = sorted(filetyper.load_data(
    #     '../db/json/unique2_iupac_names.json')['second'])
    # seen_names = sorted(filetyper.load_data('seen_names2.json')['seen'])
    # name_to_cheminfo2(chemical_names, seen_names)


    # name_to_cheminfo2(chemical_name1, seen_names)
    # name_to_cheminfo2(chemical_name2, seen_names)
    # write_unique_reagent()
    # write_unique_names()



# solvents_to_inchi_smile()
# organic_reagents = filetyper.load_data('../db/json/Organic_reagents2.json')
# chemical_names = list(set(sum(list(organic_reagents.values()), [])))
# seen_names = sorted(filetyper.load_data('seen_names2.json')['seen'])
# name_to_cheminfo2(chemical_names, seen_names)

organic_chemicals()