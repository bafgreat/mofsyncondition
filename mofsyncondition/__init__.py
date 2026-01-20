from .nltk_setup import setup_nltk_data_path
from .spacy_setup import setup_spacy_model
setup_nltk_data_path()
setup_spacy_model("en_core_web_sm")
