#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import re
import spacy
from mofsyncondition.doc import doc_parser


def solvents_regex():
    """
    Regex expression for solvents 
    """
    solvent_list = [
        'THF', 'acetone', 'acetone', 'chloroform' + 'chloroform', 'methanol',
        'pyridine', 'DMSO', 'dimethylsulfoxide',
        'MeOH', 'tetrachloroethane', '2,2,2-Trifluorethanol', 'KOH',
        'tetrachloroethane', '1,1,2,2-tetrachloroethane', 'tetrachloroethane',
        '1-butanol', '1-butylimidazole', '1-cyclohexanol', '1-decanol', '1-heptanol', '1-hexanol',
        '1-octanol', '1-pentanol', '1-phenylethanol', '1-propanol',
        '1-undecanol', '1,1,1-trifluoroethanol', '1,1,1,3,3,3-hexafluoro-2-propanol',
        '1,1,1,3,3,3-hexafluoropropan-2-ol', '1,1,2-trichloroethane', '1,2-c2h4cl2',
        '1,2-dichloroethane', '1,2-dimethoxyethane', '1,2-dimethylbenzene', '1,2-ethanediol',
        '1,2,4-trichlorobenzene', '1,4-dimethylbenzene', '1,4-dioxane',
        '2-(n-morpholino)ethanesulfonic acid', '2-butanol', '2-butanone', '2-me-thf', '2-methf',
        '2-methoxy-2-methylpropane', '2-methyltetrahydrofuran', '2-methylpentane',
        '2-methylpropan-1-ol', '2-methylpropan-2-ol', '2-methyltetrahydrofuran', '2-proh',
        '2-propanol', '2-pyrrolidone', '2,2,2-trifluoroethanol',
        '2,2,4-trimethylpentane', '2Me-THF', '2MeTHF', '3-methyl-pentane',
        '4-methyl-1,3-dioxolan-2-one', 'acetic acid', 'aceto-nitrile', 'acetone',
        'acetonitrile', 'acetononitrile', 'AcOEt', 'AcOH', 'AgNO3', 'aniline', 'anisole',
        'benzonitrile', 'benzylalcohol', 'bromoform', 'Bu2O', 'Bu4NBr', 'Bu4NClO4',
        'Bu4NPF6', 'BuCN', 'BuOH', 'butan-1-ol', 'butan-2-ol', 'butan-2-one', 'butane',
        'butanol', 'butanone', 'butene', 'butylacetonitrile',
        'butylalcohol', 'butyl amine', 'butylchloride', 'butylimidazole',
        'butyronitrile', 'c-hexane', 'carbon disulfide', 'carbon tetrachloride',
        'chlorobenzene', 'chloroform', 'chloromethane', 'chlorotoluene', 'CHX', 'cumene',
        'cyclohexane', 'cyclohexanol', 'cyclopentylmethylether', 'DCE', 'DCM', 'decalin',
        'decan-1-ol', 'decane', 'decanol', 'DEE', 'di-isopropylether',
        'di-n-butyl' + 'ether', 'di-n-hexylether', 'dibromoethane', 'dibutoxymethane',
        'dibutylether', 'dichloro-methane', 'dichlorobenzene', 'dichloroethane',
        'dichloromethane', 'diethoxymethane', 'diethyl' + 'carbonate', 'diethylether',
        'diethylamine', 'diethylether', 'diglyme', 'dihexyl ether', 'diiodomethane',
        'diisopropylether', 'diisopropylamine', 'dimethoxyethane', 'dimethoxymethane',
        'dimethyl' + 'acetamide', 'dimethylacetimide', 'dimethylbenzene',
        'dimethylcarbonate', 'dimethylformamide', 'dimethylsulfoxide', 'dimethylacetamide',
        'dimethylbenzene', 'dimethylformamide', 'dimethylformanide', 'dimethylsulfoxide',
        'dioctylsodium sulfosuccinate', 'dioxane', 'dioxolane', 'dipropylether', 'DMAc',
        'DMF', 'DMSO', 'Et2O', 'EtAc', 'EtAcO', 'EtCN', 'ethane' + 'diol', 'ethane-1,2-diol',
        'ethanol', 'ethyl(S)-2-hydroxypropanoate', 'ethylacetate', 'ethylbenzoate',
        'ethylformate', 'ethyllactate', 'ethylpropionate', 'ethylacetamide',
        'ethylacetate', 'ethylene' + 'carbonate', 'ethyleneglycol', 'ethyleneglycol',
        'ethylhexan-1-ol', 'EtOAc', 'EtOH', 'eucalyptol', 'F3-ethanol', 'F3-EtOH', 'formamide',
        'glycerol', 'H2O', 'H2O2', 'H2SO4', 'HBF4', 'HCl', 'HClO4', 'HCO2H', 'HCONH2',
        'heptan-1-ol', 'heptane', 'heptanol', 'heptene', 'HEX', 'hexadecylamine',
        'hexafluoroisopropanol', 'hexafluoropropanol', 'hexan-1-ol', 'hexane', 'hexanes',
        'hexanol', 'hexene', 'hexyl' + 'ether', 'HFIP', 'HFP', 'HNO3', 'hydrochloric acid',
        'hydrogen peroxide', 'iodobenzene', 'isohexane', 'isooctane', 'isopropanol',
        'isopropylbenzene', 'ligroine', 'limonene', 'Me-THF', 'Me2CO',
        'MeCN', 'MeCO2Et', 'MeNO2', 'MeOH', 'mesitylene', 'methanamide', 'methanol',
        'MeTHF', 'methoxybenzene', 'methoxyethylamine', 'methylacetamide',
        'methylacetoacetate', 'methylbenzene', 'methylbutane',
        'methylcyclohexane', 'methylethylketone', 'methylformamide',
        'methylformate', 'methyl isobutyl ketone', 'methyllaurate',
        'methylmethanoate', 'methylnaphthalene', 'methylpentane',
        'methylpropan-1-ol', 'methylpropan-2-ol', 'methylpropionate',
        'methylpyrrolidin-2-one', 'methylpyrrolidine', 'methylpyrrolidinone',
        'methylt-butylether', 'methyltetrahydrofuran', 'methyl-2-pyrrolidone',
        'methylbenzene', 'methylcyclohexane', 'methylene' + 'chloride', 'methylformamide',
        'methyltetrahydrofuran', 'MIBK', 'morpholine', 'mTHF', 'n-butanol',
        'n-butyl' + 'acetate', 'n-decane', 'n-heptane', 'n-HEX', 'n-hexane', 'n-methylformamide',
        'n-methylpyrrolidone', 'n-nonane', 'n-octanol', 'n-pentane', 'n-propanol',
        'n,n-dimethylacetamide', 'n,n-dimethylformamide', 'N,N-dimethylformamide', 'n,n-DMF',
        'NaOH', 'nBu4NBF4', 'nitric acid',
        'nitrobenzene', 'nitromethane', 'nonane', 'nujol', 'o-dichlorobenzene', 'o-xylene',
        'octan-1-ol', 'octane', 'octanol', 'octene', 'ODCB', 'p-xylene', 'pentan-1-ol', 'pentane',
        'pentanol', 'pentanone', 'pentene', 'PeOH', 'perchloric acid', 'PhCH3', 'PhCl', 'PhCN',
        'phenoxyethanol', 'phenyl acetylene', 'Phenyl ethanol', 'phenylamine',
        'phenylethanolamine', 'phenylmethanol', 'PhMe', 'phosphate',
        'phosphate buffered saline', 'pinane', 'piperidine', 'polytetrafluoroethylene',
        'propan-1-ol', 'propan-2-ol', 'propane', 'propane-1,2-diol', 'propane-1,2,3-triol',
        'propanol', 'propene', 'propionic acid', 'propionitrile',
        'propylacetate', 'propylamine', 'propylene carbonate',
        'propyleneglycol', 'pyridine', 'pyrrolidone', 'quinoline',
        'sodium hydroxide', 'sodium perchlorate', 'sulfuric acid', 't-butanol',
        'tert-butanol', 'tert-butyl alcohol', 'tetrabutylammonium hexafluorophosphate',
        'tetrabutylammonium hydroxide', 'tetrachloroethane', 'tetrachloroethylene',
        'tetrachloromethane', 'tetrafluoroethylene', 'tetrahydrofuran', 'tetralin',
        'tetramethylsilane', 'tetramethylurea', 'tetrapiperidine', 'TFA', 'TFE', 'THF', 'toluene',
        'tri-n-butylphosphate', 'triacetate', 'triacetin', 'tribromomethane',
        'tributyl phosphate', 'trichlorobenzene', 'trichloroethene', 'trichloromethane',
        'triethyl amine', 'triethyl phosphate', 'triethylamine',
        'trifluoroacetic acid', 'trifluoroethanol', 'trimethyl benzene',
        'trimethyl pentane', 'tris', 'undecan-1-ol', 'undecanol', 'valeronitrile', 'water',
        'xylene', 'xylol', 'N,N-diethylformamide',
        '[nBu4N][BF4]', 'BCN', 'ACN', 'BTN', 'BHDC', 'AOT', 'DMA',
        'MOPS',  'MES', 'heavy water', 'IPA',
        'TBP', 'TEA', 'DEF', 'DMA', 'CCl4', 'potassium hydroxide', 'sodium hydroxide',
        'calcium hydroxide', 'methyl pyrrolidinone', 'ethyl lactate',
        'methyl pyrrolidin-2-one', 'benzene', 'C2H4Cl2', 'HEPES', 'EtOD',
        'CH3Ph', 'methyl benzene', 'PBS', 'trifluoroethanol ', 'CDCl3', 'methyl propan-2-ol',
        'ethylene glycol', 'CH3Cl', 'ethane diol', 'TEAP', 'CD3OD', 'propylene glycol', 'C2H5CN',
        'TBAOH', 'methyl propionate', 'methyl laurate', 'Cl2CH2', 'isopropyl benzene', 'CH3SOCH3',
        'CHCl2', 'C2D5CN', '(CH3)2CHOH', 'PrOH', 'glacial acetic acid', 'C5H5N', 'CD3COCD3',
        'butyl chloride', 'CD3SOCD3', 'KBr', 'methyl tetrahydrofuran', 'silver nitrate',
        'dimethyl formamide', 'NMP', 'C7D8', 'C6D6', 'methyl cyclohexane', 'methyl naphthalene',
        'PrCN', 'propyl acetate', 'CH3COCH3', 'di-isopropyl ether', '1-methylethyl acetate',
        'C6H6', 'methyl methanoate', 'benzyl alcohol', 'CH3COOH', 'ethylene carbonate',
        'NaClO4', 'potassium phosphate buffer', 'ethyl (S)-2-hydroxypropanoate', 'dimethyl ether',
        '2-methyl tetrahydrofuran', 'C6H5CH3', 'methyl butane', 'CH3OD', 'CHCl3', '(CDCl2)2',
        'dimethyl carbonate', 'dipropyl ether', 'HFIP,', 'TX-100', 'tri-n-butyl phosphate', 'LiCl',
        'CH3C6H5', 'CH2Cl2', 'di-n-butyl ether', '(CH3)2NCOH', 'n-butyl acetate',
        'dimethyl benzene', 'ClCH2CH2Cl', 'CH3NHCOH', 'diethyl carbonate', 'CH3CN', 'C6H12', 'C7H8',
        'NaCl', 'TBAH', 'NaHCO3', 'dimethyl acetimide', 'TBAP', 'CH3OH', 'butyl imidazole',
        'dioctyl sodium sulfosuccinate', 'potassium bromide', 'butyl acetonitrile', 'TBABF4',
        'diethyl ether', 'methyl ethyl ketone', 'methyl t-butyl ether', 'CH3NO2',
        'propyl amine', 'diisopropyl ether', 'D2O', 'ethyl formate', 'methyl formate',
        'tin dioxide', 'methyl acetamide', 'MCH', 'THF-d8', 'CD3CN', '(CH3)2CO', 'titanium dioxide',
        'ethyl propionate', 'dimethyl acetamide', 'dibutyl ether', 'H2O + TX', 'dimethyl sulfoxide',
        'CD2Cl2', 'methyl pyrrolidine', 'C2H5OH', 'butyl alcohol', 'TEOA', '(CD3)2CO',
        'methylene chloride', 'SDS', 'KPB', 'TBAF', 'ethyl acetate', 'SNO2', 'methyl propan-1-ol',
        'C6H14', 'methyl acetoacetate', 'butyl acetate', 'MeOD', 'hexyl ether',
        'cyclopentyl methyl ether', 'NPA', 'ethyl benzoate', '2-propyl acetate',
        'Na2SO4', 'C6H5Cl', 'methyl formamide', 'CH3CO2H', 'methyl pentane', 'TBAPF6',
        'H2O-Triton X', 'CH2ClCH2Cl', 'sodium chloride', 'Triton X-100', 'HDA',
        'di-n-hexyl ether', 'potassium iodide', 'potassium bromide', 'potassium chloride',
        'potassium floride', 'KI', 'KF', 'KCl', 'KBr' 'sodium iodide', 'sodium bromide',
        'sodium chloride', 'sodium floride', 'NaI', 'NaF', 'NaCl', 'NaBr'
    ]
    solvent_name_options = list(set(solvent_list))
    prefixes = ['iso', 'tert', 'sec', 'ortho', 'meta', 'para', 'meso']
    solvent_re = re.compile(r'(?:^|\b)(?:(?:%s|d\d?\d?|[\dn](?:,[\dn]){0,3}|[imnoptDLRS])-?)?(?:%s)(?:-d\d?\d?)?(?=$|\b)'
                            % ('|'.join(re.escape(s) for s in prefixes),
                               '|'.join(re.escape(s).replace(r'\ ', r'[\s\-]?') for s in solvent_name_options)))
    # solvent_name_reg = "|".join(solvent_name_options)
    # pattern = re.compile(solvent_name_reg)
    return solvent_name_options


