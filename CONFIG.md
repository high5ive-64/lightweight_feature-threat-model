# Configuration Guide

This document explains all configuration options for Feature Threat Model.

## Quick Start

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set your values (see below).

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Configuration Options

### Application Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | `Feature Threat Model API` | Name shown in API docs |
| `HOST` | `0.0.0.0` | Host address to bind to |
| `PORT` | `8000` | Port to listen on |
| `RELOAD` | `true` | Enable auto-reload for development |

### Provider Selection

| Variable | Default | Description |
|----------|---------|-------------|
| `PROVIDER` | `openai` | LLM backend to use (`openai` or `lmstudio`) |

### OpenAI Settings

Used when `PROVIDER=openai`.

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *required* | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model to use (e.g., `gpt-4o`, `gpt-4o-mini`) |
| `OPENAI_BASE_URL` | *OpenAI default* | Optional custom base URL for OpenAI-compatible endpoints |

### LM Studio Settings

Used when `PROVIDER=lmstudio`.

| Variable | Default | Description |
|----------|---------|-------------|
| `LMSTUDIO_BASE_URL` | `http://127.0.0.1:1234/v1` | LM Studio server URL |
| `LMSTUDIO_API_KEY` | `lm-studio` | API key (LM Studio accepts any value) |
| `LMSTUDIO_MODEL` | `local-model` | Model name loaded in LM Studio |

### Threat Model Generation Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_RETRIES` | `2` | Number of retry attempts for LM Studio validation failures |
| `DEFAULT_SEVERITY` | `Medium` | Default severity for threats |

## Environment Variable Priority

Configuration is loaded in this order (later overrides earlier):

1. Default values in `app/config.py`
2. `.env` file
3. Environment variables in your shell

## Example Configurations

### Using OpenAI

```env
PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

### Using LM Studio

```env
PROVIDER=lmstudio
LMSTUDIO_BASE_URL=http://127.0.0.1:1234/v1
LMSTUDIO_MODEL=meta-llama-3.1-8b-instruct
```

### Using a Custom OpenAI-Compatible Endpoint

```env
PROVIDER=openai
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://your-endpoint.com/v1
OPENAI_MODEL=your-model
```

## Debugging

To view current configuration:

```bash
python -m app.config
```

This prints all resolved settings as JSON.