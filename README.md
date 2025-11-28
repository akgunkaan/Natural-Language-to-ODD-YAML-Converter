# Natural Language to ODD YAML Converter PoC

This project implements a Python-based system to convert detailed natural language descriptions about Operational Design Domains (ODD) into structured, hierarchical YAML format. It leverages advanced Natural Language Processing (NLP) techniques including SpaCy for efficient tokenization and lemmatization, and pre-trained BERT models for Named Entity Recognition (NER) to accurately identify key domain entities. Flexible Python dataclass models represent the various ODD entities, enabling organized and extensible data modeling.

## Features

- **Interactive GUI:** Users can input ODD descriptions in natural text and receive YAML output interactively.  
- **NLP Pipeline:** Utilizes SpaCy for text preprocessing (tokenization, lemmatization, stopword removal) and HuggingFace's BERT models for precise entity recognition.  
- **Structured Modeling:** Converts extracted data into detailed Python dataclasses capturing environmental, vehicle, operational, and sensor conditions.  
- **YAML Export:** Outputs the structured ODD data in a human-readable and hierarchical YAML format.  
- **Extensible Architecture:** Easily extendable for additional entity types, relationships, or sector-specific logic.  

## AI Models and Services Used

| AI Service / Model            | Capability Provided                                           | Library Used              |
|------------------------------|---------------------------------------------------------------|---------------------------|
| spaCy – en_core_web_sm       | NLP preprocessing, POS tagging, dependency parsing, lemmatization | spaCy                     |
| dslim/bert-base-NER          | Named Entity Recognition (NER)                                | HuggingFace Transformers  |
| Transformers Pipeline (ner)  | Prebuilt NER pipeline service                                 | HuggingFace Transformers  |


## Requirements

- Python 3.7+  
- Libraries: spacy, transformers (for BERT and other transformer models), pyyaml, ipywidgets, nltk, optuna  
- SpaCy English model: `en_core_web_sm`

<img width="382" height="1125" alt="image" src="https://github.com/user-attachments/assets/8017b0a3-faa8-4f40-bfc4-c1457e7f3b07" />
