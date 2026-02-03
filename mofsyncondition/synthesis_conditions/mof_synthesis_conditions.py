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

nlp_chem = spacy.load("en_chem_ner")
nlp = spacy.load("en_mof_chem_ner")

@dataclass
class MOFSynConditionExtractor:
    """
    Extract MOF synthesis paragraphs and structured synthesis conditions.

    This extractor combines:
    - spaCy NER for chemical/process entities (metal salts, ligands, solvents, etc.)
    - Regex-based condition extraction for time and temperature, with bucketing.
    """

    paragraph_model: str = "SVM_tfv"

    ner_model: Any = None

    context_window: int = 200
    use_spacy_sentence: bool = False
    tokenizer: Callable[[str], Tuple[List[str], Any]] = doc_parser.tokenize_doc

    def __post_init__(self) -> None:
        """
        Initialize cached patterns and the NER model (if not provided).

        Notes
        -----
        The NER model is loaded once and reused for speed.
        """
        self._solvents_pattern = chemical_entity_regex.solvents_regex()
        self._modulators_pattern = chemical_entity_regex.modulators_regex()
        self._method_pattern = chemical_entity_regex.synthetic_method_re()
        self._mof_alias_list = chemical_entity_regex.mof_regex()

        if self.ner_model is None:
            self.ner_model = spacy.load("en_mof_chem_ner")

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

    def extract_ner_entities(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Run the spaCy synthesis NER model on text and return grouped entities.

        Parameters
        ----------
        text : str
            Paragraph text.

        Returns
        -------
        entities : dict
            Mapping from entity label to list of entity dicts:
            {
            "METAL_SALT": [{"text": "...", "start": 10, "end": 25}, ...],
            "SOLVENT": [...],
            ...
            }

        Notes
        -----
        This method does not attempt to deduplicate overlapping entities.
        If you want that, add a post-processing step (span merge by priority).
        """
        doc = self.ner_model(text or "")
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for ent in doc.ents:
            grouped.setdefault(ent.label_, []).append(
                {"text": ent.text, "start": ent.start_char, "end": ent.end_char}
            )
        return grouped

    @staticmethod
    def _unique_texts(ents: List[Dict[str, Any]]) -> List[str]:
        """
        Return unique entity texts in a stable order.
        """
        seen = set()
        out = []
        for e in ents or []:
            t = (e.get("text") or "").strip()
            if t and t not in seen:
                seen.add(t)
                out.append(t)
        return out

    def extract_time_events(self, paragraph: str) -> List[Dict[str, object]]:
        """
        Extract time mentions from a paragraph using regex-based detection.

        The extractor:
        - finds numeric and non-numeric time expressions (e.g., '2 h', 'overnight')
        - vetoes spectroscopy/peak-list contexts
        - assigns a coarse process bucket using keyword-weighted context scoring

        Returns
        -------
        events : list of dict
            One dict per time mention with keys:
            - coarse_bucket : str
            - time_text : str
            - unit : str
            - is_numeric : bool
            - is_ambiguous : bool
            - sentence : str
            - char_start : int
            - char_end : int
        """
        return chemical_entity_regex.extract_time_event_dicts_from_paragraph(
            paragraph,
            nlp=self.ner_model if self.use_spacy_sentence else None,
            use_spacy_for_sentence=self.use_spacy_sentence,
            window=self.context_window,
        )

    def extract_temperature_events(self, paragraph: str) -> List[Dict[str, object]]:
        """
        Extract temperature mentions from a paragraph using regex-based detection.

        The extractor:
        - supports numeric temperatures and ranges (e.g., '120 °C', '20–25 °C', '298 K')
        - supports ambiguous mentions (e.g., 'RT', 'room temperature')
        - expands compact lists (e.g., '120, 140, 160 °C')
        - vetoes spectroscopy/isotope-like contexts (e.g., '13C' in NMR)

        Returns
        -------
        events : list of dict
            One dict per temperature mention with keys:
            - coarse_bucket : str
            - temperature_text : str
            - unit_scale : str  (celsius/fahrenheit/kelvin/ambient/unknown)
            - is_numeric : bool
            - is_ambiguous : bool
            - sentence : str
            - char_start : int
            - char_end : int
        """
        return chemical_entity_regex.extract_temperature_event_dicts_from_paragraph(
            paragraph,
            window=self.context_window,
        )

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

    def extract_synthetic_info(self, par_text: str, chemical_names=None):
        """
        Extract structured synthesis info from a paragraph.

        This method merges:
        - NER-derived entities (metal salts, ligands, solvents, modulators, MOFs, atmosphere, methods)
        - Regex-derived time and temperature events (with coarse bucketing and sentences)

        Parameters
        ----------
        par_text : str
            Paragraph text.
        chemical_names : optional
            Legacy input (CHEMICAL list). If provided, used as fallback; otherwise NER is used.

        Returns
        -------
        data : dict
            High-level structured output (reagents + conditions + methods).
        data_2 : dict
            Debug/raw output including NER entities and event lists.
        """
        data: Dict[str, Any] = {}
        data_2: Dict[str, Any] = {}

        par_text = par_text or ""

        ner = self.extract_ner_entities(par_text)
        data_2["chemical_reagents"] = {}

        metal_salts = self._unique_texts(ner.get("METAL_SALT", []))
        ligands = self._unique_texts(ner.get("ORGANIC_LIGAND", []))
        solvents = self._unique_texts(ner.get("SOLVENT", []))
        modulators = self._unique_texts(ner.get("MODULATOR", []))
        atmospheres = self._unique_texts(ner.get("ATMOSPHERE", []))
        syn_methods_ner = self._unique_texts(ner.get("SYNTH_METHOD", []))
        mofs = self._unique_texts(ner.get("MOF", []))
        data_2["chemical_reagents"]["metal_salts"] = metal_salts
        data_2["chemical_reagents"]["ligands"] = ligands
        data_2["chemical_reagents"]["solvents"] = solvents
        data_2["chemical_reagents"]["modulators"] = modulators
        data_2["chemical_reagents"]["mofs"] = mofs
        par_tokens, par_doc = self.tokenizer(par_text)

        if chemical_names is None:
            chemical_names = []
            chemical_names.extend(metal_salts)
            chemical_names.extend(ligands)
            chemical_names.extend(solvents)
            chemical_names.extend(modulators)
            chemical_names.extend(mofs)
        chemical_names = chemical_entity_regex.clean_chemicals(list(chemical_names or []))

        time_events = self.extract_time_events(par_text)
        temp_events = self.extract_temperature_events(par_text)

        # data_2["time_events"] = time_events
        # data_2["temperature_events"] = temp_events

        pH = conditions_extraction.get_ph_toks(par_tokens)

        operating_conditions = {
            "atmosphere": atmospheres
        }

        quantities = chemical_entity_regex.extract_chemical_quantities2(par_text, chemical_names)
        reagents: List[Dict[str, Any]] = []
        for m in metal_salts:
            reagents.append({"name": m, "role": "metal_salt", "amount": quantities.get(m, "")})
        for lig in ligands:
            reagents.append({"name": lig, "role": "organic_ligand", "amount": quantities.get(lig, "")})
        for mod in modulators:
            reagents.append({"name": mod, "role": "modulator", "amount": quantities.get(mod, "")})
        for sol in solvents:
            reagents.append({"name": sol, "role": "solvent", "amount": quantities.get(sol, "")})
        for mof in mofs:
            reagents.append({"name": mof, "role": "mof_alias"})

        syn_methods_regex = self.get_synthetic_method(par_tokens)
        synthetic_methods = list({*(syn_methods_ner or []), *(syn_methods_regex or [])})

        data["chemical_reagents"] = reagents
        data["chemicals"] = chemical_names
        data["synthetic_methods"] = synthetic_methods

        data["conditions"] = {
            "time_events": time_events,
            "temperature_events": temp_events,
            "pH": pH,
            "operating_conditions": operating_conditions,
        }

        data_2["conditions"] = {
            "time_events": time_events,
            "temperature_events": temp_events,
            "pH": pH,
            "operating_conditions": operating_conditions,
        }

        data_2["quantities"] = quantities
        data_2["chemical_names"] = chemical_names
        data_2["synthetic_methods"] = list(set([i.lower() for i in synthetic_methods]))
        return data, data_2

    def syn_data_from_document(self, filename: str):
        """
        Generator yielding synthesis paragraphs and extracted data from a document.
        Parameters
        ----------
            filename : str
                Path to the document file.

        Returns
        -------
            Yields tuples of (paragraph text, data dict, data_2 dict) for each synthesis paragraph.

        """
        for paragraph in self.get_synthetic_paragraph(filename):
            chemical_names = [ent.text for ent in nlp_chem(paragraph).ents if ent.label_ == "CHEMICAL"]
            if len(chemical_names) == 0:
                chemical_names = None
            data, data_2 = self.extract_synthetic_info(paragraph, chemical_names=chemical_names)
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





