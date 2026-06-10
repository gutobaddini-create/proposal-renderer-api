from __future__ import annotations

import re
from typing import Any


EMAIL_MARKDOWN_RE = re.compile(
    r"\[([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})\]\(mailto:[^)]+\)"
)
MAILTO_RE = re.compile(r"mailto:([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})")


def sanitize_string(value: str) -> str:
    value = EMAIL_MARKDOWN_RE.sub(r"\1", value)
    value = MAILTO_RE.sub(r"\1", value)
    return value


def sanitize_proposal_json(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {key: sanitize_proposal_json(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [sanitize_proposal_json(value) for value in obj]
    if isinstance(obj, str):
        return sanitize_string(obj)
    return obj


def collect_warnings(obj: Any) -> list[str]:
    warnings: list[str] = []

    def visit(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, nested_value in value.items():
                next_path = f"{path}.{key}" if path else str(key)
                visit(nested_value, next_path)
        elif isinstance(value, list):
            for index, nested_value in enumerate(value):
                visit(nested_value, f"{path}[{index}]")
        elif isinstance(value, str) and "[informar]" in value.lower():
            warnings.append(f"Campo pendente encontrado em {path}.")

    visit(obj, "")
    return warnings
