# AI / AI-Agents (10xlearn)

This repository is a growing home for small, focused AI and AI-agent proof-of-concepts.
The goal is to keep everything in one place while still organizing each PoC like a small, self-contained package.

Right now the first packaged project is:

- `RAG/`: a Retrieval-Augmented Generation PoC built with LlamaIndex and ChromaDB

## Repository Approach

This repo is intentionally structured like a monolith:

- one repository for related experiments
- one folder per PoC or domain
- each project keeps its own code, dependencies, and run instructions

That gives us a few benefits:

- shared visibility across experiments
- easier incremental expansion without creating many tiny repos
- clearer boundaries inside each project folder

As the repo grows, new projects can follow the same pattern:

```text
.
├── README.md
├── RAG/
│   ├── requirements.txt
│   └── llamaindex/
│       └── basic/

```

## Current Project: `RAG`

The `RAG` folder is designed to be runnable as its own project.

### Structure

```text
RAG/
├── requirements.txt
└── llamaindex/
    ├── __init__.py
    └── basic/
        ├── __init__.py
        ├── db.py
        ├── indexing.py
        ├── ingestion_pipeline.py
        └── rag.py
```

### What It Does

- `ingestion_pipeline.py` downloads and prepares the dataset, creates embeddings, and stores vectors in ChromaDB
- `db.py` configures the local Chroma vector store
- `indexing.py` loads the vector store into a LlamaIndex index
- `rag.py` runs a query against the indexed data

## Setup

This project currently uses `uv` for environment management, but the Python dependencies are still declared in `RAG/requirements.txt`.

### 1. Create and activate the environment

```bash
cd RAG
uv venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 3. Configure environment variables

Keep your local secrets outside the repo structure at the same level as `RAG/`.

Example layout:

```text
.
├── .env.local
└── RAG/
```

Before running the project, rename `.env.local` to `.env` after adding your own secrets.

Expected secret:

```env
HF_TOKEN=your_huggingface_token
OPEN_ROUTER_KEY=your_openrouterkey
```

## Running The RAG PoC

Run modules from inside `RAG/`:

### Ingest data

```bash
cd RAG
python -m llamaindex.basic.ingestion_pipeline
```
### Run indexing
```bash
python -m llamaindex.basic.indexing
```
### Run a query

```bash
cd RAG
python -m llamaindex.basic.rag
```

## Roadmap

Likely next improvements:

- add a `RAG/.env.example`
- add more RAG variants under `RAG/llamaindex/`
- add new top-level PoC folders for other agent or retrieval experiments
