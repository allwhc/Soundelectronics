import json
import os
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, PageBreak, KeepTogether, ListFlowable, ListItem, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

NAVY = HexColor("#0b3559")
NAVY_DARK = HexColor("#072540")
GOLD = HexColor("#e8a020")
MUTED = HexColor("#5b6773")
TEXT = HexColor("#1c2733")

SRC_ROOT = r"C:\Users\Lab_Engineer\Downloads\Catalog\Catalog"
BROCHURE_ROOT = r"C:\Users\Lab_Engineer\Downloads\Catalog\brochure"
OUT_PDF = os.path.join(BROCHURE_ROOT, "sound-electronics-catalog.pdf")

with open(os.path.join(BROCHURE_ROOT, "manifest.json"), encoding="utf-8") as f:
    manifest = json.load(f)

SECTIONS = [
    ("1.Backlight", "Backlight"),
    ("2.Converters", "Converters"),
    ("3.TCONS", "T-CONs"),
    ("4.Microscope", "Microscope"),
    ("5.Programmers and Tester and Multimeter", "Programmers, Testers & Multimeters"),
    ("6.FFC", "FFC Cables"),
    ("7.Inverter and Power Supply", "Inverter & Power Supply"),
    ("8.Amplifier board", "Amplifier Boards"),
    ("9.Bluetooth Panel", "Bluetooth Panels"),
    ("10.Panel", "Panels"),
    ("10.Speakers for TV 0.5", "Speakers for TV"),
    ("11.Stand 0.5", "TV Stands"),
    ("11.Tools", "Tools"),
]

PANEL_NOTE = "Variety of panels from 32\u2033 to 65\u2033 available. Packing for transport is done with utmost care in foam and wooden box."

OTHER_PRODUCTS = [
    "All kinds of HDMI Cable from 1.5M to 50M",
    "All types of Wall Mount",
    "Universal combo motherboard for TV",
    "All kinds of adapter and Metal SMPS from 5V1A to 24V20A",
    "FBT for CRT TV, CRT base, Solder wire and Yoke",
    "CRT TV KIT",
    "Other power chords and RC cables",
    "Converters like HDMI to VGA, VGA to HDMI, HDMI to AV, AV to HDMI",
]

# ---- image cache: convert webp -> compressed JPEG in-memory, sized for print ----
_img_cache = {}

def load_print_image(rel_path, max_px=500, quality=62):
    if rel_path in _img_cache:
        return _img_cache[rel_path]
    abs_path = os.path.join(BROCHURE_ROOT, rel_path.replace("/", os.sep))
    im = Image.open(abs_path).convert("RGB")
    w, h = im.size
    if max(w, h) > max_px:
        scale = max_px / max(w, h)
        im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    buf = BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    buf.seek(0)
    _img_cache[rel_path] = (buf, im.size)
    return buf, im.size

def rl_image(rel_path, max_w, max_h, max_px=500, quality=62):
    buf, (w, h) = load_print_image(rel_path, max_px=max_px, quality=quality)
    ratio = min(max_w / w, max_h / h)
    disp_w, disp_h = w * ratio, h * ratio
    buf.seek(0)
    return RLImage(buf, width=disp_w, height=disp_h)

# ---- styles ----
styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleBig", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=26, textColor=HexColor("#ffffff"), alignment=TA_CENTER, spaceAfter=6)
tagline_style = ParagraphStyle("Tagline", parent=styles["Normal"], fontName="Helvetica",
                                fontSize=10, textColor=HexColor("#cfe0ee"), alignment=TA_CENTER, leading=14)
contact_style = ParagraphStyle("Contact", parent=styles["Normal"], fontName="Helvetica",
                                fontSize=9.5, textColor=HexColor("#e6eef5"), alignment=TA_CENTER, leading=14)
section_head_style = ParagraphStyle("SectionHead", parent=styles["Heading1"], fontName="Helvetica-Bold",
                                     fontSize=16, textColor=NAVY, spaceAfter=10, spaceBefore=0)
feature_text_style = ParagraphStyle("FeatureText", parent=styles["Normal"], fontName="Helvetica-Bold",
                                     fontSize=12, textColor=NAVY_DARK, leading=17)
other_item_style = ParagraphStyle("OtherItem", parent=styles["Normal"], fontName="Helvetica",
                                   fontSize=10.5, textColor=TEXT, leading=15)
contact_card_name = ParagraphStyle("ContactName", parent=styles["Heading2"], fontName="Helvetica-Bold",
                                    fontSize=14, textColor=NAVY, alignment=TA_CENTER, spaceAfter=4)
contact_card_line = ParagraphStyle("ContactLine", parent=styles["Normal"], fontName="Helvetica",
                                    fontSize=10, textColor=TEXT, alignment=TA_LEFT, leading=14)
footer_style = ParagraphStyle("Footer", parent=styles["Normal"], fontName="Helvetica",
                               fontSize=8.5, textColor=HexColor("#8fa5b8"), alignment=TA_CENTER)

PAGE_W, PAGE_H = A4
MARGIN = 16 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

story = []

# ---- Cover page ----
def cover_table_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 130 * mm, PAGE_W, 130 * mm, fill=1, stroke=0)
    canvas.restoreState()

logo_buf, (lw, lh) = load_print_image("assets/images/logo.webp", max_px=300, quality=90)
logo_ratio = min(28 * mm / lw, 28 * mm / lh)
logo_img = RLImage(logo_buf, width=lw * logo_ratio, height=lh * logo_ratio)

story.append(Spacer(1, 14 * mm))
story.append(logo_img)
story.append(Spacer(1, 6 * mm))
story.append(Paragraph("SOUND ELECTRONICS", title_style))
story.append(Paragraph(
    "Wholesale Dealer in Panel, LED/LCD Spare Parts, IC, Transistor, CRT Spares,<br/>"
    "Wires &amp; Cables, LNB, Receiver, LCD/LED Stand &amp; Other Spares", tagline_style))
