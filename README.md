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


## Usage Example

This study illustrates the end-to-end process of transforming a raw, spoken Air Traffic Control (ATC) instruction into a machine-readable Operational Design Domain (ODD) YAML format. This process is crucial for integrating spoken commands into AI-driven aviation systems.


<img width="589" height="1346" alt="neutral to odd" src="https://github.com/user-attachments/assets/1553456b-f3ba-4e45-9f23-4370df82454a" />




| Step  | Phase                               | Description                                                                                                                                                                                                           | Output Example                                                                                   |
| ----- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| FAZ 1 | Raw Input                           | The Air Traffic Controller (ATCo) issues a voice command over the radio, which is captured as an audio signal.                                                                                                        | `[Audio Signal of: "Lufthansa four eight five, descend one zero zero feet, flight level."]`      |
| FAZ 2 | Speech Recognition (ASR/STT)        | The audio signal is converted into raw text. This uses acoustic models, pronunciation lexicons, language models, and transcription rules. Recognition accuracy is typically measured using the Word Error Rate (WER). | `DLH485 DESCEND 100 FL`                                                                          |
| FAZ 3 | Language Understanding / Annotation | The transcribed text is interpreted and structured within the operational context using ontology-based annotation. This produces a standardized, structured ATC command object.                                       | `[Structured ATC Command: {callsign: "DLH485", action: "DESCEND", altitude: "100", unit: "FL"}]` |
| FAZ 4 | ODD YAML Conversion                 | The structured command is converted into a standardized, machine-readable ODD YAML format, which represents its Operational Design Domain.                                                                            | (See YAML Example below)                                                                         |


## ⚙️ ODD YAML
```yaml
operation_design_domain:
  instruction:
    callsign: "DLH485"
    action: "DESCEND"
    target_altitude: 
      value: 100
      unit: "FL"
```

## Requirements

- Python 3.7+  
- Libraries: spacy, transformers (for BERT and other transformer models), pyyaml, ipywidgets, nltk, optuna  
- SpaCy English model: `en_core_web_sm`

<img width="382" height="1125" alt="image" src="https://github.com/user-attachments/assets/8017b0a3-faa8-4f40-bfc4-c1457e7f3b07" />
