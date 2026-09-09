# Private Document Intelligence Engine

![CI](https://github.com/Takato-1887/rag-document-engine/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> A production-grade, local-first Retrieval-Augmented Generation (RAG) system — built from the ground up across 20 phases, with GPU-accelerated embeddings, hybrid search, and full observability. No cloud dependency required for inference.

## Why this project

Most RAG tutorials stop at "load a PDF, embed it, ask a question." This project goes further: it's built the way a production system actually needs to be — typed, tested, CI-gated, containerized, and evaluated against real retrieval-quality metrics (RAGAS), not just vibes.

Everything runs **locally** on consumer hardware (developed on an RTX 5050 8GB laptop GPU) — no OpenAI API key required, though cloud LLM providers are supported as an option.
