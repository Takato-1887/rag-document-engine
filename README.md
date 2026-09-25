 # Private Document Intelligence Engine

![CI](https://github.com/Takato-1887/rag-document-engine/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> A production-grade, local-first Retrieval-Augmented Generation (RAG) system — built from the ground up across 20 phases, with GPU-accelerated embeddings, hybrid search, and full observability. No cloud dependency required for inference.

## Why this project

Most RAG tutorials stop at "load a PDF, embed it, ask a question." This project goes further: it's built the way a production system actually needs to be — typed, tested, CI-gated, containerized, and evaluated against real retrieval-quality metrics (RAGAS), not just vibes.

Everything runs **locally** on consumer hardware (developed on an RTX 5050 8GB laptop GPU) — no OpenAI API key required, though cloud LLM providers are supported as an option.

## Architecture
Documents → Ingestion → Chunking → Embedding (GPU) → Vector Store
↓
User Query → Hybrid Search (dense + sparse) → Re-Ranking → LLM → Answer

*(Full architecture diagram coming as the pipeline is built out — see Project Status below.)*

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Package management | uv |
| Embeddings | sentence-transformers (GPU/CUDA) |
| Vector store | *(TBD — Phase 5)* |
| LLM serving | Ollama (local) / OpenAI / Anthropic (optional) |
| API | FastAPI |
| Frontend | Gradio |
| Evaluation | RAGAS |
| Experiment tracking | MLflow |
| Deployment | Docker |
| CI/CD | GitHub Actions |
| Code quality | Ruff, mypy, pre-commit |

## Getting Started

### Prerequisites
- Python 3.12
- [uv](https://docs.astral.sh/uv/) package manager
- (Optional but recommended) NVIDIA GPU with CUDA support for embedding acceleration



## Getting Started

### Prerequisites
- Python 3.12
- [uv](https://docs.astral.sh/uv/) package manager
- (Optional but recommended) NVIDIA GPU with CUDA support for embedding acceleration

### Setup

```bash
git clone https://github.com/Takato-1887/rag-document-engine.git
cd rag-document-engine

# Install dependencies and pre-commit hooks
uv tool install rust-just   # one-time, if you don't have `just`
just install

# Copy environment template and fill in your values
cp .env.example .env
```
### Common commands

```bash
just check         # run all quality checks (lint, format, types, tests) — mirrors CI
just test          # run test suite
just lint-fix       # auto-fix lint issues
just verify-config  # sanity-check your .env loads correctly
```
See the `justfile` for the full command list, or run `just` with no arguments.

## Project Status

Currently in active development, following a 20-phase build roadmap.



