#!/usr/bin/python
from __future__ import print_function, unicode_literals
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import re

# https://opsin.ch.cam.ac.uk


def check_parentheses(s):
    """ Return True if the parentheses in string s match, otherwise False. """
    j = 0
    for c in s:
        if c == ')':
            j -= 1
            if j < 0:
                return False
        elif c == '(':
            j += 1
    return j == 0


def IUPAC_multiplicity():
    mult = ['mono', 'di', 'tri', 'tetra', 'penta', 'hexa', 'hepta', 'octa', 'nona',
            'deca', 'undeca', 'dodeca', 'trideca', 'tetradeca', 'pentadeca', 'hexadeca', 'heptadeca',
            'octadeca', 'nonadeca', 'icosa', 'cosa', 'henicosa', 'docoasa', 'tricosa', 'tetracosa', 'pentacosa',
            'hexacosa', 'heptacosa', 'octacosa', 'nonacosa']
    return mult


def find_parentheses(s):
    """ Find and return the location of the matching parentheses pairs in s.
    https://scipython.com/blog/parenthesis-matching-in-python/ 
    Given a string, s, return a dictionary of start: end pairs giving the
    indexes of the matching parentheses in s. Suitable exceptions are
    raised if s contains unbalanced parentheses.

    """
    # The indexes of the open parentheses are stored in a stack, implemented
    # as a list
    stack = []
    unclosed = []
    parentheses_locs = {}
    for i, c in enumerate(s):
        if c == '(':
            stack.append(i)
        elif c == ')':
            try:
                parentheses_locs[stack.pop()] = i
            except:
                unclosed.append(i)
    return parentheses_locs


def find_curl_brackets(s):
    """ Find and return the location of the matching parentheses pairs in s.
    https://scipython.com/blog/parenthesis-matching-in-python/ 
    Given a string, s, return a dictionary of start: end pairs giving the
    indexes of the matching parentheses in s. Suitable exceptions are
    raised if s contains unbalanced parentheses.

    """
    # The indexes of the open parentheses are stored in a stack, implemented
    # as a list
    stack = []
    parentheses_locs = {}
    unclosed = []
    for i, c in enumerate(s):
        if c == '{':
            stack.append(i)
        elif c == '}':
            try:
                parentheses_locs[stack.pop()] = i
            except IndexError:
                unclosed.append(i)
    return parentheses_locs


def find_square_brackets(s):
    """ Find and return the location of the matching parentheses pairs in s.
    https://scipython.com/blog/parenthesis-matching-in-python/ 
    Given a string, s, return a dictionary of start: end pairs giving the
    indexes of the matching parentheses in s. Suitable exceptions are
    raised if s contains unbalanced parentheses.

    """
    # The indexes of the open parentheses are stored in a stack, implemented
    # as a list
    stack = []
    parentheses_locs = {}
    unclosed = []
    for i, c in enumerate(s):
        if c == '[':
            stack.append(i)
        elif c == ']':
            try:
                parentheses_locs[stack.pop()] = i
            except IndexError:
                unclosed.append(i)
    return parentheses_locs


def Remove_unclosed_brackets(s):
    """
    A simple algorithm to remove unbalanced brackets
    Algorithm
    1) Search for all balanced brackets
    2) Seacrh for all bra and kets
    3) loop through the list of bra and kets and find indices that are not present in the 
    list of all balanced brackets
    4) Remove all characters at the identified indices
    """
    new_list_1 = list(find_parentheses(s).keys()) + \
        list(find_parentheses(s).values())
    new_list_2 = list(find_square_brackets(s).keys()) + \
        list(find_square_brackets(s).values())
    new_list_3 = list(find_square_brackets(s).keys()) + \
        list(find_square_brackets(s).values())
    All_brackets = new_list_1 + new_list_2 + new_list_3
    brackets = [i for i in range(len(s)) if s[i] == '(' or s[i] == ')' or s[i]
                == '{' or s[i] == '}' or s[i] == '[' or s[i] == '}']
    To_remove = [i for i in brackets if not i in All_brackets]
    new_list = list(s)
    for i, c in enumerate(new_list):
        if i in To_remove:
            new_list[i] = ''
    new_list = ''.join(new_list)
    return new_list


