"""Проверки примеров задания и граничных случаев обработки операций."""

from copy import deepcopy
from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def operations() -> list[dict[str, Any]]:
    """Вернуть независимый набор операций из условий домашней работы."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_default(operations: list[dict[str, Any]]) -> None:
    """По умолчанию остаются выполненные операции в исходном порядке."""
    assert filter_by_state(operations) == [operations[0], operations[1]]


def test_filter_canceled(operations: list[dict[str, Any]]) -> None:
    """Переданный статус заменяет значение по умолчанию."""
    assert filter_by_state(operations, "CANCELED") == [operations[2], operations[3]]


def test_filter_unknown_status(operations: list[dict[str, Any]]) -> None:
    """Если совпадений нет, возвращается пустой список."""
    assert filter_by_state(operations, "PENDING") == []


def test_filter_missing_state() -> None:
    """Записи без статуса не попадают в результат."""
    assert filter_by_state([{"id": 1}, {"state": "executed"}]) == []


def test_sort_default(operations: list[dict[str, Any]]) -> None:
    """Результат совпадает с примером сортировки по убыванию."""
    assert sort_by_date(operations) == [
        operations[0], operations[3], operations[2], operations[1]
    ]


def test_sort_ascending(operations: list[dict[str, Any]]) -> None:
    """Параметр False располагает старые операции первыми."""
    assert sort_by_date(operations, False) == [
        operations[1], operations[2], operations[3], operations[0]
    ]


@pytest.mark.parametrize("reverse", [True, False])
def test_sort_same_date(reverse: bool) -> None:
    """При равных датах порядок сохраняется в обоих направлениях."""
    data = [
        {"id": 2, "date": "2024-01-01T12:00:00"},
        {"id": 1, "date": "2024-01-01T12:00:00"},
    ]
    assert sort_by_date(data, reverse) == data


def test_new_lists_without_mutation(operations: list[dict[str, Any]]) -> None:
    """Обе функции создают новый список и не меняют переданные данные."""
    original = deepcopy(operations)
    filtered = filter_by_state(operations)
    sorted_operations = sort_by_date(operations)
    assert filtered is not operations
    assert sorted_operations is not operations
    assert operations == original


def test_empty_lists() -> None:
    """Пустой ввод возвращает новые пустые списки."""
    data: list[dict[str, Any]] = []
    assert filter_by_state(data) == []
    assert sort_by_date(data) == []
    assert filter_by_state(data) is not data
    assert sort_by_date(data) is not data


def test_sort_missing_date() -> None:
    """Отсутствие обязательного ключа date сообщает о неверном вводе."""
    with pytest.raises(KeyError, match="date"):
        sort_by_date([{"id": 1}])
