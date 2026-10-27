from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

pdfmetrics.registerFont(
    TTFont(
        "DejaVuSans",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    )
)

def generate_pdf_report(
    notebook_name: str,
    energy_kwh: float,
    carbon_g: float,
    optimized_energy_kwh: float,
    optimized_carbon_g: float,
    suggestions: list[str],
) -> bytes:
    """Generuje raport PDF z szacunkowych wyników analizy."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    for style_name in ("Title", "Normal", "Heading2", "Italic"):
        styles[style_name].fontName = "DejaVuSans"

    elements = []

    elements.append(
        Paragraph("Green Data Science Dashboard", styles["Title"])
    )
    elements.append(Spacer(1, 16))

    elements.append(
        Paragraph(f"Notebook: {notebook_name}", styles["Normal"])
    )
    elements.append(Spacer(1, 16))

    data = [
        ["Parametr", "Scenariusz bazowy", "Zoptymalizowany"],
        [
            "Energia (kWh)",
            f"{energy_kwh:.4f}",
            f"{optimized_energy_kwh:.4f}",
        ],
        [
            "Emisja (g CO2e)",
            f"{carbon_g:.2f}",
            f"{optimized_carbon_g:.2f}",
        ],
    ]

    table = Table(data, colWidths=[140, 165, 165])

    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgreen),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(table)
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph("Sugestie optymalizacji", styles["Heading2"])
    )

    if suggestions:
        for suggestion in suggestions:
            elements.append(
                Paragraph(f"- {suggestion}", styles["Normal"])
            )
            elements.append(Spacer(1, 6))
    else:
        elements.append(
            Paragraph(
                "Nie wykryto problemow w podstawowej analizie statycznej.",
                styles["Normal"],
            )
        )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Uwaga: wyniki sa symulacja oparta na przyjetych "
            "parametrach. Nie stanowia rzeczywistego pomiaru "
            "zuzycia energii ani emisji.",
            styles["Italic"],
        )
    )

    document.build(elements)

    return buffer.getvalue()
