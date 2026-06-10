from __future__ import annotations

from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def _paragraph(text: Any, style: ParagraphStyle) -> Paragraph:
    return Paragraph(str(text or ""), style)


def generate_pdf(data: dict[str, Any], output_dir: Path) -> Path:
    path = output_dir / "proposta.pdf"
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]
    body_style.leading = 15

    provider = data.get("provider", {})
    client = data.get("client", {})
    proposal = data.get("proposal", {})
    investment = proposal.get("investment", {})
    term = proposal.get("term", {})

    story = [
        _paragraph(proposal.get("title", "Proposta Jurídica"), title_style),
        Spacer(1, 0.4 * cm),
        _paragraph(proposal.get("subtitle", ""), body_style),
        Spacer(1, 1 * cm),
        Table(
            [
                ["Contratante", client.get("name", "")],
                ["Proponente", provider.get("name", "")],
                ["Responsável", provider.get("responsible", "")],
                ["E-mail", provider.get("email", "")],
            ],
            colWidths=[4 * cm, 11 * cm],
        ),
        Spacer(1, 0.8 * cm),
        _paragraph("Investimento", heading_style),
        _paragraph(investment.get("amountText", ""), body_style),
        Spacer(1, 0.4 * cm),
        _paragraph("Prazo", heading_style),
        _paragraph(term.get("duration", ""), body_style),
        PageBreak(),
    ]

    for section in data.get("layoutPlan", []):
        story.append(_paragraph(section.get("title") or section.get("heading") or "Seção", heading_style))
        content = section.get("content") or section.get("body") or section.get("text") or section
        if isinstance(content, list):
            for item in content:
                story.append(_paragraph(f"- {item}", body_style))
        elif isinstance(content, dict):
            for key, value in content.items():
                story.append(_paragraph(f"<b>{key}:</b> {value}", body_style))
        else:
            story.append(_paragraph(content, body_style))
        story.append(Spacer(1, 0.4 * cm))

    story.extend(
        [
            PageBreak(),
            _paragraph("Aceite", heading_style),
            _paragraph("De acordo com os termos apresentados nesta proposta.", body_style),
            Spacer(1, 1.2 * cm),
            Table(
                [["", ""], ["Contratante", "Proponente"]],
                colWidths=[7 * cm, 7 * cm],
                style=TableStyle(
                    [
                        ("LINEABOVE", (0, 1), (0, 1), 1, colors.black),
                        ("LINEABOVE", (1, 1), (1, 1), 1, colors.black),
                        ("ALIGN", (0, 1), (-1, -1), "CENTER"),
                    ]
                ),
            ),
        ]
    )
    doc.build(story)
    return path
