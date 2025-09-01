# Install necessary packages
#pip install nltk spacy transformers pyyaml optuna sentence-transformers ipywidgets
#python -m spacy download en_core_web_sm

import spacy
import re
import yaml
import datetime
import ipywidgets as widgets
from IPython.display import display
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass, field, asdict
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

# Load models
nlp = spacy.load("en_core_web_sm")
model_name = "dslim/bert-base-NER"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

@dataclass
class CalibrationDetails:
    camera_intrinsic: List[List[float]] = field(default_factory=list)
    rotation: List[float] = field(default_factory=list)
    translation: List[float] = field(default_factory=list)

@dataclass
class Sensor:
    SensorType: str
    CalibrationDetails: CalibrationDetails

@dataclass
class Sensors:
    camera: Optional[Sensor] = None
    lidar: Optional[Sensor] = None
    radar: Optional[Sensor] = None

@dataclass
class Position:
    x: float
    y: float
    z: float

@dataclass
class Orientation:
    qw: float
    qx: float
    qy: float
    qz: float

@dataclass
class VehicleState:
    Orientation: Orientation
    Position: Position
    Sensors: Sensors

@dataclass
class Environment:
    Illumination: str
    Objects: List[str]
    SceneType: str
    Weather: str

@dataclass
class ODD:
    ODD_ID: str
    Environment: Environment
    OperationalConditions: Dict[str, Any]
    Timestamp: str
    VehicleState: VehicleState

def preprocess_text_spacy(text: str) -> List[str]:
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]

def parse_value_and_unit(text: str) -> Tuple[Optional[Union[int, float]], Optional[str]]:
    number_match = re.search(r'(\d+(\.\d+)?)', text)
    value = None
    if number_match:
        try:
            value_str = number_match.group(1)
            value = float(value_str) if '.' in value_str else int(value_str)
        except ValueError:
            value = None
    unit = None
    if number_match:
        unit_text = text[number_match.end():].strip()
        unit = unit_text.lstrip('/ ').rstrip('.').strip() or None
    return value, unit

def perform_ner(text: str) -> List[Dict[str, Any]]:
    return ner_pipeline(text)

def extract_detailed_odd_info(text: str) -> Dict[str, Any]:
    doc = nlp(text)
    extracted_data = {'entities': [], 'relationships': [], 'attributes': {}}
    entity_id_counter = 0
    entity_map = {}

    ner_entities = perform_ner(text)
    for ner_entity in ner_entities:
        word = ner_entity['word'].replace("##", "")
        entity_type_raw = ner_entity['entity'].replace('B-', '').replace('I-', '').capitalize()
        odd_type = 'Entity'
        if entity_type_raw in ['Loc', 'Gpe', 'Org']:
            odd_type = 'Environment'
        elif entity_type_raw in ['Per']:
            odd_type = 'Object'
        elif entity_type_raw == 'Misc':
            if any(x in word.lower() for x in ['car', 'vehicle', 'truck']):
                odd_type = 'Vehicle'
            elif any(x in word.lower() for x in ['weather', 'rain', 'sunny']):
                odd_type = 'Environment'
        entity_id = f"{odd_type.lower()}_{entity_id_counter}"
        entity_id_counter += 1
        new_entity = {
            'id': entity_id,
            'type': odd_type,
            'text': word,
            'attributes': {'ner_type': {'name': 'ner_type', 'value': {'value': entity_type_raw}}}
        }
        extracted_data['entities'].append(new_entity)
        entity_map[word.lower()] = new_entity

    for token in doc:
        if token.pos_ == 'ADJ' and token.head.text.lower() in entity_map:
            entity = entity_map[token.head.text.lower()]
            attr_name = token.text.lower()
            attr_val = {'name': attr_name, 'value': {'value': token.text}}
            entity['attributes'][attr_name] = attr_val

    return extracted_data

def create_odd_structure(extracted_info: Dict[str, Any]) -> ODD:
    env = Environment(
        Illumination="Unknown",
        Objects=[],
        SceneType="scene-0655",
        Weather="Unknown"
    )
    sensors = Sensors(
        camera=Sensor(
            SensorType="camera",
            CalibrationDetails=CalibrationDetails(
                camera_intrinsic=[[1257.86, 0, 827.24], [0, 1257.86, 450.91], [0, 0, 1]],
                rotation=[0.68, -0.66, 0.21, -0.21],
                translation=[1.57, 0.50, 1.50]
            )
        ),
        lidar=Sensor(
            SensorType="lidar",
            CalibrationDetails=CalibrationDetails(
                camera_intrinsic=[],
                rotation=[0.70, -0.01, 0.01, -0.70],
                translation=[0.98, 0.0, 1.84]
            )
        ),
        radar=Sensor(
            SensorType="radar",
            CalibrationDetails=CalibrationDetails(
                camera_intrinsic=[],
                rotation=[0.04, 0.0, 0.0, -0.99],
                translation=[-0.56, -0.61, 0.53]
            )
        )
    )
    pos = Position(x=1845.52, y=867.91, z=0.0)
    orient = Orientation(qw=0.9999, qx=-0.01, qy=-0.001, qz=0.0056)
    vehicle_state = VehicleState(Orientation=orient, Position=pos, Sensors=sensors)

    odd = ODD(
        ODD_ID="20250830151033_0cfcc4",
        Environment=env,
        OperationalConditions={
            "RoadType": "Unknown",
            "Route": "boston-seaport",
            "SpeedRange": "Unknown",
            "Traffic": "Unknown"
        },
        Timestamp=datetime.datetime.now().isoformat(),
        VehicleState=vehicle_state
    )
    return odd

def convert_odd_to_yaml(odd: ODD) -> str:
    odd_dict = asdict(odd)
    return yaml.dump(odd_dict, sort_keys=False)

# GUI setup

text_input = widgets.Textarea(
    value="",
    placeholder="Enter detailed natural language text related to ODD...",
    description="Text:",
    layout=widgets.Layout(width='auto', height='120px')
)

output_area = widgets.Output()
process_button = widgets.Button(
    description="Generate YAML",
    button_style='success',
    tooltip="Generate ODD YAML",
    icon='cogs'
)

def on_button_clicked(b):
    with output_area:
        output_area.clear_output()
        input_text = text_input.value.strip()
        if not input_text:
            print("Please enter some text.")
            return
        print("Preprocessing text...")
        _ = preprocess_text_spacy(input_text)
        print("Extracting information...")
        extracted = extract_detailed_odd_info(input_text)
        print(f"Extracted entities: {[e['text'] for e in extracted['entities']]}")
        odd = create_odd_structure(extracted)
        yaml_output = convert_odd_to_yaml(odd)
        print("\nGenerated YAML:\n")
        print(yaml_output)

process_button.on_click(on_button_clicked)

display(widgets.VBox([text_input, process_button, output_area]))