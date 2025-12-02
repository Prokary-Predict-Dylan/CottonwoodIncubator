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
    Fully safe, readable PDF export with:
        • stacked rows
        • automatic page breaks
        • non-overlapping labels
        • in-memory return
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    def new_page():
        c.showPage()
        # Title on every new page
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, height - 1*inch, "ProkaryPredict — Block Report")
        c.setFont("Helvetica", 10)
        return height - 1.3*inch

    # First page header
    y = new_page()

    # Metadata section
    if metadata:
        for k, v in metadata.items():
            c.drawString(1*inch, y, f"{k}: {v}")
            y -= 12
    y -= 20

    # Nothing to draw
    if not blocks:
        c.drawString(1*inch, y, "No blocks available.")
        c.save()
        buffer.seek(0)
        return buffer.getvalue()

    # Compute horizontal scaling
    total_len = max(b["end"] for b in blocks)
    x_margin = 1 * inch
    block_height = 18
    row_spacing = 10
    scale = (width - 2 * x_margin) / total_len

    # Function to break pages when needed
    def ensure_space(rows_needed=1):
        nonlocal y
        if y - rows_needed*(block_height + row_spacing + 15) < 1*inch:
            y = new_page()

    # Row placement registry to avoid overlaps
    row_positions = {}   # row → list of (start, end)
    row_heights = []      # for tracking drawing positions

    for block in blocks:
        start = block["start"]
        end = block["end"]

        # Determine row by collision-checking
        row = 0
        while True:
            if row not in row_positions:
                row_positions[row] = []
                break
            collision = False
            for (s, e) in row_positions[row]:
                if not (end < s or start > e):
                    collision = True
                    break
            if not collision:
                break
            row += 1

        row_positions[row].append((start, end))

    # Sort rows for consistent top-to-bottom output
    sorted_rows = sorted(row_positions.keys())

    # Draw rows
    for row in sorted_rows:
        blocks_in_row = [b for b in blocks if any(
            b["start"] == s and b["end"] == e
            for (s, e) in row_positions[row]
        )]

        # Space check
        ensure_space(1)

        row_y = y - (block_height + row_spacing)

        # Draw each block in this row
        for b in blocks_in_row:
            start = b["start"]
            end = b["end"]
            w = max(6, (end - start) * scale)

            color_r, color_g, color_b = hex_to_rgb_fraction(b["color"])
            c.setFillColorRGB(color_r, color_g, color_b)
            c.rect(x_margin + (start * scale), row_y, w, block_height, fill=1, stroke=0)

            # Label appears above rectangle
            c.setFillColorRGB(0, 0, 0)
            label = b["label"]

            # Truncate labels that exceed block width
            max_chars = int(w / 5)
            if len(label) > max_chars and max_chars > 3:
                label = label[:max_chars - 3] + "..."

            c.setFont("Helvetica", 8)
            c.drawString(x_margin + (start * scale), row_y + block_height + 2, label)

        # Move down for next row
        y = row_y - 15

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
