#!/usr/bin/python
from __future__ import print_function

__author__ = "Dr. Dinga Wonanke"
__status__ = "production"

import re
import spacy
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union, Iterable
from pathlib import Path

from mofsyncondition.doc import convert_html_to_text
from mofsyncondition.conditions import conditions_extraction
from mofsyncondition.conditions import chemical_entity_regex
from mofsyncondition.synparagraph import extract_synthesis_paragraphs
from mofsyncondition.doc import doc_parser

ParagraphInput = Union[str, Path, List[str], Iterable[str]]

nlp = spacy.load("en_chem_ner")


@dataclass
class MOFSynConditionExtractor:
    """
    A class for extracting MOF synthesis paragraphs and structured
    synthesis conditions from scientific documents.

    Notes
    -----
    This class caches compiled regex patterns and configuration so repeated
    calls over many paragraphs/documents are faster and consistent.
    """

    paragraph_model: str = "NN_tfv"
    characterisation_labels: set = field(
        default_factory=lambda: {
            "characterization",
            "characterisation",
            "melting_temperature",
            "nmr",
            "ir",
            "raman",
            "elemental_analysis",
            "tga",
            "dsc",
        }
    )
    tokenizer: Callable[[str], Tuple[List[str], Any]] = doc_parser.tokenize_doc
    _solvents_pattern: Any = field(init=False, repr=False)
    _modulators_pattern: Any = field(init=False, repr=False)
    _method_pattern: Any = field(init=False, repr=False)
    _mof_alias_list: Any = field(init=False, repr=False)
    _metal_precursor_pattern: Any = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """
        Initialize cached patterns.
        """
        self._solvents_pattern = chemical_entity_regex.solvents_regex()
        self._modulators_pattern = chemical_entity_regex.modulators_regex()
        self._method_pattern = chemical_entity_regex.synthetic_method_re()
        self._mof_alias_list = chemical_entity_regex.mof_regex()
        self._metal_precursor_pattern = self._build_metal_precursor_pattern()

    def _build_metal_precursor_pattern(self) -> re.Pattern:
        """
        Build and compile the metal precursor regex pattern once.

        Returns
        -------
            pattern: re.Pattern
                Compiled regex pattern for matching metal precursor tokens.
        """
        metals = chemical_entity_regex.metal_atom_dic()
        metals_items = list(metals.items())
        all_metals = "|".join([m for metal_tuple in metals_items for m in metal_tuple])

        multiplicity = chemical_entity_regex.iupac_multiplicity()

        # multiplicity optional, metals grouped safely
        pattern_str = r"\b(?:{mult})?(?:{metals})\b".format(mult=multiplicity, metals=all_metals)
        return re.compile(pattern_str)

    def get_synthetic_paragraph(self, source: ParagraphInput, model: Optional[str] = None):
        """
        A function that extract synthetic paragraphs from a file or
        list of paragraphs. The function uses neural
        network with tfv model as default model
        to extract synthetic paragraphs.

        Parameters
        ----------
            source: str or Path or list of strings


            model: str.type
                The paragraph classification model to use.
                If None, uses self.paragraph_model.

        Returns
        -------
            synthetic_paragraphs: list of strings

        Notes:
        ------
            Potential models include:
                1. Models with TFV features:
                    NN_tfv : Neural Network with TFV model
                    RF_tfv : Random Forest with TFV model
                    SVM_tfv : Support Vector Machine with TFV model
                    LR_tfv : Logistic Regression with TFV model
                    NB_tfv : Naive Bayes with TFV model
                    DT_tfv : Decision Tree with TFV model
                2. Models with CV features:
                    NN_CV : Neural Network with CV model
                    RF_CV : Random Forest with CV model
                    SVM_CV : Support Vector Machine with CV model
                    LR_CV : Logistic Regression with CV model
                    NB_CV : Naive Bayes with CV model
                    DT_CV : Decision Tree with CV model
        """
        model = model or self.paragraph_model

        if isinstance(source, (str, Path)):
            paragraphs = convert_html_to_text.file_2_list_of_paragraphs(str(source))

        elif isinstance(source, (list, tuple)):
            paragraphs = list(source)

        else:
            try:
                paragraphs = list(source)
            except TypeError as e:
                raise TypeError(
                    "source must be a filepath (str/Path) or an iterable of paragraph strings"
                ) from e

        return extract_synthesis_paragraphs.all_synthesis_paragraphs(paragraphs, model=model)

    @staticmethod
    def _iter_chemicals(obj):
        """
        Internal helper to flatten chemical containers into a list of strings.
        """
        if obj is None:
            return []
        if isinstance(obj, str):
            return [obj]
        if isinstance(obj, dict):
            return [str(k) for k in obj.keys()]
        if isinstance(obj, (list, tuple, set)):
            out: List[str] = []
            for x in obj:
                out.extend(MOFSynConditionExtractor._iter_chemicals(x))
            return out
        return [str(obj)]

    def select_content_for_method(self, all_tokens, pattern):
        """
        function to extract content based on regex pattern

        Parameters:
        ------------
            all_tokens: list of strings
            pattern: compiled regular expression pattern

        Returns:
        --------
            contents: list of strings matching the pattern
        """
        contents: List[str] = []
        for i, token in enumerate(all_tokens):
            match = re.search(pattern, token)
            if match:
                if token.lower() == "evaporation":
                    prev = [t.lower() for t in all_tokens[max(0, i - 3): i]]
                    if "slow" in prev:
                        contents.append("slow evaporation")
                else:
                    contents.append(token)
        return list(set(contents))

    @staticmethod
    def select_content(all_tokens, list_content):
        """
        function to select content from a list of tokens based on a given list

        Parameters
        ----------
            all_tokens: list containing all strings
            list_content: list containing selected strings

        Returns:
        -------
            content: list containing selected strings from all_tokens
        """
        wanted = set(list_content)
        return [tok for tok in all_tokens if tok in wanted]

    def solvents_in_text(self, all_tokens):
        """
        A function to find solvents from a list of chemicals

        Parameters
        ----------
            all_tokens: list of strings
                List of chemical tokens.

        Returns
        -------
            solvents: list of strings
        """
        solvents: List[str] = []
        for token in all_tokens:
            s = token.strip()
            if self._solvents_pattern.fullmatch(s):
                solvents.append(s)
            else:
                solvents.extend([m.group(0) for m in self._solvents_pattern.finditer(token)])
        return list(set(solvents))

    def modulators_in_text(self, all_tokens):
        """
        A function to find modulators from a list of chemicals

        Parameters
        ----------
            all_tokens: list of strings
                List of chemical tokens.

        Returns
        -------
            modulators: list of strings
        """
        modulators: List[str] = []
        for token in all_tokens:
            s = token.strip()
            if self._modulators_pattern.fullmatch(s):
                modulators.append(s)
            else:
                modulators.extend([m.group(0) for m in self._modulators_pattern.finditer(token)])
        return list(set(modulators))

    def metal_precursors_in_text(self, all_tokens):
        """
        A function to extract metal precursors from a list of chemicals

        Parameters
        ----------
            tokens: list
                List of chemical tokens (strings, or nested containers).

        Returns
        -------
            metal_salt: list of strings
        """
        flat: List[str] = []
        for token in all_tokens:
            flat.extend(self._iter_chemicals(token))

        metal_salt = [chem for chem in flat if re.match(self._metal_precursor_pattern, chem)]
        return list(set(metal_salt))

    def mof_alias_in_text(self, all_tokens):
        """
        A function to find MOF aliases in a list of tokens

        Parameters
        ----------
            all_tokens: list of strings

        Returns
        -------
            mofs: list of strings
        """
        mofs: List[str] = []
        for token in all_tokens:
            s = str(token).strip()

            # if the whole token is a MOF alias
            if self._mof_alias_list.fullmatch(s):
                mofs.append(s)
            else:
                # if there are embedded matches inside the token
                mofs.extend([m.group(0) for m in self._mof_alias_list.finditer(s)])

        return list(set(mofs))

    def all_reaction_temperature(self, par_tokens, par_doc):
        """
        A function that extract temperature from tokens

        Parameters
        ----------
            par_tokens: list of strings
            par_doc: spacy-like doc object

        Returns
        -------
            temp_dict: dict
                Dictionary containing temperature information.
        """
        temperature = conditions_extraction.get_temperatures_toks(par_tokens)
        return chemical_entity_regex.reaction_temperature_breakdown2(temperature, par_doc)

    def all_reaction_time(self, par_tokens, par_doc):
        """
        A function that extract reaction time from tokens

        Parameters
        ----------
            par_tokens: list of strings
            par_doc: spacy-like doc object

        Returns
        -------
            time_dict: dict
                Dictionary containing time, token number and units
        """
        time_in_token = conditions_extraction.get_times_toks(par_tokens)
        return chemical_entity_regex.reaction_time_breakdown2(time_in_token, par_doc)

    def get_operating_conditions(self, par_tokens):
        """
        A function that extract operating conditions from tokens

        Parameters
        ----------
            par_tokens: list of strings

        Returns
        -------
            pressures: list of dict
                Extracted atmosphere/pressure-like operating conditions.
        """
        return conditions_extraction.get_atmosphere_toks(par_tokens)

    def get_synthetic_method(self, all_tokens):
        """
        A function to extract synthetic methods from a list of tokens

        Parameters
        ----------
            all_tokens: list of strings
                Tokenized paragraph tokens.

        Returns
        -------
            synthesis_method: list of strings
        """
        synthesis_method = self.select_content_for_method(all_tokens, self._method_pattern)
        synthesis_method = [m.capitalize() for m in synthesis_method]
        synthesis_method = [chemical_entity_regex.method_abbreviation(m) for m in synthesis_method]
        return list(set(synthesis_method))

    def find_organic_reagents(self, quantities, all_solvents):
        """
        guest organic reagens

        Parameters
        ----------
            quantities: dict
                Dictionary of extracted quantities keyed by chemical name.
            all_solvents: list
                List of solvent names to exclude.

        Returns
        -------
            organic_precursors: list
                Organic reagents excluding metal precursors and solvents.
        """
        organic_precursors: List[str] = []
        for element in list((quantities or {}).keys()):
            for chem in self._iter_chemicals(element):
                if not re.match(self._metal_precursor_pattern, chem):
                    organic_precursors.append(chem)

        solvents_set = set(all_solvents)
        return list({e for e in organic_precursors if e not in solvents_set})

    @staticmethod
    def collect_time_steps(time_obj):
        """
        A function to collect time steps from a time object

        Parameters:
        -----------
          time_obj: dict.type

        Returns:
        -------
          tmp_steps = [
            {"step": "stirring_mixing", "events": [ {raw, unit, text, ...}, ... ]},
            ...
          ]
        """
        tmp_steps: List[Dict[str, Any]] = []
        steps_list = (time_obj or {}).get("steps", []) or []
        for step_block in steps_list:
            step_name = step_block.get("step")
            events: List[Dict[str, Any]] = []
            for e in (step_block.get("events") or []):
                events.append(
                    {
                        "raw": e.get("value"),
                        "unit": e.get("unit"),
                        "text": e.get("text"),
                        "coarse_bucket": e.get("coarse_bucket"),
                        "context_labels": e.get("fine_labels", []),
                        "sentence": e.get("sentence", ""),
                        "override_bucket": e.get("override_bucket", ""),
                        "sent_start": e.get("sent_start", -1),
                    }
                )
            tmp_steps.append({"step": step_name, "events": events})
        return tmp_steps

    def extract_synthetic_info(self, par_text, chemical_names):
        """
        A function to extract synthetic information from paragraph text and chemical names

        Parameters
        ----------
            par_text: a string of paragraph text
            chemical_names: list of chemical names in the paragraph

        Returns
        -------
            data: a dictionary containing the extracted synthetic information
            data_2: a dictionary containing intermediate/raw extracted information
        """
        data: Dict[str, Any] = {}
        data_2: Dict[str, Any] = {}

        par_tokens, par_doc = self.tokenizer(par_text)

        chemical_names = chemical_entity_regex.clean_chemicals(list(chemical_names or []))

        all_solvents = self.solvents_in_text(chemical_names)
        all_modulators = self.modulators_in_text(chemical_names)

        mofs = self.mof_alias_in_text(chemical_names)
        metals = [i for i in self.metal_precursors_in_text(chemical_names) if i not in mofs]

        time = self.all_reaction_time(par_tokens, par_doc)
        temperature = self.all_reaction_temperature(par_tokens, par_doc)

        pH = conditions_extraction.get_ph_toks(par_tokens)
        pressures = self.get_operating_conditions(par_tokens)

        quantities = chemical_entity_regex.extract_chemical_quantities2(par_text, chemical_names)
        organic_reagents = self.find_organic_reagents(quantities, all_solvents)

        synthetic_methods = self.get_synthetic_method(par_tokens)

        reagents: List[Dict[str, Any]] = []
        for metal in metals:
            reagents.append({"name": metal, "role": "metal_precursor", "amount": quantities.get(metal, "")})
        for lig in organic_reagents:
            reagents.append({"name": lig, "role": "organic_reagent", "amount": quantities.get(lig, "")})
        for mod in all_modulators:
            reagents.append({"name": mod, "role": "modulator", "amount": quantities.get(mod, "")})
        for sol in all_solvents:
            reagents.append({"name": sol, "role": "solvent", "amount": quantities.get(sol, "")})
        for mof in mofs:
            reagents.append({"name": mof, "role": "mof name"})

        data_2["time"] = time
        data_2["temperature"] = temperature
        data_2["pH"] = pH
        data_2["pressures"] = pressures
        data_2["organic_reagents"] = organic_reagents
        data_2["metal_salts"] = metals
        data_2["modulators"] = all_modulators
        data_2["solvents"] = all_solvents
        data_2["mofs"] = mofs
        data_2["quantities"] = quantities
        data_2["chemical_names"] = chemical_names
        data_2["synthetic_methods"] = synthetic_methods

        data["chemical_reagents"] = reagents

        tmp_time: Dict[str, Any] = {}
        for t, d_t in (time.get("buckets", {}) or {}).items():
            tmp_d = []
            for item in d_t:
                ctx = item.get("context", {}) or {}
                tmp_d.append(
                    {
                        "raw": item.get("value"),
                        "unit": item.get("unit"),
                        "text": item.get("text"),
                        "step": ctx.get("chosen_fine"),
                        "context_labels": ctx.get("fine_labels", []),
                    }
                )
            tmp_time[t] = tmp_d

        temp_temperature: Dict[str, Any] = {}
        temp_characterisation: Dict[str, Any] = {}

        for t, d_t in (temperature or {}).items():
            tmp_temp = []
            tmp_char = []
            for item in d_t:
                ctx = item.get("context", {}) or {}
                fine_labels = ctx.get("fine_labels", []) or []

                entry = {
                    "raw": item.get("value"),
                    "unit": item.get("unit"),
                    "text": item.get("text"),
                    "context_labels": fine_labels,
                }

                if any(lbl in self.characterisation_labels for lbl in fine_labels):
                    tmp_char.append(entry)
                else:
                    tmp_temp.append(entry)

            if tmp_temp:
                temp_temperature[t] = tmp_temp
            if tmp_char:
                temp_characterisation[t] = tmp_char

        data["characterisation_temperatures"] = temp_characterisation
        data["conditions"] = {
            "time": tmp_time,
            "temperature": temp_temperature,
            "pH": pH,
            "operating_conditions": pressures,
        }
        data["chemicals"] = chemical_names
        data["synthetic_methods"] = synthetic_methods

        return data, data_2

    def syn_data_from_document(self, filename: str):
        for paragraph in self.get_synthetic_paragraph(filename):
            chemical_names = [ent.text for ent in nlp(paragraph).ents if ent.label_ == "CHEMICAL"]
            data, data_2 = self.extract_synthetic_info(paragraph, chemical_names)
            yield paragraph, data, data_2


def read_file(file_path: str) -> str:
    """
    A function to read a file path and normalise it to a list of plain text.
    The function reads both html and pdf files. Use return
    of this function as input for get_synthetic_paragraph function.

    Parameters
    ----------
        file_path: str.type
            The path to the file to be read.

    Returns
    -------
        plain_text: str.type
            The content of the file as a plain text.
    """
    return convert_html_to_text.file_2_list_of_paragraphs(file_path)