def Remove_mu(s):
    '''
    Remove all mu in names
    '''
    all_span = []
    mu = re.finditer('(\u03BC-)|(\u03BC\d-)', s)
    for val in mu:
        all_span.extend(list(range(val.span()[0], val.span()[1])))
    new_string = list(s)
    for i, c in enumerate(new_string):
        if i in all_span:
            new_string[i] = ''
    new_string = ''.join(new_string)
    return new_string


def find_metals():
    '''
    Runs through the list of metals name found in ../data/Files/metals.txt and write regex
    parsers to identify the metal part of iupac name. 
    In coordination chemistry the IUPAC name follows the following standard
    [(Organinc ligand)(metal ions)] (guests, or ions if it is a coordination salt)
    To extract organic ligands, it is important to identify the metal ions since the organic 
    linkers come prior to the metal ions. 
    '''
    contents = File_typer.get_contents('../data/Files/metals.txt')
    metal = []
    mult = IUPAC_multiplicity()
    for metals in contents:
        metal.append('-'+metals.strip().lower()+'|')
        metal.append(metals.strip().lower()+'\s*|')
        for prefix in mult:
            metal.append('-'+prefix+metals.strip().lower()+'|')
    tin = []
    for i in mult:
        tin.append('-'+prefix+'-' + i.strip().lower()+'|')
        metal.append('-'+prefix+i.strip().lower()+'|')

    metal = metal+tin
    metal = ''.join(metal)
    return metal[:-1]


def Check_salt():
    '''
    It is important to check whether the coordination compound is a salt or not. 
    If it is a salt, we perform some simple checks in order to identify the correct metal ions
    '''
    contents = File_typer.get_contents('../data/Files/metals.txt')
    metal = []
    mult_1 = IUPAC_multiplicity()
    mult = [i.capitalize() for i in mult_1]+mult_1
    for metals in contents:
        metal.append('^'+metals.strip()+'\s|')
        metal.append('^'+metals.strip().lower()+'\s|')
        metal.append('^([cC]atena-*[\(\{\[]*)*' + metals.strip()+'\s|')
        metal.append('^([cC]atena-*[\(\{\[]*)*' + metals.strip().lower()+'\s|')
        for prefix in mult:
            metal.append(
                '^([cC]atena-*[\(\{\[]*)*'+prefix+metals.strip()+'\s|')
            metal.append(
                '^([cC]atena-*[\(\{\[]*)*'+prefix+metals.strip().lower()+'\s|')
            metal.append(
                '^([cC]atena-*[\(\{\[]*)*' + prefix+'-' + metals.strip() + '\s|')
            metal.append(
                '^([cC]atena-*[\(\{\[]*)*' + prefix+'-' + metals.strip().lower() + '\s|')
            metal.append(
                '^([cC]atena-*[\(\{\[]*)*' + prefix+'-*(.*?)-*' + metals.strip() + '\s|')
            metal.append(
                '^([cC]atena-*[\(\{\[]*)*' + prefix+'-*(.*?)-*' + metals.strip().lower() + '\s|')
    metal = ''.join(metal)
    return metal[:-1]


def Things_to_remove():
    '''
    There are lots of junks in the name which should be remove.
    Here, we filter out all what is considered junks like 
    prefixes and suffixes
    '''
    Remove = ['-aqua$|\(hydroxo\)-aqua$|-hexaoxo$|^tetrakis\(|^tris\(|bis\(|']
    mul = IUPAC_multiplicity()
    bis = [kis+'kis' for kis in mul[3:]]+['bis', 'tris']
    mult = bis+mul
    for prefix in mult:
        Remove.append('^'+prefix+'\(|')
        Remove.append('^'+prefix+'-\(|')
        Remove.append('^'+prefix+'|')
        Remove.append('-'+prefix+'$|')
        Remove.append('-'+prefix+'aqua$|')
        Remove.append('-aqua$|')
        Remove.append('-aqua-'+prefix+'|')
        for pre2 in mult:
            Remove.append('-'+prefix+'aqua-'+pre2+'$|')
            Remove.append('-'+prefix+'-aqua-'+pre2+'$|')
            Remove.append('^'+prefix+pre2+'|')
    Remove = ''.join(Remove)
    return Remove[:-1]


