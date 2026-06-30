#!/usr/bin/env python3
import os
import re
import subprocess
import markdown

def convert_md_to_pdf():
    md_file = "COMP5541_Group_Project_Report.md"
    html_file = "COMP5541_Group_Project_Report.html"
    pdf_file = "COMP5541_Group_Project_Report.pdf"

    if not os.path.exists(md_file):
        print(f"❌ Error: {md_file} not found!")
        return

    print("📖 Reading Markdown report...")
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split metadata/title block and the body by the first '---' line
    parts = content.split("\n---\n", 1)
    if len(parts) == 2:
        metadata_block, body_block = parts
    else:
        metadata_block = ""
        body_block = content

    print("Parsing report metadata...")
    course = "COMP5541 Machine Learning and Data Analytics"
    project_title = "Evaluating and Comparing Large Language Models (LLMs) on Complex Reasoning and Semantic Pragmatics"
    track = "Track A — Comparative Evaluation of LLMs"
    
    title_match = re.search(r"^#\s*(.*)", metadata_block, re.MULTILINE)
    if title_match:
        project_title = title_match.group(1).strip()
        
    course_match = re.search(r"\*\*Course\*\*:\s*(.*)", metadata_block)
    if course_match:
        course = course_match.group(1).strip()

    track_match = re.search(r"\*\*Track\*\*:\s*(.*)", metadata_block)
    if track_match:
        track = track_match.group(1).strip()

    # Extract team members
    team_members = []
    member_matches = re.findall(r"\d+\.\s+\*\*(.*?)\*\*\s*\((.*?)\)\s*—\s*(.*)", metadata_block)
    for name, sid, role in member_matches:
        team_members.append({
            "name": name.strip(),
            "sid": sid.replace("Student ID:", "").replace("`", "").strip(),
            "role": role.strip()
        })

    # Hardcoded fallback for the two specific group members if parsing failed
    if not team_members or len(team_members) < 2:
        team_members = [
            {"name": "Shen Jinsong", "sid": "25104146g", "role": "Lead: Reasoning Ability & Charting Scripts"},
            {"name": "Zeng Chuanming", "sid": "25108601g", "role": "Lead: Semantic Understanding & Scoring Pipeline"}
        ]

    abstract_text = ""
    abstract_match = re.search(r"\*\*Abstract\*\*\s*\n(.*)", metadata_block, re.DOTALL)
    if abstract_match:
        abstract_text = abstract_match.group(1).strip()
    else:
        abstract_match = re.search(r"\*\*Abstract\*\*:(.*)", metadata_block, re.DOTALL)
        if abstract_match:
            abstract_text = abstract_match.group(1).strip()

    print("Converting Markdown to HTML...")
    html_body = markdown.markdown(body_block, extensions=['extra', 'tables', 'toc'])

    # Post-process block equations: $$...$$ -> centered block equations
    def clean_block_math(match):
        eq = match.group(1).strip()
        eq = eq.replace(r"\cdot", " &middot; ")
        eq = eq.replace(r"\times", " &times; ")
        # Subscripts: e.g., S_i -> S<sub>i</sub>, w_c -> w<sub>c</sub>
        eq = re.sub(r"([a-zA-Z])_([a-zA-Z0-9])", r"\1<sub>\2</sub>", eq)
        return f'<div class="latex-equation">{eq}</div>'

    html_body = re.sub(r"\$\$(.*?)\$\$", clean_block_math, html_body, flags=re.DOTALL)

    # Post-process inline equations: $...$ -> italic math
    def clean_inline_math(match):
        eq = match.group(1).strip()
        eq = eq.replace(r"\cdot", "·")
        eq = eq.replace(r"\times", "×")
        eq = re.sub(r"([a-zA-Z])_([a-zA-Z0-9])", r"\1<sub>\2</sub>", eq)
        return f'<i>{eq}</i>'

    html_body = re.sub(r"\$(.*?)\$", clean_inline_math, html_body)

    # Post-process images to wrap them in LaTeX-style figure containers with automatic numbering
    fig_counter = 0
    def replace_image(match):
        nonlocal fig_counter
        fig_counter += 1
        alt = match.group(1)
        src = match.group(2)
        return f'<div class="latex-figure"><img src="{src}" /><div class="figure-caption">Figure {fig_counter}: {alt}</div></div>'

    html_body = re.sub(
        r'<p><img\s+alt="([^"]+)"\s+src="([^"]+)"\s*/?></p>',
        replace_image,
        html_body
    )

    # Post-process tables to format them as LaTeX booktabs tables
    table_counter = 0
    def replace_table(match):
        nonlocal table_counter
        table_counter += 1
        table_content = match.group(1)
        caption = "Taxonomy of LLM Evaluation Dimensions"
        if table_counter == 2:
            caption = "Quantitative Performance Summary and Evaluation Matrix"
        return f"""
        <div class="latex-table-container">
            <div class="table-caption">Table {table_counter}: {caption}</div>
            <table class="latex-table">
                {table_content}
            </table>
        </div>
        """

    html_body = re.sub(
        r'<table>(.*?)</table>',
        replace_table,
        html_body,
        flags=re.DOTALL
    )

    # LaTeX Preprint CSS stylesheet (Georgia/Times-serif, A4 layout, centered header, booktabs tables)
    css = """
    body {
        font-family: 'Times New Roman', Times, Georgia, serif;
        color: #000000;
        line-height: 1.6;
        font-size: 11pt;
        margin: 0;
        padding: 0;
    }
    @page {
        size: A4;
        margin: 2.8cm 2.5cm 2.8cm 2.5cm;
        @bottom-center {
            content: counter(page);
            font-family: 'Times New Roman', Times, Georgia, serif;
            font-size: 10pt;
            color: #000;
        }
    }
    .header-block {
        text-align: center;
        margin-top: 1cm;
        margin-bottom: 2cm;
    }
    .header-title {
        font-size: 18pt;
        font-weight: bold;
        margin-bottom: 1.2em;
        line-height: 1.3;
    }
    .header-authors {
        font-size: 11pt;
        margin-bottom: 0.3em;
        font-weight: normal;
    }
    .header-affiliation {
        font-size: 11pt;
        margin-bottom: 0.3em;
        font-style: normal;
    }
    .header-date {
        font-size: 11pt;
        margin-top: 0.5em;
    }
    .abstract-container {
        margin: 1.5cm 1.5cm 2cm 1.5cm;
        text-align: justify;
    }
    .abstract-title {
        text-align: center;
        font-weight: bold;
        font-size: 10pt;
        margin-bottom: 0.6em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .abstract-text {
        font-size: 10pt;
        line-height: 1.5;
    }
    h2, h3, h4, h5, h6 {
        font-family: 'Times New Roman', Times, Georgia, serif;
        color: #000000;
        font-weight: bold;
        margin-top: 1.8em;
        margin-bottom: 0.6em;
        page-break-after: avoid;
        break-after: avoid;
    }
    h2 {
        font-size: 14pt;
        border: none;
        padding: 0;
    }
    h2:first-of-type {
        page-break-before: always;
    }
    h3 {
        font-size: 12pt;
    }
    p {
        margin-top: 0;
        margin-bottom: 0;
        text-indent: 2em;
        text-align: justify;
    }
    /* LaTeX style: No text indent for the first paragraph of a section or after headings */
    h2 + p, h3 + p, h4 + p, div.content-body > p:first-of-type, .latex-equation + p, .latex-figure + p, .latex-table-container + p {
        text-indent: 0;
    }
    /* Add slight paragraph spacing inside list items or blockquotes */
    li p {
        text-indent: 0;
        margin: 0;
    }
    ul, ol {
        margin-top: 0.5em;
        margin-bottom: 0.8em;
        padding-left: 2em;
    }
    li {
        margin-bottom: 0.3em;
        text-align: justify;
    }
    
    /* LaTeX Booktabs Table Styling */
    .latex-table-container {
        margin: 2em 0;
        text-align: center;
        page-break-inside: avoid;
        break-inside: avoid;
    }
    .table-caption {
        font-size: 10pt;
        margin-bottom: 8px;
        text-align: center;
    }
    table.latex-table {
        width: 100%;
        border-collapse: collapse;
        margin: 0 auto;
        font-size: 9.5pt;
        border-top: 1.5px solid black;
        border-bottom: 1.5px solid black;
    }
    table.latex-table th {
        border-bottom: 1.0px solid black;
        padding: 8px 10px;
        font-weight: bold;
        text-align: left;
        background-color: transparent !important;
        color: black !important;
    }
    table.latex-table td {
        border: none;
        padding: 8px 10px;
        vertical-align: top;
        background-color: transparent !important;
        color: black !important;
    }
    
    /* LaTeX Figure Styling */
    .latex-figure {
        margin: 2.5em 0;
        text-align: center;
        page-break-inside: avoid;
        break-inside: avoid;
    }
    img, .latex-figure img {
        max-width: 80% !important;
        height: auto !important;
        display: block;
        margin: 1.5em auto;
        border: none;
        box-shadow: none;
    }
    .figure-caption {
        margin-top: 10px;
        font-size: 9.5pt;
        text-align: center;
        font-style: italic;
    }
    
    /* LaTeX Equation Styling */
    .latex-equation {
        text-align: center;
        margin: 1.5em 0;
        font-size: 11pt;
        font-style: italic;
    }
    blockquote {
        border: none;
        background-color: transparent;
        margin: 1.5em 2em;
        padding: 0;
        font-style: italic;
        text-align: justify;
    }
    blockquote p {
        text-indent: 0;
    }
    pre, code {
        font-family: 'Courier New', Courier, monospace;
        font-size: 9pt;
    }
    pre {
        background-color: #fafafa;
        border: 0.5px solid #ccc;
        padding: 10px;
        margin: 1.5em 0;
        page-break-inside: avoid;
        break-inside: avoid;
    }
    code {
        background-color: #fafafa;
        padding: 1px 3px;
        border: 0.5px solid #ddd;
        border-radius: 2px;
    }
    pre code {
        border: none;
        padding: 0;
        background-color: transparent;
    }
    """

    authors_str = " & ".join([f"{m['name']} ({m['sid']})" for m in team_members])

    header_html = f"""
    <div class="header-block">
        <div class="header-title">{project_title}</div>
        <div class="header-authors">{authors_str}</div>
        <div class="header-affiliation">The Hong Kong Polytechnic University</div>
        <div class="header-date">June 28, 2026</div>
    </div>
    """

    abstract_html = ""
    if abstract_text:
        abstract_html = f"""
        <div class="abstract-container">
            <div class="abstract-title">Abstract</div>
            <div class="abstract-text">{abstract_text}</div>
        </div>
        """

    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{project_title}</title>
    <style>
        {css}
    </style>
</head>
<body>
    {header_html}
    {abstract_html}
    <div class="content-body">
        {html_body}
    </div>
</body>
</html>
"""

    print(f"Saving temporary HTML file: {html_file}")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(full_html)

    print("Invoking Google Chrome headless printer to generate PDF...")
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    chrome_cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_file}",
        html_file
    ]

    try:
        subprocess.run(chrome_cmd, check=True)
        print(f"Success! Generated PDF report at:\n   {os.path.abspath(pdf_file)}")
    except Exception as e:
        print(f"Error during Chrome PDF generation: {e}")

if __name__ == "__main__":
    convert_md_to_pdf()
