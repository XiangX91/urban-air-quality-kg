"""
Urban Air Quality Knowledge Merge Module

This module merges structured urban air quality information from two JSON files,
using fuzzy matching to avoid duplicates and explicitly merging entities and relations.

Author: Xiang Xie (xiang.xie@ncl.ac.uk)
Date: 28/02/2025
"""

import json
from fuzzywuzzy import process
from pathlib import Path

def load_json(filepath):
    """Explicitly load JSON data from the given file path."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(filepath, data):
    """Explicitly save JSON data to the given file path."""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

def fuzzy_match(entity, entity_list, threshold=85):
    """Return the best fuzzy match above threshold or None explicitly."""
    result = process.extractOne(entity, entity_list)
    if result:
        match, score = result
        return match if score >= threshold else None
    return None

def merge_knowledge(base_filepath, new_filepath, output_filepath):
    """Merge air quality knowledge explicitly from two JSON files."""
    base_data = load_json(base_filepath)
    new_data = load_json(new_filepath)

    entity_categories = ['pollutants', 'pollution_sources', 'mitigation_measures',
                         'meteorological_factors', 'street_canyons']

    # Merge entities explicitly
    for category in entity_categories:
        base_entities = base_data.get(category, {})
        new_entities = new_data.get(category, {})

        if isinstance(base_entities, dict):
            for subclass, entities in new_entities.items():
                base_subclass_entities = base_entities.get(subclass, [])
                for entity in entities:
                    matched_entity = fuzzy_match(entity, base_subclass_entities)
                    if not matched_entity:
                        base_subclass_entities.append(entity)
                base_entities[subclass] = base_subclass_entities
        elif isinstance(base_entities, list):
            for entity in new_entities:
                matched_entity = fuzzy_match(entity, base_entities)
                if not matched_entity:
                    base_entities.append(entity)

        base_data[category] = base_entities

    # Merge relations explicitly
    relation_categories = [
        'pollutant_source_relations',
        'source_mitigation_relations',
        'meteorological_dispersion_relations',
        'street_canyon_dispersion_relations'
    ]

    for rel_category in relation_categories:
        base_relations = base_data.get(rel_category, [])
        new_relations = new_data.get(rel_category, [])

        for relation in new_relations:
            matched_relation = []

            for item in relation:
                if rel_category == 'meteorological_dispersion_relations' and isinstance(item, dict):
                    factor_type = item.get('type')
                    base_meteorological_factors = base_data.get('meteorological_factors', [])
                    matched_type = fuzzy_match(factor_type, base_meteorological_factors)
                    if matched_type:
                        matched_relation.append({'type': matched_type, 'range': item.get('range', '')})
                    else:
                        base_meteorological_factors.append(factor_type)
                        base_data['meteorological_factors'] = base_meteorological_factors
                        matched_relation.append(item)
                else:
                    flat_base_entities = sum(base_data['pollutants'].values(), []) + \
                                         sum(base_data['pollution_sources'].values(), []) + \
                                         sum(base_data['mitigation_measures'].values(), []) + \
                                         base_data.get('street_canyons', [])
                    matched_item = fuzzy_match(item, flat_base_entities)
                    matched_relation.append(matched_item if matched_item else item)

            if matched_relation not in base_relations:
                base_relations.append(matched_relation)

        base_data[rel_category] = base_relations

    save_json(output_filepath, base_data)
    print("✅ JSON files merged successfully into:", output_filepath)

# Example usage explicitly
if __name__ == "__main__":
    base_filepath = Path('Validated_air_quality_knowledge.json')
    new_filepath = Path('extracted_knowledge.json')
    output_filepath = Path('merged_air_quality_knowledge.json')

    merge_knowledge(base_filepath, new_filepath, output_filepath)