def Separate_bis():
    '''
    Seperate everything that has a prefix 
    '''
    Separate = []
    mult = IUPAC_multiplicity()+['bis', 'tris']
    for prefix in mult:
        Separate.append('\)-'+prefix+'|')
        for kis in mult[3:-2]:
            Separate.append("(\)-" + kis+'kis)|')
    Separate = ''.join(Separate)
    return Separate[:-1]


def Bis():
    '''
    Remove prefixes at the start of names 
    '''
    Separate = []
    mult = IUPAC_multiplicity()
    bis = [kis+'kis' for kis in mult[3:]]+['bis', 'tris']
    for prefix in bis+mult:
        Separate.append('^'+prefix+'\(|')
        Separate.append('^'+prefix+'\{|')
        Separate.append('^'+prefix+'\|')
        Separate.append('^'+prefix+'\(\(|')
        for kis in bis:
            Separate.append("^" + kis+'\('+prefix+'\(|')
            Separate.append("^" + kis+'\('+prefix+'\[|')
            Separate.append("^" + kis+'\('+prefix+'\{|')
            Separate.append("^" + kis+'\{'+prefix+'\(|')
            Separate.append("^" + kis+'\{'+prefix+'\[|')
            Separate.append("^" + kis+'\{'+prefix+'\{|')
            Separate.append("^" + kis+'\['+prefix+'\{|')
            Separate.append("^" + kis+'\['+prefix+'\(|')
            Separate.append("^" + kis+'\['+prefix+'\[|')
    Separate = ''.join(Separate)
    return Separate[:-1]


def Nasty_suffix():
    '''
    Some names have some nasty suffixes like 
    -N,N; -O, O''
    We try to clean this out as much as possibe; 
    '''
    Suffix = ["-[npcos]('*?)[\d*'*\)*\s*]$|"]
    i = 0
    temp = ["-[npcos]('*?)\d*"]
    while i < 31:
        temp.append("[,][npcos]('*?)\d*\)*\s*")
        value = ''.join(temp+['$|'])
        Suffix.append(value)
        i += 1
    Suffix = ''.join(Suffix)[:-1]
    return Suffix


def Correct_metal(name):
    '''
    There are some typos in the name of metals. 
    This function coorects these typos
    '''
    if type(name) is str:
        if 'trimanganese' in name:
            name.replace('trimanganese', '-trimanganese')
        elif ')copper' in name:
            name.replace(')copper', ')-copper')
        elif ')terbium' in name:
            name.replace(')terbium', ')-terbium')
        elif ')dicadmium' in name:
            name.replace(')dicadmium', ')-cadmium')
        elif ')cadmium' in name:
            name.replace(')cadmium', ')-cadmium')
        elif '\)diiron' in name:
            name.replace(')diiron', ')-iron')
        elif ')silver' in name:
            name.replace(')silver', ')-silver')
        elif ')chromium' in name:
            name.replace(')chromium', ')-chromium')
        elif ')zinc' in name:
            name.replace(')zinc', ')-zinc')
        elif ')magnesium' in name:
            name.replace(')magnesium', ')-magnesium')
        elif '[diaquacalcium(ii)]' in name:
            name.replace('[diaquacalcium(ii)]', '-calcium(ii)')
        elif name == 'nan':
            pass
    else:
        pass
    return name


