from __future__ import annotations

from pathlib import Path
from typing import Any

from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.brand_assets import get_logo_path


PAGE_WIDTH, PAGE_HEIGHT = A4
NAVY = colors.HexColor("#172033")
GOLD = colors.HexColor("#B58A45")
INK = colors.HexColor("#20242A")
MUTED = colors.HexColor("#667085")
PAPER = colors.HexColor("#F7F4EF")
LINE = colors.HexColor("#D9D2C5")
SOFT_BLUE = colors.HexColor("#EEF2F7")


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _paragraph(text: Any, style: ParagraphStyle) -> Paragraph:
    return Paragraph(_clean(text).replace("\n", "<br/>"), style)


def _content_to_rows(content: Any) -> list[list[Any]]:
    if isinstance(content, list):
        return [[f"{index}.", _clean(item)] for index, item in enumerate(content, start=1)]
    if isinstance(content, dict):
        return [[_clean(key), _clean(value)] for key, value in content.items()]
    return [["", _clean(content)]]


def _draw_background(canvas, doc) -> None:
    canvas.saveState()
    page = doc.page
    logo_path = get_logo_path()

    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

    if page == 1:
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_HEIGHT - 8.6 * cm, PAGE_WIDTH, 8.6 * cm, fill=1, stroke=0)
        canvas.setFillColor(GOLD)
        canvas.rect(0, PAGE_HEIGHT - 8.75 * cm, PAGE_WIDTH, 0.15 * cm, fill=1, stroke=0)
        canvas.drawImage(
            ImageReader(str(logo_path)),
            PAGE_WIDTH - 7.1 * cm,
            PAGE_HEIGHT - 2.7 * cm,
            width=5.5 * cm,
            height=1.9 * cm,
            preserveAspectRatio=True,
            mask="auto",
        )
    else:
        canvas.setFillColor(PAPER)
        canvas.rect(0, PAGE_HEIGHT - 1.35 * cm, PAGE_WIDTH, 1.35 * cm, fill=1, stroke=0)
        canvas.setFillColor(NAVY)
        canvas.rect(0, PAGE_HEIGHT - 1.35 * cm, PAGE_WIDTH, 0.12 * cm, fill=1, stroke=0)
        canvas.drawImage(
            ImageReader(str(logo_path)),
            1.6 * cm,
            PAGE_HEIGHT - 1.1 * cm,
            width=3.2 * cm,
            height=0.85 * cm,
            preserveAspectRatio=True,
            mask="auto",
        )
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(PAGE_WIDTH - 1.6 * cm, PAGE_HEIGHT - 0.72 * cm, f"Página {page}")

    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_WIDTH, 1.35 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.8 * cm, 1.0 * cm, "Documento gerado automaticamente pela API Renderizadora de Propostas")
    canvas.setFillColor(GOLD)
    canvas.rect(0, 1.35 * cm, PAGE_WIDTH, 0.05 * cm, fill=1, stroke=0)
    canvas.restoreState()


def _build_styles() -> dict[str, ParagraphStyle]:
    styles = getSampleStyleSheet()
    return {
        "cover_kicker": ParagraphStyle(
            "CoverKicker",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=GOLD,
            alignment=TA_LEFT,
            uppercase=True,
            spaceAfter=10,
        ),
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            textColor=colors.white,
            alignment=TA_LEFT,
            spaceAfter=14,
        ),
        "cover_subtitle": ParagraphStyle(
            "CoverSubtitle",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=12,
            leading=18,
            textColor=colors.HexColor("#E6EAF0"),
            alignment=TA_LEFT,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=23,
            textColor=NAVY,
            spaceBefore=8,
            spaceAfter=9,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=NAVY,
            spaceBefore=7,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=INK,
            spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=MUTED,
        ),
        "label": ParagraphStyle(
            "Label",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=11,
            textColor=MUTED,
        ),
        "value": ParagraphStyle(
            "Value",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=14,
            textColor=INK,
        ),
        "callout": ParagraphStyle(
            "Callout",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=17,
            textColor=NAVY,
            alignment=TA_CENTER,
        ),
    }


