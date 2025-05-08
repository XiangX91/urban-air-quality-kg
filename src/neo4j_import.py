"""
Urban Air Quality Knowledge Graph Import Module

This module provides functionality to import structured urban air quality
information from validated JSON data into a Neo4j knowledge graph database.

Author: Xiang Xie (xiang.xie@ncl.ac.uk)
Date: 01/02/2025
"""

import json
from neo4j import GraphDatabase
from pathlib import Path

def import_air_quality_json_to_neo4j(json_filepath, uri, username, password):
    """
    Imports air quality JSON data into a local Neo4j database.

    Args:
        json_filepath (str or Path): Path to the validated air quality JSON file.
        uri (str): Neo4j database URI (default local is "bolt://localhost:7687").
        username (str): Username for the Neo4j database (default is usually "neo4j").
        password (str): Password for the Neo4j database.

    Requirements for local Neo4j setup:
    -----------------------------------
    1. Install Neo4j Community Edition:
       - Download from: https://neo4j.com/download-center/#community
       - Install and run the Neo4j Desktop or server.

    2. Setup local Neo4j instance:
       - Default URI: bolt://localhost:7687
       - Default Username: neo4j
       - Set a password upon first login via the Neo4j browser (usually http://localhost:7474).

    3. Install required Python package explicitly:
       ```
       pip install neo4j
       ```

    4. Ensure Neo4j is running locally before executing this script.

    Example Usage:
    --------------
    ```python
    import_air_quality_json_to_neo4j(
        json_filepath="Validated_air_quality_knowledge.json",
        uri="bolt://localhost:7687",
        username="neo4j",
        password="your_password_here"
    )
    ```
    """
    # Connect to Neo4j explicitly
    driver = GraphDatabase.driver(uri, auth=(username, password))

    # Load JSON data explicitly
    with open(json_filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    def insert_data(tx, data):
        # Create Pollutant nodes explicitly
        for category, pollutants in data["pollutants"].items():
            for pollutant in pollutants:
                tx.run("""
                    MERGE (p:Pollutant {name: $pollutant, category: $category})
                """, pollutant=pollutant, category=category)

        # Create Pollution Source nodes explicitly
        for category, sources in data["pollution_sources"].items():
            for source in sources:
                tx.run("""
                    MERGE (s:Source {name: $source, category: $category})
                """, source=source, category=category)

        # Create Mitigation Measure nodes explicitly
        for category, measures in data["mitigation_measures"].items():
            for measure in measures:
                tx.run("""
                    MERGE (m:MitigationMeasure {name: $measure, category: $category})
                """, measure=measure, category=category)

        # Create Meteorological Factor nodes explicitly
        for factor in data["meteorological_factors"]:
            tx.run("""
                MERGE (mf:MeteorologicalFactor {name: $factor})
            """, factor=factor)

        # Create Street Canyon nodes explicitly
        for canyon in data["street_canyons"]:
            tx.run("""
                MERGE (sc:StreetCanyon {description: $canyon})
            """, canyon=canyon)

        # Create explicit relationships (Pollutant-Source)
        for pollutant, source in data["pollutant_source_relations"]:
            tx.run("""
                MATCH (p:Pollutant {name: $pollutant}), (s:Source {name: $source})
                MERGE (s)-[:EMITS]->(p)
            """, pollutant=pollutant, source=source)

        # Create explicit relationships (Source-Mitigation)
        for source, mitigation in data["source_mitigation_relations"]:
            tx.run("""
                MATCH (s:Source {name: $source}), (m:MitigationMeasure {name: $mitigation})
                MERGE (m)-[:MITIGATES]->(s)
            """, source=source, mitigation=mitigation)

        # Create explicit relationships (Meteorological Dispersion)
        for relation in data["meteorological_dispersion_relations"]:
            factor = relation["meteorological_factor"]["type"]
            pollutant = relation["pollutant"]
            tx.run("""
                MATCH (mf:MeteorologicalFactor {name: $factor}), (p:Pollutant {name: $pollutant})
                MERGE (mf)-[:AFFECTS_DISPERSION]->(p)
            """, factor=factor, pollutant=pollutant)

        # Create explicit relationships (Street Canyon Dispersion)
        for relation in data["street_canyon_dispersion_relations"]:
            description = relation["street_canyon_description"]
            pollutant = relation["pollutant"]
            tx.run("""
                MATCH (sc:StreetCanyon {description: $description}), (p:Pollutant {name: $pollutant})
                MERGE (sc)-[:AFFECTS_DISPERSION]->(p)
            """, description=description, pollutant=pollutant)

    # Execute the data insertion explicitly
    with driver.session() as session:
        session.execute_write(insert_data, data)

    # Close the Neo4j connection explicitly
    driver.close()

    print("✅ Data successfully imported into Neo4j!")

# If this script is run directly, perform the following example action explicitly
if __name__ == "__main__":
    # User must explicitly adjust these details
    import_air_quality_json_to_neo4j(
        json_filepath="Validated_air_quality_knowledge.json",
        uri="bolt://localhost:7687",
        username="neo4j",
        password="your_password_here"
    )
