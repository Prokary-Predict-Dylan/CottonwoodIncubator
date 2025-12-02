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
    Blocks are stacked vertically to avoid overlapping labels.
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
    block_height = 20
    spacing = 10  # vertical space between stacked blocks
    scale = (width - 2 * x_margin) / total_len

    # Stack blocks vertically in rows to avoid overlap
    current_row = 0
    row_positions = {}

    for b in blocks:
        start = b["start"]
        end = b["end"]

        # check for overlapping blocks in x-axis
        row = 0
        while True:
            occupied = False
            for (s, e, r) in row_positions.get(row, []):
                if not (end < s or start > e):
                    occupied = True
                    break
            if not occupied:
                break
            row += 1

        if row not in row_positions:
            row_positions[row] = []
        row_positions[row].append((start, end, row))

        y_box = y - (row * (block_height + spacing))

        # Draw rectangle
        w = max(6, (end - start) * scale)
        r, g, b_ = hex_to_rgb_fraction(b["color"])
        c.setFillColorRGB(r, g, b_)
        c.rect(x_margin + (start * scale), y_box, w, block_height, fill=1, stroke=0)

        # Draw label above rectangle
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 8)
        c.drawString(x_margin + (start * scale), y_box + block_height + 2, b["label"])

    # Finish PDF
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()

