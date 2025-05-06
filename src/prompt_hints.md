
## Explicit Instructions for JSON Output Generation by LLM

When extracting structured data from urban air quality texts, strictly follow the JSON structure below. Do not deviate, and do not invent fields or placeholders.

**JSON OUTPUT EXAMPLE (Strictly Follow this Format):**

```json
{
  "pollutants": {
    "ParticulateMatter": ["PM2.5"],
    "GaseousPollutants": ["NOx"],
    "TraceElements": [],
    "HazardousOrganicCompounds": [],
    "Uncategorized": []
  },
  "pollution_sources": {
    "MobileSource": ["Cars"],
    "StationarySource": ["Factories"],
    "AreaSource": [],
    "AgriculturalSource": [],
    "NaturalSource": [],
    "Uncategorized": []
  },
  "mitigation_measures": {
    "PolicyBasedMeasure": ["Low-emission zones"],
    "TechnologicalMeasure": [],
    "Uncategorized": []
  },
  "meteorological_factors": ["Wind speed"],
  "street_canyons": ["Vehicle speed"],
  "pollutant_source_relations": [
    ["NOx", "Cars"]
  ],
  "source_mitigation_relations": [
    ["Cars", "Low-emission zones"]
  ],
  "meteorological_dispersion_relations": [
    {
      "meteorological_factor": "Wind speed",
      "pollutants": ["NOx"],
      "effect": "Increased wind speed disperses NOx reducing its concentration."
    }
  ],
  "street_canyon_dispersion_relations": [
    {
      "street_canyon_factor": "Vehicle speed",
      "pollutant": "NOx",
      "effect": "Reduced vehicle speed increases NOx concentrations.",
      "direction": ""
    }
  ]
}
```

**Explicit rules for LLM JSON generation:**

- Every category explicitly defined must appear exactly as shown.
- If a category has no information, explicitly return empty lists (`[]`).
- DO NOT add any fields, categories, or values not explicitly demonstrated here.
- Return ONLY valid JSON without explanations or additional commentary.
