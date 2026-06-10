from __future__ import annotations

from pathlib import Path
from typing import Any

from docx import Document


def generate_visual_docx_placeholder(data: dict[str, Any], output_dir: Path) -> Path:
    path = output_dir / "proposta_visual.docx"
    document = Document()
    proposal = data.get("proposal", {})
    document.add_heading(proposal.get("title", "Proposta Jurídica"), level=0)
    document.add_paragraph(
        "Documento visual de alta fidelidade pendente. Nesta versão inicial, "
        "use o PDF e o Word editável gerados pela API."
    )
    document.save(path)
    return path
