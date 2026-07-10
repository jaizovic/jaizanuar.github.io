"""Build downloadable PDFs from the published article HTML files."""
from pathlib import Path
from html.parser import HTMLParser
from xml.sax.saxutils import escape
import re

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT / "articles"
OUTPUT = ROOT / "papers" / "pdf"


def clean(text):
    return re.sub(r"\s+", " ", text).strip()


class ArticleParser(HTMLParser):
    """Extract the visible text from the article reader without extra packages."""
    def __init__(self):
        super().__init__()
        self.in_reader = False
        self.current = None
        self.buffer = []
        self.items = []
        self.title = ""
        self.metadata = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "main" and "reader" in attrs.get("class", "").split():
            self.in_reader = True
        if self.in_reader and tag in {"h1", "h2", "p", "li", "div"}:
            self.current = (tag, attrs.get("class", ""))
            self.buffer = []

    def handle_data(self, data):
        if self.current:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        if self.current and tag == self.current[0]:
            text = clean("".join(self.buffer))
            if text:
                if tag == "h1":
                    self.title = text
                elif tag == "div" and "article-meta" in self.current[1].split():
                    self.metadata = text
                elif tag in {"h2", "p", "li"}:
                    self.items.append((tag, "lead" in self.current[1].split(), text))
            self.current = None
            self.buffer = []
        if tag == "main":
            self.in_reader = False


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(HexColor("#bfdbfe"))
    canvas.line(18 * mm, 14 * mm, A4[0] - 18 * mm, 14 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(HexColor("#475569"))
    canvas.drawString(18 * mm, 9 * mm, "Jaiz Anuar | jaizanuar.com")
    canvas.drawRightString(A4[0] - 18 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(source):
    parser = ArticleParser()
    parser.feed(source.read_text(encoding="utf-8"))
    title = parser.title
    metadata = parser.metadata
    filename = source.with_suffix(".pdf").name

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("ArticleTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=23, leading=28, textColor=HexColor("#0f172a"), spaceAfter=9)
    meta_style = ParagraphStyle("Metadata", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9, leading=13, textColor=HexColor("#2563eb"), spaceAfter=19)
    heading_style = ParagraphStyle("Heading", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=HexColor("#0f172a"), spaceBefore=13, spaceAfter=8)
    body_style = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.5, leading=16, textColor=HexColor("#334155"), alignment=TA_LEFT, spaceAfter=10)
    lead_style = ParagraphStyle("Lead", parent=body_style, fontName="Helvetica", fontSize=12, leading=18, textColor=HexColor("#1e293b"), spaceAfter=16)

    doc = BaseDocTemplate(str(OUTPUT / filename), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=19 * mm, bottomMargin=21 * mm)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="article")
    doc.addPageTemplates(PageTemplate(id="article", frames=[frame], onPage=footer))
    story = [Paragraph(escape(title), title_style), Paragraph(escape(metadata), meta_style)]
    for tag, is_lead, text in parser.items:
        if tag == "h2":
            story.append(Paragraph(escape(text), heading_style))
        else:
            style = lead_style if is_lead else body_style
            story.append(Paragraph(escape(text), style))
    story.append(Spacer(1, 4 * mm))
    doc.build(story)


OUTPUT.mkdir(parents=True, exist_ok=True)
for article in ARTICLES.glob("*.html"):
    if article.name != "index.html":
        build_pdf(article)
