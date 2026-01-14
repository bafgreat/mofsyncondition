from __future__ import annotations
import nltk


def setup_nltk_data_path() -> None:
    """
    Download nltk data punk.
    """
    try:
        import importlib.resources as ir  # py>=3.9
        nltk_data_dir = ir.files("mofsyncondition").joinpath("nltk_data")
        nltk.data.path.insert(0, str(nltk_data_dir))
    except Exception:
        pass
