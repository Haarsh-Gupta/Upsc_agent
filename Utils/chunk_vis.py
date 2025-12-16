from IPython.display import HTML, display
import random

def visualize_chunks(chunks):
    """
    Black background, colored text per chunk.
    """
    html_blocks = []
    for i, chunk in enumerate(chunks):

        # pick bright text color
        r = random.randint(120, 255)
        g = random.randint(120, 255)
        b = random.randint(120, 255)
        color = f"rgb({r},{g},{b})"

        block = f"""
        <div style="
            background: #36454F;
            padding: 12px;
            margin: 12px 0;
            border-radius: 8px;
            white-space: pre-wrap;
            line-height: 1.4;
            font-family: monospace;
        ">
            <span style="color:{color};font-weight:bold;">Chunk {i+1}</span><br><br>
            <span style="color:{color};">
            {chunk.replace("<","&lt;").replace(">","&gt;")}
            </span>
        </div>
        """
        html_blocks.append(block)

    display(HTML("<div>" + "".join(html_blocks) + "</div>"))
