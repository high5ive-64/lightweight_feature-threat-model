# Security

This project helps generate threat models; it is not itself a security boundary. Treat it as you would any internal service.

## Best practices

- **Secrets**: Store API keys and sensitive config in `.env`; do not commit this file.
- **Access**: For internal deployments, consider restricting access (e.g., network-level controls or simple auth).
- **LLM output**: Validate and review all generated threat models before using them for decisions.
- **Providers**: Understand differences between providers (e.g., structured output guarantees vs. best-effort JSON).

## Reporting issues

For security-related issues (e.g., accidental secret exposure), open an issue or contact the maintainers directly.