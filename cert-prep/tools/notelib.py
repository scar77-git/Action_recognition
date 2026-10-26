"""Shared builder for the daily study-note PDFs."""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-B", FONT_DIR + "DejaVuSans-Bold.ttf"))
# Oblique faces aren't installed everywhere; fall back to upright ones.
for _name, _file, _fallback in (("DV-I", "DejaVuSans-Oblique.ttf", "DejaVuSans.ttf"),
                                ("DV-BI", "DejaVuSans-BoldOblique.ttf", "DejaVuSans-Bold.ttf")):
    _path = FONT_DIR + _file
    pdfmetrics.registerFont(TTFont(_name, _path if os.path.exists(_path) else FONT_DIR + _fallback))
pdfmetrics.registerFont(TTFont("DVM", FONT_DIR + "DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-BI")

INK = colors.HexColor("#1F2933")
ACCENT = colors.HexColor("#C2410C")      # AWS-ish orange
AZURE = colors.HexColor("#1D4ED8")
MUTED = colors.HexColor("#52606D")
RULE = colors.HexColor("#CBD2D9")
HEAD_BG = colors.HexColor("#FFF1E6")
ZEBRA = colors.HexColor("#F7F9FB")
WARN_BG = colors.HexColor("#FEF3C7")
OK_BG = colors.HexColor("#E7F6EC")

_base = getSampleStyleSheet()
S = {
    "title": ParagraphStyle("title", fontName="DV-B", fontSize=20, leading=25, textColor=INK, spaceAfter=4),
    "sub": ParagraphStyle("sub", fontName="DV", fontSize=10, leading=14, textColor=MUTED, spaceAfter=10),
    "h1": ParagraphStyle("h1", fontName="DV-B", fontSize=14, leading=18, textColor=ACCENT, spaceBefore=12, spaceAfter=6, keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="DV-B", fontSize=11.5, leading=15, textColor=INK, spaceBefore=8, spaceAfter=4, keepWithNext=1),
    "body": ParagraphStyle("body", fontName="DV", fontSize=9.5, leading=13.5, textColor=INK, spaceAfter=5, alignment=TA_LEFT),
    "bullet": ParagraphStyle("bullet", fontName="DV", fontSize=9.5, leading=13.5, textColor=INK, leftIndent=12, bulletIndent=2, spaceAfter=2.5),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=8.4, leading=11, textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="DV-B", fontSize=8.4, leading=11, textColor=INK),
    "code": ParagraphStyle("code", fontName="DVM", fontSize=8.4, leading=11.5, textColor=INK, backColor=ZEBRA,
                           borderPadding=6, leftIndent=4, spaceBefore=4, spaceAfter=8),
    "box": ParagraphStyle("box", fontName="DV", fontSize=9.2, leading=13, textColor=INK),
}


class Note:
    def __init__(self, path, title, subtitle, wide=False):
        self.path = path
        self.pagesize = landscape(A4) if wide else A4
        self.width = self.pagesize[0] - 30 * mm  # usable width between the 15 mm margins
        self.title = title
        self.story = [Paragraph(title, S["title"]), Paragraph(subtitle, S["sub"])]

    def h1(self, t): self.story.append(Paragraph(t, S["h1"]))
    def h2(self, t): self.story.append(Paragraph(t, S["h2"]))
    def p(self, t): self.story.append(Paragraph(t, S["body"]))
    def code(self, t): self.story.append(Preformatted(t, S["code"]))
    def space(self, h=6): self.story.append(Spacer(1, h))
    def page_break(self): self.story.append(PageBreak())

    def bullets(self, items):
        for it in items:
            self.story.append(Paragraph(it, S["bullet"], bulletText="•"))
        self.space(3)

    def numbered(self, items):
        for i, it in enumerate(items, 1):
            self.story.append(Paragraph(it, S["bullet"], bulletText=f"{i}."))
        self.space(3)

    def table(self, header, rows, widths):
        data = [[Paragraph(h, S["cellb"]) for h in header]]
        data += [[Paragraph(c, S["cell"]) for c in r] for r in rows]
        total = self.width
        t = Table(data, colWidths=[w * total for w in widths], repeatRows=1)
        style = [
            ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
            ("LINEBELOW", (0, 0), (-1, 0), 0.8, ACCENT),
            ("LINEBELOW", (0, 1), (-1, -1), 0.3, RULE),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]
        for i in range(2, len(data), 2):
            style.append(("BACKGROUND", (0, i), (-1, i), ZEBRA))
        t.setStyle(TableStyle(style))
        self.story.append(t)
        self.space(8)

    def callout(self, label, text, kind="warn"):
        bg = {"warn": WARN_BG, "ok": OK_BG}.get(kind, ZEBRA)
        t = Table([[Paragraph(f"<b>{label}</b><br/>{text}", S["box"])]], colWidths=[self.width])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg),
            ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        self.story.append(KeepTogether([t, Spacer(1, 8)]))

    def build(self):
        title = self.title

        def footer(canvas, doc):
            canvas.saveState()
            canvas.setFont("DV", 7.5)
            canvas.setFillColor(MUTED)
            canvas.drawString(15 * mm, 10 * mm, title)
            canvas.drawRightString(self.pagesize[0] - 15 * mm, 10 * mm, f"Page {doc.page}")
            canvas.restoreState()

        doc = SimpleDocTemplate(self.path, pagesize=self.pagesize, leftMargin=15 * mm, rightMargin=15 * mm,
                                topMargin=15 * mm, bottomMargin=18 * mm, title=title,
                                author="AWS GenAI Pro / AI-103 prep")
        doc.build(self.story, onFirstPage=footer, onLaterPages=footer)
