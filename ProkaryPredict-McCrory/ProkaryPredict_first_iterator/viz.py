# viz.py
import plotly.graph_objects as go

def blocks_to_genome_figure(blocks, genome_length=None):
    """
    Creates a linear genome visualization:
      - X-axis = genomic coordinates
      - Each block = a gene/feature
      - Color = functional category
      - Hover shows gene name, length, category
    """
    if genome_length is None:
        genome_length = max(b["end"] for b in blocks) if blocks else 1

    fig = go.Figure()

    # We'll stack multiple rows if blocks overlap
    rows = []
    for b in sorted(blocks, key=lambda x: x["start"]):
        # find the first row this block fits in
        placed = False
        for i, row in enumerate(rows):
            if all(b["start"] > r["end"] or b["end"] < r["start"] for r in row):
                row.append(b)
                b_row = i
                placed = True
                break
        if not placed:
            rows.append([b])
            b_row = len(rows) - 1

        # Plot the rectangle
        fig.add_trace(go.Bar(
            x=[b["end"] - b["start"]],
            y=[1],  # height is normalized; will use row spacing
            base=[b["start"]],
            orientation='h',
            marker=dict(color=b["color"], line=dict(color="black", width=1)),
            hoverinfo='text',
            text=f"{b['label']}<br>len: {b['length']}<br>cat: {b['category']}",
            name=b['label'],
            showlegend=False
        ))

    # Adjust layout
    fig.update_layout(
        title="Linear Genome Map",
        xaxis_title="Genomic coordinate",
        yaxis=dict(
            visible=False,
            tickvals=[]
        ),
        barmode='stack',
        height=50 + 25 * len(rows),  # enough vertical space for stacked rows
        margin=dict(l=20, r=20, t=30, b=20)
    )
    fig.update_xaxes(range=[0, genome_length * 1.02])
    return fig
