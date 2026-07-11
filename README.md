# AI / AI-Agents (10xlearn)

This repository is a growing workspace for learning, experimenting, and building with AI.
Instead of keeping everything in separate small repos, the idea here is to keep related work in one place while still giving each area its own space.

Right now the repository has multiple categories:

- `python-for-ai/` for Python fundamentals with an AI-focused learning path
- `agents/` for learning and experimenting with AI agent workflows
- `RAG/` for Retrieval-Augmented Generation experiments

For shared setup guidance, see [SETUP.md](/home/shubham/projects/AI/10xlearn/SETUP.md:1).

## Repository Approach

This repo is intentionally organized like a monolith for AI learning and small proof-of-concepts:

- one repository for related AI tracks
- one top-level folder per topic or category
- each folder can evolve as its own small learning module or project

That structure helps keep things simple:

- everything stays visible in one place
- new categories can be added without creating a new repo every time
- each area still has clear boundaries

## Current Repository Structure

```text
.
├── README.md
├── RAG/
│   ├── requirements.txt
│   └── llamaindex/
│       └── basic/
├── agents/
│   ├── requirements.txt
│   └── learn/
│       ├── agentworkflow/
│       └── multistep/
└── python-for-ai/
    ├── README.md
    └── learn/
        ├── variables.ipynb
        ├── functions.ipynb
        └── package.ipynb
```

## Categories

### `python-for-ai`

This module is meant for learning or revisiting Python fundamentals with AI use cases in mind.
It is especially useful for developers coming from other languages, or for anyone who wants a smoother start with Python before jumping deeper into AI frameworks and tooling.

Current learning material includes notebook-based lessons such as:

- variables
- functions
- packages

Read more in [python-for-ai/README.md](/home/shubham/projects/AI/10xlearn/python-for-ai/README.md:1).

### `agents`

This area is focused on learning AI-agent patterns and workflows.
Based on the current structure, it includes experiments around:

- basic workflows
- multi-step flows
- agent workflows with context and supervision patterns

This section is more code-driven right now and can grow into a more structured learning path over time.

### `RAG`

The `RAG` folder is for Retrieval-Augmented Generation experiments built around LlamaIndex.
At the moment it includes a basic setup for:

- ingestion
- indexing
- querying
- evaluation

This makes it the more implementation-focused part of the repo compared to the learning-first modules.

## How to navigate this repo

If your goal is to build a stronger foundation first, start with `python-for-ai/`.
If you want to understand agent patterns, explore `agents/`.
If you want to experiment with retrieval pipelines and LLM-backed querying, go into `RAG/`.

Each top-level folder should be treated as its own area of work, with its own code, dependencies, and documentation as it grows.

For environment setup and dependency installation, follow the shared instructions in [SETUP.md](/home/shubham/projects/AI/10xlearn/SETUP.md:1), then use any module-specific documentation where needed.

## Direction

This repository will likely keep expanding with more categories over time.
The main goal is to make `10xlearn` a practical place for learning by building, not just collecting isolated code samples.
