#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import pickle
import csv
import json
import codecs
from zipfile import ZipFile
import numpy as np
import pandas as pd


def numpy_to_json(ndarray, file_name):
    '''
    Serialise a numpy object
    '''
    json.dump(ndarray.tolist(), codecs.open(file_name, 'w',
              encoding='utf-8'), separators=(',', ':'), sort_keys=True)
    return


def list_2_json(list_obj, file_name):
    '''
    write a list to json
    '''
    json.dump(list_obj, codecs.open(file_name, 'w', encoding='utf-8'))

def write_json(json_obj, file_name):
    '''
    write a python dictionary object to json
    '''
    # Serializing json
    json_object = json.dumps(json_obj, indent=4, sort_keys=True)
    with open(file_name, "w", encoding='utf-8') as outfile:
        outfile.write(json_object)

def json_to_numpy(json_file):
    '''
    serialised a numpy array to json
    '''
    json_reader = codecs.open(json_file, 'r', encoding='utf-8').read()
    json_reader = np.array(json.loads(json_reader))
    return read_json


def append_json(new_data, filename):
    '''
    append a new data in an existing json file 
    '''
    with open(filename, 'r+', encoding='utf-8') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.update(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4, sort_keys=True)


def read_json(file_name):
    '''
    load a json file
    '''
    with open(file_name, 'r', encoding='utf-8') as f_obj:
        data = json.load(f_obj)

    return data


def csv_read(csv_file):
    '''
    Read a csv file 
    '''
    f_obj = open(csv_file, 'r', encoding='utf-8')
    data = csv.reader(f_obj)
    return data


def get_contents(filename):
    '''
    Read a file and return a list content
    '''
    with open(filename, 'r', encoding='utf-8') as f_obj:
        contents = f_obj.readlines()
    return contents


def put_contents(filename, output):
    '''
    write a list object into a file
    '''
    with open(filename, 'w', encoding='utf-8') as f_obj:
        f_obj.writelines(output)
    return


def append_contents(filename, output):
    '''
    append contents into a file
    '''
    with open(filename, 'a', encoding='utf-8') as f_obj:
        f_obj.writelines(output)
    return


def save_pickle(model, file_path):
    '''
    write to a pickle file
    '''
    with open(file_path, 'wb') as file:
        pickle.dump(model, file)


def append_pickle(new_data, filename):
    '''
    append to a pickle file
    '''
    with open(filename, 'ab') as f_:
        # append the new data to the file
        pickle.dump(new_data, f_)


def pickle_load(filename):
    '''
    load a pickle file
    '''
    data = open(filename, 'rb')
    data = pickle.load(data)
    return data


def read_zip(zip_file):
    '''
    read a zip file
    '''
    content = ZipFile(zip_file, 'r')
    content.extractall(zip_file)
    content.close()
    return content


def load_data(filename):
    ''' 
    function that recognises file extenion and chooses the correction
    function to load the data.
    '''
    file_ext = filename[filename.rindex('.')+1:]
    if file_ext == 'json':
        data = read_json(filename)
    elif file_ext == 'csv':
        data = pd.read_csv(filename)
    elif file_ext == 'p' or file_ext == 'pkl':
        data = pickle_load(filename)
    elif file_ext == 'xlsx':
        data = pd.read_excel(filename)
    else:
        data = get_contents(filename)
    return data
