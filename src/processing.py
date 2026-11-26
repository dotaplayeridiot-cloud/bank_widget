"""Фильтрация и сортировка банковских операций."""

from typing import Any


def filter_by_state(
    operations: list[dict[str, Any]], state: str = "EXECUTED"
) -> list[dict[str, Any]]:
    """Вернуть новый список операций с указанным статусом.

    Порядок операций сохраняется. Записи без ключа state пропускаются.
    Исходный список и словари не изменяются.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(
    operations: list[dict[str, Any]], is_reverse: bool = True
) -> list[dict[str, Any]]:
    """Вернуть новый список операций, отсортированный по дате.

    Даты — строки ISO 8601 в едином формате, как в примерах задания.
    По умолчанию новые операции идут первыми; is_reverse=False меняет порядок.
    При одинаковых датах сохраняется исходный порядок. Ключ date обязателен.
    Исходный список и словари не изменяются.
    """
    return sorted(operations, key=lambda operation: operation["date"], reverse=is_reverse)
