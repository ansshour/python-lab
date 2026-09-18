"""Check generated links, assets, anchors, search index, and offline math."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import os
import sys

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = set()
        self.links = []
        self.external_assets = []
        self.math = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "math":
            self.math = True
        asset = tag in {"script", "img", "iframe", "source"} or (
            tag == "link" and attrs.get("rel") == "stylesheet")
        for key in ("href", "src"):
            if key not in attrs:
                continue
            url = attrs[key]
            if asset and (urlsplit(url).scheme in {"https", "http"} or url.startswith("//")):
                self.external_assets.append(url)
            if not urlsplit(url).scheme and not url.startswith("//"):
                self.links.append(url)

root = Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve()
pages = {path.resolve(): Page(path.read_text()) for path in root.rglob("*.html")}
errors = []
base_path = urlsplit(os.environ.get("SITE_URL", "http://127.0.0.1:8000/")).path.rstrip("/") + "/"
for path, page in pages.items():
    for url in page.links:
        parts = urlsplit(url)
        target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
        if parts.path.startswith("/"):
            if not parts.path.startswith(base_path):
                errors.append(f"{path.name}: ссылка вне базового пути {base_path}: {url}")
                continue
            target = root / unquote(parts.path[len(base_path):])
        if target.is_dir():
            target /= "index.html"
        if not target.is_file():
            errors.append(f"{path.name}: отсутствует файл {url}")
        elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
            errors.append(f"{path.name}: отсутствует якорь {url}")
    errors.extend(f"{path.name}: внешний ресурс: {url}" for url in page.external_assets)
index = json.loads((root / "search/search_index.json").read_text())
if not any("сырники" in entry.get("text", "").lower() or "сырники" in entry.get("title", "").lower() for entry in index["docs"]):
    errors.append("В поисковом индексе отсутствуют сырники")
if not pages[root / "portions.html"].math:
    errors.append("Отсутствует формула MathML")
if "Домашние рецепты" not in (root / "index.html").read_text():
    errors.append("Отсутствует контрольная строка")
print("\n".join(errors) if errors else f"Проверено HTML-страниц: {len(pages)}; ссылки, поиск и формула исправны")
sys.exit(bool(errors))
