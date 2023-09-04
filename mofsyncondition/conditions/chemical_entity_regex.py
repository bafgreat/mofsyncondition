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
        'methanol', 'pyridine', 'pyridine', 'DMSO', 'dimethylsulfoxide', 'dimethylsulfoxide',
        'MeOH', 'MeOH', 'tetrachloroethane', '2,2,2-Trifluorethanol', 'KOH',
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
        'butanol', 'butanone', 'butene', 'butyl' + 'acetonitrile',
        'butyl' + 'alcohol', 'butyl amine', 'butylchloride', 'butylimidazole',
        'butyronitrile', 'c-hexane', 'carbon disulfide', 'carbon tetrachloride',
        'chlorobenzene', 'chloroform', 'chloromethane', 'chlorotoluene', 'CHX', 'cumene',
        'cyclohexane', 'cyclohexanol', 'cyclopentyl' +
        'methylether', 'DCE', 'DCM', 'decalin',
        'decan-1-ol', 'decane', 'decanol', 'DEE', 'di-isopropyl' + 'ether',
        'di-n-butyl' + 'ether', 'di-n-hexyl' +
        'ether', 'dibromoethane', 'dibutoxymethane',
        'dibutyl' + 'ether', 'dichloro-methane', 'dichlorobenzene', 'dichloroethane',
        'dichloromethane', 'diethoxymethane', 'diethyl' + 'carbonate', 'diethyl' + 'ether',
        'diethylamine', 'diethylether', 'diglyme', 'dihexyl ether', 'diiodomethane',
        'diisopropyl' + 'ether', 'diisopropylamine', 'dimethoxyethane', 'dimethoxymethane',
        'dimethyl' + 'acetamide', 'dimethylacetimide', 'dimethylbenzene',
        'dimethylcarbonate', 'dimethylformamide', 'dimethylsulfoxide', 'dimethylacetamide',
        'dimethylbenzene', 'dimethylformamide', 'dimethylformanide', 'dimethylsulfoxide',
        'dioctylsodium sulfosuccinate', 'dioxane', 'dioxolane', 'dipropylether', 'DMAc', 'DMF', 'DMSO', 'Et2O',
        'EtAc', 'EtAcO', 'EtCN', 'ethane' + 'diol', 'ethane-1,2-diol', 'ethanol',
        'ethyl' + '(S)-2-hydroxypropanoate', 'ethyl' +
                    'acetate', 'ethyl' + 'benzoate',
        'ethyl' + 'formate', 'ethyl' + 'lactate', 'ethyl' + 'propionate', 'ethylacetamide',
        'ethylacetate', 'ethylene' + 'carbonate', 'ethylene' + 'glycol', 'ethyleneglycol',
        'ethylhexan-1-ol', 'EtOAc', 'EtOH', 'eucalyptol', 'F3-ethanol', 'F3-EtOH', 'formamide',
        'formic' + 'acid', 'glacial' + 'acetic' + 'acid', 'glycerol', 'H2O', 'H2O2',
        'H2SO4', 'HBF4', 'HCl', 'HClO4', 'HCO2H', 'HCONH2', 'heptan-1-ol',
        'heptane', 'heptanol', 'heptene', 'HEX', 'hexadecylamine', 'hexafluoroisopropanol',
        'hexafluoropropanol', 'hexan-1-ol', 'hexane', 'hexanes', 'hexanol', 'hexene',
        'hexyl' + 'ether', 'HFIP', 'HFP', 'HNO3', 'hydrochloric' + 'acid',
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
        'n,n-dimethylacetamide', 'n,n-dimethylformamide', 'N,N-dimethylformamide', 'n,n-DMF', 'NaOH', 'nBu4NBF4', 'nitric' + 'acid',
        'nitrobenzene', 'nitromethane', 'nonane', 'nujol', 'o-dichlorobenzene', 'o-xylene',
        'octan-1-ol', 'octane', 'octanol', 'octene', 'ODCB', 'p-xylene', 'pentan-1-ol', 'pentane',
        'pentanol', 'pentanone', 'pentene', 'PeOH', 'perchloric acid', 'PhCH3', 'PhCl', 'PhCN',
        'phenoxyethanol', 'phenyl acetylene', 'Phenyl ethanol', 'phenylamine',
        'phenylethanolamine', 'phenylmethanol', 'PhMe', 'phosphate',
        'phosphate buffered saline', 'pinane', 'piperidine', 'polytetrafluoroethylene',
        'propan-1-ol', 'propan-2-ol', 'propane', 'propane-1,2-diol', 'propane-1,2,3-triol',
        'propanol', 'propene', 'propionic acid', 'propionitrile',
        'propylacetate', 'propylamine', 'propylene' + 'carbonate',
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
        'TBP', 'TEA', 'DEF', 'DMA', 'CCl4'
    ]
    solvent_name_options = list(set(solvent_list))
    # solvent_name_options = [r"\b" + name + r"\s" for name in solvent_name_options]
    # map(re.compile, solvent_name_options)
    solvent_name_reg = "|".join(solvent_name_options)
    pattern = re.compile(solvent_name_reg)
    return solvent_name_options


