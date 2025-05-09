# urban-air-quality-kg

## Overview

This project provides a semantically enriched **Knowledge Graph (KG)** for exploring urban air quality phenomena and associated mitigation measures. It leverages **Neo4j** for graph management, **SentenceTransformers** for embedding generation, and a **local Retrieval-Augmented Generation (RAG) pipeline** powered by a locally hosted large language model (LLM), enabling users to query and interact with air quality data in natural language.

---

## 🚀 Features

- **Knowledge Graph Storage:** Uses Neo4j for storing and managing structured data about pollutants, pollution sources, meteorological factors, and mitigation measures.
- **Semantic Embeddings:** Employs SentenceTransformers to embed KG nodes semantically, enabling effective similarity searches.
- **Local RAG Pipeline:** Integrates a locally hosted large language model using Llama.cpp for natural language querying and information retrieval from the KG.

---

## 📂 Repository Structure



## Installation

Follow these steps to set up the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/XiangX91/urban-air-quality-kg.git
cd urban-air-quality-kg
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Neo4j


## Interactive Urban Air Quality Knowledge Graph (baseline)
**Click on the image above to explore the interactive knowledge graph.**
[![Interactive Visualisation](images/visualisation-preview.png)](https://xiangx91.github.io/urban-air-quality-kg/visualisation/)

## License
This work is licensed under a [Creative Commons Attribution 4.0 International License](LICENSE).