def Correct_linker_name(name, mu):
    '''
    Perform some changes in the name of the linkers
    '''
    othername = ''
    aqua_2 = [
        '^aqua-|hydroxo$|aqua$|\(hydroxo\)-aqua$|bishydroxo$|trishydroxo$|bis-hydroxo$|tris-hydroxo$|diaqua$|di-aqua$']
    oxo_2 = []
    chloro_2 = ['(\([Cc]hloro\)$)|[Cc]hloro$|']
    bromo_2 = ['\([Bb]romo\)$|[Bb]romo$|']
    fluoro_2 = ['\(*[fF]luoro$\)*|\(*[fF]loro\)*$|[fF]luoro$|[fF]loro$|']
    iodo_2 = ['\(*[iI]odo\)*$|']
    for i in ['bis', 'tris', 'tetrakis']+mu:
        aqua_2.append(i+'aqua$|'+i+'-aqua$|'+i+'hydroxo$|'+i +
                      'kishydroxo$|'+i+'kis-hydroxo$|hyroxo$|')
        aqua_2.append('[^\(]aqua-|^aqua'+i+'|' +
                      '^hydroxo'+i+'|'+'^hydroxo'+i+'|')
        oxo_2.append(i+'oxo$|'+i+'-oxo$|'+i+'kis-oxo$|'+i+'kisoxo$|')
        chloro_2.append(i+'[Cc]hloro$|'+i+'kis[Cc]hloro$|' +
                        i+'-[Cc]hloro$|'+i+'kis-[Cc]hloro$|')
        bromo_2.append(i+'[bB]romo$|'+i+'kis[bB]romo$|' +
                       i+'-[Bb]romo$|'+i+'kis-[Bb]romo$|')
        fluoro_2.append(i+'[fF]luoro$|'+i+'kis[fF]luoro$|'+i+'[fF]luoro$|'+i+'kis-[fF]luoro$|' +
                        i+'[fF]loro$|'+i+'kis[fF]loro$|'+i+'[fF]loro$|'+i+'kis-[fF]loro$|')
        iodo_2.append(i+'[iI]odo$|'+i+'kis[iI]odo$|' +
                      i+'-[iI]odo$|'+i+'kis-[iI]odo$|')
        for j in mu+['bis', 'tris']:
            aqua_value = i+j+'aqua$|'+i+j+'-aqua$|'+i+'-'+j+'aqua$|'+i+'kis'+j+'aqua$|'+i+'kis'+j+'-aqua$|'+i+j+'kisaqua$|'+i+j + \
                'kis-aqua$|'+i+'aqua-'+j+'$|'+i+'-aqua-'+j+'$|'+i+j+'-aqua-' + \
                j+'$|'+i+j+'kis-aqua-'+j+'$|'+i+'kis'+j+'-aqua-'+j+'$|'
            aqua_2.append(aqua_value)
            oxo_value = i+j+'oxo$|'+i+j+'-oxo$|'+i+'-'+j+'oxo$|'+i+'kis' + \
                j+'oxo$|'+i+'kis'+j+'-oxo$|'+i+j+'kisoxo$|'+i+j+'kis-oxo$|'
            oxo_2.append(oxo_value)
    aqua = ''.join(aqua_2)[:-1]
    oxo = ''.join(oxo_2)[:-1]
    chloro = ''.join(chloro_2)[:-1]
    bromo = ''.join(bromo_2)[:-1]
    fluoro = ''.join(fluoro_2)[:-1]
    iodo = ''.join(iodo_2)[:-1]
    if re.search('(...)-[iI]odo$', name):
        span = re.search('-[Ii]odo$', name).span()[0]
        new_name = name[:span]
    elif re.search('(...)-[bB]romo$', name):
        span = re.search('-[bB]romo$', name).span()[0]
        new_name = name[:span]
    elif re.search('(...)-[cC]hloro$', name):
        span = re.search('-[cC]hloro$', name).span()[0]
        new_name = name[:span]
    elif re.search('(...)-[fF]loro$|[fF]luoro\$', name):
        span = re.search('-[fF]loro$|[fF]luoro$', name).span()[0]
        new_name = name[:span]
    elif re.search(aqua, name):
        span = re.search(aqua, name).span()
        new_name = 'water'
        othername = name[:span[0]]+name[span[1]:]
    elif re.search(oxo, name):
        new_name = 'oxo'
    elif re.search(fluoro, name):
        new_name = 'hydrogen floride'
    elif re.search(chloro, name):
        new_name = 'hydrogen chloride'
    elif re.search(bromo, name):
        new_name = 'hydrogen bromide'
    elif re.search(iodo, name):
        new_name = 'hydrogen iodide'
    elif 'methoxo' in name:
        new_name = name.replace('methoxo', 'methoxy')
    elif re.search('zoato',  name):
        span = re.search('zoato',  name).span()
        new_name = name[:span[0]] + 'zoic acid'
    elif re.search('pivalyloxo|pivalyl|pivaloyl|pivaloylato|pivalato',  name.lower()):
        span = re.search(
            'pivalyloxo|pivalyl|pivaloyl|pivaloylato|pivalato',  name.lower()).span()
        new_name = name[:span[0]] + 'pivalic acid'
    else:
        new_name = name
    return new_name, othername


