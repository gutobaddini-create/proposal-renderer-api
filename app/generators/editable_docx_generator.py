from __future__ import annotations

from pathlib import Path
from typing import Any

from docx import Document


def _add_key_value(document: Document, label: str, value: Any) -> None:
    paragraph = document.add_paragraph()
    paragraph.add_run(f"{label}: ").bold = True
    paragraph.add_run(str(value or ""))


def generate_editable_docx(data: dict[str, Any], output_dir: Path) -> Path:
    path = output_dir / "proposta_editavel.docx"
    document = Document()

    provider = data.get("provider", {})
    client = data.get("client", {})
    proposal = data.get("proposal", {})
    investment = proposal.get("investment", {})
    term = proposal.get("term", {})

    document.add_heading(proposal.get("title", "Proposta Jurídica"), level=0)
    if proposal.get("subtitle"):
        document.add_paragraph(proposal["subtitle"])

    document.add_heading("Dados da proposta", level=1)
    _add_key_value(document, "Contratante", client.get("name"))
    _add_key_value(document, "Proponente", provider.get("name"))
    _add_key_value(document, "Responsável", provider.get("responsible"))
    _add_key_value(document, "E-mail", provider.get("email"))

    document.add_heading("Investimento", level=1)
    document.add_paragraph(str(investment.get("amountText", "")))

    document.add_heading("Prazo", level=1)
    document.add_paragraph(str(term.get("duration", "")))

    document.add_heading("Escopo", level=1)
    for section in data.get("layoutPlan", []):
        document.add_heading(str(section.get("title") or section.get("heading") or "Seção"), level=2)
        content = section.get("content") or section.get("body") or section.get("text") or section
        if isinstance(content, list):
            for item in content:
                document.add_paragraph(str(item), style="List Bullet")
        elif isinstance(content, dict):
            for key, value in content.items():
                _add_key_value(document, str(key), value)
        else:
            document.add_paragraph(str(content or ""))

    document.add_heading("Aceite", level=1)
    document.add_paragraph("De acordo com os termos apresentados nesta proposta.")
    document.add_paragraph("\nContratante: ______________________________")
    document.add_paragraph("Proponente: ______________________________")

    document.save(path)
    return path
