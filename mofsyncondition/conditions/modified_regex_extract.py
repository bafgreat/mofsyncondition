#!/usr/bin/python
from __future__ import print_function, unicode_literals
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import re
from rdkit import Chem
from rdkit.Chem import AllChem
import requests

# Constants for external API services
OPCIN_URL = "https://opsin.ch.cam.ac.uk/opsin/"
PUBCHEM_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/property/InChIKey,CanonicalSMILES/JSON"

def check_parentheses(s):
    """
    Check if the parentheses in the string are balanced.

    Args:
        s (str): Input string containing parentheses.

    Returns:
        bool: True if parentheses are balanced, False otherwise.
    """
    stack = []
    for c in s:
        if c == '(':
            stack.append(c)
        elif c == ')':
            if not stack or stack.pop() != '(':
                return False
    return not stack

def find_matching_brackets(s):
    """
    Find and return the locations of matching parentheses, square brackets, and curly brackets in the string.

    Args:
        s (str): Input string containing brackets.

    Returns:
        dict: Dictionary with start and end positions of matching brackets.
    """
    stack = []
    locs = {'()': {}, '[]': {}, '{}': {}}
    pairs = {'(': ')', '[': ']', '{': '}'}
    for i, c in enumerate(s):
        if c in pairs.keys():
            stack.append((c, i))
        elif c in pairs.values():
            if stack:
                opening, pos = stack.pop()
                if pairs[opening] == c:
                    locs[opening + c][pos] = i
    return locs

def remove_unbalanced_brackets(s):
    """
    Remove unbalanced brackets from the string.

    Args:
        s (str): Input string containing brackets.

    Returns:
        str: Modified string with unbalanced brackets removed.
    """
    locs = find_matching_brackets(s)
    valid_indices = set()
    for loc in locs.values():
        valid_indices.update(loc.keys())
        valid_indices.update(loc.values())

    return ''.join(c for i, c in enumerate(s) if i in valid_indices)

def get_chemical_info(name):
    """
    Retrieve chemical information (InChIKey and SMILES) from OPSIN and PubChem.

    Args:
        name (str): The IUPAC name or common name of the chemical.

    Returns:
        dict: Dictionary containing InChIKey and SMILES.
    """
    # Query OPSIN
    opsin_response = requests.get(OPCIN_URL + name + ".json")
    opsin_data = opsin_response.json()

    # Extract SMILES from OPSIN
    smiles = opsin_data.get('smiles', None)

    # Query PubChem if OPSIN fails or SMILES not available
    if not smiles:
        pubchem_response = requests.get(PUBCHEM_URL.format(name))
        pubchem_data = pubchem_response.json()
        try:
            properties = pubchem_data['PropertyTable']['Properties'][0]
            inchi_key = properties.get('InChIKey', None)
            smiles = properties.get('CanonicalSMILES', None)
        except (KeyError, IndexError):
            inchi_key = None
            smiles = None
    else:
        inchi_key = opsin_data.get('inchiKey', None)

    return {'InChIKey': inchi_key, 'SMILES': smiles}

def remove_mu(s):
    """
    Remove Greek letter 'mu' and its variants from the string.

    Args:
        s (str): Input string containing 'mu'.

    Returns:
        str: Modified string with 'mu' removed.
    """
    return re.sub(r'(\u03BC-)|(\u03BC\d-)', '', s)

def find_metals(file_path):
    """
    Generate regex patterns to identify metal ions based on a list from a file.

    Args:
        file_path (str): Path to the file containing metal names.

    Returns:
        str: Regex pattern for matching metal ions.
    """
    with open(file_path, 'r') as file:
        metals = file.read().splitlines()

    patterns = []
    for metal in metals:
        metal = metal.strip().lower()
        patterns.append(f'-{metal}|{metal}\s*')
        for prefix in IUPAC_multiplicity():
            patterns.append(f'-{prefix}{metal}|{prefix}{metal}\s*')

    return '|'.join(patterns)

def check_salt(file_path):
    """
    Generate regex patterns to check if a compound is a salt.

    Args:
        file_path (str): Path to the file containing metal names.

    Returns:
        str: Regex pattern for identifying salts.
    """
    with open(file_path, 'r') as file:
        metals = file.read().splitlines()

    patterns = []
    for metal in metals:
        metal = metal.strip().lower()
        patterns.append(f'^{metal}\s*')
        for prefix in IUPAC_multiplicity():
            patterns.append(f'^{prefix}{metal}\s*')

    return '|'.join(patterns)

