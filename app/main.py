from fastapi import FastAPI
from nl4dv import NL4DV
import os
from pydantic import BaseModel, Field
from typing import Dict, Any

# Defaults
query = "show me a scatterplot of mpg and horsepower"
data_url = "https://raw.githubusercontent.com/nl4dv/nl4dv/master/examples/assets/data/cars-w-year.csv"
data_value = None
alias_url = "https://raw.githubusercontent.com/nl4dv/nl4dv/master/examples/assets/aliases/cars-w-year.json"
alias_value = None
label_attribute = "Model"
ignore_words = list()
reserve_words = list()
debug = True
thresholds = {"synonymity": 95, "string_similarity": 85}
importance_scores = {"attribute":{"attribute_exact_match":1,"attribute_similarity_match":0.9,"attribute_alias_exact_match":0.8,"attribute_alias_similarity_match":0.75,"attribute_synonym_match":0.5,"attribute_domain_value_match":0.5},"task":{"explicit":1,"implicit":0.5},"vis":{"explicit":1}}
dependency_parser_config = {"name": "corenlp", "model": os.path.join(".", "assets","jars","stanford-english-corenlp-2018-10-05-models.jar"),"parser": os.path.join(".", "assets","jars","stanford-parser.jar")}
# dependency_parser_config = {"name": "spacy", "model": "en_core_web_sm", "parser": None}
# dependency_parser_config = {"name": "corenlp-server", "url": "http://localhost:9000"}
attribute_datatype = {"Year": "T"}


# InputParams class
class InputParams(BaseModel):
    query: str = query
    data_url: str = data_url
    data_value: Any = data_value
    alias_url: str = alias_url
    alias_value: Any = alias_value
    dependency_parser_config: dict = dependency_parser_config
    ignore_words: list = ignore_words
    reserve_words: list = reserve_words
    debug: bool = debug
    label_attribute: str = label_attribute
    thresholds: dict = thresholds
    importance_scores: dict = importance_scores
    attribute_datatype: dict = attribute_datatype


# InputParams class
class ResponseModel(BaseModel):
    query_raw: str = query
    query: str = query
    dataset: str = data_url if data_url else data_value,
    alias: str = alias_url if alias_url else alias_value,
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
        }
    ]
    followUpQuery: bool = False
    contextObj: list = None


# Initialize an instance of NL4DV
nl4dv_instance = NL4DV(verbose=False, debug=True, importance_scores=importance_scores, thresholds=thresholds, data_url=data_url, alias_url=alias_url, label_attribute=label_attribute, dependency_parser_config=dependency_parser_config, attribute_datatype=attribute_datatype)

# Create a FastAPI() application.
app = FastAPI()

@app.post("/analyze_query", response_model=ResponseModel)
async def analyze_query(input_params: InputParams):
    global query, data_url, data_value, alias_url, alias_value, dependency_parser_config, label_attribute, ignore_words, reserve_words, debug, thresholds, importance_scores, attribute_datatype

    # Update data, if needed
    if input_params.data_url != data_url:
        nl4dv_instance.set_data(data_url=input_params.data_url)
        data_url = input_params.data_url
    elif input_params.data_value != data_value:
        nl4dv_instance.set_data(data_value=input_params.data_value)
        data_value = input_params.data_value

    # Update alias, if needed
    if input_params.alias_url != alias_url:
        nl4dv_instance.set_alias_map(alias_url=input_params.alias_url)
        alias_url = input_params.alias_url
    elif input_params.alias_value != alias_value:
        nl4dv_instance.set_alias_map(alias_value=input_params.alias_value)
        alias_value = input_params.alias_value

    # Update dependency parser, if needed
    if input_params.dependency_parser_config != dependency_parser_config:
        nl4dv_instance.set_dependency_parser(config=input_params.dependency_parser_config)
        dependency_parser_config = input_params.dependency_parser_config

    # Update ignore_words, if needed
    if input_params.ignore_words != ignore_words:
        nl4dv_instance.set_ignore_words(ignore_words=input_params.ignore_words)
        ignore_words = input_params.ignore_words

    # Update reserve_words, if needed
    if input_params.reserve_words != reserve_words:
        nl4dv_instance.set_reserve_words(reserve_words=input_params.reserve_words)
        reserve_words = input_params.reserve_words

    # Update label_attribute, if needed
    if input_params.label_attribute != label_attribute:
        nl4dv_instance.set_label_attribute(label_attribute=input_params.label_attribute)
        label_attribute = input_params.label_attribute

    # Update attribute_datatype, if needed
    if input_params.attribute_datatype != attribute_datatype:
        nl4dv_instance.set_attribute_datatype(attr_type_obj=input_params.attribute_datatype)
        attribute_datatype = input_params.attribute_datatype

    # Update thresholds, if needed
    if input_params.thresholds != thresholds:
        nl4dv_instance.set_thresholds(thresholds=input_params.thresholds)
        thresholds = input_params.thresholds

    # Update importance_scores, if needed
    if input_params.importance_scores != importance_scores:
        nl4dv_instance.set_importance_scores(importance_scores=input_params.importance_scores)
        importance_scores = input_params.importance_scores

    # Execute the query
    output = nl4dv_instance.analyze_query(input_params.query, debug=input_params.debug) if input_params.query is not None else {}

    # Return the output
    return output
