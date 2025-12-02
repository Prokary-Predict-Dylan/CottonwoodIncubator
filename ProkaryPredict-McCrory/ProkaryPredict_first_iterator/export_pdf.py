# export_pdf.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io

def hex_to_rgb_fraction(hexcolor):
    hexcolor = hexcolor.lstrip('#')
    r = int(hexcolor[0:2], 16) / 255.0
    g = int(hexcolor[2:4], 16) / 255.0
    b = int(hexcolor[4:6], 16) / 255.0
    return (r, g, b)

def export_blocks_pdf(blocks, metadata=None):
    """
    Returns a byte string containing the PDF.
    This version generates the PDF fully in memory (no writing to disk).
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # ---- Title ----
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, height - 1 * inch, "ProkaryPredict — Block Report")

    # ---- Metadata ----
    c.setFont("Helvetica", 10)
    y = height - 1.3 * inch
    if metadata:
        for k, v in metadata.items():
            c.drawString(1 * inch, y, f"{k}: {v}")
            y -= 12
    y -= 20

    # ---- Draw blocks ----
    if blocks:
        total_len = max(b["end"] for b in blocks)
    else:
        total_len = 1

    x_margin = 1 * inch
    y_box = y - 40
    scale = (width - 2 * x_margin) / total_len

    for b in blocks:
        w = max(6, (b["end"] - b["start"]) * scale)
        r, g, b_ = hex_to_rgb_fraction(b["color"])

        # Block rectangle
        c.setFillColorRGB(r, g, b_)
        c.rect(x_margin + (b["start"] * scale), y_box, w, 20, fill=1, stroke=0)

        # Block label
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 8)
        c.drawString(x_margin + (b["start"] * scale), y_box - 12, b["label"])

    # Finish PDF
    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.getvalue()
