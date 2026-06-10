from __future__ import annotations

from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor


NAVY = RGBColor(23, 32, 51)
GOLD = RGBColor(181, 138, 69)
MUTED = RGBColor(102, 112, 133)


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _add_key_value(document: Document, label: str, value: Any) -> None:
    paragraph = document.add_paragraph()
    label_run = paragraph.add_run(f"{label}: ")
    label_run.bold = True
    label_run.font.color.rgb = NAVY
    paragraph.add_run(_clean(value))


def _set_document_styles(document: Document) -> None:
    normal = document.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10)

    for style_name in ["Heading 1", "Heading 2"]:
        style = document.styles[style_name]
        style.font.name = "Arial"
        style.font.color.rgb = NAVY
        style.font.bold = True


def _add_section_content(document: Document, content: Any) -> None:
    if isinstance(content, list):
        for item in content:
            document.add_paragraph(_clean(item), style="List Bullet")
    elif isinstance(content, dict):
        table = document.add_table(rows=0, cols=2)
        table.style = "Table Grid"
        for key, value in content.items():
            cells = table.add_row().cells
            cells[0].text = _clean(key)
            cells[1].text = _clean(value)
    else:
        document.add_paragraph(_clean(content))


def generate_editable_docx(data: dict[str, Any], output_dir: Path) -> Path:
    path = output_dir / "proposta_editavel.docx"
    document = Document()
    _set_document_styles(document)

    provider = data.get("provider", {})
    client = data.get("client", {})
    proposal = data.get("proposal", {})
    investment = proposal.get("investment", {})
    term = proposal.get("term", {})

    title = document.add_heading(proposal.get("title", "Proposta Jurídica"), level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if title.runs:
        title.runs[0].font.color.rgb = NAVY

    if proposal.get("subtitle"):
        subtitle = document.add_paragraph(proposal["subtitle"])
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in subtitle.runs:
            run.font.color.rgb = MUTED

    document.add_paragraph()
    document.add_heading("Dados da proposta", level=1)
    _add_key_value(document, "Contratante", client.get("name"))
    _add_key_value(document, "Proponente", provider.get("name"))
    _add_key_value(document, "Responsável", provider.get("responsible"))
    _add_key_value(document, "E-mail", provider.get("email"))

    if proposal.get("objective"):
        document.add_heading("Objetivo", level=1)
        document.add_paragraph(_clean(proposal.get("objective")))

    document.add_heading("Investimento", level=1)
    document.add_paragraph(_clean(investment.get("amountText", "")))

    document.add_heading("Prazo", level=1)
    document.add_paragraph(_clean(term.get("duration", "")))

    document.add_heading("Escopo", level=1)
    for section in data.get("layoutPlan", []):
        document.add_heading(_clean(section.get("title") or section.get("heading") or "Seção"), level=2)
        content = section.get("content") or section.get("body") or section.get("text") or section
        _add_section_content(document, content)

    document.add_heading("Aceite", level=1)
    document.add_paragraph("De acordo com os termos apresentados nesta proposta.")
    document.add_paragraph("\nContratante: ______________________________")
    document.add_paragraph("Proponente: ______________________________")

    document.save(path)
    return path
