# mofsyncondition

**mofsyncondition** is a Python module for automatically extracting **synthesis conditions of metal–organic frameworks (MOFs)** from scientific journal articles.

The module reads **HTML files or PDF-derived text files**, uses **machine learning models** to identify paragraphs describing synthetic protocols and then extracts relevant synthesis conditions. In its current state, the extraction of synthesis conditions is primarily performed using **intelligent regular expressions**. The resulting dataset is being used to fine-tune a **large language model (LLM) for MOFs**.

---

## Overview

Extracting synthesis conditions from MOF literature is a key challenge in data-driven materials discovery.
`mofsyncondition` addresses this problem by:

- Reading journal articles in HTML, pdf or xml format
- Identifying synthesis-related paragraphs using ML-based classification
- Extracting structured synthesis conditions from unstructured text
- Generating datasets suitable for machine learning and LLM training

---

## Key Features

- Support for HTML and PDF-derived text inputs
- ML-based identification of synthesis protocols
- Regex-driven extraction of synthesis conditions
- Modular and extensible Python design
- Scalable for large literature datasets

---

## Extracted Synthesis Information

The module aims to extract synthesis parameters such as:

- Metal precursors
- Organic linkers
- Solvents
- Additives / modulators
- Reaction temperature
- Reaction time
- pH (when available)
- Synthetic methods (e.g. solvothermal, hydrothermal)
- Pressure and humidity (when available)
- Name of MOF or formular is provided

---

## Installation

Clone the repository and install the package locally:

```bash
git clone https://github.com/bafgreat/mofsyncondition.git
cd mofsyncondition
pip install .
```

## PYPI

 The module can be install using PYPI

 ```bash
    pip install mofsyncondition
 ```

## Usage

### 1. Extract synthetic paragraph from file

Assuming you have different files and wish to extract list
of paragraphs describing synthesis simply run the following code.

```Python
    from mofsyncondition.synthesis_conditions import extractor

    # filepaths
    pdf_file_path = '../filename.pdf'
    html_file_path = '../filename.html'
    xml_file_path = '../filename.xml'

    # declare extractor class
    text_extractor = extractor.MOFSynConditionExtractor()

    # PDF extraction

    list_of_paragraphs = text_extractor.read_file(pdf_file_path)
    synthetic_paragraphs = text_extractor.get_synthetic_paragraph(list_of_paragraphs)


    # html extraction

    list_of_paragraphs = text_extractor.read_file(html_file_path)
    synthetic_paragraphs = text_extractor.get_synthetic_paragraph(list_of_paragraphs)


    # xml extraction

    list_of_paragraphs = text_extractor.read_file(xml_file_path)
    synthetic_paragraphs = text_extractor.get_synthetic_paragraph(list_of_paragraphs)
```

By default the paragraph sentiment model uses NN_tfv. Below is a list of other models.

## ML Model Performance (5-Fold Cross-Validation Averages)

| Rank | Model | Avg Accuracy | Avg Precision | Notes |
|------|-------|--------------|---------------|-------|
| 1 | SVM_tfv | 0.9905 | 0.8163 | Best overall accuracy |
| 2 | **NN_tfv** | 0.9903 | 0.8143 | **Default model** |
| 3 | RF_tfv | 0.9904 | 0.7730 | High accuracy, lower precision |
| 4 | RF_CV | 0.9902 | 0.7692 | Stable but conservative |
| 5 | NN_CV | 0.9889 | 0.8240 | High precision |
| 6 | LR_tfv | 0.9895 | 0.7853 | Fast baseline |
| 7 | LR_CV | 0.9885 | 0.8040 | Balanced baseline |
| 8 | SVM_CV | 0.9885 | 0.8124 | Robust alternative |
| 9 | DT_CV | 0.9865 | 0.7795 | Interpretable |
|10 | DT_tfv | 0.9851 | 0.7692 | Simple model |
|11 | NB_CV | 0.9837 | 0.8337 | Highest precision |
|12 | NB_tfv | 0.9657 | 0.0232 | Not recommended |

 To use any model, simply add the name of the model to the
 function. e.g

 ```Python
    list_of_paragraphs = text_extractor.read_file(xml_file_path)
    synthetic_paragraphs = text_extractor.get_synthetic_paragraph(list_of_paragraphs, model="NN_CV")
 ```

### 2. Extract paragaraph level synthetic condition from file

Suppose you have an document (pdf, html, xml) and wish to extract
all synthesis conditions. The below lines of code it the faster way
to do so. This is faster than using transformer models and take large
documents and parse thousand of files.

```Python
import spacy
from mofsyncondition.synthesis_conditions.extractor import MOFSynConditionExtractor
from mofsyncondition.io import filetyper

data_extractor = MOFSynConditionExtractor()

transformer_dataset = []
standard_dataset = []
file_path = "./data_test/Test2.pdf"

all_files = ["./data_test/Test2.pdf", "./data_test/ABAFUH.xml", "./data_test/Test3.html"]
for file_path in all_files:
    syn_data  = data_extractor.syn_data_from_document(file_path)
    for paragraph, data_style_1, data_style_2 in syn_data:
        transformer_dataset.append({'paragraph':paragraph, "condition":data_style_1})
        standard_dataset.append({'paragraph':paragraph, "condition":data_style_2})
```

## LICENSE

 MIT license
