# Contributing

Thanks for considering contributions! This project is intended as a minimal, practical tool for feature-level threat modeling.

## How to contribute

- **New providers**: Add a new backend in `app/llm/` and register it in `factory.py`.
- **Prompt/schema improvements**: Adjust `prompting.py` and `schemas.py` with clear rationale.
- **Integrations**: Add helpers or examples for Jira, Linear, GitHub Issues, etc.
- **Docs**: Clarify usage, examples, or security considerations.

## Guidelines

- Keep changes focused and minimal.
- Ensure the app runs with both OpenAI and LM Studio providers when possible.
- Update README.md if behaviour or configuration changes.
- Avoid adding heavy dependencies; this is intended as a lightweight service.

## Pull requests

- Describe what the change does and why.
- Include example requests/responses if relevant.
- Note any configuration changes required.