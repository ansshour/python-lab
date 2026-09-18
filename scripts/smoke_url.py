"""Verify an actual HTTP deployment, including a page in a subdirectory."""
from urllib.request import urlopen
from urllib.parse import urljoin
import json
import sys

base = sys.argv[1].rstrip("/") + "/"
for suffix, marker in [("", "Домашние рецепты"), ("recipes.html", "Сырники"), ("portions.html", "<math")]:
    with urlopen(urljoin(base, suffix), timeout=30) as response:
        body = response.read().decode()
        if response.status != 200 or marker not in body:
            raise SystemExit(f"FAILED: {suffix}, HTTP {response.status}, marker={marker in body}")
        print(f"HTTP {response.status}: {suffix or 'index.html'}; контрольная строка найдена")
with urlopen(urljoin(base, "search/search_index.json"), timeout=30) as response:
    data = json.load(response)
    assert data["docs"], "Пустой поисковый индекс"
    print(f"HTTP {response.status}: поиск содержит {len(data['docs'])} записей")