def fix_name(metal_extract):
    '''
    The names of some metals have typos.
    We deal with this by writing finding this typos and correcting them. 
    '''
    if 'bairium' in metal_extract:
        metal_extract.replace('bairium', 'barium')
    elif 'abrium' in metal_extract:
        metal_extract.replace('abrium', 'barium')
    elif 'zirconiun' in metal_extract:
        metal_extract.replace('zirconiun', 'zirconium')
    elif 'zirconinum' in metal_extract:
        metal_extract.replace('zirconinum', 'zirconium')
    elif 'Neodmium' in metal_extract:
        metal_extract.replace('neodmium', 'neodymium')
    elif 'siler' in metal_extract:
        metal_extract.replace('siler', 'silver')
    elif 'cadmiu' in metal_extract:
        metal_extract.replace('cadmiu', 'cadmium')
    elif 'sodmium' in metal_extract:
        metal_extract.replace('sodmium', 'sodium')
    elif 'praseodimium' in metal_extract:
        metal_extract.replace('praseodimium', 'praseodymium')
    elif 'laed' in metal_extract:
        metal_extract.replace('laed', 'lead')
    elif 'stontium' in metal_extract:
        metal_extract.replace('stontium', 'strontium')
    elif 'magneium' in metal_extract:
        metal_extract.replace('magneium', 'magnesium')
    elif 'praseodimium' in metal_extract:
        metal_extract.replace('praseodimium', 'praseodymium')
    elif 'potaasium' in metal_extract:
        metal_extract.replace('potaasium', 'potassium')
    elif 'siliver' in metal_extract:
        metal_extract.replace('siliver', 'silver')
    elif 'zirconim' in metal_extract:
        metal_extract.replace('zirconim', 'zirconium')
    elif 'bismiuth' in metal_extract:
        metal_extract.replace('bismiuth', 'bismuth')
    elif 'ytterbum' in metal_extract:
        metal_extract.replace('ytterbum', 'ytterbium')
    elif 'zirconiuum' in metal_extract:
        metal_extract.replace('zirconiuum', 'zirconium')
    elif 'lathanum' in metal_extract:
        metal_extract.replace('lathanum', 'lanthanum')
    elif 'dypsrosium' in metal_extract:
        metal_extract.replace('dypsrosium', 'dysprosium')
    return metal_extract