def solvents2_regex():
    solvent_list = ['(CD3)2CO', '(CDCl2)2', '(CH3)2CHOH', '(CH3)2CO', '(CH3)2NCOH', '[nBu4N][BF4]', '1-butanol',
                    '1-butylimidazole', '1-cyclohexanol', '1-decanol', '1-heptanol', '1-hexanol', '1-methylethyl acetate',
                    '1-octanol', '1-pentanol', '1-phenylethanol', '1-propanol', '1-undecanol', '1,1,1-trifluoroethanol',
                    '1,1,1,3,3,3-hexafluoro-2-propanol', '1,1,1,3,3,3-hexafluoropropan-2-ol', '1,1,2-trichloroethane',
                    '1,2-c2h4cl2', '1,2-dichloroethane', '1,2-dimethoxyethane', '1,2-dimethylbenzene', '1,2-ethanediol',
                    '1,2,4-trichlorobenzene', '1,4-dimethylbenzene', '1,4-dioxane', '2-(n-morpholino)ethanesulfonic acid',
                    '2-butanol', '2-butanone', '2-me-thf', '2-methf', '2-methoxy-2-methylpropane', '2-methyl tetrahydrofuran',
                    '2-methylpentane', '2-methylpropan-1-ol', '2-methylpropan-2-ol', '2-methyltetrahydrofuran', '2-proh',
                    '2-propanol', '2-propyl acetate', '2-pyrrolidone', '2,2,2-trifluoroethanol', '2,2,4-trimethylpentane',
                    '2Me-THF', '2MeTHF', '3-methyl-pentane', '4-methyl-1,3-dioxolan-2-one', 'acetic acid', 'aceto-nitrile',
                    'acetone', 'acetonitrile', 'acetononitrile', 'ACN', 'AcOEt', 'AcOH', 'AgNO3', 'aniline', 'anisole', 'AOT',
                    'BCN', 'benzene', 'benzonitrile', 'benzyl alcohol', 'BHDC', 'bromoform', 'BTN', 'Bu2O', 'Bu4NBr',
                    'Bu4NClO4', 'Bu4NPF6', 'BuCN', 'BuOH', 'butan-1-ol', 'butan-2-ol', 'butan-2-one', 'butane', 'butanol',
                    'butanone', 'butene', 'butyl acetate', 'butyl acetonitrile', 'butyl alcohol', 'butyl amine',
                    'butyl chloride', 'butyl imidazole', 'butyronitrile', 'c-hexane', 'C2D5CN', 'C2H4Cl2', 'C2H5CN', 'C2H5OH',
                    'C5H5N', 'C6D6', 'C6H12', 'C6H14', 'C6H5CH3', 'C6H5Cl', 'C6H6', 'C7D8', 'C7H8', 'carbon disulfide',
                    'carbon tetrachloride', 'CCl4', 'CD2Cl2', 'CD3CN', 'CD3COCD3', 'CD3OD', 'CD3SOCD3', 'CDCl3', 'CH2Cl2',
                    'CH2ClCH2Cl', 'CH3C6H5', 'CH3Cl', 'CH3CN', 'CH3CO2H', 'CH3COCH3', 'CH3COOH', 'CH3NHCOH', 'CH3NO2',
                    'CH3OD', 'CH3OH', 'CH3Ph', 'CH3SOCH3', 'CHCl2', 'CHCl3', 'chlorobenzene', 'chloroform', 'chloromethane',
                    'chlorotoluene', 'CHX', 'Cl2CH2', 'ClCH2CH2Cl', 'cumene', 'cyclohexane', 'cyclohexanol', 'cyclopentyl methyl ether',
                    'D2O', 'DCE', 'DCM', 'decalin', 'decan-1-ol', 'decane', 'decanol', 'DEE', 'di-isopropyl ether',
                    'di-n-butyl ether', 'di-n-hexyl ether', 'dibromoethane', 'dibutoxymethane', 'dibutyl ether',
                    'dichloro-methane', 'dichlorobenzene', 'dichloroethane', 'dichloromethane', 'diethoxymethane',
                    'diethyl carbonate', 'diethyl ether', 'diethylamine', 'diethylether', 'diglyme', 'dihexyl ether',
                    'diiodomethane', 'diisopropyl ether', 'diisopropylamine', 'dimethoxyethane', 'dimethoxymethane',
                    'dimethyl acetamide', 'dimethyl acetimide', 'dimethyl benzene', 'dimethyl carbonate', 'dimethyl ether',
                    'dimethyl formamide', 'dimethyl sulfoxide', 'dimethylacetamide', 'dimethylbenzene', 'dimethylformamide',
                    'dimethylformanide', 'dimethylsulfoxide', 'dioctyl sodium sulfosuccinate', 'dioxane', 'dioxolane',
                    'dipropyl ether', 'DMA', 'DMAc', 'DMF', 'DMSO', 'Et2O', 'EtAc', 'EtAcO', 'EtCN', 'ethane diol',
                    'ethane-1,2-diol', 'ethanol', 'ethyl (S)-2-hydroxypropanoate', 'ethyl acetate', 'ethyl benzoate',
                    'ethyl formate', 'ethyl lactate', 'ethyl propionate', 'ethylacetamide', 'ethylacetate', 'ethylene carbonate',
                    'ethylene glycol', 'ethyleneglycol', 'ethylhexan-1-ol', 'EtOAc', 'EtOD', 'EtOH', 'eucalyptol', 'F3-ethanol',
                    'F3-EtOH', 'formamide', 'formic acid', 'glacial acetic acid', 'glycerol', 'H2O', 'H2O + TX', 'H2O-Triton X',
                    'H2O2', 'H2SO4', 'HBF4', 'HCl', 'HClO4', 'HCO2H', 'HCONH2', 'HDA', 'heavy water', 'HEPES', 'heptan-1-ol',
                    'heptane', 'heptanol', 'heptene', 'HEX', 'hexadecylamine', 'hexafluoroisopropanol', 'hexafluoropropanol',
                    'hexan-1-ol', 'hexane', 'hexanes', 'hexanol', 'hexene', 'hexyl ether', 'HFIP,', 'HFP', 'HNO3',
                    'hydrochloric acid', 'hydrogen peroxide', 'iodobenzene', 'IPA', 'isohexane', 'isooctane', 'isopropanol',
                    'isopropyl benzene', 'KBr', 'KPB', 'LiCl', 'ligroine', 'limonene', 'MCH', 'Me-THF', 'Me2CO', 'MeCN',
                    'MeCO2Et', 'MeNO2', 'MeOD', 'MeOH', 'MES', 'mesitylene', 'methanamide', 'methanol', 'MeTHF',
                    'methoxybenzene', 'methoxyethylamine', 'methyl acetamide', 'methyl acetoacetate', 'methyl benzene',
                    'methyl butane', 'methyl cyclohexane', 'methyl ethyl ketone', 'methyl formamide', 'methyl formate',
                    'methyl isobutyl ketone', 'methyl laurate', 'methyl methanoate', 'methyl naphthalene', 'methyl pentane',
                    'methyl propan-1-ol', 'methyl propan-2-ol', 'methyl propionate', 'methyl pyrrolidin-2-one',
                    'methyl pyrrolidine', 'methyl pyrrolidinone', 'methyl t-butyl ether', 'methyl tetrahydrofuran',
                    'methyl-2-pyrrolidone', 'methylbenzene', 'methylcyclohexane', 'methylene chloride', 'methylformamide',
                    'methyltetrahydrofuran', 'MIBK', 'morpholine', 'mTHF', 'n-butanol', 'n-butyl acetate', 'n-decane',
                    'n-heptane', 'n-HEX', 'n-hexane', 'n-methylformamide', 'n-methylpyrrolidone', 'n-nonane', 'n-octanol',
                    'n-pentane', 'n-propanol', 'n,n-dimethylacetamide', 'n,n-dimethylformamide', 'n,n-DMF', 'Na2SO4', 'NaCl',
                    'NaClO4', 'NaHCO3', 'NaOH', 'KOH', 'nBu4NBF4', 'nitric acid', 'nitrobenzene', 'nitromethane', 'NMP', 'nonane',
                    'NPA', 'nujol', 'o-dichlorobenzene', 'o-xylene', 'octan-1-ol', 'octane', 'octanol', 'octene', 'ODCB',
                    'p-xylene', 'PBS', 'pentan-1-ol', 'pentane', 'pentanol', 'pentanone', 'pentene', 'PeOH', 'perchloric acid',
                    'PhCH3', 'PhCl', 'PhCN', 'phenoxyethanol', 'phenyl acetylene', 'Phenyl ethanol', 'phenylamine',
                    'phenylethanolamine', 'phenylmethanol', 'PhMe', 'phosphate', 'phosphate buffered saline', 'pinane',
                    'piperidine', 'polytetrafluoroethylene', 'potassium bromide', 'potassium phosphate buffer', 'PrCN', 'PrOH',
                    'propan-1-ol', 'propan-2-ol', 'propane', 'propane-1,2-diol', 'propane-1,2,3-triol', 'propanol', 'propene',
                    'propionic acid', 'propionitrile', 'propyl acetate', 'propyl amine', 'propylene carbonate',
                    'propylene glycol', 'pyridine', 'pyrrolidone', 'quinoline', 'SDS', 'silver nitrate', 'SNO2',
                    'sodium chloride', 'sodium hydroxide', 'sodium perchlorate', 'sulfuric acid', 't-butanol', 'TBABF4', 'TBAF',
                    'TBAH', 'TBAOH', 'TBAP', 'TBAPF6', 'TBP', 'TEA', 'TEAP', 'TEOA', 'tert-butanol', 'tert-butyl alcohol',
                    'tetrabutylammonium hexafluorophosphate', 'tetrabutylammonium hydroxide', 'tetrachloroethane',
                    'tetrachloroethylene', 'tetrachloromethane', 'tetrafluoroethylene', 'tetrahydrofuran', 'tetralin',
                    'tetramethylsilane', 'tetramethylurea', 'tetrapiperidine', 'TFA', 'TFE', 'THF', 'THF-d8', 'tin dioxide',
                    'titanium dioxide', 'toluene', 'tri-n-butyl phosphate', 'triacetate', 'triacetin', 'tribromomethane',
                    'tributyl phosphate', 'trichlorobenzene', 'trichloroethene', 'trichloromethane', 'triethyl amine',
                    'triethyl phosphate', 'triethylamine', 'trifluoroacetic acid', 'trifluoroethanol', 'trifluoroethanol ',
                    'trimethyl benzene', 'trimethyl pentane', 'tris', 'Triton X-100', 'TX-100', 'undecan-1-ol', 'undecanol',
                    'valeronitrile', 'water', 'xylene', 'xylol'
                    ]
    prefixes = ['iso', 'tert', 'sec', 'ortho', 'meta', 'para', 'meso']
    solvent_re = re.compile(r'(?:^|\b)(?:(?:%s|d\d?\d?|[\dn](?:,[\dn]){0,3}|[imnoptDLRS])-?)?(?:%s)(?:-d\d?\d?)?(?=$|\b)'
                            % ('|'.join(re.escape(s) for s in prefixes),
                               '|'.join(re.escape(s).replace(r'\ ', r'[\s\-]?') for s in solvent_list)))
    return solvent_re


