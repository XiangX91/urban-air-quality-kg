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

def generate_prompt(text_chunk, ontology):
    prompt = "You are an urban air quality knowledge extraction agent.\n\n"

    # Ontology structure from YAML explicitly stated
    for cls, details in ontology.get('classes', {}).items():
        prompt += f"{cls}: {details['description']}\n"
        for attr, attr_details in details.get('attributes', {}).items():
            prompt += f"- {attr}: {attr_details['description']}\n"
        prompt += "\n"

    prompt += """
Your task is to extract explicitly stated or clearly implied information from the provided text.

IMPORTANT JSON OUTPUT RULES:
- Your response MUST be valid JSON, no exceptions.
- Keys and strings must be enclosed in double quotes.
- Always separate items with commas. No trailing commas allowed.
- If no information is found for a category, return an empty list.
- Do NOT include commentary or extra tokens outside the JSON structure.

Use the following JSON structure precisely:

{
  "pollutants": [{"name": "", "category": ""}],
  "pollution_sources": [{"name": "", "source_type": ""}],
  "mitigation_measures": [{"name": "", "measure_type": ""}],
  "pollutant_source_relations": [{"pollutant": {"name": ""}, "source": {"name": ""}}],
  "source_mitigation_relations": [{"source": {"name": ""}, "mitigation": {"name": ""}}],
  "meteorological_factors": [],
  "street_canyon_factors": [],
  "total_reduction_percentage": 0.0
}

Provided text:
\"\"\"
{text_chunk}
\"\"\"

Respond ONLY with the JSON. Ensure the JSON is strictly valid. No text should appear after the JSON.
"""
    return prompt

def extract_json_from_text(input_txt_path, ontology_yaml_path, output_json_path, model_path):
    """Extract structured knowledge from text and save as JSON.

    Args:
        input_txt_path (Path): Path to input text file.
        ontology_yaml_path (Path): Path to YAML ontology file.
        output_json_path (Path): Path to save the output JSON file.
        model_path (Path): Path to LLM model file.
    """
    ontology = load_ontology(ontology_yaml_path)

    with open(input_txt_path, 'r', encoding='utf-8') as file:
        text = file.read()

    prompt = generate_prompt(text, ontology)

    # Initialize LLM
    llm = Llama(model_path=str(model_path), n_ctx=8192)

    # Get response from LLM
    response = llm(prompt, max_tokens=4096, stop=["###STOP###"])

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
        output_json_path=Path("../data/output/extracted_knowledge.json"),
        model_path=Path("path/to/llm_model.gguf")
    )