def Final_curate(word_fragement, bis_seperate, bis_bracket, To_remove, all_mult, Suffix):
    '''
    Perform the final cleaning of the MOFs. This is the slowest part of the script 
    because it does a lot of loops. 

    Need to figure out a means to reduce the number of loops. 
    '''
    ligand_name = []
    second_curate = []
    for words in word_fragement:
        if len(re.findall(bis_seperate, words)) > 0:
            dash = re.finditer(bis_seperate, words)
            temp = [0]
            for i in dash:
                temp.append(i.span()[0]+1)
            ligand = [words[i:j] for i, j in zip(temp, temp[1:]+[None])]
            for word in ligand:
                if word.startswith('-'):
                    ligand_name.append(word[1:])
                else:
                    ligand_name.append(word)
        else:
            ligand_name.append(words)
    for i, words in enumerate(ligand_name):
        if len(re.findall(Suffix, words.lower())) > 0:
            temp = []
            suffix = re.finditer(Suffix, words.lower())
            for index in suffix:
                temp.extend(range(index.span()[0], index.span()[1]))
            list_value = list(words)
            for j, c in enumerate(list_value):
                if j in temp:
                    list_value[j] = ''
            ligand_name[i] = ''.join(list_value)
    for i,  words in enumerate(ligand_name):
        if re.search(bis_bracket, words.lower()):
            span = re.search(bis_bracket, words.lower()).span()
            str_val = words[span[1]:]
            if str_val.endswith(')'):
                str_val = str_val[:-1]
                ligand_name[i] = str_val
    for i, words in enumerate(ligand_name):
        if (words.startswith('(') or words.startswith('{') or words.startswith('[')) and (words.endswith(')') or words.endswith('}') or words.endswith(']')):
            ligand_name[i] = words[1:-1]
    for i, value in enumerate(ligand_name):
        new_string = Remove_mu(value)
        ligand_name[i] = new_string
    for i, value in enumerate(ligand_name):
        if len(re.findall(To_remove, value.lower())) > 0:
            tmp = []
            unwanted = re.finditer(To_remove, value.lower())
            for index in unwanted:
                try:
                    ne = value[index.span()[1]]+value[index.span()[1]+1]
                    one = value[index.span()[1]]+value[index.span()
                                                       [1]+1]+value[index.span()[1]+2]
                    tyl = value[index.span()[1]]+value[index.span()
                                                       [1]+1]+value[index.span()[1]+2]
                    if ne != 'ne' and one != 'one' and tyl != 'tyl':
                        tmp.extend(range(index.span()[0], index.span()[1]))
                except IndexError:
                    tmp.extend(range(index.span()[0], index.span()[1]))
            list_value = list(value)
            for j, c in enumerate(list_value):
                if j in tmp:
                    list_value[j] = ''
            ligand_name[i] = ''.join(list_value)
    for i, value in enumerate(ligand_name):
        if re.findall('(ato)|(ido)|phito', value):
            if re.search('sulfato', value.lower()):
                span = re.search('sulfato', value.lower()).span()
                ligand_name[i] = value[:span[0]] + 'sulphuric acid'
            elif re.search('phosphonatooxo|phosphonato\)oxo|phosphonato', value.lower()):
                span = re.search(
                    'phosphonatooxo|phosphonato\)oxo|phosphonato', value.lower()).span()
                if re.search('[a-zA-Z]', value[span[1]]):
                    list_value = list(value)
                    list_value[span[1]-1] = 'e'
                    ligand_name[i] = ''.join(list_value)
                else:
                    ligand_name[i] = value[:span[0]] + 'phosphonic acid'
            elif re.search('azido', value.lower()):
                span = re.search('azido', value.lower()).span()
                ligand_name[i] = value[:span[0]] + 'hydrazoic acid'
            elif re.search('sulfido', value.lower()):
                span = re.search('sulfido', value.lower()).span()
                ligand_name[i] = value[:span[0]] + 'hydrogen sulfide'
            elif re.search('hydroxido', value.lower()):
                span = re.search('hydroxido', value.lower()).span()
                ligand_name[i] = value[:span[0]] + 'hydroxide'
            elif re.search('phosphato', value.lower()):
                span = re.search('phosphato', value.lower()).span()
                ligand_name[i] = value[:span[0]] + 'phosphoric acid'
            elif re.search('phosphito', value.lower()):
                span = re.search('phosphito', value.lower()).span()
                ligand_name[i] = value[:span[0]] + 'phosphorous acid'
            elif re.search('tartrato', value.lower()):
                span = re.search('tartrato', value.lower()).span()
                ligand_name[i] = value[:span[0]] + 'tartaric acid'
            elif re.search('oxido', value.lower()):
                span = re.search('oxido', value.lower()).span()
                ligand_name[i] = value[:span[0]] + 'oxide'
            elif re.search('ato-', value) and not re.search('ato-[A-Z]', value):
                span = re.search('ato-',  value).span()
                ligand_name[i] = value[:span[0]] + 'acetyl-'+value[span[1]:]
            elif re.search('acetato', value):
                span = re.search('acetato',  value).span()
                ligand_name[i] = value[:span[0]] + 'acetic acid'
            else:
                ato = re.finditer('(ato)|(ido)|phito', value)
                for val in ato:
                    ligand_name[i] = value[:val.span()[0]]+'ic acid'
    for i, words in enumerate(ligand_name):
        new_word = Remove_unclosed_brackets(words)
        ligand_name[i] = new_word
    for i, words in enumerate(ligand_name):
        if (words.startswith('(') or words.startswith('{') or words.startswith('[')) and (words.endswith(')') or words.endswith('}') or words.endswith(']')):
            ligand_name[i] = words[1:-1]
    for i, words in enumerate(ligand_name):
        new_word, othername = Correct_linker_name(words.lower(), all_mult)
        ligand_name[i] = new_word
        if len(othername) > 0:
            ligand_name.append(othername)
    for i, value in enumerate(ligand_name):
        if value.lower() == 'bromo':
            ligand_name[i] = 'hydrogen bromide'
        elif value.lower() == 'chloro':
            ligand_name[i] = 'hydrogen chloride'
        elif value.lower() == 'iodo':
            ligand_name[i] = 'hydrogen iodide'
        elif value.lower() == 'floro' or value.lower() == 'fluoro':
            ligand_name[i] = 'hydrogen floride'
    for words in ligand_name:
        if not words.lower() in all_mult:
            second_curate.append(words)
    remove_mu = ''.join([m_u + '$|'+'-'+m_u + '$|' +
                        m_u + '-$|' for m_u in all_mult])[:-1]
    for index, words in enumerate(second_curate):
        if re.search(remove_mu, words):
            span = re.search(remove_mu, words).span()
            second_curate[index] = words[:span[0]]
    temp = []
    Final_edit = []
    for value in second_curate:
        if value.lower() not in temp and len(value) != 0:
            if value.startswith('-'):
                value = value[1:]
            Final_edit.append(value)
            temp.append(value.lower())
    return Final_edit


