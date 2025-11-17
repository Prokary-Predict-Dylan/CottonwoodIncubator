# export_pdf.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def hex_to_rgb_fraction(hexcolor):
    hexcolor = hexcolor.lstrip('#')
    r = int(hexcolor[0:2], 16)/255.0
    g = int(hexcolor[2:4], 16)/255.0
    b = int(hexcolor[4:6], 16)/255.0
    return (r,g,b)

def export_blocks_pdf(filename, blocks, metadata=None):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 1*inch, "ProkaryPredict — Block Report")
    c.setFont("Helvetica", 10)
    y = height - 1.3*inch
    if metadata:
        for k,v in metadata.items():
            c.drawString(1*inch, y, f"{k}: {v}")
            y -= 12
    y -= 8
    # horizontal schematic
    x_margin = 1*inch
    x = x_margin
    y_box = y - 40
    total_len = max(b['end'] for b in blocks) if blocks else 1
    scale = (width - 2*x_margin) / total_len
    for b in blocks:
        w = max(6, (b['end'] - b['start'])*scale)
        r,g,b_ = hex_to_rgb_fraction(b['color'])
        c.setFillColorRGB(r,g,b_)
        c.rect(x + (b['start']*scale), y_box, w, 20, fill=1, stroke=0)
        c.setFillColorRGB(0,0,0)
        c.drawString(x + (b['start']*scale), y_box - 12, b['label'])
    c.save()