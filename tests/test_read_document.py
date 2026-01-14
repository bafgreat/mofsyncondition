from pathlib import Path
import pytest
from mofsyncondition.synthesis_conditions import extractor


@pytest.fixture(scope="module")
def text_extractor():
    return extractor.MOFSynConditionExtractor()


@pytest.fixture(scope="module")
def data_dir():
    here = Path(__file__).resolve().parent
    candidates = [
        here / "data_test",
        here.parent / "data_test",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    raise FileNotFoundError(
        "Could not find 'data_test' directory. Tried:\n"
        + "\n".join(str(c) for c in candidates)
    )


def test_abafuh_xml_extraction(text_extractor, data_dir):
    abafuh_xml = data_dir / "ABAFUH.xml"
    assert abafuh_xml.exists(), f"Missing file: {abafuh_xml}"

    plaintext = text_extractor.read_file(str(abafuh_xml))
    assert len(plaintext) == 88

    synthetic_paragraphs = text_extractor.get_synthetic_paragraph(plaintext)
    assert len(synthetic_paragraphs) == 10


def test_pdf_extraction(text_extractor, data_dir):
    test2_pdf = data_dir / "Test2.pdf"
    assert test2_pdf.exists(), f"Missing file: {test2_pdf}"

    plaintext = text_extractor.read_file(str(test2_pdf))
    assert len(plaintext) == 89

    synthetic_paragraphs = text_extractor.get_synthetic_paragraph(plaintext)
    assert len(synthetic_paragraphs) == 13


def test_html_extraction_with_nb_model(text_extractor, data_dir):
    test3_html = data_dir / "Test3.html"
    assert test3_html.exists(), f"Missing file: {test3_html}"

    plaintext = text_extractor.read_file(str(test3_html))
    assert len(plaintext) == 853

    synthetic_paragraphs = text_extractor.get_synthetic_paragraph(plaintext)
    assert len(synthetic_paragraphs) == 6
