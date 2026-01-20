from __future__ import annotations

import spacy
from spacy.util import is_package


def setup_spacy_model(model: str = "en_core_web_sm") -> None:
    """
    Ensure the spaCy model is installed. If missing, download it automatically.

    NOTE:
    - This installs into the *current Python environment* (site-packages).
    - It requires internet access at first run.
    """
    if is_package(model):
        return

    try:
        spacy.load(model)
        return
    except OSError:
        pass

    from spacy.cli import download as spacy_download

    try:
        spacy_download(model)
    except SystemExit as e:
        raise OSError(
            f"Automatic spaCy model download failed for '{model}'. "
            f"Try running: python -m spacy download {model}"
        ) from e

    spacy.load(model)