def Find_all_names(name, ref):
    '''
    To extract organic building units,we start by
    1) Searching for the metal in the IUPAC names, 
    since the metal is always suppose to be at the end in the name of coordination complexes. 
    2)Once the metal is found, find all the individual organic linkers that are found before the metal
    Note:
    There are a few names, where the organic linker comes at the start. This is accounted for manually. 
    '''
    Metal = {}
    Failed = []
    name = Correct_metal(name)
    # Check if system is a salt
    if re.search(salt, name):
        salt_span = re.search(salt, name).span()
        name = name[salt_span[1]:]
    try:
        first_cut = re.search(metals,  name).span()[0]
        Non_metal = name[:first_cut]
        metal_extract = name[first_cut+1:].split()[0]
        if re.search('^tinato',  name[first_cut:]):
            Non_metal = Non_metal+'tinato'
        metal_extract = fix_name(metal_extract)
        Metal[ref] = metal_extract
    except:
        pass
        Failed.append(ref+'\n')
    if re.search('([Cc]atena-*[\(\{\{]*)', Non_metal):
        non_metal_span = re.search('([Cc]atena-*[\(\{\{]*)', Non_metal).span()
        Non_metal = Non_metal[non_metal_span[1]:]
    # Removing sqare brackets
    if 'catena-[' in Non_metal:
        Non_metal = Non_metal .split('catena-[')[1]
    if 'catena[' in Non_metal:
        Non_metal = Non_metal .split('catena[')[1]
    if 'catena-bis' in Non_metal:
        Non_metal = Non_metal .split('catena-bis')[1]
    if Non_metal.endswith(')') or Non_metal.endswith('}') or Non_metal.endswith(']'):
        Non_metal = Non_metal[:-1]
    word_fragement = []
    if len(re.findall('(\)-\()', Non_metal)) > 0:
        dash = re.finditer('(\)-\()', Non_metal)
        temp = [0]
        for i in dash:
            temp.append(i.span()[0]+1)
        word_frag = [Non_metal[i:j] for i, j in zip(temp, temp[1:]+[None])]
        for word in word_frag:
            if word.startswith('-'):
                word_fragement.append(word[1:])
            else:
                word_fragement.append(word)
    else:
        word_fragement.append(Non_metal)
    list_of_reagents = Final_curate(
        word_fragement, bis_seperate, bis_bracket, To_remove, all_mult, Suffix)
    return list_of_reagents, Metal, Failed