def mof_regex():
    re_MOF1 = '^(?![aA-zZ]+\-?\d?\d?\-like)(?![aA-zZ]+\-?\d?\d?\-type(s?))(ZJU|SNU|MAF|MCF|Ir-MOF|JUC|FJI|UHM|MUV|BUT|ZJNU|Tb|she|CTH|pek|FDM|MODF|USF|NJFU|ZJU|CMOF|CTH|TPMOF|IZE|pbz|PNMOF|gea|MFM|UNLPF|PIZOF|soc|MOAAF|Y|Ho|CPO|JLU|aea|NOTT|NU|MMPF|UTSA|CPM|U[iI]O|MOF|IRMOF|T-MOF|NTU|MIL|HKUST|HNUST|LIC|PCN|ZIF|CPL|CALF|UMCM|DUT)[:;\[\]\)\{\}\]{0,3}[\-‐‑⁃‒–—―−－⁻][A-Za-z0-9_-]+[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]*[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]*[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]*[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]+$'
    re_MOF2 = '^(ZJU|SNU|MAF|MCF|Ir-MOF|JUC|FJI|UHM|MUV|BUT|ZJNU|Tb|she|CTH|pek|FDM|MODF|USF|NJFU|ZJU|CMOF|CTH|TPMOF|IZE|pbz|PNMOF|gea|MFM|UNLPF|PIZOF|soc|MOAAF|Y|Ho|CPO|JLU|aea|NOTT|NU|UTSA|MMPF|CPM|U[iI]O|MOF|T-MOF|IRMOF|NTU|MIL|HKUST|HNUST|LIC|PCN|ZIF|CPL|CALF|UMCM|DUT)([\-‐‑⁃‒–—―−－⁻])([a-zA-Z0-9]+)$'
    re_chemical_formula = '^(?![aA-zZ]+\-?\d?\d?\-ligands)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\d\(CO2\)\d?\(?N?N?\)?)(?!^(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\($)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\(CH3COO\)\d\s?\d?H?2?O?)(?!M1)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\dAs\dO\d)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\d\(μ3-OH\)\d\(CO2\)\d)(?!\[?Zn\d\(μ4-O\)\(O2CR?\)\d\])(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\((AcO|OAc)\)\d?\s?H?2?O?)(?!Me\dNH\d)(?!(\[?Zn\dO?\(O2C))(?!^M\(II\))(?!.*\(OOC\)\d$)(?!Co\(Tt\)\d?$)(?!.*\(COO−?\)\d$)(?!(M|Mn|Cu|Zn|Y|Co|Ni|Fe|Zr|Cd)\((II|i|ii|iii)\)$)(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\d?O?\(CO2\)\d\]?$)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\dO?\+?.?.?.?$)(?!UiO-type$)(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\(NO\d?\)\d?\]?.?.?.?.?.?.?.?$)(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\(ClO\d?\)\d?\]?.?.?.?.?.?.?.?$)(?!Cu\(NO\d?\).?.?.?.?.?.?.?.?$)(?!\[Zn3\(EBTC\)2\]∞$)(?!\{?Cu\d\(O2?CR\)\d\}?$)(?!HCl$)(?!Cu\(II\)$)(?!Zr6O8\(CH3COO\)26\+$)(?!Cu\(NO3\)2·3H2O$)(?!Zr6$)(?!Cu\(NO3\)2$)(\[?)(\{)?(\[)?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)(\s?)(L|\d|\(|\-)'
    formular_with_L_and_n = r"\b\w*\d*\((?:L|n|∞)\)\d*\b"
    patterns = "|".join(
        [re_MOF1, re_MOF2, re_chemical_formula, formular_with_L_and_n])
    return re.compile(patterns, flags=0)


