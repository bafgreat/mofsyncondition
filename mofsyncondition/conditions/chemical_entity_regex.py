#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import re
<<<<<<< HEAD
=======
import pubchempy as pcp
from pymatgen.core import Composition
from pymatgen.core.ion import Ion
>>>>>>> 9253cec (fixed)
from mofsyncondition.doc import doc_parser


def solvents_regex():
    """
    Regex expression for solvents
    """
<<<<<<< HEAD
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
        'MOPS',  'MES', 'heavy water', 'IPA', 'methanolic', 'water'
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
        'potassium floride', 'KI', 'KF', 'KCl', 'KBr' 'sodium iodide',
        'sodium bromide', 'sodium floride', 'NaI', 'NaF', 'NaCl', 'NaBr', 'DI-water'
    ]
    solvent_name_options = list(set(solvent_list))
    prefixes = ['iso', 'tert', 'sec', 'ortho', 'meta', 'para', 'meso']
    solvent_re = re.compile(r'(?:^|\b)(?:(?:%s|d\d?\d?|[\dn](?:,[\dn]){0,3}|[imnoptDLRS])-?)?(?:%s)(?:-d\d?\d?)?(?=$|\b)'
                            % ('|'.join(re.escape(s) for s in prefixes),
                               '|'.join(re.escape(s).replace(r'\ ', r'[\s\-]?') for s in solvent_name_options)))
=======
    solvent_list = solvent_chemical_names()
    solvent_name_options = list(set(solvent_list))
    # prefixes = ['iso', 'tert', 'sec', 'ortho', 'meta', 'para', 'meso']
    # solvent_re = re.compile(r'(?:^|\b)(?:(?:%s|d\d?\d?|[\dn](?:,[\dn]){0,3}|[imnoptDLRS])-?)?(?:%s)(?:-d\d?\d?)?(?=$|\b)'
    #                         % ('|'.join(re.escape(s) for s in prefixes),
    #                            '|'.join(re.escape(s).replace(r'\ ', r'[\s\-]?') for s in solvent_name_options)))
>>>>>>> 9253cec (fixed)
    return solvent_name_options


def mof_regex():
<<<<<<< HEAD
    re_MOF1 = '^(?![aA-zZ]+\-?\d?\d?\-like)(?![aA-zZ]+\-?\d?\d?\-type(s?))(ZJU|SNU|MAF|MCF|Ir-MOF|JUC|FJI|UHM|MUV|BUT|ZJNU|Tb|she|CTH|pek|FDM|MODF|USF|NJFU|ZJU|CMOF|CTH|TPMOF|IZE|pbz|PNMOF|gea|MFM|UNLPF|PIZOF|soc|MOAAF|Y|Ho|CPO|JLU|aea|NOTT|NU|MMPF|UTSA|CPM|U[iI]O|MOF|IRMOF|T-MOF|NTU|MIL|HKUST|HNUST|LIC|PCN|ZIF|CPL|CALF|UMCM|DUT)[:;\[\]\)\{\}\]{0,3}[\-‐‑⁃‒–—―−－⁻][A-Za-z0-9_-]+[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]*[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]*[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]*[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]+$'
    re_MOF2 = '^(ZJU|SNU|MAF|MCF|Ir-MOF|JUC|FJI|UHM|MUV|BUT|ZJNU|Tb|she|CTH|pek|FDM|MODF|USF|NJFU|ZJU|CMOF|CTH|TPMOF|IZE|pbz|PNMOF|gea|MFM|UNLPF|PIZOF|soc|MOAAF|Y|Ho|CPO|JLU|aea|NOTT|NU|UTSA|MMPF|CPM|U[iI]O|MOF|T-MOF|IRMOF|NTU|MIL|HKUST|HNUST|LIC|PCN|ZIF|CPL|CALF|UMCM|DUT)([\-‐‑⁃‒–—―−－⁻])([a-zA-Z0-9]+)$'
    re_chemical_formula = '^(?![aA-zZ]+\-?\d?\d?\-ligands)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\d\(CO2\)\d?\(?N?N?\)?)(?!^(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\($)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\(CH3COO\)\d\s?\d?H?2?O?)(?!M1)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\dAs\dO\d)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\d\(μ3-OH\)\d\(CO2\)\d)(?!\[?Zn\d\(μ4-O\)\(O2CR?\)\d\])(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\((AcO|OAc)\)\d?\s?H?2?O?)(?!Me\dNH\d)(?!(\[?Zn\dO?\(O2C))(?!^M\(II\))(?!.*\(OOC\)\d$)(?!Co\(Tt\)\d?$)(?!.*\(COO−?\)\d$)(?!(M|Mn|Cu|Zn|Y|Co|Ni|Fe|Zr|Cd)\((II|i|ii|iii)\)$)(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\d?O?\(CO2\)\d\]?$)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\dO?\+?.?.?.?$)(?!UiO-type$)(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\(NO\d?\)\d?\]?.?.?.?.?.?.?.?$)(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\(ClO\d?\)\d?\]?.?.?.?.?.?.?.?$)(?!Cu\(NO\d?\).?.?.?.?.?.?.?.?$)(?!\[Zn3\(EBTC\)2\]∞$)(?!\{?Cu\d\(O2?CR\)\d\}?$)(?!HCl$)(?!Cu\(II\)$)(?!Zr6O8\(CH3COO\)26\+$)(?!Cu\(NO3\)2·3H2O$)(?!Zr6$)(?!Cu\(NO3\)2$)(\[?)(\{)?(\[)?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)(\s?)(L|\d|\(|\-)'
=======
    '''
    A regex pattern to identify MOFs, similar to digiMOFs
    '''
    re_MOF1 = r'^(?![aA-zZ]+\-?\d?\d?\-like)(?![aA-zZ]+\-?\d?\d?\-type(s?))(ZJU|SNU|MAF|MCF|Ir-MOF|JUC|FJI|UHM|MUV|BUT|ZJNU|Tb|she|CTH|pek|FDM|MODF|USF|NJFU|ZJU|CMOF|CTH|TPMOF|IZE|pbz|PNMOF|gea|MFM|UNLPF|PIZOF|soc|MOAAF|Y|Ho|CPO|JLU|aea|NOTT|NU|MMPF|UTSA|CPM|U[iI]O|MOF|IRMOF|T-MOF|NTU|MIL|HKUST|HNUST|LIC|PCN|ZIF|CPL|CALF|UMCM|DUT)[:;\[\]\)\{\}\]{0,3}[\-‐‑⁃‒–—―−－⁻][A-Za-z0-9_-]+[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]*[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]*[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]*[:;\[\]\)\{\}\]{0,3}[A-Za-z0-9_-]+$'
    re_MOF2 = r'^(ZJU|SNU|MAF|MCF|Ir-MOF|JUC|FJI|UHM|MUV|BUT|ZJNU|Tb|she|CTH|pek|FDM|MODF|USF|NJFU|ZJU|CMOF|CTH|TPMOF|IZE|pbz|PNMOF|gea|MFM|UNLPF|PIZOF|soc|MOAAF|Y|Ho|CPO|JLU|aea|NOTT|NU|UTSA|MMPF|CPM|U[iI]O|MOF|T-MOF|IRMOF|NTU|MIL|HKUST|HNUST|LIC|PCN|ZIF|CPL|CALF|UMCM|DUT)([\-‐‑⁃‒–—―−－⁻])([a-zA-Z0-9]+)$'
    re_chemical_formula = r'^(?![aA-zZ]+\-?\d?\d?\-ligands)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\d\(CO2\)\d?\(?N?N?\)?)(?!^(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\($)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\(CH3COO\)\d\s?\d?H?2?O?)(?!M1)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\dAs\dO\d)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\d\(μ3-OH\)\d\(CO2\)\d)(?!\[?Zn\d\(μ4-O\)\(O2CR?\)\d\])(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\((AcO|OAc)\)\d?\s?H?2?O?)(?!Me\dNH\d)(?!(\[?Zn\dO?\(O2C))(?!^M\(II\))(?!.*\(OOC\)\d$)(?!Co\(Tt\)\d?$)(?!.*\(COO−?\)\d$)(?!(M|Mn|Cu|Zn|Y|Co|Ni|Fe|Zr|Cd)\((II|i|ii|iii)\)$)(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\d?O?\(CO2\)\d\]?$)(?!(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\dO?\+?.?.?.?$)(?!UiO-type$)(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\(NO\d?\)\d?\]?.?.?.?.?.?.?.?$)(?!\[?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)\(ClO\d?\)\d?\]?.?.?.?.?.?.?.?$)(?!Cu\(NO\d?\).?.?.?.?.?.?.?.?$)(?!\[Zn3\(EBTC\)2\]∞$)(?!\{?Cu\d\(O2?CR\)\d\}?$)(?!HCl$)(?!Cu\(II\)$)(?!Zr6O8\(CH3COO\)26\+$)(?!Cu\(NO3\)2·3H2O$)(?!Zr6$)(?!Cu\(NO3\)2$)(\[?)(\{)?(\[)?(Mg|M|Ni|Zn|Mn|Cu|Zr|Me|CoCl|Co|Cd)(\s?)(L|\d|\(|\-)'
