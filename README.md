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
