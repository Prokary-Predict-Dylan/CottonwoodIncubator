# export_pdf.py
import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def export_gene_reaction_pdf(model, metadata=None):
    """
    Export a gene → reaction mapping from a COBRApy model to a readable PDF.
    Each gene gets its own row; automatic page breaks prevent overlap.
    
    Returns:
        bytes of PDF file
    """
    # Prepare mapping
    mapping = []
    for rxn in model.reactions:
        for gene in rxn.genes:
            mapping.append({
                "Gene ID": gene.id,
                "Reaction ID": rxn.id,
                "Reaction Name": rxn.name,
                "Reaction Equation": rxn.reaction
            })

    df = pd.DataFrame(mapping)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- Helper for new page ---
    def new_page():
        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, height - 1*inch, "ProkaryPredict — Gene-Reaction Report")
        c.setFont("Helvetica", 10)
        return height - 1.3*inch  # starting y position

    y = new_page()

    # Metadata section
    if metadata:
        for k, v in metadata.items():
            c.drawString(1*inch, y, f"{k}: {v}")
            y -= 12
        y -= 10

    if df.empty:
        c.drawString(1*inch, y, "No genes or reactions found in the model.")
        c.save()
        buffer.seek(0)
        return buffer.getvalue()

    # Set column widths
    col_widths = [1.5*inch, 1.5*inch, 2.5*inch, 3*inch]
    row_height = 14
    spacing = 4  # space between rows

    # Draw header
    c.setFont("Helvetica-Bold", 10)
    x_positions = [1*inch]
    for i in range(1, len(col_widths)):
        x_positions.append(x_positions[-1] + col_widths[i-1])

    for i, col in enumerate(df.columns):
        c.drawString(x_positions[i], y, col)
    y -= row_height + spacing
    c.setFont("Helvetica", 9)

    # Draw rows
    for idx, row in df.iterrows():
        # Page break if needed
        if y < 1*inch:
            y = new_page()
            # redraw header
            c.setFont("Helvetica-Bold", 10)
            for i, col in enumerate(df.columns):
                c.drawString(x_positions[i], y, col)
            y -= row_height + spacing
            c.setFont("Helvetica", 9)

        for i, col in enumerate(df.columns):
            text = str(row[col])
            max_chars = int(col_widths[i] / 5)  # approx char width
            if len(text) > max_chars:
                text = text[:max_chars-3] + "..."
            c.drawString(x_positions[i], y, text)
        y -= row_height + spacing

    c.save()
    buffer.seek(0)
    return buffer.getvalue()