def mof_regex():
    re_MOF1 = '^(?![aA-zZ]+\-?\d?\d?\-like)(?![aA-zZ]+\-?\d?\d?\-type(s?))(ZJU|SNU|MAF|MCF|Ir-MOF|JUC|FJI|UHM|MUV|BUT|ZJNU|Tb|she|CTH|pek|FDM|MODF|USF|NJFU|ZJU|CMOF|CTH|TPMOF|IZE|pbz|PNMOF|gea|MFM|UNLPF|PIZOF|soc|MOAAF|Y|Ho|CPO|JLU|aea|NOTT|NU|MMPF|UTSA|CPM|U[iI]O|MOF|IRMOF|T-MOF|NTU|MIL|HKUST|HNUST|LIC|PCN|ZIF|CPL|CALF|UMCM|DUT)[:;\[\]\)\{\}\]{0,3}[\-‐‑⁃‒–—―−－⁻][A-Za-z0-9_-]+[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]*[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]*[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]*[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]+$'
    re_MOF2 = '^(ZJU|SNU|MAF|MCF|Ir-MOF|JUC|FJI|UHM|MUV|BUT|ZJNU|Tb|she|CTH|pek|FDM|MODF|USF|NJFU|ZJU|CMOF|CTH|TPMOF|IZE|pbz|PNMOF|gea|MFM|UNLPF|PIZOF|soc|MOAAF|Y|Ho|CPO|JLU|aea|NOTT|NU|UTSA|MMPF|CPM|U[iI]O|MOF|T-MOF|IRMOF|NTU|MIL|HKUST|HNUST|LIC|PCN|ZIF|CPL|CALF|UMCM|DUT)([\-‐‑⁃‒–—―−－⁻])([a-zA-Z0-9]+)$'
    re_chemical_formula = '^(?![aA-zZ]+\-?\d?\d?\-ligands)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\d\(CO2\)\d?\(?N?N?\)?)(?!^(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\($)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\(CH3COO\)\d\s?\d?H?2?O?)(?!M1)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\dAs\dO\d)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\d\(μ3-OH\)\d\(CO2\)\d)(?!\[?Zn\d\(μ4-O\)\(O2CR?\)\d\])(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\((AcO|OAc)\)\d?\s?H?2?O?)(?!Me\dNH\d)(?!(\[?Zn\dO?\(O2C))(?!^M\(II\))(?!.*\(OOC\)\d$)(?!Co\(Tt\)\d?$)(?!.*\(COO−?\)\d$)(?!(M|Mn|Cu|Zn|Y|Co|Ni|Fe|Zr|Cd)\((II|i|ii|iii)\)$)(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\d?O?\(CO2\)\d\]?$)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\dO?\+?.?.?.?$)(?!UiO-type$)(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\(NO\d?\)\d?\]?.?.?.?.?.?.?.?$)(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\(ClO\d?\)\d?\]?.?.?.?.?.?.?.?$)(?!Cu\(NO\d?\).?.?.?.?.?.?.?.?$)(?!\[Zn3\(EBTC\)2\]∞$)(?!\{?Cu\d\(O2?CR\)\d\}?$)(?!HCl$)(?!Cu\(II\)$)(?!Zr6O8\(CH3COO\)26\+$)(?!Cu\(NO3\)2·3H2O$)(?!Zr6$)(?!Cu\(NO3\)2$)(\[?)(\{)?(\[)?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)(\s?)(L|\d|\(|\-)'
    patterns = "|".join([re_MOF1, re_MOF2, re_chemical_formula])
    return re.compile(patterns, flags=0)