def metal_salts_formular():
    base_metal = ['Mg', 'Al', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn',
                  'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Y', 'Zr', 'Nb', 'Mo',
                  'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'Hf', 'Ta', 'W', 'Re', 'Os',
                  'Ir', 'Pt', 'Au', 'Hg', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Rb',
                  'Sr', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd',
                  'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
    prefix = '^'
    suffix = r'(\((?:[IVX]+|\d+)\))?(\w+)\)?(\d*)'
    list_of_formulars = [prefix+metal +
                         suffix for metal in base_metal if metal not in ['Zn']]
    metal_formulars = '|'.join(list_of_formulars)
    full_names = ['[Mm]olybdenum', '[Nn]iobium', '[Yy]ttrium', '[Cc]hromium',
                  '[Ss]candium', '[Nn]ickel', '[Ll]ead',
                  '[Tt]itanium', '[Zz]inc', '[Mm]anganese', '[Vv]anadium',
                  '[Mm]agnesium', '[Cc]opper', '[Ii]ron', '[Ff]errous',
                  '[Aa]lumin(ium|um|o)', '[Cc]admium', '[Zz]irconium',
                  '[Cc]obalt', '[Rr]ubidium', '[Cc]esium',
                  '[Ff]rancium', '[Gg]old', '[Mm]ercury', '[Hh]assium',
                  '[Ii]ridium', '[Os]mium', '[Rr]henium', '[Tt]antalum',
                  '[Hh]afnium', '[Rr]utherfordium', '[Ss]eaborgium',
                  '[Bb]ohrium', '[Bb]arium', '[lL]anthanium', 'Rubidium',
                  '[Yy]ttrium', '[Cc]aesium']
    full_names = '|'.join(full_names)
    name_pattern = r'\b('+full_names+r')\b'
    return metal_formulars+'|'+name_pattern


def synthetic_method_re():
    """
    Match synthetic methods
    """
    list_of_methods = [
        r"\b[Ss]ol\w*thermal(?:ly)?\b",
        r"\b[Hh]\w*thermal(?:ly)?\b",
        r"\b[so]l\w*gel(?:ly)?\b",
        r"\b[Mm]icrowave\w*\b",
        r"\w*onochemical\w*",
        # r"\w*o\w*thermal\w*",
        r"\w*o\w*chemical\w*",
        r"\w*[eE]vaporation",
        r"[Ss]low diffusion",
        r"[Bb]ranched tube",
        r"[Cc]onventional solution casting",
        r'[lL]inker exchange',
        r'[mM]illing'
    ]
    method = '|'.join(list_of_methods)
    return re.compile(method)


def key_words_regex():
    '''
    '''
    crystalization = [r"[Cc]rystal\w*", r'[Gg]rown', '[gG]row\w*']
    stability = [
        r"[sS]tability",
        r"[sS]table",
        r'^no\s\w+(\s\w+)?\sloss$',
        r"no\s+\w*\s+(mass|weight)\s+\w*\s+loss"
    ]
    analysis = [
        r"[eE]lemental analysis\b",
        r"[dD]ry|[dD]rying|[dD]ried|[dD]egassed|[Dd]egas|[Dd]esolvated",
        r'[dD]esolvate|[rR]emove|[rR]emoval',
        r"[tT]hermal gravimetry",
        r"[tT]hermal gravimetric",
        r"[tT]hermogravimetry",
        r"[tT]hermogravimetric",
        r"[tT]hermo-gravimteric",
        r"[tT]hermo-grametric",
        r"[Tt]hermogravi\w*",
        r"[Tt]hermo-gravi\w*",
        r"[Tt]hermal grav\w*",
        r"[Tt]hermo gravimetry"
        r"[aA]nalysis",
        r"[Aa]naly[sz]e",
        r"[eE]xchange+d",
        r'sharp weight loss',
        r'refrigerator',
        r'freezer'
        r'freeze'
        r'cold',
        r'decompose[d]',
        r'chilling',
        r' cooling',
        r'chill',
        r'NMR',


    ]
    stability = re.compile('|'.join(stability))
    analysis = re.compile('|'.join(analysis))
    crystalization = re.compile('|'.join(crystalization))
    return stability,  analysis, crystalization


def method_abbreviation(word):
    """
    Takes an abbreviation and returns a full word. 
    """
    abbreviation = {
        'Microwave': 'Microwave-assisted',
        'Sonochemically': 'Sonochemical',
        'Sovothermally': 'Sovothermal',
        'Electrochemically': 'Electrochemical',
        'Mechanochemically': 'Mechanochemical',
        'Hydrothermally': 'Hydrothermal'
    }
    if word in list(abbreviation.keys()):
        return abbreviation[word]
    else:
        return word


def solvent_abbreviation(word):
    """
    Takes an abbreviation and returns full word. 
    """
    all_abbreviation = {
        'DMSO': 'dimethylsulfoxide',
        'DEF': 'N,N-dimethylformamide',
        'dimethylformamide': 'N,N-dimethylformamide',
        'MeOH': 'methanol',
        'THF': 'tetrahydrofuran',
        'n,n-DMF': 'N,N-dimethylformamide',
        'DMF': 'N,N-dimethylformamide',
        'dimethylformamide': 'N,N-dimethylformamide',
        'TFE': '2,2,2-trifluorethanol',
        'TFA': 'trifluoroacetic acid',
        'TeCA': '1,1,2,2-Tetrachloroethane',
        'TTCE': 'tetrachloroethane',
        'PCE': 'pentachloroethane',
        'HCE': 'hexachloroethane',
        '2Me-THF': '2-methyltetrahydrofuran',
        '2-MTHF': '2-methyltetrahydrofuran',
        'DMAc': 'N,N-dimethylacetamide',
        'dimethylacetamide': 'N,N-dimethylacetamide',
        'DMA': 'dimethylacetamide',
        'H2SO4': 'sulphuric acid',
        'IPA': 'isopropyl alcohol',
        'ACN': 'acetonitril',
        'H2O2': 'hydrogen peroxide',
        'CCl4': 'tetrachloromethane',
        'H2O': 'water',
        '2,6-NDC': '2,6-Naphthalenedicarboxylic acid'
        # 'KOH':'potassium hydroxide'
    }
    if word in list(all_abbreviation.keys()):
        return all_abbreviation[word]
    else:
        return word


def reaction_time_breakdown(react_time, spacy_doc):
    '''
    '''
    drying = []
    stability = []
    reaction_time = []
    crystalization_time = []
    stability_pattern, analysis_pattern, crystalization = key_words_regex()
    for time in react_time:
        seen =[]
        value = time['value']
        units = time['units']
        if time['units'] != 'N/A' and time['value'] not in ['-', '.', '_', '?', '>', '<', ',', ')', '(', '[', ']']:
            word = value+' '+time['units']
        else:
            word = value + ' '
        sentence = sentence_containing_word(spacy_doc, word)
        if sentence != None and value not in seen:
            match = re.search(analysis_pattern, sentence)
            match2 = re.search(stability_pattern, sentence)
            match3 = re.search(crystalization, sentence)
            if match3 and value not in seen:
                time_hrs = convert_time_to_hour(value, units)
                crystalization_time.append(time_hrs)
                seen.append(value)
            elif match and value not in seen:
                time_hrs = convert_time_to_hour(value, units)
                drying.append(time_hrs)
                seen.append(value)
            elif match2 and value not in seen:
                time_hrs = convert_time_to_hour(value, units)
                stability.append(time_hrs)
                seen.append(value)
            else:
                if value not in seen:
                    time_hrs = convert_time_to_hour(value, units)
                    reaction_time.append(time_hrs)
                    seen.append(value)
        
    return reaction_time, stability, drying, crystalization_time


def celsius_2_kelvin(temperature):
    """
    Simple function that converts temperature from celsius 
    to kelvin
    Parameters
    ----------
    temperature: celsius  

    Returns
    -------
    temperature: kelvin
    """
    return float(temperature) + 297.15


def convert_time_to_hour(value, units):
    '''
    Function that takes the output of the reaction time and provide time time in 
    hours 
    '''
    if value in ['-', '.', '_', '?', '>', '<', ',', ')', '(', '[', ']']:
        return ''
    time_hrs = {}
    match = re.search(r'\d+$', value)
    if match:
        value = match.group()
    
    if value == 'overnight':
        time_hrs['value'] = [24]
        time_hrs['flag'] = 'overnight'
    elif units == 'day' or units == 'days' or units == 'd':
        time_hrs['value']= [i*24 for i in numbers_to_digit(value)['value']]
        if len(numbers_to_digit(value)['flag'])> 0:
           time_hrs['flag'] = numbers_to_digit(value)['flag'] +' '+ 'days'
        else:
            time_hrs['flag'] = numbers_to_digit(value)['flag']
    elif units == 'min' or units == 'minutes' or units == 'm':
        time_hrs['value']= [round(i/60.0, 3) for i in numbers_to_digit(value)['value']]
        if len(numbers_to_digit(value)['flag'])> 0:
           time_hrs['flag'] = numbers_to_digit(value)['flag'] +' '+ 'minutes'
        else:
            time_hrs['flag'] = numbers_to_digit(value)['flag']
        # time_hrs = round(numbers_to_digit(value)/60.0, 3)
    else:
        time_hrs['value']= [float(value)]
        time_hrs['flag']= ''
    return time_hrs


def convert_temp_to_kelvin(value, units):
    '''
    Function that takes the output of the reaction time and provide time time in 
    hours 
    '''
    temperature = ''
    if value == '-':
        temperature = ''
    elif value == 'RT':
        temperature = 297.15
    elif units == '°C' or units == 'C':
        temperature = celsius_2_kelvin(value)
    else:
        temperature = float(value)
    return temperature


def reaction_temperature_breakdown(reaction_temperature, spacy_doc):
    '''
    '''
    drying_temp = []
    stability_temp = []
    reaction_temp = []
    melting_temp = []
    crystalization_temp = []
    seen = []
    stability_pattern, analysis_pattern, crystalisation_pattern = key_words_regex()
    for temp in reaction_temperature:
        value = temp['value']
        units = temp['units']
        if units != 'N/A':
            word = value
        elif value == 'RT':
            word = 'room temperature'
        if value not in ['-', '.', '_', '?', '>', '<', ',']:
            sentence = sentence_containing_word(spacy_doc, word)
            if sentence != None and value not in seen:
                melting_points = re.findall(
                    r"(?i)(?:mp~|melting point|mp)\s*(\d+(?:\.\d+)?)(?:\s*-\s*(\d+(?:\.\d+)?))?", sentence)
                melting_points = [
                    i for sub in melting_points for i in sub if i]
                if value in melting_points:
                    temp = convert_temp_to_kelvin(value, units)
                    melting_temp.append(temp)
                    seen.append(value)
                else:
                    match = re.search(analysis_pattern, sentence)
                    match2 = re.search(stability_pattern, sentence)
                    match3 = re.search(crystalisation_pattern, sentence)
                    if match and value not in seen:
                        temp = convert_temp_to_kelvin(value, units)
                        crystalization_temp.append(temp)
                        seen.append(value)
                    elif match and value not in seen:
                        temp = convert_temp_to_kelvin(value, units)
                        drying_temp.append(temp)
                        seen.append(value)
                    elif match2 and value not in seen:
                        temp = convert_temp_to_kelvin(value, units)
                        stability_temp.append(temp)
                        seen.append(value)
                    else:
                        if value not in seen:
                            temp = convert_temp_to_kelvin(value, units)
                            reaction_temp.append(temp)
                            seen.append(value)
    return reaction_temp, stability_temp, drying_temp, melting_temp, crystalization_temp


def numbers_to_digit(string):
    digit_numbers = {
        'one': {'value':[1], 'flag':''},
        'two': {'value':[2],'flag':''},
        'three': {'value':[3],'flag':''},
        'four': {'value':[4], 'flag':''},
        'fours': {'value':[4],'flag':''},
        'five': {'value':[5],'flag':''},
        'fives': {'value':[5],'flag':''},
        'six': {'value':[6],'flag':''},
        'seven': {'value':[7],'flag':''},
        'sevens': {'value':[7],'flag':''},
        'eight': {'value':[8],'flag':''},
        'eights': {'value':[8],'flag':''},
        'nine': {'value':[9],'flag':''},
        'ten': {'value':[10],'flag':''},
        "eleven": {'value':[11],'flag':''},
        "twelve": {'value':[12],'flag':''},
        "thirteen": {'value':[13],'flag':''},
        "fourteen": {'value':[14],'flag':''},
        "fifteen": {'value':[15],'flag':''},
        "sixteen": {'value':[16],'flag':''},
        "seventeen": {'value':[17],'flag':''},
        "eighteen": {'value':[18],'flag':''},
        "nineteen": {'value':[19],'flag':''},
        "twenty": {'value':[20],'flag':''},
        "thirty": {'value':[30],'flag':''},
        "forty": {'value':[40],'flag':''},
        "fifty": {'value':[50],'flag':''},
        "sixty": {'value':[60],'flag':''},
        "seventy": {'value':[70],'flag':''},
        "eighty": {'value':[80],'flag':''},
        "ninety": {'value':[90],'flag':''},
        'or': {'value':[1],'flag':''},
        'few': {'value':[2,3], 'flag':'Few'},
        'several': {'value':[4,5], 'flag':'Several'},
        'half': {'value':[0.5],'flag':''},
        'some': {'value':[3,4], 'flag':'Some'},
        'many': {'value':[7, 14], 'flag':'Many'},# for many days
        'next': {'value':[1,2], 'flag':'Next'},
        'for': {'value':[3,4], 'flag':'For'},
        'of': {'value':[3, 4], 'flag': 'Period of'},
        'different': {'value':[1,2], 'flag':'Different'},
        'successive': {'value':[1,2],'flag':'Successive'},
        'additional': {'value':[1,2], 'flag':'Additional'},
        'within': {'value':[2,3], 'flag':'Within'},
        'after': {'value':[3,4], 'flag':'After'},  # Yellow crystals of [Hg (CH2COCH3)(4-NO2pcyd)]n were grown after days
        'following': {'value':[1,2],'flag':'Following'},  # 3 disappeared in the following days
        'in': {'value':[7,14], 'flag':'In days to weeks'},  # Crystals were observed to lose solvent slowly and decompose in days to weeks when
        'over': {'value':[4,5] ,'flag':'Over'}# over days
    }
    if is_digit(string):
        return {'value':[float(string)],'flag':''}
    else:
        return digit_numbers[string.lower()]


def is_digit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def sentence_containing_word(spacy_doc, word):
    '''
    function to return sentence containing word
    '''
    for sent in spacy_doc.sents:
        if word in sent.text:
            return sent.text

def sentence_containing_words(spacy_doc, words):
    '''
    function to return sentence containing word
    '''
    for sent in spacy_doc.sents:
        if all(word in sent.text for word in words):
            return sent.text



def get_ph(paragraph):
    pH_regex = r"(\d+\.\d+)\s*p\s*h|\s*p\s*h\s*(\d+\.\d+)|(\d+\.\d+)\s*(acidic|acid|neutral|base|basic)|\s*(acidic|acid|neutral|base|basic)\s*(\d+\.\d+)"
    matches = re.findall(pH_regex, paragraph)
    return matches


def chemical_formula_regex(paragraph):
    pattern = r'^([A-Z][a-z]*)(\((I{1,3}|IV|V|VI{1,3}|[VIX])\))?(\d*)([A-Z][a-z]*)(\d*)+$'
    # print(re.findall(pattern, paragraph))
    return  # re.compile(pattern)


def find_ccdc_number(spacy_doc):
    '''
    Extract ccdc numbers for journals
    Parameters
    ----------
    spacy_doc: spacy document, which is paragraph containing CCDC 

    Returns
    -------
    ccdc_number
    '''
    numbers = []
    for sentence in spacy_doc.sents:
        if "CCDC" in sentence.text:
            numbers.extend(re.findall(r'\d{6,}',  sentence.text))
            break
    if len(numbers) == 2:
        ccdc_number = list(range(int(min(numbers)), int(max(numbers))+1))
    else:
        ccdc_number = [int(i) for i in numbers]
    return list(set(ccdc_number))


def extract_chemical_quantities(paragraph, chemicals_list):
    """
    A function that extract quantities and units of a list of chemicals
    and paragraphs. 
    Parameters
    ----------
    paragraph: A text from which to extract quantities
    chemicals_list : list of chemical names

    Returns
    -------
    dictionary of keys (chemical name) and values (list of quantities and units)
    """
    extracted_data = {}
    for chemical in chemicals_list:
        tmp = []
        adj_chemical = re.escape(chemical)

        # pattern = rf'(\d+(?:\.\d+)?)\s*(?:([a-zA-Z]+))?\s+(?:of\s+)?({(adj_chemical)})|(?:({(adj_chemical)})\s+(\d+(?:\.\d+)?))\s*(?:([a-zA-Z]+))?$|{(adj_chemical)}\s*\(([\d.]+)\s*(\w+)\s*,\s*([\d.]+)\s*(\w+)\)|{adj_chemical}\s*\(([\d.]+)\s*(m[lL]|m[mM]ol|g|mg|[Mm]olar)\)'
        pattern = rf'(\d+(?:\.\d+)?)\s*(?:([a-zA-Z]+))?\s+(?:of\s+)?({(adj_chemical)})|(?:({(adj_chemical)})\s+(\d+(?:\.\d+)?))\s*(?:([a-zA-Z]+))?$|{(adj_chemical)}\s*\(([\d.]+)\s*(\w+)\s*,\s*([\d.]+)\s*(\w+)\)|{adj_chemical}\s*\(([\d.]+)\s*(?:([a-zA-Z]+))\)'

        matches = re.findall(pattern, paragraph)
        for match in matches:
            match = [[match[i], match[i+1]] for i in range(0, len(match), 2)]
            match = [i for i in match if len(i) == 2]
            match = [qty_unit for qty_unit in match if all(
                string != '' for string in qty_unit)]
            tmp.extend(match)
        if chemical == 'H2O':
            tmp = [qty_unit for qty_unit in tmp if qty_unit[1] == 'ml']
        if len(tmp) > 0:
            extracted_data[chemical] = tmp
            extracted_data[chemical] = tmp
    return extracted_data


def synthetic_warning(paragraphs):
    """
    Find warning in text, which provided synthetic
    precaution
    Parameters
    ----------
    paragraph: A text from which to extract quantities

    Returns
    -------
    text 
    """
    warning = {}
    pattern = r"(?i)\bcaution\b.*?[.?!]|(?i)\warning\b.*?[.?!]"
    for i, paragraph in enumerate(paragraphs):
        match = re.search(pattern, paragraph)
        if match:
            warning[i] = paragraph
    return warning


def extract_abbreviations(text):
    # Step 1: Identify potential abbreviations
    pattern = re.compile(r'\b[A-Z][A-Za-z\.]*[A-Za-z]\b')
    potential_abbreviations = pattern.findall(text)

    # Step 2: Identify candidate definitions
    candidate_definitions = []
    for abbreviation in potential_abbreviations:
        pattern = re.compile(r'(?<=\b{0}\s)\(.*?\)'.format(abbreviation))
        candidate_definitions.extend(pattern.findall(text))

    # Step 3: Filter candidate definitions
    abbreviations = {}
    for abbreviation in set(potential_abbreviations):
        abbreviation_pattern = re.compile(r'\b{0}\b'.format(abbreviation))
        matching_definitions = [
            definition for definition in candidate_definitions if abbreviation_pattern.search(definition)]
        if matching_definitions:
            abbreviations[abbreviation] = max(matching_definitions, key=len)

    return abbreviations


def find_subject(doc):
    '''
    find the subject of a python document
    '''
    for token in doc:
        if ("subj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]


def extract_esi(paragraphs):
    '''
    '''
    plain_text = ''
    par = doc_parser.paragraph_containing_word(paragraphs, 'DOI')
    for text in list(par.values()):
        if 'ESI' and 'DOI' in text:
            plain_text += ''.join(text)
    doi_esi = re.findall(
        r"\b10\.\d{4,}(?:\.\d+)*\/\S+\b", plain_text, re.IGNORECASE)
    return doi_esi


def all_elements():
    radius = {
        'H': 0.31,
        'He': 0.28,
        'Li': 1.28,
        'Be': 0.96,
        'B': 0.85,
        'C': 0.76,
        'N': 0.71,
        'O': 0.66,
        'F': 0.57,
        'Ne': 0.58,
        'Na': 1.66,
        'Mg': 1.41,
        'Al': 1.21,
        'Si': 1.11,
        'P': 1.07,
        'S': 1.05,
        'Cl': 1.02,
        'Ar': 1.06,
        'K': 2.03,
        'Ca': 1.76,
        'Sc': 1.7,
        'Ti': 1.6,
        'V': 1.53,
        'Cr': 1.39,
        'Mn': 1.39,
        'Fe': 1.32,
        'Co': 1.26,
        'Ni': 1.24,
        'Cu': 1.32,
        'Zn': 1.22,
        'Ga': 1.22,
        'Ge': 1.2,
        'As': 1.19,
        'Se': 1.2,
        'Br': 1.2,
        'Kr': 1.16,
        'Rb': 2.2,
        'Sr': 1.95,
        'Y': 1.9,
        'Zr': 1.75,
        'Nb': 1.64,
        'Mo': 1.54,
        'Tc': 1.47,
        'Ru': 1.46,
        'Rh': 1.42,
        'Pd': 1.39,
        'Ag': 1.45,
        'Cd': 1.44,
        'In': 1.42,
        'Sn': 1.39,
        'Sb': 1.39,
        'Te': 1.38,
        'I': 1.39,
        'Xe': 1.4,
        'Cs': 2.44,
        'Ba': 2.15,
        'La': 2.07,
        'Ce': 2.04,
        'Pr': 2.03,
        'Nd': 2.01,
        'Pm': 1.99,
        'Sm': 1.98,
        'Eu': 1.98,
        'Gd': 1.96,
        'Tb': 1.94,
        'Dy': 1.92,
        'Ho': 1.92,
        'Er': 1.89,
        'Tm': 1.9,
        'Yb': 1.87,
        'Lu': 1.87,
        'Hf': 1.75,
        'Ta': 1.7,
        'W': 1.62,
        'Re': 1.51,
        'Os': 1.44,
        'Ir': 1.41,
        'Pt': 1.36,
        'Au': 1.36,
        'Hg': 1.32,
        'Tl': 1.45,
        'Pb': 1.46,
        'Bi': 1.48,
        'Po': 1.4,
        'At': 1.5,
        'Rn': 1.5,
        'Fr': 2.6,
        'Ra': 2.21,
        'Ac': 2.15,
        'Th': 2.06,
        'Pa': 2,
        'U': 1.96,
        'Np': 1.9,
        'Pu': 1.87,
        'Am': 1.8,
        'Cm': 1.69
    }
    return list(radius.keys())

def get_unique(data):
    """
    Function to return unique values in a data structure as a list
    """
    unique = []
    for all_data in data:
        if all_data not in unique:
            unique.append(all_data)
    return unique