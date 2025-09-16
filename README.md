# 🔐 Secure Multi-Model Inference Gateway (FastAPI + Ollama)

> A lightweight, secure, and extensible HTTP gateway for dispatching prompt requests to local LLMs via Ollama.  
> Designed for air-gapped, privacy-sensitive environments (e.g., defense, aerospace, R&D).

---

## 🧠 Motivation

In high-security environments (like defense, enterprise research, or robotics), cloud-based LLMs can't be used due to privacy concerns. This gateway allows:

- Secure **local inference** using multiple models
- Controlled access with API key authentication
- Clean routing between models via a RESTful interface
- Future extensions like **multi-model voting**, **access control**, and **auditing**

---

## ✅ Core Features

- 🔁 **POST /request** — send prompts and route to correct model
- 🔐 **API Key Auth** — secure access with `X-API-KEY`
- 🧠 **Model Validation** — supports any installed Ollama model
- 🧼 **Streaming Response Handling** — parses Ollama JSONL output
- 🔧 **Graceful Error Handling** — handles connection and inference failures
- 🛡️ **Air-Gapped Ready** — no external dependencies

---

## 🔐 Security Features

| Feature | Description |
|--------|-------------|
| 🔑 API Key Authentication | Blocks unauthorized access (`X-API-KEY: admin`) |
| 🚫 Model Filtering | Rejects prompts for unknown models |
| 🧯 Ollama Error Handling | Returns `502` if Ollama is unreachable |
| ✅ Response Sanitization | Only returns plain text content |
| 🌐 No External Calls | All inference runs **entirely locally**

---

## 🚀 API Usage

### 🔁 POST `/request`

```json
{
  "model": "phi",
  "request": "Give me a fun fact about black holes."
}
