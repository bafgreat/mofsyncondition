# mofsyncondition

**mofsyncondition** is a Python module for automatically extracting **synthesis conditions of metal–organic frameworks (MOFs)** from scientific journal articles.

The module reads **HTML files or PDF-derived text files**, uses **machine learning models** to identify paragraphs describing synthetic protocols and then extracts relevant synthesis conditions. In its current state, the extraction of synthesis conditions is primarily performed using **intelligent regular expressions**. The resulting dataset is being used to fine-tune a **large language model (LLM) for MOFs**.

---

## Overview

Extracting synthesis conditions from MOF literature is a key challenge in data-driven materials discovery.
`mofsyncondition` addresses this problem by:

- Reading journal articles in HTML or text format
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
    synthetic_paragraphs = text_extractor.get_synthetic_paragraph(    list_of_paragraphs)


    # html extraction

    list_of_paragraphs = text_extractor.read_file(html_file_path)
    synthetic_paragraphs = text_extractor.get_synthetic_paragraph(    list_of_paragraphs)


    # xml extraction

    list_of_paragraphs = text_extractor.read_file(xml_file_path)
    synthetic_paragraphs = text_extractor.get_synthetic_paragraph(    list_of_paragraphs)
```

By default the paragraph sentiment model uses NN_tfv, which is the most
accurate model. Below are a list of other models to select.

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

 To use any model, simply add the name of the model to the
 function. e.g

 ```Python
    list_of_paragraphs = text_extractor.read_file(xml_file_path)
    synthetic_paragraphs = text_extractor.get_synthetic_paragraph(    list_of_paragraphs, model="NN_CV")
 ```

