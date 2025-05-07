import json
from pathlib import Path

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def validate_entities(data):
    errors = []

    # Gather explicitly defined entities
    pollutants = {name for category in data['pollutants'].values() for name in category}
    sources = {name for category in data['pollution_sources'].values() for name in category}
    measures = {name for category in data['mitigation_measures'].values() for name in category}
    meteorological_factors = set(data['meteorological_factors'])
    street_canyon_factors = set(data['street_canyons'])

    # Validate pollutant-source relations explicitly
    for pollutant, source in data['pollutant_source_relations']:
        if pollutant not in pollutants:
            errors.append(f"Missing pollutant entity: '{pollutant}' in pollutant-source relation.")
        if source not in sources:
            errors.append(f"Missing source entity: '{source}' in pollutant-source relation.")

    # Validate source-mitigation relations explicitly
    for source, mitigation in data['source_mitigation_relations']:
        if source not in sources:
            errors.append(f"Missing source entity: '{source}' in source-mitigation relation.")
        if mitigation not in measures:
            errors.append(f"Missing mitigation measure entity: '{mitigation}' in source-mitigation relation.")

    # Validate meteorological dispersion relations explicitly
    for relation in data['meteorological_dispersion_relations']:
        factor = relation['meteorological_factor']['type']
        pollutant = relation['pollutant']
        if factor not in meteorological_factors:
            errors.append(f"Missing meteorological factor entity: '{factor}' in meteorological dispersion relation.")
        if pollutant not in pollutants:
            errors.append(f"Missing pollutant entity: '{pollutant}' in meteorological dispersion relation.")

    # Validate street canyon dispersion relations explicitly
    for relation in data['street_canyon_dispersion_relations']:
        factor = relation['street_canyon_description']
        pollutant = relation['pollutant']
        if factor not in street_canyon_factors:
            errors.append(f"Missing street canyon factor entity: '{factor}' in street canyon dispersion relation.")
        if pollutant not in pollutants:
            errors.append(f"Missing pollutant entity: '{pollutant}' in street canyon dispersion relation.")

    return errors

def AQ_Json_validator(json_filepath):
    data = load_json(json_filepath)
    errors = validate_entities(data)

    if not errors:
        print("✅ JSON validation passed. All entities explicitly match correctly.")
    else:
        print("🚨 JSON validation errors found:")
        for error in errors:
            print(f"- {error}")

if __name__ == "__main__":
    # Explicitly replace with your actual JSON file path
    json_filepath = Path("Validated_air_quality_knowledge.json")
    AQ_Json_validator(json_filepath)
