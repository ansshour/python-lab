"""Create a self-contained HTML text report with local evidence images."""
from pathlib import Path
from markdown import markdown

root = Path(__file__).resolve().parent.parent
report = root / "report"
content = markdown((report / "REPORT.md").read_text(), extensions=["tables", "fenced_code", "toc"])
style = '''
:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#f4f1e9;color:#253126;font:16px/1.65 system-ui,sans-serif}
main{max-width:1100px;margin:40px auto;padding:64px;background:#fffefa;border-radius:16px}
h1,h2,h3{font-family:Georgia,serif;line-height:1.25;color:#3d5137}h1{font-size:42px}h2{margin-top:54px;padding-top:22px;border-top:1px solid #dedccd}h3{margin-top:32px}
a{color:#456d40}table{border-collapse:collapse;width:100%;font-size:14px;margin:24px 0;display:block;overflow-x:auto}th,td{padding:12px;border:1px solid #dddccf;vertical-align:top;min-width:110px}th{background:#e9eee1;text-align:left}tr:nth-child(even){background:#fafaf5}
pre{background:#f0f2eb;padding:20px;border-radius:8px;overflow:auto;font:12px/1.55 ui-monospace,monospace}code{overflow-wrap:anywhere}img{display:block;max-width:100%;max-height:650px;object-fit:contain;object-position:left top;margin:24px 0;border:1px solid #dedccd}
@media(max-width:700px){main{margin:0;padding:24px;border-radius:0}h1{font-size:30px}}
@media print{body{background:white}main{margin:0;padding:0;max-width:none}h2,h3{break-after:avoid}pre{white-space:pre-wrap}table{font-size:10px}img{max-height:160mm}a{color:inherit}tr{break-inside:avoid}}
'''
(report / "REPORT.html").write_text(f'<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Отчёт — Домашние рецепты</title><style>{style}</style><main>{content}</main></html>')
print(report / "REPORT.html")
