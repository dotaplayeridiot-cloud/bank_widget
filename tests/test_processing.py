"""Проверки фильтрации, сортировки и сохранности исходных данных."""

from copy import deepcopy
from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, indexes", [("EXECUTED", [0, 1]), ("CANCELED", [2, 3]), ("PENDING", []), ("executed", []), ("", [])]
)
def test_filter_states(operations: list[dict[str, Any]], state: str, indexes: list[int]) -> None:
    """Фильтровать по разным статусам с учетом регистра."""
    assert filter_by_state(operations, state) == [operations[index] for index in indexes]


def test_filter_default(operations: list[dict[str, Any]]) -> None:
    """По умолчанию возвращать выполненные операции в исходном порядке."""
    assert filter_by_state(operations) == [operations[0], operations[1]]


def test_filter_missing_state(incomplete_operations: list[dict[str, Any]]) -> None:
    """Пропустить записи без нужного статуса."""
    assert filter_by_state(incomplete_operations) == []


@pytest.mark.parametrize("is_reverse, indexes", [(True, [0, 3, 2, 1]), (False, [1, 2, 3, 0])])
def test_sort_direction(operations: list[dict[str, Any]], is_reverse: bool, indexes: list[int]) -> None:
    """Сортировать даты в обоих направлениях."""
    assert sort_by_date(operations, is_reverse) == [operations[index] for index in indexes]


def test_sort_default(operations: list[dict[str, Any]]) -> None:
    """По умолчанию выводить новые операции первыми."""
    assert sort_by_date(operations) == [operations[0], operations[3], operations[2], operations[1]]


@pytest.mark.parametrize("is_reverse", [True, False])
def test_sort_same_date(equal_date_operations: list[dict[str, Any]], is_reverse: bool) -> None:
    """При одинаковых датах сохранять исходный порядок в обе стороны."""
    assert sort_by_date(equal_date_operations, is_reverse) == equal_date_operations


@pytest.mark.parametrize("is_reverse", [True, False])
def test_no_mutation(operations: list[dict[str, Any]], is_reverse: bool) -> None:
    """Вернуть новые списки, не изменяя исходные записи."""
    original = deepcopy(operations)
    filtered = filter_by_state(operations)
    ordered = sort_by_date(operations, is_reverse)
    assert filtered is not operations
    assert ordered is not operations
    assert operations == original


@pytest.mark.parametrize("is_reverse", [True, False])
def test_empty_lists(is_reverse: bool) -> None:
    """Пустой ввод обрабатывается без ошибок и возвращает новый список."""
    data: list[dict[str, Any]] = []
    assert filter_by_state(data) == []
    assert sort_by_date(data, is_reverse) == []
    assert filter_by_state(data) is not data
    assert sort_by_date(data, is_reverse) is not data


def test_missing_date(incomplete_operations: list[dict[str, Any]]) -> None:
    """Отсутствие обязательного ключа date вызывает KeyError."""
    with pytest.raises(KeyError, match="date"):
        sort_by_date(incomplete_operations)


@pytest.mark.parametrize("dates", [["2024-02-01", "2024-01-01"], ["bad-date", ""], ["31.01.2024", "01.02.2024"]])
def test_string_date_contract(dates: list[str]) -> None:
    """Сортировка строк не валидирует даты: ISO-формат обеспечивает хронологический порядок."""
    data: list[dict[str, Any]] = [{"date": date} for date in dates]
    assert sort_by_date(data, False) == [{"date": dates[1]}, {"date": dates[0]}]


def test_incomparable_dates() -> None:
    """Несовместимые типы ключа date вызывают TypeError."""
    with pytest.raises(TypeError):
        sort_by_date([{"date": "2024-01-01"}, {"date": None}])
