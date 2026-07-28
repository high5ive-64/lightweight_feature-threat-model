<<<<<<< HEAD
# lightweight_feature-threat-model
A lightweight API to help create threat models for new prod features
=======
# Feature Threat Model

A minimal, opinionated FastAPI service for generating STRIDE-based threat models for new features using real LLM providers.

This tool is designed for **security engineers and engineering managers** who want to integrate threat modeling into their feature development workflow without the overhead of a full threat modeling platform.

---

## Table of Contents

- [Features](#features)
- [What is STRIDE?](#what-is-stride)
- [Use Cases](#use-cases)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Example Requests](#example-requests)
- [Project Structure](#project-structure)
- [Adding a New Provider](#adding-a-new-provider)
- [Design Notes](#design-notes)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)
- [Example Outputs](#example-requests) 

---

## Features

- **STRIDE threat modeling** for feature-level changes
- **Real LLM backends**:
  - OpenAI (Responses API with structured parsing)
  - LM Studio (OpenAI-compatible endpoint with validation retries)
- **Clean provider abstraction** for easy extension
- **JSON and Markdown export** endpoints
- **Simple configuration** via `.env` or environment variables
- **Lightweight and fast** – no heavy dependencies

---

## What is STRIDE?

STRIDE is a threat modeling framework developed by Microsoft that categorizes threats into six types:

| Category | Description | Example |
|----------|-------------|---------|
| **Spoofing** | Impersonating a user or system | Attacker uses stolen credentials to access user data |
| **Tampering** | Modifying data or code | Attacker modifies API requests to escalate privileges |
| **Repudiation** | Denying actions without proof | User claims they didn't perform an action, no audit trail exists |
| **Information Disclosure** | Exposing sensitive information | API returns more data than intended, exposing PII |
| **Denial of Service** | Disrupting service availability | Attacker floods endpoint, causing service degradation |
| **Elevation of Privilege** | Gaining unauthorized access | User exploits bug to access admin functions |

This tool uses STRIDE to systematically identify threats for new features.

---

## Use Cases

### When to Use This Tool

- **Feature design reviews** – Generate threat models during PRD or design doc reviews
- **Backlog refinement** – Identify security requirements before sprint planning
- **Architecture discussions** – surface threats in new integrations or trust boundaries
- **Security champion workflows** – Enable engineers to self-serve threat models

### Example Scenarios

- "We're adding file uploads to support tickets – what are the threats?"
- "New webhook integration with third-party service – what could go wrong?"
- "Adding admin dashboard with elevated privileges – what should we consider?"

---

## Quick Start

### Prerequisites

- Python 3.11+
- Access to either:
  - OpenAI API key, or
  - LM Studio running locally

### Step-by-Step

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/feature-threat-model.git
cd feature-threat-model

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment
cp .env.example .env
# Edit .env with your API keys and preferences

# 5. Run the API server
uvicorn app.main:app --reload
```

API docs will be available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Configuration

All configuration is managed via `.env` or environment variables.

### Minimal Configuration

```env
# Choose provider: "openai" or "lmstudio"
PROVIDER=openai

# OpenAI settings (required if PROVIDER=openai)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

### Full Configuration

See [CONFIG.md](CONFIG.md) for detailed documentation on all options.

```env
# Application Settings
APP_NAME="Feature Threat Model API"
HOST=0.0.0.0
PORT=8000
RELOAD=true

# Provider Selection
PROVIDER=openai

# OpenAI Settings
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://your-custom-endpoint.com/v1

# LM Studio Settings
LMSTUDIO_BASE_URL=http://127.0.0.1:1234/v1
LMSTUDIO_API_KEY=lm-studio
LMSTUDIO_MODEL=meta-llama-3.1-8b-instruct

# Threat Model Generation
MAX_RETRIES=2
DEFAULT_SEVERITY=Medium
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check and current provider |
| `/providers` | GET | List supported and configured providers |
| `/threat-model` | POST | Generate JSON threat model |
| `/threat-model.md` | POST | Generate Markdown threat model |

---

## Example Requests

### Example 1: Basic Feature

```bash
curl -X POST "http://127.0.0.1:8000/threat-model" \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

### Example 2: File Upload Feature

```json
{
  "feature_name": "User profile picture upload",
  "summary": "Users can upload a profile picture (max 5MB) to their account",
  "actors": ["Authenticated User"],
  "data_elements": ["Profile picture", "User ID", "File metadata"],
  "entry_points": ["REST API /users/{id}/avatar"],
  "trust_boundaries": ["Client to API", "API to object storage"],
  "integrations": ["S3", "Image resizing service"],
  "internet_facing": true,
  "authentication": "JWT bearer token",
  "authorization": "Users can only update their own profile",
  "sensitive_actions": ["File upload", "File deletion"]
}
```

### Example 3: Markdown Export

```bash
curl -X POST "http://127.0.0.1:8000/threat-model.md" \
  -H "Content-Type: application/json" \
  -d '{
    "feature_name": "Webhook notifications",
    "summary": "Send order events to customer-configured webhook URLs",
    "actors": ["System", "Customer"],
    "data_elements": ["Order data", "Webhook URL", "Secret token"],
    "entry_points": ["Event processor", "HTTP client"],
    "trust_boundaries": ["Internal service to external URL"],
    "integrations": [],
    "internet_facing": true,
    "authentication": "HMAC signature",
    "authorization": "N/A",
    "sensitive_actions": ["Webhook delivery"]
  }' \
  -o threat-model.md
```

### Example 4: Using test_request.json

```bash
# View the example request
cat test_request.json

# Send it to the API
curl -X POST "http://127.0.0.1:8000/threat-model" \
  -H "Content-Type: application/json" \
  -d @test_request.json

# Save Markdown output
curl -X POST "http://127.0.0.1:8000/threat-model.md" \
  -H "Content-Type: application/json" \
  -d @test_request.json \
  -o output.md
```

---

## Project Structure
feature-threat-model/
├── app/
│ ├── main.py # FastAPI routes and endpoints
│ ├── config.py # Centralized configuration
│ ├── schemas.py # Pydantic request/response models
│ ├── prompting.py # System and user prompt templates
│ ├── markdown.py # Markdown report renderer
│ ├── service.py # Business logic orchestration
│ └── llm/
│ ├── base.py # Abstract provider interface
│ ├── factory.py # Provider selection logic
│ ├── openai_provider.py # OpenAI implementation
│ └── lmstudio_provider.py # LM Studio implementation
├── requirements.txt # Python dependencies
├── .env.example # Configuration template
├── test_request.json # Example API request
├── README.md # This file
├── CONFIG.md # Configuration documentation
├── CONTRIBUTING.md # Contribution guidelines
├── SECURITY.md # Security considerations
├── LICENSE # MIT license
└── setup.sh # One-line setup script


---

## Adding a New Provider

The architecture supports adding new LLM backends easily.

### Step 1: Create Provider Implementation

Create `app/llm/your_provider.py`:

```python
from app.llm.base import LLMProvider
from app.schemas import FeatureInput, ThreatModelResponse


class YourProvider(LLMProvider):
    def __init__(self) -> None:
        # Initialize your client
        pass

    def generate_threat_model(self, feature: FeatureInput) -> ThreatModelResponse:
        # Call your LLM and return ThreatModelResponse
        pass
```

### Step 2: Register in Factory

Update `app/llm/factory.py`:

```python
from app.llm.your_provider import YourProvider

def get_provider() -> LLMProvider:
    provider = settings.provider.lower()
    if provider == "openai":
        return OpenAIProvider()
    if provider == "lmstudio":
        return LMStudioProvider()
    if provider == "your_provider":  # Add this
        return YourProvider()
    raise ValueError(f"Unsupported provider: {provider}")
```

### Step 3: Add Configuration

Add fields in `app/config.py` and document in `.env.example`.

### Step 4: Test

```bash
PROVIDER=your_provider uvicorn app.main:app --reload
```

---

## Design Notes

### Philosophy

- **Feature-focused**: Assesses net-new features, not entire systems
- **Actionable output**: Concise threats with mitigations, not generic advice
- **Explicit uncertainty**: Captures assumptions and open questions
- **Provider-flexible**: Swap backends without code changes

### Why This Approach?

Traditional threat modeling tools are often:

- Too heavy for quick feature reviews
- Focused on diagramming over actionable output
- Difficult to integrate into development workflows

This tool aims to be:

- **Fast**: Get a threat model in seconds
- **Lightweight**: Minimal dependencies, easy to deploy
- **Integratable**: JSON output for automation, Markdown for humans

### Output Schema

All threat models follow a consistent structure:

- `feature_name`, `summary` – Feature description
- `assets` – Identified data/assets at risk
- `trust_boundaries` – Security boundaries identified
- `threats[]` – STRIDE-categorized threats with:
  - `stride`, `title`, `scenario`, `impact`
  - `likelihood`, `severity`
  - `mitigations[]`, `assumptions[]`
- `abuse_cases[]` – Specific attack scenarios
- `security_questions[]` – Open questions for the team

---

## Security Considerations

### Secrets Management

- **Never commit `.env`** – It's ignored by `.gitignore`
- **Use environment variables** in production deployments
- **Rotate API keys** regularly

### LLM Output

- **Treat as untrusted** – Always review and validate
- **Human in the loop** – Don't auto-apply mitigations
- **Context matters** – Models may miss domain-specific threats

### Access Control

- **Internal use** – Consider adding auth (API key, SSO)
- **Network isolation** – Run behind firewall or VPC
- **Rate limiting** – Prevent abuse in shared environments

### Provider-Specific Notes

- **OpenAI**: Structured output is more reliable but still review
- **LM Studio**: Local models may be less reliable; use retries

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Good First Contributions

- Add new LLM providers (Anthropic, Ollama, etc.)
- Improve prompt templates for better output
- Add integrations (Jira, Linear, GitHub Issues)
- Create UI frontends (Streamlit, HTML form)
- Enhance documentation and examples

### How to Contribute

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Make your changes and test locally
4. Open a pull request describing the change

---

## License

MIT License – see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- Inspired by [STRIDE GPT](https://github.com/mrwadams/stride-gpt)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Uses [Pydantic](https://docs.pydantic.dev/)

---

## Support

- Open an issue for bugs or feature requests
- Contact maintainers for security-related concerns

---

**Happy threat modeling! 🛡️**
>>>>>>> 64dfa9e (Initial commit)
