# Setup

This repository is organized into separate modules, and each module can manage its own dependencies.
The overall setup approach is simple:

- use `uv` for virtual environment management
- create the virtual environment inside the module you want to work on
- install dependencies from that module's `requirements.txt` if it has one

## General approach

Each top-level folder in this repo should be treated as its own working area.
That means you usually do setup from inside the specific module, not from the root of the repository.

For example:

- `python-for-ai/` for Python learning notebooks and exercises
- `agents/` for agent workflow learning and experiments
- `RAG/` for retrieval-augmented generation experiments

## Basic setup flow

### 1. Move into the module

```bash
cd <module-name>
```

Example:

```bash
cd agents
```

### 2. Create a virtual environment with `uv`

```bash
uv venv
```

This creates a local `.venv/` inside that module.

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 4. Install dependencies if the module has a `requirements.txt`

```bash
uv pip install -r requirements.txt
```

## Current modules with `requirements.txt`

At the moment, dependency files are present in:

- `agents/requirements.txt`
- `RAG/requirements.txt`

Some modules may be more notebook-focused or learning-focused and may not need a dedicated `requirements.txt` yet.

## Recommended workflow

If you are working on one module, keep its virtual environment isolated to that module.
That keeps the setup cleaner and avoids mixing unrelated dependencies across different categories in the repo.

In short:

- create the environment inside the module
- activate it before working
- install only that module's dependencies

## Notes

- if a module grows, it can keep evolving its own setup instructions
- root-level documentation gives the general pattern, while module-level docs can add module-specific details
- this structure makes it easier to expand the repo without forcing every category into the same environment
