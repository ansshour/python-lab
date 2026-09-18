# Домашние рецепты

[![Site CI](https://github.com/ansshour/python-lab/actions/workflows/pages.yml/badge.svg)](https://github.com/ansshour/python-lab/actions/workflows/pages.yml)

Небольшая книга рецептов на MkDocs Material: поиск, карточки блюд и расчёт порций.

- [Сайт](https://ansshour.github.io/python-lab/)
- [Отчёт](report/REPORT.md)
- [Запуски CI](https://github.com/ansshour/python-lab/actions)

## Локальный запуск

Нужен Python **3.14.7**. Установка изолирована от системного Python.

```sh
uv tool run --from virtualenv==21.7.14 virtualenv --python python3.14 .venv
source .venv/bin/activate
python -m pip install --require-hashes -r requirements.txt
python -m mkdocs serve --dev-addr 127.0.0.1:8017
```

Альтернатива: `uv sync --frozen`. Версии зафиксированы в `uv.lock` и
экспорте `requirements.txt` с хешами. После изменения зависимостей обновите экспорт:

```sh
uv export --frozen --format requirements-txt --no-emit-project --output-file requirements.txt
```

## Проверки

```sh
python scripts/check_spelling.py
python -m mkdocs build --strict
python scripts/check_site.py
python scripts/smoke_url.py https://ansshour.github.io/python-lab/
```

Проверка орфографии использует локальный русский словарь; она не проверяет
стиль и грамматику. `SITE_URL` задаёт полный адрес сайта с подкаталогом.
Одинаковое значение нужно передавать сборке и `check_site.py`.
Формулы используют встроенный MathML; внешние шрифты отключены.

GitHub Pages публикуется официальными Actions. Для GitVerse подготовлен
`.gitverse/workflows/site.yml`; запуск на GitVerse и доставка на Helios
ожидают данных аккаунтов. Порядок подключения описан в отчёте.

## Лицензии

Код — [MIT](LICENSE). Контент — [CC BY 4.0](LICENSE-CONTENT.md).
