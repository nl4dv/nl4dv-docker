from typing import Optional

from fastapi import FastAPI
from nl4dv import NL4DV
import os
from pydantic import BaseModel, Field


# Set the Dependency Parser
# ToDo: Update the configs for the parser_type={corenlp, corenlp-server} elif conditions.
def set_dependency_parser(parser_type):
    global nl4dv_instance, current_dependency_parser
    if parser_type == "spacy":
        dependency_parser_config = {"name": "spacy", "model": "en_core_web_sm", "parser": None}
        nl4dv_instance.set_dependency_parser(config=dependency_parser_config)
    elif parser_type == "corenlp-server":
        dependency_parser_config = {"name": "corenlp-server", "url": "http://localhost:9000"}
        nl4dv_instance.set_dependency_parser(config=dependency_parser_config)
    elif parser_type == "corenlp":
        dependency_parser_config = {"name": "corenlp", "model": os.path.join(".", "assets","jars","stanford-english-corenlp-2018-10-05-models.jar"),"parser": os.path.join(".", "assets","jars","stanford-parser.jar")}
        nl4dv_instance.set_dependency_parser(config=dependency_parser_config)
    else:
        pass


# Defaults
current_dataset = "cars-w-year.csv"
current_dependency_parser = "corenlp"
current_query = "show me a scatterplot of mpg and horsepower"

# InputParams class
# ToDo: Eventually add support to set label_attribute, ignore_words, stop_words, and other configurations.
class InputParams(BaseModel):
    query: str = current_query
    dataset: str = current_dataset
    dependency_parser: str = current_dependency_parser


# InputParams class
# ToDo: Eventually add support to set label_attribute, ignore_words, stop_words, and other configurations.
class ResponseModel(BaseModel):
    query_raw: str = current_query
    query: str = current_query
    dataset: str = current_dataset
    attributeMap: dict = {
    "MPG": {
        "name": "MPG",
        "queryPhrase": [
            "mpg"
        ],
        "inferenceType": "explicit",
        "isAmbiguous": False,
        "ambiguity": []
        },
    "Horsepower": {
        "name": "Horsepower",
        "queryPhrase": [
            "horsepower"
        ],
        "inferenceType": "explicit",
        "isAmbiguous": False,
        "ambiguity": []
        }
    }
    taskMap: dict = {
        "correlation": [
            {
                "task": "correlation",
                "queryPhrase": [],
                "operator": None,
                "values": None,
                "attributes": [
                    "MPG",
                    "Horsepower"
                ],
                "inferenceType": "implicit"
            }
        ]
    }
    visList: list = [
    {
        "attributes": [
            "MPG",
            "Horsepower"
        ],
        "queryPhrase": "scatterplot",
        "visType": "scatterplot",
            "tasks": [
            "correlation"
        ],
        "inferenceType": "explicit",
        "vlSpec": {
            "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
            "mark": {
                "type": "point",
                "tooltip": True
            },
            "encoding": {
                "x": {
                    "field": "MPG",
                    "type": "quantitative",
                    "aggregate": None,
                    "axis": {
                        "format": "s"
                    }
                },
                "y": {
                    "field": "Horsepower",
                    "type": "quantitative",
                    "aggregate": None,
                    "axis": {
                        "format": "s"
                    }
                },
                "tooltip": {
                    "field": "Model"
                }
            },
            "transform": [],
            "data": {
                "url": "./assets/data/cars-w-year.csv",
                "format": {
                    "type": "csv"
                }
            }
        }
    }]
    followUpQuery: bool = False
    contextObj: list = None

# Initialize an instance of NL4DV
# ToDo: Update the path to data
nl4dv_instance = NL4DV(data_url = os.path.join(".", "assets", "data", current_dataset))
set_dependency_parser(parser_type=current_dependency_parser)

# Create a FastAPI() application.
app = FastAPI()


@app.post("/analyze_query", response_model=ResponseModel)
async def analyze_query(input_params: InputParams):
    global current_dataset, current_dependency_parser

    # Update dataset, if needed
    if input_params.dataset != current_dataset:
        nl4dv_instance.set_data(data_url=os.path.join(".", "assets", "data", input_params.dataset))
        current_dataset = input_params.dataset

    if input_params.dependency_parser != current_dependency_parser:
        set_dependency_parser(parser_type=input_params.dependency_parser)
        current_dependency_parser = input_params.dependency_parser

    # Execute the query
    if input_params.query is not None:
        output = nl4dv_instance.analyze_query(input_params.query)
    else:
        output = {}

    # Return the output
    return output
