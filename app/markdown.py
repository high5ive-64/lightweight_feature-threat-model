from app.schemas import FeatureInput, ThreatModelResponse


def render_markdown(feature: FeatureInput, model: ThreatModelResponse) -> str:
    lines = [
        f"# Threat model: {model.feature_name}",
        "",
        "## Feature summary",
        feature.summary,
        "",
        "## Inputs",
        f"- Actors: {', '.join(feature.actors) or 'Unknown'}",
        f"- Data elements: {', '.join(feature.data_elements) or 'Unknown'}",
        f"- Entry points: {', '.join(feature.entry_points) or 'Unknown'}",
        f"- Trust boundaries: {', '.join(feature.trust_boundaries) or 'Unknown'}",
        f"- Integrations: {', '.join(feature.integrations) or 'None'}",
        f"- Internet facing: {'Yes' if feature.internet_facing else 'No'}",
        f"- Authentication: {feature.authentication or 'Not provided'}",
        f"- Authorization: {feature.authorization or 'Not provided'}",
        f"- Sensitive actions: {', '.join(feature.sensitive_actions) or 'None'}",
        "",
        "## Assets",
    ]

    for asset in model.assets:
        lines.append(f"- {asset}")

    lines.extend(["", "## Threats"])

    for idx, threat in enumerate(model.threats, start=1):
        lines.extend([
            f"### {idx}. {threat.title}",
            f"- STRIDE: {threat.stride}",
            f"- Severity: {threat.severity}",
            f"- Likelihood: {threat.likelihood}",
            f"- Scenario: {threat.scenario}",
            f"- Impact: {threat.impact}",
            "- Mitigations:",
        ])
        for mitigation in threat.mitigations:
            lines.append(f"  - {mitigation}")
        if threat.assumptions:
            lines.append("- Assumptions:")
            for assumption in threat.assumptions:
                lines.append(f"  - {assumption}")
        lines.append("")

    lines.append("## Abuse cases")
    for abuse_case in model.abuse_cases:
        lines.append(f"- {abuse_case}")

    lines.extend(["", "## Security questions"])
    for question in model.security_questions:
        lines.append(f"- {question}")

    return "\n".join(lines)