story.append(Spacer(1, 6 * mm))
story.append(Paragraph(
    "Mayank &mdash; +91 97736 79006 &nbsp;|&nbsp; rdjainsound@gmail.com<br/>"
    "6A, Soonawala Building, 44-B, Proctor Road, near Hotel Grant, Grant Road (E), Mumbai 400 007",
    contact_style))
story.append(Spacer(1, 20 * mm))
story.append(PageBreak())

# ---- Product sections ----
CARD_COLS = 3
CARD_GAP = 4 * mm
CARD_W = (CONTENT_W - (CARD_COLS - 1) * CARD_GAP) / CARD_COLS
CARD_H = CARD_W

for idx, (key, title) in enumerate(SECTIONS, start=1):
    images = manifest.get(key, {}).get("images", [])
    section_flow = []
    section_flow.append(Paragraph(f"{idx:02d}&nbsp;&nbsp;{title}", section_head_style))
    section_flow.append(HRFlowable(width="100%", thickness=0.75, color=HexColor("#e3e7eb"), spaceAfter=8))

    if key == "10.Panel" and images:
        img = images[0]
        pic = rl_image(img["file"], max_w=CONTENT_W * 0.55, max_h=90 * mm, max_px=700, quality=70)
        text_p = Paragraph(PANEL_NOTE, feature_text_style)
        t = Table([[pic, text_p]], colWidths=[CONTENT_W * 0.55, CONTENT_W * 0.45])
        t.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (1, 0), (1, 0), 12),
        ]))
        section_flow.append(t)
    else:
        rows = []
        row = []
        for i, img in enumerate(images):
            pic = rl_image(img["file"], max_w=CARD_W - 6, max_h=CARD_H - 6, max_px=450, quality=60)
            cell = Table([[pic]], colWidths=[CARD_W], rowHeights=[CARD_H])
            cell.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOX", (0, 0), (-1, -1), 0.5, HexColor("#e3e7eb")),
            ]))
            row.append(cell)
            if len(row) == CARD_COLS:
                rows.append(row)
                row = []
        if row:
            while len(row) < CARD_COLS:
                row.append("")
            rows.append(row)
        if rows:
            grid = Table(rows, colWidths=[CARD_W] * CARD_COLS,
                         rowHeights=[CARD_H] * len(rows),
                         spaceBefore=0, spaceAfter=0)
            grid.setStyle(TableStyle([
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), CARD_GAP),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), CARD_GAP),
            ]))
            section_flow.append(grid)

    story.append(KeepTogether(section_flow[:2]))
    story.extend(section_flow[2:])
    story.append(Spacer(1, 4 * mm))
    if idx != len(SECTIONS):
        story.append(PageBreak())

# ---- Other products page ----
story.append(PageBreak())
story.append(Paragraph(f"{len(SECTIONS)+1:02d}&nbsp;&nbsp;Other Products We Deal In", section_head_style))
story.append(HRFlowable(width="100%", thickness=0.75, color=HexColor("#e3e7eb"), spaceAfter=10))
items = [ListItem(Paragraph(p, other_item_style), spaceAfter=8) for p in OTHER_PRODUCTS]
story.append(ListFlowable(items, bulletType="1", start=1, leftIndent=14))

# ---- Contact page ----
story.append(PageBreak())
story.append(Spacer(1, 10 * mm))
contact_logo_buf, (clw, clh) = load_print_image("assets/images/logo.webp", max_px=250, quality=90)
cl_ratio = min(20 * mm / clw, 20 * mm / clh)
story.append(RLImage(contact_logo_buf, width=clw * cl_ratio, height=clh * cl_ratio))
story.append(Spacer(1, 4 * mm))
story.append(Paragraph("SOUND ELECTRONICS", contact_card_name))
story.append(Paragraph(
    "Wholesale Dealer in Panel, LED/LCD Spare Parts, IC, Transistor, CRT Spares, "
    "Wires &amp; Cables, LNB, Receiver, LCD/LED Stand &amp; Other Spares",
    ParagraphStyle("tag2", parent=tagline_style, textColor=MUTED, spaceAfter=10)))
story.append(Spacer(1, 6 * mm))
story.append(Paragraph("Mayank &mdash; +91 97736 79006", contact_card_line))
story.append(Spacer(1, 3 * mm))
story.append(Paragraph("rdjainsound@gmail.com", contact_card_line))
story.append(Spacer(1, 3 * mm))
story.append(Paragraph("6A, Soonawala Building, 44-B, Proctor Road, near Hotel Grant, Grant Road (E), Mumbai 400 007", contact_card_line))
story.append(Spacer(1, 14 * mm))
story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#e3e7eb")))
story.append(Spacer(1, 6 * mm))
story.append(Paragraph("&copy; 2026 Sound Electronics. All rights reserved.", footer_style))

def on_page(canvas, doc):
    if doc.page == 1:
        cover_table_bg(canvas, doc)
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(HexColor("#9aa7b2"))
    canvas.drawRightString(PAGE_W - MARGIN, 10 * mm, f"Page {doc.page}")
    canvas.drawString(MARGIN, 10 * mm, "Sound Electronics Catalog")
    canvas.restoreState()

doc = SimpleDocTemplate(
    OUT_PDF, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN, topMargin=MARGIN, bottomMargin=MARGIN,
    title="Sound Electronics - Product Catalog", author="Sound Electronics"
)
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)

size_mb = os.path.getsize(OUT_PDF) / 1e6
print(f"PDF written: {OUT_PDF} ({size_mb:.2f} MB)")