>>>>>>> 9253cec (fixed)
    formular_with_L_and_n = r"\b\w*\d*\((?:L|n|∞)\)\d*\b"
    patterns = "|".join(
        [re_MOF1, re_MOF2, re_chemical_formula, formular_with_L_and_n])
    return re.compile(patterns, flags=0)


def metal_salts_formular():
    '''
    Creating a regex pattern to find metal salts in a list of chemicals
    '''
<<<<<<< HEAD
    base_metal = ['Li', 'Be', 'Ba', 'Mg', 'Al', 'Ka' 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn',
                  'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ha', 'Rb', 'Sr',
=======
    base_metal = ['Li', 'Be', 'Ba', 'Mg', 'Al', 'K' 'Ca', 'Sc', 'Ti', 'V',
                  'Cr', 'Mn','Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ha', 'Rb', 'Sr',
>>>>>>> 9253cec (fixed)
                  'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
                  'In', 'Sn', 'CS', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm',
                  'Eu', 'Gd', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
                  'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Ti',
                  'Pb', 'Bi', 'Po', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np',
<<<<<<< HEAD
                  'Pu', 'Am', 'Cm', 'BK', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Md',
=======
                  'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Md',
>>>>>>> 9253cec (fixed)
                  'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn',
                  'Uut', 'Fl', 'Lv'
                  ]
    prefix = '^'
    suffix = r'(\((?:[IVX]+|\d+)\))?(\w+)\)?(\d*)'
    list_of_formulars = [prefix+metal +
                         suffix for metal in base_metal if metal not in ['Zn']]
    metal_formulars = '|'.join(list_of_formulars)
    full_names = ['[Ll]ithium', '[Bb]eryllium', '[Ss]odium', '[Pp]otassium',
                  '[Mm]agnesium', '[Aa]lumin(ium|um|o)', '[cC]alcium', '[Ss]candium',
                  '[Tt]itanium|[Tt]itanous|[Tt]itanic', '[Vv]anadium|[vV]anadous|[Vv]anadic',
                  '[Cc]hromium|[cC]hromous|[cC]hromic', '[Mm]anganese|[Mm]anganous|[Mm]anganic',
                  '[Ii]ron|[Ff]errous|[Ff]erric', '[Cc]obalt|[cC]obaltous|[Cc]obaltic',
                  '[Nn]ickel|[nN]ickelous|[Nn]ickelic', '[Cc]opper|[cC]uprous|[Cc]upric',
                  '[Zz]inc', 'Gallium', '[Rr]ubidium', '[Ss]trontium', '[Yy]ttrium',
                  '[Zz]irconium', '[Nn]iobium', '[Mm]olybdenum', 'Technetium',
                  '[rR]uthenium', '[Rr]hodium', '[Pp]alladium', '[Cc]admium', '[Ii]ndium',
                  '[tT]in|[sS]tannous|[Ss]tannic', '[Cc]esium', '[Bb]arium', '[lL]anthanium',
                  '[Cc]erium', '[pP]raseodymium', '[Nn]eodymium', '[Pp]romethium', '[Ss]amarium',
                  '[E]uropium', '[Gg]adolinium', '[Tt]erbium', '[Dd]ysprosium', '[Hh]olmium',
                  '[Ee]rbium', '[Tt]hulium', '[Yy]tterbium', '[Ll]utetium', '[Hh]afnium',
                  '[Tt]antalum', '[Tt]ungsten', '[Rr]henium', '[Os]mium', '[Ii]ridium',
                  '[Pp]latinum', '[Gg]old|[aA]urous|[Aa]uric',
                  '[Mm]ercury|[mM]ercurous|[m]Mercuric', '[Tt]hallium',
                  '[Ll]ead|[pP]lumbous|[Pp]lumbic', '[Bb]ismuth', '[Pp]olonium',
                  '[Ff]rancium', '[Rr]adium', '[Aa]ctinium', '[Tt]horium', '[Pp]rotactinium',
                  '[Uu]ranium', '[Nn]eptunium', '[Pp]lutonium', '[Aa]mericium', '[Cc]urium',
                  '[Bb]erkelium', '[cC]alifornium', '[eE]insteinium', '[Ff]ermium',
                  '[mM]endelevium', '[Nn]obelium', '[Ll]awrencium', '[Rr]utherfordium',
                  '[Dd]ubnium', '[Ss]eaborgium', '[Bb]ohrium', '[Hh]assium',
                  '[Mm]eitnerium', '[dD]armstadtium', '[Rr]oentgenium', '[cC]opernicium',
                  '[Uu]nuntrium', '[Ff]levorium', '[Ll]ivermorium'
                  ]
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
    key words for regex pattern to partition time and temperature
    '''
    crystalization = [r"[Cc]rystal\w*", r'[Gg]rown', r'[gG]row\w*']
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
    if re.match(r'\bDMSO\b', word, re.IGNORECASE):
        return 'dimethylsulfoxide'
    elif re.match(r'\b([Nn],[Nn]-)?DEF\b|\bdiethylformamide\b', word, re.IGNORECASE):
        return 'N,N-diethylformamide',
    elif word in ['MeOH']:
        return 'methanol'
    elif word in ['THF']:
        return 'tetrahydrofuran'
    elif re.match(r'\b(n,n-)?DMF\b', word, re.IGNORECASE):
        return 'N,N-dimethylformamide'
    elif word in ['TFE']:
        return '2,2,2-trifluorethanol'
    elif word in ['TFA']:
        return 'trifluoroacetic acid'
    elif word in ['TeCA']:
        return '1,1,2,2-Tetrachloroethane'
    elif word in ['TTCE']:
        return 'tetrachloroethane'
    elif word in ['PCE']:
        return 'pentachloroethane'
    elif word in ['HCE']:
        return 'hexachloroethane'
    elif word in ['2Me-THF']:
        return '2-methyltetrahydrofuran'
    elif word in ['2-MTHF']:
        return '2-methyltetrahydrofuran'
    elif re.match(r'\bDMAc\b|\bDMA\b', word, re.IGNORECASE):
        return '2-methyltetrahydrofuran'
    elif word in ['H2SO4']:
        return 'sulphuric acid'
    elif word in ['IPA']:
        return 'isopropyl alcohol'
    elif word in ['ACN']:
        return 'acetonitril'
    elif word in ['H2O2']:
        return 'hydrogen peroxide'
    elif word in ['CCl4']:
        return 'tetrachloromethane'
    elif word in ['H2O']:
        return 'water'
    elif re.search(r'\b(2,6-)?[Nn][Dd][Cc]\b', word, re.IGNORECASE):
        return '2,6-naphthalenedicarboxylic acid'
    elif word in ['KOH']:
        return 'potassium hydroxide'
    elif re.match(r"\b(\d*,?\d+µ?-)?[pP]hen\b", word, re.IGNORECASE):
        return word + "anthroline"
    elif word in ['H2dte', 'dte']:
        return '1,4-ditetrazolylethylene'
    elif word in ['H2dtb', 'dtb']:
        return '1,3-dis(2H-tetrazol-5-yl)benzene'
    elif word in ['H4bptc', 'bptc']:
        return "2,3,3',4-biphenyltetracarboxylic acid",
    elif re.match(r"\b(\d*,?\d+µ?-)?bipy\b", word):
        return word + "ridine"
<<<<<<< HEAD
    
=======

>>>>>>> 9253cec (fixed)
    elif re.match(r"\b(\d*,?\d+µ?-)?H2BDC|BDC\b", word):
        match = re.search(r"\d,\d-", word)
        if match:
            digits = match.group()
            return digits + 'benzenedicarboxylic acid'
        else:
            return 'benzenedicarboxylic acid'
<<<<<<< HEAD
        
=======

>>>>>>> 9253cec (fixed)
    elif re.match(r"\b(\d*,?\d+µ?-)?H2BTC|BTC\b", word):
        match = re.search(r"\d,\d-", word)
        if match:
            digits = match.group()
            return digits + 'benzenetricarboxylic acid'
        else:
            return 'benzenetricarboxylic acid'
    elif word in ['bpee']:
        return '1,2-bis(4-pyridyl)ethylene'
    elif re.match(r'\bNaOAc\b|\bCH3COONa\b', word, re.IGNORECASE):
        return 'sodium acetate'
    elif word in ['CH2Cl2']:
        return 'dichloromethane'
    elif re.match(r'\bEtOAc\b|\bETAC\b|\bEA\b', word, re.IGNORECASE):
        return 'ethyl acetate'
    elif word in ['bpa']:
        return 'bisphenol'
    elif re.match(r'\bEtOH\b|\bC2H5OH\b|\bE2OH\b|\bAA\b|\bETH\b', word, re.IGNORECASE):
        return 'ethanol'
    elif word in ['NH4SCN']:
        return 'ammonium thiocyanate'
    elif word in ['NaN3']:
        return 'sodium azide'
    elif word in ['H2mip', 'mip']:
        return '5-methylisophthalic acid'
    elif word in ['DI', 'DI-water', 'di-water', 'DI-H2O', 'di-H2O']:
        return 'deionised water'
    elif re.match(r"\b(\d*,?\d+µ?-)?[H2]?tdc\b", word, re.IGNORECASE):
        return '1,2,5-thiadiazole-3,4-dicarboxylate'
    else:
        return word


def reaction_time_breakdown(react_time, spacy_doc):
    '''
    Function that partition time data found in text as:
    1. reaction time
    2. stability time
    3. drying time
    4. crystalization time
    '''
    drying = []
    stability = []
    reaction_time = []
    crystalization_time = []
    stability_pattern, analysis_pattern, crystalization = key_words_regex()
    for time in react_time:
        seen = []
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
        time_hrs['value'] = [i*24 for i in numbers_to_digit(value)['value']]
        if len(numbers_to_digit(value)['flag']) > 0:
            time_hrs['flag'] = numbers_to_digit(value)['flag'] + ' ' + 'days'
        else:
            time_hrs['flag'] = numbers_to_digit(value)['flag']
    elif units == 'min' or units == 'minutes' or units == 'm':
        time_hrs['value'] = [round(i/60.0, 3)
                             for i in numbers_to_digit(value)['value']]
        if len(numbers_to_digit(value)['flag']) > 0:
            time_hrs['flag'] = numbers_to_digit(
                value)['flag'] + ' ' + 'minutes'
        else:
            time_hrs['flag'] = numbers_to_digit(value)['flag']
        # time_hrs = round(numbers_to_digit(value)/60.0, 3)
    else:
        time_hrs['value'] = [float(value)]
        time_hrs['flag'] = ''
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
    A function the partion temperature as:
    1. reaction temperature
    2  stability_temperature
    3. drying temperature,
    4. melting temperature
    5. crystalization temperature
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
                    if match3 and value not in seen:
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
    """
    Funtion that corrects time information extracted from journal articles
    """
    digit_numbers = {
        'one': {'value': [1], 'flag': ''},
        'two': {'value': [2], 'flag': ''},
        'three': {'value': [3], 'flag': ''},
        'four': {'value': [4], 'flag': ''},
        'fours': {'value': [4], 'flag': ''},
        'five': {'value': [5], 'flag': ''},
        'fives': {'value': [5], 'flag': ''},
        'six': {'value': [6], 'flag': ''},
        'seven': {'value': [7], 'flag': ''},
        'sevens': {'value': [7], 'flag': ''},
        'eight': {'value': [8], 'flag': ''},
        'eights': {'value': [8], 'flag': ''},
        'nine': {'value': [9], 'flag': ''},
        'ten': {'value': [10], 'flag': ''},
        "eleven": {'value': [11], 'flag': ''},
        "twelve": {'value': [12], 'flag': ''},
        "thirteen": {'value': [13], 'flag': ''},
        "fourteen": {'value': [14], 'flag': ''},
        "fifteen": {'value': [15], 'flag': ''},
        "sixteen": {'value': [16], 'flag': ''},
        "seventeen": {'value': [17], 'flag': ''},
        "eighteen": {'value': [18], 'flag': ''},
        "nineteen": {'value': [19], 'flag': ''},
        "twenty": {'value': [20], 'flag': ''},
        "thirty": {'value': [30], 'flag': ''},
        "forty": {'value': [40], 'flag': ''},
        "fifty": {'value': [50], 'flag': ''},
        "sixty": {'value': [60], 'flag': ''},
        "seventy": {'value': [70], 'flag': ''},
        "eighty": {'value': [80], 'flag': ''},
        "ninety": {'value': [90], 'flag': ''},
        'or': {'value': [1], 'flag': ''},
        'few': {'value': [2, 3], 'flag': 'Few'},
        'several': {'value': [4, 5], 'flag': 'Several'},
        'half': {'value': [0.5], 'flag': ''},
        'some': {'value': [3, 4], 'flag': 'Some'},
        'many': {'value': [7, 14], 'flag': 'Many'},  # for many days
        'next': {'value': [1, 2], 'flag': 'Next'},
        'for': {'value': [3, 4], 'flag': 'For'},
        'of': {'value': [3, 4], 'flag': 'Period of'},
        'different': {'value': [1, 2], 'flag': 'Different'},
        'successive': {'value': [1, 2], 'flag': 'Successive'},
        'additional': {'value': [1, 2], 'flag': 'Additional'},
        'within': {'value': [2, 3], 'flag': 'Within'},
        # Yellow crystals of [Hg (CH2COCH3)(4-NO2pcyd)]n were grown after days
        'after': {'value': [3, 4], 'flag': 'After'},
        # 3 disappeared in the following days
        'following': {'value': [1, 2], 'flag': 'Following'},
        # Crystals were observed to lose solvent slowly and decompose in days to weeks when
        'in': {'value': [7, 14], 'flag': 'In days to weeks'},
        'over': {'value': [4, 5], 'flag': 'Over'}  # over days
    }
    if is_digit(string):
        return {'value': [float(string)], 'flag': ''}
    else:
        return digit_numbers[string.lower()]


def is_digit(x):
    """
    Function that checks wheter a character is a digit
    """
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


<<<<<<< HEAD
def _multiplicity():
=======
def iupac_multiplicity():
    """
    A function that creates a regex pattern to match iupac multiplicity
    """
>>>>>>> 9253cec (fixed)
    mult = ['mono', 'di', 'tri', 'tetra', 'penta', 'hexa', 'hepta', 'octa', 'nona',
            'deca', 'undeca', 'dodeca', 'trideca', 'tetradeca', 'pentadeca', 'hexadeca', 'heptadeca',
            'octadeca', 'nonadeca', 'icosa', 'cosa', 'henicosa', 'docoasa', 'tricosa', 'tetracosa', 'pentacosa',
            'hexacosa', 'heptacosa', 'octacosa', 'nonacosa']
    mult = '('+'|'.join(mult)+')-?'
    return mult


def get_ph(paragraph):
    """
    A regex function to extract pH from text
    """
    pH_regex = r"(\d+\.\d+)\s*p\s*h|\s*p\s*h\s*(\d+\.\d+)|(\d+\.\d+)\s*(acidic|acid|neutral|base|basic)|\s*(acidic|acid|neutral|base|basic)\s*(\d+\.\d+)"
    matches = re.findall(pH_regex, paragraph)
    return matches


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
    pre_conj = prepositions_and_conjunctions(
    ) + ['h', "condensate", '', 'each', 'd', 'D', 'and']
    extracted_data = {}
    pattern_to_filter = re.compile(r'^[Tt]afl[omn]$|[Tt]eflo[nm]$')
    chemicals_list = [
        chemical for chemical in chemicals_list if not pattern_to_filter.match(chemical)]
    unit_pattern = re.compile(r'[mM][lL]|milliliter')
    for chemical in chemicals_list:
        tmp = []
        adj_chemical = r'\[?'+re.escape(chemical)+r'\]?'
        pattern = rf'(\d+(?:\.\d+)?)\s*(?:([a-zA-Z]+))?\s+(?:of\s+)?({(adj_chemical)})|(?:({(adj_chemical)})\s+(\d+(?:\.\d+)?))\s*(?:([a-zA-Z]+))?$|{(adj_chemical)}\s*\(([\d.]+)\s*(\w+)\s*,\s*([\d.]+)\s*(\w+)\)|{adj_chemical}\s*\(([\d.]+)\s*(?:([a-zA-Z]+))\)'
        matches = re.findall(pattern, paragraph)
        for match in matches:
            match = [[match[i], match[i+1]] for i in range(0, len(match), 2)]
            match = [i for i in match if len(i) == 2]
            match = [{'quantity': qty_unit[0], 'unit': standardize_units(qty_unit[1])} for qty_unit in match if all(
                string not in pre_conj for string in qty_unit)]
            tmp.extend(match)
        if chemical == 'H2O':
            tmp = [qty_unit for qty_unit in tmp if unit_pattern.match(
                qty_unit['unit'])]
        if len(tmp) > 0:
            if chemical == 'DI':
                chemical = 'deionised water'
            elif chemical == 'H2O':
                chemical = 'water'
            if isinstance(chemical, tuple) or isinstance(chemical, list):
<<<<<<< HEAD
                if len(chemical[0])> 0:
                    print ('len', chemical[0])
                    chemical = chemical[0]
                elif len(chemical[1])> 0:
                    chemical = chemical[1]
                elif len(chemical[2])> 0:
=======
                if len(chemical[0]) > 0:
                    print('len', chemical[0])
                    chemical = chemical[0]
                elif len(chemical[1]) > 0:
                    chemical = chemical[1]
                elif len(chemical[2]) > 0:
>>>>>>> 9253cec (fixed)
                    chemical = chemical[2]
            else:
                chemical = solvent_abbreviation(chemical)
            extracted_data[chemical] = tmp
            # extracted_data[chemical] = tmp
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
<<<<<<< HEAD


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


def metal_atom_dic():
    '''
    creating a reg pattern to find metal 
    '''
    metals_dic = {
        'Li': '[Ll]ithium',
        'Na': '[Ss]odium',
        'Mg': '[Mm]agnesium',
        'Al': '[Aa]lumin(ium|um|o)',
        'Ca': '[cC]alcium',
        'Sc': '[Ss]candium',
        'K': '[pP]otassium',
        'Ti': '[Tt]itanium|[Tt]itanous|[Tt]itanic',
        'V': '[Vv]anadium|[vV]anadous|[Vv]anadic',
        'Cr': '[Cc]hromium|[cC]hromous|[cC]hromic',
        'Mn': '[Mm]anganese|[Mm]anganous|[Mm]anganic',
        'Fe': '[Ii]ron|[Ff]errous|[Ff]erric',
        'Co': '[Cc]obalt|[cC]obaltous|[Cc]obaltic',
        'Ni': '[Nn]ickel|[nN]ickelous|[Nn]ickelic',
        'Cu': '[Cc]opper|[cC]uprous|[Cc]upric',
        'Zn': '[Zz]inc',
        'Ha': 'Gallium',
        'Rb': '[Rr]ubidium',
        'Sr': '[Ss]trontium',
        'Y': '[Yy]ttrium',
        'Zr': '[Zz]irconium',
        'Nb': '[Nn]iobium',
        'Mo': '[Mm]olybdenum',
        'Tc': 'Technetium',
        'Ru': '[rR]uthenium',
        'Rh': '[Rr]hodium',
        'Pd': '[Pp]alladium',
        'Cd': '[Cc]admium',
        'In': '[Ii]ndium',
        'Sn': '[tT]in|[sS]tannous|[Ss]tannic',
        'Cs': '[Cc]esium',
        'Ba': '[Bb]arium',
        'La': '[lL]anthanium|[lL]anthanide',
        'Ln': '[lL]anthanium|[lL]anthanide',
        'Ce': '[Cc]erium',
        'Pr': '[pP]raseodymium',
        'Nd': '[Nn]eodymium',
        'Pm': '[Pp]romethium',
        'Sm': '[Ss]amarium',
        'Eu': '[E]uropium',
        'Gd': '[Gg]adolinium',
        'Tb': '[Tt]erbium',
        'Dy': '[Dd]ysprosium',
        'Ho': '[Hh]olmium',
        'Er': '[Ee]rbium',
        'Tm': '[Tt]hulium',
        'Yb': '[Yy]tterbium',
        'Lu': '[Ll]utetium',
        'Hf': '[Hh]afnium',
        'Ta': '[Tt]antalum',
        'W': '[Tt]ungsten',
        'Re': '[Rr]henium',
        'Os': '[Os]mium',
        'Ir': '[Ii]ridium',
        'Pt': '[Pp]latinum',
        'Au': '[Gg]old|[aA]urous|[Aa]uric',
        'Hg': '[Mm]ercury|[mM]ercurous|[m]Mercuric',
        'Tl': '[Tt]hallium',
        'PB': '[Ll]ead|[pP]lumbous|[Pp]lumbic',
        'Bi': '[Bb]ismuth',
        'Po': '[Pp]olonium',
        'Fr': '[Ff]rancium',
        'Ra': '[Rr]adium',
        'Ac': '[Aa]ctinium',
        'Th': '[Tt]horium',
        'Pa': '[Pp]rotactinium',
        'U': '[Uu]ranium',
        'Np': '[Nn]eptunium',
        'PU': '[Pp]lutonium',
        'Am': '[Aa]mericium',
        'Cm': '[Cc]urium',
        'Bk': '[Bb]erkelium',
        'Cf': '[cC]alifornium',
        'Es': '[eE]insteinium',
        'Fm': '[Ff]ermium',
        'Md': '[mM]endelevium',
        'No': '[Nn]obelium',
        'Lr': '[Ll]awrencium',
        'Rf': '[Rr]utherfordium',
        'Db': '[Dd]ubnium',
        'Sg': '[Ss]eaborgium',
        'Bh': '[Bb]ohrium',
        'Hs': '[Hh]assium',
        'Mt': '[Mm]eitnerium',
        'Ds': '[dD]armstadtium',
        'Rg': '[Rr]oentgenium',
        'Cn': '[cC]opernicium',
        'Uut': '[Uu]nuntrium',
        'Fl': '[Ff]levorium',
        'Lv': '[Ll]ivermorium'
    }
    # full_name = [metals_dic[metal] for metal in list_of_metals]
    # pattern = r'\b('+'|'.join(full_name+list_of_metals) +r')\b'
    return metals_dic


def standardize_units(unit):
    unit = unit.lower()
    all_units = {
        'ml': 'milliliter',
        'g': 'gram',
        'mg': 'milligram',
        'gm': 'milligram',
        'mmol': 'millimole',
        'µmol': 'micromole',
        'µg': 'microgram',
        'µl': 'microliter',
        'l': 'liter',
        'kg': 'kilogram',
        'm': 'molar',
        'µm': 'micromolar'
    }
    if unit in list(all_units.keys()):
        return all_units[unit]
    else:
        return unit


def prepositions_and_conjunctions():
    prep = ['aboard', 'about', 'above', 'across',
            'after', 'against', 'along', 'amid',
            'amidst', 'among', 'around', 'as', 'at',
            'before', 'behind', 'below', 'beneath',
            'beside', 'between', 'beyond', 'but', 'by',
            'concerning', 'considering', 'despite', 'down',
            'during', 'except', 'for', 'from', 'in',
            'inside', 'into', 'like', 'near', 'of',
            'off', 'on', 'onto', 'out', 'outside',
            'over', 'past', 'regarding', 'round',
            'since', 'through', 'throughout', 'to',
            'toward', 'towards', 'under', 'underneath',
            'unlike', 'until', 'unto', 'up', 'upon',
            'with', 'within', 'without', "each"
            ]
    conj = ['and', 'but', 'or', 'yet', 'so', 'for',
            'nor', 'although', 'as', 'because',
            'before', 'if', 'once', 'since',
            'than', 'that', 'though', 'till',
            'unless', 'until', 'when', 'where',
            'while'
            ]
    return prep+conj
=======


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


def metal_atom_dic():
    '''
    creating a reg pattern to find metal
    '''
    metals_dic = {
        'Li': '[Ll]ithium',
        'Na': '[Ss]odium|[Ss]odmium',
        'Mg': '[Mm]agnesium|[mM]agnesium',
        'Al': '[Aa]lumin(ium|um|o|ate)',
        'Ca': '[cC]alcium',
        'Sc': '[Ss]candium',
        'K': '[pP]otassium|[pP]otaasium',
        'Ti': '[Tt]itanium|[Tt]itanous|[Tt]itanic|[Tt]itanate',
        'V': '[Vv]anadium|[vV]anadous|[Vv]anadic',
        'Cr': '[Cc]hromium|[cC]hromous|[cC]hromic|[cC]hromate',
        'Mn': '[Mm]anganese|[Mm]anganous|[Mm]angan(ic|ate)',
        'Fe': '[Ii]ron|[Ff]errous|[Ff]erric|[Ff]errate',
        'Co': '[Cc]obalt|[cC]obaltous|[Cc]obaltic',
        'Ni': '[Nn]ickel|[nN]ickelous|[Nn]ickelic',
        'Cu': '[Cc]opper|[cC]uprous|[Cc]upr(ic|ate)',
        'Zn': '[Zz]inc',
        'Ha': 'Gallium',
        'Rb': '[Rr]ubidium',
        'Sr': '[Ss]trontium|stontium',
        'Y': '[Yy]ttrium',
        'Zr': '[Zz]irconium|[zZ]irconiun|[zZ]irconinum|zirconim|zirconiuum',
        'Nb': '[Nn]iobium',
        'Mo': '[Mm]olybdenum',
        'Tc': 'Technetium',
        'Ru': '[rR]uthenium',
        'Rh': '[Rr]hodium',
        'Pd': '[Pp]alladium',
        'Cd': '[Cc]admium|[cC]admiu',
        'In': '[Ii]ndium',
        'Sn': '[tT]in|[sS]tannous|[Ss]tannic',
        'Cs': '[Cc]esium',
        'Ba': '[Bb]arium|[bB]airium|abrium',
        'La': '[lL]anthanium|[lL]anthan(ide|ate)|[lL]athanum',
        # 'Ln': '[lL]anthanium|[lL]anthanide',
        'Ce': '[Cc]erium',
        'Pr': '[pP]raseodymium|[Pp]raseodimium|[Pp]raseodimium',
        'Nd': '[Nn]eodymium|[nN]eodmium',
        'Pm': '[Pp]romethium',
        'Sm': '[Ss]amarium',
        'Eu': '[E]uropium',
        'Gd': '[Gg]adolinium',
        'Tb': '[Tt]erbium',
        'Dy': '[Dd]ysprosium|[dD]ypsrosium',
        'Ho': '[Hh]olmium',
        'Er': '[Ee]rbium',
        'Tm': '[Tt]hulium',
        'Yb': '[Yy]tterbium|ytterbum',
        'Lu': '[Ll]utetium',
        'Hf': '[Hh]afnium',
        'Ta': '[Tt]antalum',
        'W': '[Tt]ungsten',
        'Re': '[Rr]henium',
        'Os': '[Os]mium',
        'Ir': '[Ii]ridium',
        'Pt': '[Pp]latinum',
        'Au': '[Gg]old|[aA]urous|[Aa]uric',
        'Hg': '[Mm]ercury|[mM]ercurous|[m]Mercuric',
        'Tl': '[Tt]hallium',
        'PB': '[Ll]ead|[pP]lumbous|[Pp]lumbic',
        'Bi': '[Bb]ismuth|bismiuth',
        'Po': '[Pp]olonium',
        'Fr': '[Ff]rancium',
        'Ra': '[Rr]adium',
        'Ac': '[Aa]ctinium',
        'Th': '[Tt]horium',
        'Pa': '[Pp]rotactinium',
        'U': '[Uu]ranium',
        'Np': '[Nn]eptunium',
        'PU': '[Pp]lutonium',
        'Am': '[Aa]mericium',
        'Cm': '[Cc]urium',
        'Bk': '[Bb]erkelium',
        'Cf': '[cC]alifornium',
        'Es': '[eE]insteinium',
        'Fm': '[Ff]ermium',
        'Md': '[mM]endelevium',
        'No': '[Nn]obelium',
        'Lr': '[Ll]awrencium',
        'Rf': '[Rr]utherfordium',
        'Db': '[Dd]ubnium',
        'Sg': '[Ss]eaborgium',
        'Bh': '[Bb]ohrium',
        'Hs': '[Hh]assium',
        'Mt': '[Mm]eitnerium',
        'Ds': '[dD]armstadtium',
        'Rg': '[Rr]oentgenium',
        'Cn': '[cC]opernicium',
        'Uut': '[Uu]nuntrium',
        'Fl': '[Ff]levorium',
        'Lv': '[Ll]ivermorium',
        'Pb': '[Ll]ead|[lL]aed',
        'Ag': '[Ss]ilver|siler|siliver'
    }
    return metals_dic


def element_name_to_symbol(element):
    '''
    A function that returns the chemical symbol of an element
    '''
    if re.match('[Ll]ithium', element):
        return 'Li'
    elif re.match('[Ss]odium|[Ss]odmium', element):
        return 'Na'
    elif re.match('[Mm]agnesium|[mM]agnesium', element):
        return 'Mg'
    elif re.match('[Aa]lumin(ium|um|o|ate)', element):
        return 'Al'
    elif re.match('[cC]alcium', element):
        return 'Ca'
    elif re.match('[Ss]candium', element):
        return 'Sc'
    elif re.match('[pP]otassium|[pP]otaasium', element):
        return 'K'
    elif re.match('[Tt]itanium|[Tt]itanous|[Tt]itanic|[Tt]itanate', element):
        return 'Ti'
    elif re.match('[Vv]anadium|[vV]anadous|[Vv]anadic', element):
        return 'V'
    elif re.match('[Cc]hromium|[cC]hromous|[cC]hromic|[cC]hromate', element):
        return 'Cr'
    elif re.match('[Mm]anganese|[Mm]anganous|[Mm]angan(ic|ate)', element):
        return 'Mn'
    elif re.match('[Ii]ron|[Ff]errous|[Ff]erric|[Ff]errate', element):
        return 'Fe'
    elif re.match('[Cc]obalt|[cC]obaltous|[Cc]obaltic', element):
        return 'Co'
    elif re.match('[Nn]ickel|[nN]ickelous|[Nn]ickelic', element):
        return 'Ni'
    elif re.match('[Cc]opper|[cC]uprous|[Cc]upr(ic|ate)', element):
        return 'Cu'
    elif re.match('[Zz]inc', element):
        return 'Zn'
    elif re.match('Gallium', element):
        return 'Ha'
    elif re.match('[Rr]ubidium', element):
        return 'Rb'
    elif re.match('[Ss]trontium|stontium', element):
        return 'Sr'
    elif re.match('[Yy]ttrium', element):
        return 'Y'
    elif re.match('[Zz]irconium|[zZ]irconiun|[zZ]irconinum|zirconim|zirconiuum', element):
        return 'Zr'
    elif re.match('[Nn]iobium', element):
        return 'Nb'
    elif re.match('[Mm]olybdenum', element):
        return 'Mo'
    elif re.match('Technetium', element):
        return 'Tc'
    elif re.match('[rR]uthenium', element):
        return 'Ru'
    elif re.match('[Rr]hodium', element):
        return 'Rh'
    elif re.match('[Pp]alladium', element):
        return 'Pd'
    elif re.match('[Cc]admium|[cC]admiu', element):
        return 'Cd'
    elif re.match('[Ii]ndium', element):
        return 'In'
    elif re.match('[tT]in|[sS]tannous|[Ss]tannic', element):
        return 'Sn'
    elif re.match('[Cc]esium', element):
        return 'Cs'
    elif re.match('[Bb]arium|[bB]airium|abrium', element):
        return 'Ba'
    elif re.match('[lL]anthanium|[lL]anthan(ide|ate)|[lL]athanum', element):
        return 'La'
    elif re.match('[Cc]erium', element):
        return 'Ce'
    elif re.match('[pP]raseodymium|[Pp]raseodimium|[Pp]raseodimium', element):
        return 'Pr'
    elif re.match('[Nn]eodymium|[nN]eodmium', element):
        return 'Nd'
    elif re.match('[Pp]romethium', element):
        return 'Pm'
    elif re.match('[Ss]amarium', element):
        return 'Sm'
    elif re.match('[E]uropium', element):
        return 'Eu'
    elif re.match('[Gg]adolinium', element):
        return 'Gd'
    elif re.match('[Tt]erbium', element):
        return 'Tb'
    elif re.match('[Dd]ysprosium|[dD]ypsrosium', element):
        return 'Dy'
    elif re.match('[Hh]olmium', element):
        return 'Ho'
    elif re.match('[Ee]rbium', element):
        return 'Er'
    elif re.match('[Tt]hulium', element):
        return 'Tm'
    elif re.match('[Yy]tterbium|ytterbum', element):
        return 'Yb'
    elif re.match('[Ll]utetium', element):
        return 'Lu'
    elif re.match('[Hh]afnium', element):
        return 'Hf'
    elif re.match('[Tt]antalum', element):
        return 'Ta'
    elif re.match('[Tt]ungsten', element):
        return 'W'
    elif re.match('[Rr]henium', element):
        return 'Re'
    elif re.match('[Os]mium', element):
        return 'Os'
    elif re.match('[Ii]ridium', element):
        return 'Ir'
    elif re.match('[Pp]latinum', element):
        return 'Pt'
    elif re.match('[Gg]old|[aA]urous|[Aa]uric', element):
        return 'Au'
    elif re.match('[Mm]ercury|[mM]ercurous|[m]Mercuric', element):
        return 'Hg'
    elif re.match('[Tt]hallium', element):
        return 'Tl'
    elif re.match('[Ll]ead|[pP]lumbous|[Pp]lumbic', element):
        return 'PB'
    elif re.match('[Bb]ismuth|bismiuth', element):
        return 'Bi'
    elif re.match('[Pp]olonium', element):
        return 'Po'
    elif re.match('[Ff]rancium', element):
        return 'Fr'
    elif re.match('[Rr]adium', element):
        return 'Ra'
    elif re.match('[Aa]ctinium', element):
        return 'Ac'
    elif re.match('[Tt]horium', element):
        return 'Th'
    elif re.match('[Pp]rotactinium', element):
        return 'Pa'
    elif re.match('[Uu]ranium', element):
        return 'U'
    elif re.match('[Nn]eptunium', element):
        return 'Np'
    elif re.match('[Pp]lutonium', element):
        return 'PU'
    elif re.match('[Aa]mericium', element):
        return 'Am'
    elif re.match('[Cc]urium', element):
        return 'Cm'
    elif re.match('[Bb]erkelium', element):
        return 'Bk'
    elif re.match('[cC]alifornium', element):
        return 'Cf'
    elif re.match('[eE]insteinium', element):
        return 'Es'
    elif re.match('[Ff]ermium', element):
        return 'Fm'
    elif re.match('[mM]endelevium', element):
        return 'Md'
    elif re.match('[Nn]obelium', element):
        return 'No'
    elif re.match('[Ll]awrencium', element):
        return 'Lr'
    elif re.match('[Rr]utherfordium', element):
        return 'Rf'
    elif re.match('[Dd]ubnium', element):
        return 'Db'
    elif re.match('[Ss]eaborgium', element):
        return 'Sg'
    elif re.match('[Bb]ohrium', element):
        return 'Bh'
    elif re.match('[Hh]assium', element):
        return 'Hs'
    elif re.match('[Mm]eitnerium', element):
        return 'Mt'
    elif re.match('[dD]armstadtium', element):
        return 'Ds'
    elif re.match('[Rr]oentgenium', element):
        return 'Rg'
    elif re.match('[cC]opernicium', element):
        return 'Cn'
    elif re.match('[Uu]nuntrium', element):
        return 'Uut'
    elif re.match('[Ff]levorium', element):
        return 'Fl'
    elif re.match('[Ll]ivermorium', element):
        return 'Lv'
    elif re.match('[Ll]ead|[lL]aed', element):
        return 'Pb'
    elif re.match('[Ss]ilver|siler|siliver', element):
        return 'Ag'


def standardize_units(unit):
    unit = unit.lower()
    all_units = {
        'ml': 'milliliter',
        'g': 'gram',
        'mg': 'milligram',
        'gm': 'milligram',
        'mmol': 'millimole',
        'µmol': 'micromole',
        'µg': 'microgram',
        'µl': 'microliter',
        'l': 'liter',
        'kg': 'kilogram',
        'm': 'molar',
        'µm': 'micromolar'
    }
    if unit in list(all_units.keys()):
        return all_units[unit]
    else:
        return unit


def prepositions_and_conjunctions():
    prep = ['aboard', 'about', 'above', 'across',
            'after', 'against', 'along', 'amid',
            'amidst', 'among', 'around', 'as', 'at',
            'before', 'behind', 'below', 'beneath',
            'beside', 'between', 'beyond', 'but', 'by',
            'concerning', 'considering', 'despite', 'down',
            'during', 'except', 'for', 'from', 'in',
            'inside', 'into', 'like', 'near', 'of',
            'off', 'on', 'onto', 'out', 'outside',
            'over', 'past', 'regarding', 'round',
            'since', 'through', 'throughout', 'to',
            'toward', 'towards', 'under', 'underneath',
            'unlike', 'until', 'unto', 'up', 'upon',
            'with', 'within', 'without', "each"
            ]
    conj = ['and', 'but', 'or', 'yet', 'so', 'for',
            'nor', 'although', 'as', 'because',
            'before', 'if', 'once', 'since',
            'than', 'that', 'though', 'till',
            'unless', 'until', 'when', 'where',
            'while'
            ]
    return prep+conj


def metal_pattern(metals):
    '''
    function that takes a list of metals and return a regex pattern
    '''
    pattern_list = []
    metals_dic = metal_atom_dic()
    for i in list(set(metals)):
        pattern_list.append(i)
        if i in list(metals_dic.keys()):
            pattern_list.append(metals_dic[i])
        try:
            symbol = element_name_to_symbol(i)
            if symbol is not None:
                pattern_list.append(symbol)
                pattern_list.append(metals_dic[symbol])

        except:
            pass


    return re.compile('|'.join(pattern_list))


def solvent_chemical_names():
    """
    Names of solvents
    """
    solvent_list = [
        'THF', 'acetone', 'acetone', 'chloroform', 'methanol',
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
        'di-n-butylether', 'di-n-hexylether', 'dibromoethane', 'dibutoxymethane',
        'dibutylether', 'dichloro-methane', 'dichlorobenzene', 'dichloroethane',
        'dichloromethane', 'diethoxymethane', 'diethylcarbonate', 'diethylether',
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
        'trimethyl pentane', 'undecan-1-ol', 'undecanol', 'valeronitrile', 'water',
        'xylene', 'xylol', 'N,N-diethylformamide',
        '[nBu4N][BF4]', 'BCN', 'ACN', 'BTN', 'BHDC', 'AOT', 'DMA',
        'MOPS',  'MES', 'heavy water', 'IPA', 'methanolic', 'water'
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
        'ethyl propionate', 'dimethyl acetamide', 'dibutyl ether', 'H2O TX', 'dimethyl sulfoxide',
        'CD2Cl2', 'methyl pyrrolidine', 'C2H5OH', 'butyl alcohol', 'TEOA', '(CD3)2CO',
        'methylene chloride', 'SDS', 'KPB', 'TBAF', 'ethyl acetate', 'SNO2', 'methyl propan-1-ol',
        'C6H14', 'methyl acetoacetate', 'butyl acetate', 'MeOD', 'hexyl ether',
        'cyclopentyl methyl ether', 'NPA', 'ethyl benzoate', '2-propyl acetate',
        'Na2SO4', 'C6H5Cl', 'methyl formamide', 'CH3CO2H', 'methyl pentane', 'TBAPF6',
        'H2O-Triton X', 'CH2ClCH2Cl', 'sodium chloride', 'Triton X-100', 'HDA',
        'di-n-hexyl ether', 'potassium iodide', 'potassium bromide', 'potassium chloride',
        'potassium floride', 'KI', 'KF', 'KCl', 'KBr' 'sodium iodide','sodium bromide',
        'sodium floride', 'NaI', 'NaF', 'NaCl', 'NaBr', 'DI-water', 'water', "formaldehyde",
        "CH2O","HCHO", "1,2-diaminocyclohexane", "Benzene", "Carbon tetrachloride",
        "1,2-Dichloroethane", "1,1-Dichloroethene", "1,1,1-Trichloroethane", "Acetonitrile",
        "Chlorobenzene", "Chloroform", "Cyclohexane", "Cumene", "1,2-Dichloroethene", "Dichloromethane",
        "1,2-Dimethoxyethane", "N,N-Dimethylacetamide", "N,N-Dimethylformamide", "1,4-Dioxane",
        "2-Ethoxyethanol", "Ethyleneglycol", "Formamide", "Hexane", "Methanol", "2-Methoxyethanol",
        "Methylbutyl ketone", "Methylcyclohexane", "Methylisobutylketone", "N-Methylpyrrolidone",
        "Nitromethane", "Pyridine", "Sulfolane", "Tetrahydrofuran", "Tetralin", "Toluene",
        "1,1,2-Trichloroethene", "Xylene", "Acetic acid", "Acetone", "Anisole", "1-Butanol",
        "2-Butanol", "Butyl acetate", "tert-Butylmethyl ether", "Dimethyl sulfoxide",
        "Ethanol", "Ethyl acetate", "Ethyl ether", "Ethyl formate", "Formic acid", "Heptane",
        "Isobutyl acetate", "Isopropyl acetate", "Methyl acetate", "3-Methyl-1-butanol",
        "Methylethyl ketone", "2-Methyl-1-propanol", "Pentane", "1-Pentanol", "1-Propanol",
        "2-Propanol", "Propyl acetate", "Triethylamine", "1,1-Diethoxypropane", "1,1-Dimethoxymethane",
        "2,2-Dimethoxypropane", "Isooctane", "Isopropyl ether", "Methylisopropyl ketone", "Methyltetrahydrofuran",
        "Petroleum ether", "Trichloroacetic acid", "Trifluoroacetic acid"
    ]
    return solvent_list


def clean_hydrate_spaces(chemical_name):
    """
    Removes spaces surrounding the '·' symbol in hydrated compounds.
    Example: 'Ni(CH3COO)2 · 4H2O' -> 'Ni(CH3COO)2·4H2O'
    """
    return re.sub(r'\s*·\s*', '·', chemical_name)


def convert_metal_ions(chemical_name):
    """
    Converts metal oxidation states to proper format.
    Example: 'CuII' -> 'Cu2+', 'Cu2' -> 'Cu2+'
    """
    metals = ['Li', 'Be', 'Ba', 'Mg', 'Al', 'Ka', 'Ca', 'Sc', 'Ti', 'V',
              'Cr', 'Mn','Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ha', 'Rb', 'Sr',
              'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
              'In', 'Sn', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm',
              'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf',
              'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Ti', 'Pb',
              'Bi', 'Po', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu',
              'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf',
              'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Uut', 'Fl', 'Lv']

    metals_regex = '|'.join(metals)

    # Ensures oxidation states appear alone and not as part of a chemical formula (e.g., BiI3)
    return re.sub(rf'\b({metals_regex})([IVXLCDM]+|[0-9]+)\b(?![a-z0-9])',
                  lambda m: f"{m.group(1)}{m.group(2).replace('I', '1+').replace('II', '2+').replace('III', '3+').replace('IV', '4+').replace('V', '5+').replace('VI', '6+').replace('VII', '7+').replace('VIII', '8+')}",
                  chemical_name)


def extract_metal_salt(chemical_name):
    """
    Extracts the metal salt from complex chemical names.
    Example: 'Co(OAc)2·2H2O/H2dpa/1,10′-phen1:2:1' -> 'Co(OAc)2·2H2O'
    """
    match = re.search(r'([A-Z][a-z]?[\w()]+·?\d*H?2?O?)', chemical_name)
    return match.group(1) if match else chemical_name


def process_chemical_name(chemical_name):
    """
    Process the chemical name through all transformation functions.
    """
    cleaned_name = clean_hydrate_spaces(chemical_name)
    # converted_name = convert_metal_ions(cleaned_name)
    return cleaned_name

def is_chemical_formula(salt):
    """Check if the given salt is written in chemical formula notation."""
    # A regex pattern to check if the input contains chemical symbols and formula notation
    formula_pattern = re.compile(r"[A-Z][a-z]?\d*|\(|\)|\.|\[|\]|\d+")

    # A regex pattern to check for common full name patterns (words with parentheses for oxidation states)
    full_name_pattern = re.compile(r"[A-Za-z]+(\(\w+\))?\s?[a-z]*")

    # Check which pattern matches better
    formula_match = formula_pattern.findall(salt)
    full_name_match = full_name_pattern.findall(salt)

    # If more chemical formula-like patterns are found, classify as a formula
    if len(formula_match) > len(full_name_match):
        return True
    elif len(formula_match) == len(full_name_match):
        return True
    else:
        return False

def correct_spacing(chemical_name):
    """
    Corrects spacing around parentheses in chemical names.
    Example: '(Cu( II ) 2)' -> '(Cu(II)2)'
    """
    corrected_name = re.sub(r'\(\s*([1ivxIVX]+)\s*\)', r'(\1)', chemical_name)
    return corrected_name


def get_chemical_formula(chemical_name):
    """Fetch the molecular formula of a given chemical name using PubChemPy."""
    try:
        compound = pcp.get_compounds(chemical_name, 'name')
        if compound:
            composition = Composition(compound[0].molecular_formula)
            ion = Ion(composition)
            return ion.get_reduced_formula_and_factor(hydrates=True)[0]
        else:
            return chemical_name  # Return name if formula not found
    except Exception:
         return chemical_name  # Handle errors gracefully



def filter_common_names(synonyms):
    exclude_keywords = [
        "DTXSID", "NSC", "CHEMBL", "MFCD", "DTXCID", "CCRIS", "BDBM",
        "EPA", "HSDB", "NCIOpen", "AKOS", "HY-", "SB", "DB", "Tox21",
        "Beilstein", "Open", "InChI", "SMILES", "Canonical", "Aktisal",
        "[Dutch]", "[German]", "[French]", "Acido", "Acide", "99.999%",
        "purified", "AI3", "CHEBI", "9E7R5L6H31", "EC ", "CAS", "OXD",
        "IMPURITY", "%", "Vetec", "AS-", "SY", "N0", "D91724", "CI",
        "EINECS", "WLN:", "Activate", "microg/mL", "micro", "milli",
        "gram", "kilo", "nano", "pico", "femto", "atto", "centi", "[Czech]",
        "g/L", "mg/L", "ug/L", "ng/L", "pg/L", "fg/L", "ag/L", "g/mL"
    ]

    pattern_three_digit = re.compile(r'\b(?=.*\d{3,})_?\d+(?:-\d+)*\b')
    pattern_false_name = re.compile(r'''^(?!.*(?:zuur|red|blue|green|yellow|black|violet|purple|
                                    color|white|cyan|orange|pink|brown|grey|gray|silver|gold|metal|oxide|
                                    salt|acid|base|solution|liquid|solid|powder|crystal|compound|complex|
                                    product|reagent|catalyst|precursor|material|substance|element|metal|
                                    nonmetal|organic|inorganic|organometallic|organometalloid|organometal|
                                    Honey|USP|HPLC|VANDF|Toxic|ppm|MART.|FHFI|FCC|GRAPH|grade|suitable|
                                    Taimax|salt|stavelova|saeure|uisal|velova|doi|standard|natural|UN|
                                    WHO|Spectrophotometry|AG-|ACS|FEMA|RCRA|brn\s*|Dutch|German|French|
                                    English|Danish|Swedish|Norwegian|Finnish|Dutch|German|Pressure|PSI|
                                    solvent|technical|IARC|WHO|EPA|USP|NF|BP|EP|JP|PhEur|Pharm|Pharmacopoeia|
                                    Guard|GC|HPLC|LC|MS|UV|IR|NMR|TLC|FTIR|FT-NMR|Eyebrow|Restore| U.S.P.|CVS|
                                    Secondary|primary|Reference|Standard|Reagent|Analytical|BioXtra|BioUltra|
                                    BioChemika|Cell Culture|Cell Biology|Cell Culture|Cell Biology|Cell Culture|
                                    Wilbur-Ellis Smut-Guard|Hand|Foot|Hoof|Horse|Pony|Cattle|Sheep|Goat|Swine|
                                    Poultry|Dog|Cat|Pet|Animal|Livestock|Pig|Horse|Pony|Cattle|Sheep|Goat|
                                    Swine|Poultry|Dog|Cat|Pet|Animal|Livestock|Pig|Horse|Pony|Cattle|Sheep|Body|
                                    arm|leg|forearm|foreleg|upper arm|upper leg|lower arm|lower leg|Get|Set|Go|gel|
                                    santizer|Rubbing|#|

                                    tested|Polish|Spanish|Italian|Japanese|Chinese|Russian|Korean|Portuguese)).+$''', re.IGNORECASE)
    pattern_code_with_dash = re.compile(r'^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+$')
    cas_pattern = re.compile(r'^\d{2,7}-\d{2}-\d$')

    def is_common_name(syn):
        syn_lower = syn.lower()

        if any(kw.lower() in syn_lower for kw in exclude_keywords):
            return False

        if pattern_three_digit.match(syn):
            return False

        if syn.startswith('/'):
            return False

        if not pattern_false_name.match(syn):
            return False

        if pattern_code_with_dash.match(syn):
            return False

        if not re.search(r'[a-zA-Z]', syn):
            return False

        if re.fullmatch(r'[A-Za-z]+[0-9]{3,}', syn):
            return False

        if ' ' in syn or syn.isalpha():
            return True

        return is_valid_formula(syn) if syn.isalnum() else False

    return [syn for syn in synonyms if is_common_name(syn)]

>>>>>>> 9253cec (fixed)
