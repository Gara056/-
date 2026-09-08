#!/usr/bin/env python3
from pathlib import Path
import markdown

src = Path(__file__).with_name("TZ-racion-studio.md")
body = markdown.markdown(
    src.read_text(encoding="utf-8"),
    extensions=["tables", "fenced_code", "sane_lists", "toc"],
)

html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<title>ТЗ Racion Studio — автоматизация меню и КБЖУ</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>
@page {{ size: A4; margin: 16mm 14mm; }}
:root {{
  --paper: #f6f1e8;
  --ink: #1f1b16;
  --muted: #6b645b;
  --sage: #5e7a68;
  --sage-dark: #3f5648;
  --sand: #d9c7b0;
  --line: #e7dccb;
  --card: #fffcf7;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0 auto;
  max-width: 820px;
  padding: 32px 28px 64px;
  background: var(--paper);
  color: var(--ink);
  font-family: Manrope, "Segoe UI", sans-serif;
  font-size: 10.5pt;
  line-height: 1.5;
}}
h1, h2, h3, h4 {{
  font-family: Fraunces, Georgia, serif;
  font-weight: 500;
  color: var(--sage-dark);
  line-height: 1.25;
}}
h1 {{
  font-size: 26pt;
  color: var(--ink);
  border-bottom: none;
  margin: 0 0 8px;
}}
h2 {{
  font-size: 16pt;
  margin-top: 32px;
  padding-top: 12px;
  border-top: 1px solid var(--sand);
}}
h3 {{ font-size: 12.5pt; margin-top: 20px; }}
p {{ margin: 8px 0; }}
a {{ color: var(--sage-dark); }}
hr {{ border: none; border-top: 1px solid var(--sand); margin: 24px 0; }}
table {{
  border-collapse: collapse;
  width: 100%;
  margin: 12px 0;
  font-size: 9pt;
  background: var(--card);
}}
th, td {{
  border: 1px solid var(--line);
  padding: 6px 8px;
  text-align: left;
  vertical-align: top;
}}
th {{
  background: #efe8dc;
  font-weight: 600;
  color: var(--sage-dark);
}}
tr:nth-child(even) td {{ background: #faf6ef; }}
code, pre {{
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 8.5pt;
  background: #efe8dc;
  border-radius: 4px;
}}
pre {{ padding: 12px; overflow-x: auto; white-space: pre-wrap; }}
blockquote {{
  margin: 12px 0;
  padding: 8px 14px;
  border-left: 3px solid var(--sage);
  background: rgba(94, 122, 104, 0.08);
  color: var(--ink);
  font-style: normal;
}}
ul, ol {{ margin: 8px 0; padding-left: 22px; }}
li {{ margin: 3px 0; }}
.banner {{
  font-size: 8.5pt;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--sage);
  margin-bottom: 10px;
}}
@media print {{
  body {{ max-width: none; padding: 0; background: white; }}
}}
</style>
</head>
<body>
<p class="banner">Техническое задание · v0.9.1 · 8 сентября 2026</p>
{body}
</body>
</html>
"""

out = Path(__file__).with_name("TZ-racion-studio.html")
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