def _info_card(styles: dict[str, ParagraphStyle], rows: list[tuple[str, Any]]) -> Table:
    table_rows = [
        [_paragraph(label.upper(), styles["label"]), _paragraph(value, styles["value"])]
        for label, value in rows
        if _clean(value)
    ]
    table = Table(table_rows, colWidths=[4.2 * cm, 10.2 * cm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return table


def _section_table(styles: dict[str, ParagraphStyle], content: Any) -> Table:
    rows = _content_to_rows(content)
    table_rows = [[_paragraph(left, styles["label"]), _paragraph(right, styles["body"])] for left, right in rows]
    table = Table(table_rows, colWidths=[2.7 * cm, 11.7 * cm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("BACKGROUND", (0, 0), (0, -1), SOFT_BLUE),
            ]
        )
    )
    return table


def generate_pdf(data: dict[str, Any], output_dir: Path) -> Path:
    path = output_dir / "proposta.pdf"
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.6 * cm,
    )
    styles = _build_styles()

    provider = data.get("provider", {})
    client = data.get("client", {})
    proposal = data.get("proposal", {})
    investment = proposal.get("investment", {})
    term = proposal.get("term", {})

    story: list[Any] = [
        Spacer(1, 0.7 * cm),
        _paragraph("PROPOSTA JURÍDICA", styles["cover_kicker"]),
        _paragraph(proposal.get("title", "Proposta Jurídica"), styles["cover_title"]),
        _paragraph(proposal.get("subtitle", ""), styles["cover_subtitle"]),
        Spacer(1, 3.1 * cm),
        _info_card(
            styles,
            [
                ("Cliente", client.get("name")),
                ("Proponente", provider.get("name")),
                ("Responsável", provider.get("responsible")),
                ("Contato", provider.get("email")),
            ],
        ),
        Spacer(1, 0.9 * cm),
        Table(
            [
                [
                    _paragraph(f"<b>{investment.get('amountText', '')}</b>", styles["callout"]),
                    _paragraph(f"<b>{term.get('duration', '')}</b>", styles["callout"]),
                ]
            ],
            colWidths=[7.1 * cm, 7.1 * cm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), PAPER),
                    ("BOX", (0, 0), (-1, -1), 0.8, GOLD),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, GOLD),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                    ("TOPPADDING", (0, 0), (-1, -1), 14),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            ),
        ),
        PageBreak(),
        _paragraph("Visão Geral", styles["h1"]),
        HRFlowable(width="100%", color=GOLD, thickness=1, spaceAfter=10),
    ]

    objective = proposal.get("objective")
    if objective:
        story.extend([_paragraph(objective, styles["body"]), Spacer(1, 0.25 * cm)])

    for index, section in enumerate(data.get("layoutPlan", []), start=1):
        title = section.get("title") or section.get("heading") or f"Seção {index}"
        content = section.get("content") or section.get("body") or section.get("text") or section
        story.append(_paragraph(f"{index}. {title}", styles["h2"]))
        story.append(_section_table(styles, content))
        story.append(Spacer(1, 0.35 * cm))

    story.extend(
        [
            PageBreak(),
            _paragraph("Investimento, Prazo e Aceite", styles["h1"]),
            HRFlowable(width="100%", color=GOLD, thickness=1, spaceAfter=10),
            _paragraph("Investimento", styles["h2"]),
            _paragraph(investment.get("amountText", ""), styles["body"]),
            _paragraph("Prazo", styles["h2"]),
            _paragraph(term.get("duration", ""), styles["body"]),
            Spacer(1, 0.5 * cm),
            _paragraph("Aceite", styles["h2"]),
            _paragraph("De acordo com os termos apresentados nesta proposta.", styles["body"]),
            Spacer(1, 1.1 * cm),
            Table(
                [["", "", ""], ["Contratante", "", "Proponente"]],
                colWidths=[6.2 * cm, 1.6 * cm, 6.2 * cm],
                style=TableStyle(
                    [
                        ("LINEABOVE", (0, 1), (0, 1), 1.2, NAVY),
                        ("LINEABOVE", (2, 1), (2, 1), 1.2, NAVY),
                        ("ALIGN", (0, 1), (-1, -1), "CENTER"),
                        ("TEXTCOLOR", (0, 1), (-1, -1), MUTED),
                        ("TOPPADDING", (0, 1), (-1, -1), 8),
                    ]
                ),
            ),
        ]
    )
    doc.build(story, onFirstPage=_draw_background, onLaterPages=_draw_background)
    return path
