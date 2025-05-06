"""
Urban Air Quality Knowledge Extraction Module

This module provides functionality to extract structured urban air quality
information from plain text, guided by a YAML-based ontology.

Author: Xiang Xie (xiang.xie@ncl.ac.uk)
Date: 08/01/2025
"""

import yaml
import json
import re
from llama_cpp import Llama
from pathlib import Path

def load_ontology(ontology_path):
    """Load the urban air quality ontology from a YAML file."""
    with open(ontology_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def create_body_prompt(text_chunk, ontology_yaml_path, hints_file_path):
    """
    Generate an explicit LLM extraction prompt based on a formal YAML ontology and supplemental prompt hints.

    Args:
        text_chunk (str): The text for structured data extraction.
        ontology_yaml_path (Path): Path to the ontology YAML file.
        hints_file_path (Path): Path to the supplemental hints markdown file.

    Returns:
        str: Explicitly formatted prompt for LLM.
    """
    # Load the YAML ontology explicitly
    ontology = load_ontology(ontology_yaml_path)

    # Load supplemental hints explicitly
    with open(hints_file_path, "r", encoding="utf-8") as f:
        prompt_hints = f.read()

    # Clearly summarize ontology classes, attributes, and enums
    ontology_description = "**Ontology Reference (Explicitly defined entities, attributes, and categories):**\n\n"
    for cls_name, cls_content in ontology.get("classes", {}).items():
        ontology_description += f"- **{cls_name}**: {cls_content.get('description')}\n"
        attributes = cls_content.get("attributes", {})
        if attributes:
            ontology_description += "  - Attributes:\n"
            for attr_name, attr_details in attributes.items():
                ontology_description += f"    - {attr_name}: {attr_details.get('description')}\n"

    enums = ontology.get("enums", {})
    if enums:
        ontology_description += "\n- **Enumerations:**\n"
        for enum_name, enum_content in enums.items():
            ontology_description += f"  - **{enum_name}**: {', '.join(enum_content.get('permissible_values', {}).keys())}\n"

    # Create the explicit prompt using ontology + hints
    prompt = f"""
You are an environmental knowledge extraction agent.

Your task is to extract structured knowledge explicitly based on the provided ontology definitions and instructions. 
Use the ontology entities, attributes, and categories described below to guide your extraction:

{ontology_description}

Additionally, strictly follow the JSON format provided below:

{prompt_hints}

Text:
\"\"\"
{text_chunk}
\"\"\"

Provide ONLY the structured JSON. Do NOT include any additional text.
"""
    return prompt

def extract_json_from_text(input_txt_path, ontology_yaml_path, hints_file_path, output_json_path, model_path):
    """Extract structured knowledge from text and save as JSON.

    Args:
        input_txt_path (Path): Path to input text file.
        ontology_yaml_path (Path): Path to YAML ontology file.
        output_json_path (Path): Path to save the output JSON file.
        model_path (Path): Path to LLM model file.
    """
    with open(input_txt_path, 'r', encoding='utf-8') as file:
        text = file.read()

    prompt = create_body_prompt(text, ontology_yaml_path, hints_file_path)

    # Initialize LLM
    llm = Llama(model_path=str(model_path), n_ctx=8192)

    # Get response from LLM
    response = llm(prompt, max_tokens=4096)

    response_text = response['choices'][0]['text']

    # Robustly extract JSON from the response
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    extracted_json = json.loads(json_match.group()) if json_match else {}

    # Save extracted JSON
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(extracted_json, json_file, indent=2)

    print(f"✅ JSON saved to: {output_json_path}")

# Example usage
if __name__ == '__main__':
    extract_json_from_text(
        input_txt_path=Path("../data/input/sample.txt"),
        ontology_yaml_path=Path("../ontology/urban_air_quality.yaml"),
        hints_file_path=Path("../prompt_hints.md"),
        output_json_path=Path("../data/output/extracted_knowledge.json"),
        model_path=Path("path/to/llm_model.gguf")
    )