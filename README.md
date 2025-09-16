# Secure Multi-Model Inference Gateway (FastAPI + Ollama)

A local HTTP server for secure prompt routing to multiple locally installed LLMs using [Ollama](https://ollama.com). Built with FastAPI, the gateway enforces API key authentication, model validation, and fault-tolerant streaming, and is intended for air-gapped or privacy-sensitive deployments (e.g., defense, research, simulation environments).



## Overview

This project implements a secure inference gateway that:

- Exposes a single HTTP POST endpoint (`/request`)
- Accepts prompts and model names via JSON
- Routes the prompt to a specified local LLM via Ollama
- Streams the response line-by-line back to the client
- Enforces access control with an API key
- Handles upstream failures gracefully (e.g., Ollama not reachable)


## Features

- Model routing (e.g., `"phi"`, `"mistral"`, `"tinyllama"`)
- API key check (`X-API-KEY`)
- JSON-based POST request format
- Streaming response reconstruction from JSONL
- Exception handling for broken model connections
- All models run locally — no cloud access required


## Architecture Summary

- FastAPI app runs on `http://localhost:8085`
- Loads available model list from Ollama via `/api/tags`
- Validates all requested model names before inference
- Sends prompt to `http://localhost:11434/api/generate`
- Collects `"response"` fields from JSONL chunks
- Returns full answer as plain text

## Security Model

| Layer | Mechanism |
|-------|-----------|
| API Access | Requires valid `X-API-KEY` header |
| Model validation | Rejects unknown or unsupported models |
| Isolation | No external HTTP requests made; inference stays local |
| Failure handling | Returns status `502` if Ollama fails or is offline |


## 🛠️ Installing Dependencies

Before running the Secure Inference Gateway, make sure you have:

- Python 3.8+
- [Ollama](https://ollama.com) installed and configured
- Required Python packages

### 1. Install Python Dependencies

It's recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn requests
```


## Usage

### Request Format (JSON)

```json
{
  "model": "phi",
  "request": "Give me a fun fact about gravity."
}
