# Bank Widget

Учебный проект виджета банковских операций клиента. Маскирует реквизиты,
преобразует даты, фильтрует операции по статусу и сортирует их по дате.

## Установка

Требуются Python 3.15 и Poetry. Откройте папку проекта в PyCharm,
выберите интерпретатор Poetry и установите зависимости:

```bash
poetry install --with dev,lint
```

## Структура

- `src/masks.py` — маскировка карт и счетов.
- `src/widget.py` — маскировка строки с реквизитами и форматирование даты.
- `src/processing.py` — фильтрация и сортировка операций.
- `tests/` — проверки функций.

## Обработка операций

`filter_by_state(operations, state="EXECUTED")` возвращает новый список
операций с указанным статусом, сохраняя их исходный порядок.
Записи без `state` пропускаются; регистр статуса учитывается.

`sort_by_date(operations, is_reverse=True)` возвращает новый список,
отсортированный по ключу `date`: по умолчанию новые операции идут первыми.
Передайте `is_reverse=False` для сортировки от старых к новым.
Даты должны быть строками ISO 8601 в едином формате, например
`2019-07-03T18:35:29.512364`, как в условиях задания. Ключ `date` обязателен.
При одинаковых датах сохраняется исходный порядок записей.
Обе функции не меняют исходный список и словари; пустой ввод даёт пустой список.

```python
from src.processing import filter_by_state, sort_by_date

operations = [
    {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 2, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 3, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
]

executed = filter_by_state(operations)
print([item["id"] for item in executed])  # [1, 3]
print([item["id"] for item in filter_by_state(operations, "CANCELED")])  # [2]
print([item["id"] for item in sort_by_date(operations)])  # [1, 2, 3]
print([item["id"] for item in sort_by_date(operations, False)])  # [3, 2, 1]
```

## Маскировка и даты

```python
from src.widget import get_date, mask_account_card

print(mask_account_card("Visa Platinum 7000792289606361"))
# Visa Platinum 7000 79** **** 6361
print(mask_account_card("Счет 73654108430135874305"))  # Счет **4305
print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
```

## Проверки

В PyCharm можно запустить папку `tests` через Run → pytest.
Для запуска из командной строки в корне проекта:

```bash
poetry run pytest -q
poetry run flake8 src tests
poetry run mypy src tests
poetry run isort --check-only src tests
```

Тесты проверяют статусы EXECUTED/CANCELED, отсутствие совпадений,
оба направления сортировки, равные даты, пустые списки и неизменность ввода.

## Разработка по GitFlow

- `main` — основная ветка.
- `develop` — ветка разработки.
- `feature/homework_10_1` — домашняя работа по продвинутому Git.

Изменения оформляются отдельными коммитами. Для проверки домашней работы
создаётся pull request из `feature/homework_10_1` в `develop`.
Файлы IDE, виртуальные окружения и кеши исключены через `.gitignore`.