def things_to_remove():
    """
    Generate regex patterns to remove unwanted prefixes and suffixes from names.

    Returns:
        str: Regex pattern for removing prefixes and suffixes.
    """
    remove_patterns = ['-aqua$', r'\(hydroxo\)-aqua$', '-hexaoxo$', '^tetrakis\(', '^tris\(', 'bis\(', '']
    for prefix in IUPAC_multiplicity():
        remove_patterns.extend([
            f'^{prefix}\(|', f'^{prefix}-\(|', f'^{prefix}\|', f'-{prefix}$|',
            f'-aqua-{prefix}|', f'-{prefix}-aqua$|'
        ])
    return ''.join(remove_patterns)

def separate_bis():
    """
    Generate regex patterns to handle prefixes and separate them.

    Returns:
        str: Regex pattern for separating prefixes.
    """
    patterns = []
    for prefix in IUPAC_multiplicity()[3:]:
        patterns.append(f'\)-{prefix}|')
    return ''.join(patterns)

def bis():
    """
    Generate regex patterns to remove prefixes at the start of names.

    Returns:
        str: Regex pattern for removing prefixes.
    """
    patterns = []
    for prefix in IUPAC_multiplicity() + ['bis', 'tris']:
        patterns.extend([
            f'^{prefix}\(|', f'^{prefix}\{|', f'^{prefix}\|', f'^{prefix}\(\(|',
            f'{prefix}kis\(|{prefix}kis\{|{prefix}kis\|'
        ])
    return ''.join(patterns)

def nasty_suffix():
    """
    Generate regex patterns to remove unwanted suffixes.

    Returns:
        str: Regex pattern for removing unwanted suffixes.
    """
    suffixes = ["-[npcos]('*?)[\\d*'*)\\s*]$|"]
    for i in range(31):
        suffixes.append(f"[,][npcos]('*?)\\d*\\)*\\s*")
    return ''.join(suffixes)

def correct_metal(name):
    """
    Correct typos in metal names.

    Args:
        name (str): Name of the metal.

    Returns:
        str: Corrected metal name.
    """
    corrections = {
        'trimanganese': '-trimanganese', ')copper': ')-copper',
        ')terbium': ')-terbium', ')dicadmium': ')-cadmium',
        ')cadmium': ')-cadmium', ')diiron': ')-iron',
        ')silver': ')-silver', ')chromium': ')-chromium',
        ')zinc': ')-zinc', ')magnesium': ')-magnesium',
        '[diaquacalcium(ii)]': '-calcium(ii)', 'nan': ''
    }
    for typo, correction in corrections.items():
        if typo in name:
            name = name.replace(typo, correction)
    return name

def correct_linker_name(name, mu):
    """
    Correct linker names based on known patterns.

    Args:
        name (str): Name of the linker.
        mu (list): List of multiplicity terms.

    Returns:
        tuple: Corrected name and other name.
    """
    othername = ''
    aqua_patterns = [r'^aqua-|hydroxo$|aqua$|']
    for prefix in mu + ['bis', 'tris']:
        aqua_patterns.append(f'{prefix}aqua$|{prefix}-aqua$|')

    patterns = {
        'aqua': aqua_patterns,
        'oxo': [f'{prefix}oxo$|{prefix}-oxo$|'],
        'chloro': [f'{prefix}[Cc]hloro$|'],
        'bromo': [f'{prefix}[Bb]romo$|'],
        'fluoro': [f'{prefix}[fF]luoro$|'],
        'iodo': [f'{prefix}[iI]odo$|']
    }

    for key, pat_list in patterns.items():
        for pattern in pat_list:
            if re.search(pattern, name):
                othername = name
                name = re.sub(pattern, '', name)

    if not re.search(r'[^a-zA-Z]\s*$', name):
        name = re.sub('^aqua-', '', name)

    return name, othername

def format_output(output):
    """
    Format the output for printing.

    Args:
        output (dict): Dictionary containing InChIKey and SMILES.

    Returns:
        str: Formatted output string.
    """
    formatted = ""
    for key, value in output.items():
        if value:
            formatted += f"{key}: {value}\n"
    return formatted.strip()

def main():
    """
    Main function to execute the script.

    It handles input and output operations, and manages the overall workflow of processing chemical names.
    """
    import argparse

    parser = argparse.ArgumentParser(description='Process chemical names to extract InChIKey and SMILES.')
    parser.add_argument('input_file', help='Path to the input file containing chemical names.')
    parser.add_argument('output_file', help='Path to the output file for saving results.')

    args = parser.parse_args()

    with open(args.input_file, 'r') as infile, open(args.output_file, 'w') as outfile:
        for line in infile:
            name = line.strip()
            corrected_name = correct_metal(name)
            corrected_name, othername = correct_linker_name(corrected_name, IUPAC_multiplicity())
            info = get_chemical_info(corrected_name)
            formatted_output = format_output(info)
            outfile.write(f"{name}: {formatted_output}\n")
            print(f"{name} processed.")

if __name__ == "__main__":
    main()