def metal_salts_formular():
    base_metal = ['Zn', 'Mn', 'Cu', 'Fe', 'Al', 'Cd', 'Zr', 'Co', 'Mg', 'V', 'Ca',
                  'Ti', 'Pb', 'Ni', 'Na', 'Sc', 'Cr', 'Y', 'Nb', 'Mo', 'Ga', 'Ge',
                  'Ta', 'Re', 'Os', 'Rb', 'Re', 'Hf', 'Ir', 'Pt', 'Au', 'Rf', 'Db',
                  'Sg', 'Bh', 'Hs']
    prefix = '^'
    # suffix = '([HBCNOFSPI0-9\[\]\(\)])\w*'
    suffix = '([A-Za-z*0-9\[\]\(\)])(\((I{1,3}|IV|V|VI{1,3}|[VIX])\))?(\d*)([A-Z][a-z]*)(\d*)\w*'
    list_of_formulars = [prefix+metal+suffix for metal in base_metal]
    metal_formulars = '|'.join(list_of_formulars)

    name_pattern = r'\b([Mm]olybdenum|[Nn]iobium|[Yy]ttrium|[Cc]hromium|[Ss]candium|[Ss]odium|[Nn]ickel|[Ll]ead|[Tt]itanium|[Zz]inc|[Mm]anganese|[Vv]anadium|[Mm]agnesium|[Cc]opper|[Ii]ron|[Ff]errous|[Aa]lumin(ium|um|o)|[Cc]admium|[Zz]irconium|[Cc]obalt)\s(\w+)\b'

    # pattern = r'^([A-Z][a-z]*)(\((I{1,3}|IV|V|VI{1,3}|[VIX])\))?(\d*)([A-Z][a-z]*)(\d*)+$'

    # '^((Zn|Mn|Cu|Fe|Al|Cd|Zr|Co|Mg|V|Ti|Pb|Ni|Na|Sc|Cr|Y|Nb|Mo)|[Mm]olybdenum|[Nn]iobium|[Yy]ttrium|[Cc]hromium|[Ss]candium|[Ss]odium|[Nn]ickel|[Ll]ead|[Tt]itanium|[Zz]inc|[Mm]anganese|[Vv]anadium|[Mm]agnesium|[Cc]opper|[Ii]ron|[Ff]errous|[Aa]lumin(ium|um|o)|[Cc]admium|[Zz]irconium|[Cc]obalt)(\W|[0-9\+\-A-Z\.ivl\(\)\·\[\\]\\(\\)\\{\\}]+)?$'
    return re.compile(metal_formulars+'|'+name_pattern)


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
    return stability,  analysis


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
    stability_pattern, analysis_pattern = key_words_regex()
    for time in react_time:
        value = time['value']
        units = time['units']
        if time['units'] != 'N/A':
            word = value+' '+time['units']
        else:
            word = value + ' '
        sentence = sentence_containing_word(spacy_doc, word)
        if sentence != None:
            match = re.search(analysis_pattern, sentence)
            match2 = re.search(stability_pattern, sentence)
            if match:
                time_hrs = convert_time_to_hour(value, units)
                drying.append(time_hrs)
            elif match2:
                time_hrs = convert_time_to_hour(value, units)
                stability.append(time_hrs)
            else:
                time_hrs = convert_time_to_hour(value, units)
                reaction_time.append(time_hrs)

    return reaction_time, stability, drying


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
    if value == 'overnight':
        time_hrs = str(24)
    elif units == 'day' or units == 'days' or units == 'd':
        time_hrs = numbers_to_digit(value) * 24
    elif units == 'min' or units == 'minutes':
        time_hrs = round(numbers_to_digit(value)/60.0, 3)
    else:
        time_hrs = float(value)
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
    stability_pattern, analysis_pattern = key_words_regex()
    for temp in reaction_temperature:
        value = temp['value']
        units = temp['units']
        if units != 'N/A':
            word = value
        elif value == 'RT':
            word = 'room temperature'
        if value != '-':
            sentence = sentence_containing_word(spacy_doc, word)
            if sentence != None:
                melting_points = re.findall(
                    r"(?i)(?:mp~|melting point|mp)\s*(\d+(?:\.\d+)?)(?:\s*-\s*(\d+(?:\.\d+)?))?", sentence)
                melting_points = [
                    i for sub in melting_points for i in sub if i]
                if value in melting_points:
                    temp = convert_temp_to_kelvin(value, units)
                    melting_temp.append(temp)
                else:
                    match = re.search(analysis_pattern, sentence)
                    match2 = re.search(stability_pattern, sentence)
                    if match:
                        temp = convert_temp_to_kelvin(value, units)
                        drying_temp.append(temp)
                    elif match2:
                        temp = convert_temp_to_kelvin(value, units)
                        stability_temp.append(temp)
                    else:
                        temp = convert_temp_to_kelvin(value, units)
                        reaction_temp.append(temp)
    return reaction_temp, stability_temp, drying_temp, melting_temp


def numbers_to_digit(string):
    digit_numbers = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
        'or': 1,
        'few': 3,
        'several': 6,
        'half': 0.5
    }
    if is_digit(string):
        return float(string)
    else:
        return float(digit_numbers[string.lower()])


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


def get_ph(paragraph):
    pH_regex = r"(\d+\.\d+)\s*p\s*h|\s*p\s*h\s*(\d+\.\d+)|(\d+\.\d+)\s*(acidic|acid|neutral|base|basic)|\s*(acidic|acid|neutral|base|basic)\s*(\d+\.\d+)"
    matches = re.findall(pH_regex, paragraph)
    return matches


def chemical_formula_regex(paragraph):
    pattern = r'^([A-Z][a-z]*)(\((I{1,3}|IV|V|VI{1,3}|[VIX])\))?(\d*)([A-Z][a-z]*)(\d*)+$'
    print(re.findall(pattern, paragraph))
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
    chemicals_list = [i for i in chemicals_list if i != 'H']
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

    # #doi_esi = "https://doi.org/"+doi_esi[0]
    # # from PyPaperBot import PyPaperBot
    # bot = PyPaperBot()
    # bot.download_paper(doi_esi)
