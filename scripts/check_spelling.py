"""Check Russian prose in the site's Markdown using an offline dictionary."""
from pathlib import Path
import re
import sys
from pymorphy3 import MorphAnalyzer

checker = MorphAnalyzer()
allowed = set(Path("scripts/spelling-allow.txt").read_text().split())
errors = []
for path in sorted(Path("docs").rglob("*.md")):
    text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
    for number, line in enumerate(text.splitlines(), 1):
        words = re.findall(r"[а-яёА-ЯЁ]+", line.lower())
        for word in sorted(set(words) - allowed):
            if checker.word_is_known(word):
                continue
            errors.append(f"{path}:{number}: неизвестное слово: {word}")
print("\n".join(errors) if errors else "Орфография: ошибок не найдено")
sys.exit(bool(errors))
