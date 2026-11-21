"""Проверки генераторов: порядок, ленивость, формат и границы диапазона."""

from copy import deepcopy
from itertools import islice
from typing import Any

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions() -> list[dict[str, Any]]:
    """Смешанные валюты и повторяющиеся описания из примера задания."""
    rows = [
        (939719570, "USD", "Перевод организации"),
        (142264268, "USD", "Перевод со счета на счет"),
        (873106923, "RUB", "Перевод со счета на счет"),
        (895315941, "USD", "Перевод с карты на карту"),
        (594226727, "RUB", "Перевод организации"),
    ]
    return [
        {"id": identifier, "operationAmount": {"currency": {"code": currency}}, "description": description}
        for identifier, currency, description in rows
    ]


@pytest.mark.parametrize(
    "currency, expected_ids",
    [("USD", [939719570, 142264268, 895315941]), ("RUB", [873106923, 594226727]),
     ("EUR", []), ("usd", [])],
)
def test_filter_by_currency(transactions: list[dict[str, Any]], currency: str, expected_ids: list[int]) -> None:
    """Выбор валюты сохраняет порядок и не меняет исходные данные."""
    original = deepcopy(transactions)
    result = filter_by_currency(transactions, currency)
    assert iter(result) is result
    assert [item["id"] for item in result] == expected_ids
    assert list(result) == []
    assert transactions == original


def test_filter_empty() -> None:
    """Пустой ввод создает пустой итератор."""
    result = filter_by_currency([], "USD")
    with pytest.raises(StopIteration):
        next(result)


def test_filter_lazy(transactions: list[dict[str, Any]]) -> None:
    """Следующая запись не читается до запроса следующего результата."""
    result = filter_by_currency([transactions[0], {}], "USD")
    assert next(result) is transactions[0]
    with pytest.raises(KeyError):
        next(result)


def test_descriptions_example(transactions: list[dict[str, Any]]) -> None:
    """Описания из задания выдаются в исходном порядке с повторениями."""
    original = deepcopy(transactions)
    result = transaction_descriptions(transactions)
    assert iter(result) is result
    assert list(result) == [
        "Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет",
        "Перевод с карты на карту", "Перевод организации",
    ]
    assert transactions == original
    with pytest.raises(StopIteration):
        next(result)


@pytest.mark.parametrize("descriptions", [[], [""], ["A"], ["A", "A", "Б", ""]])
def test_descriptions_lengths(descriptions: list[str]) -> None:
    """Проверить пустой список, одиночное и несколько описаний."""
    assert list(transaction_descriptions([{"description": text} for text in descriptions])) == descriptions


def test_descriptions_lazy() -> None:
    """Генератор не обращается к следующему словарю заранее."""
    result = transaction_descriptions([{"description": "Первый"}, {}])
    assert next(result) == "Первый"
    with pytest.raises(KeyError):
        next(result)


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 5, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003",
                "0000 0000 0000 0004", "0000 0000 0000 0005"]),
        (9999, 10000, ["0000 0000 0000 9999", "0000 0000 0001 0000"]),
        (1234567890123456, 1234567890123456, ["1234 5678 9012 3456"]),
        (9999999999999998, 9999999999999999, ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
        (2, 1, []),
    ],
)
def test_card_numbers(start: int, stop: int, expected: list[str]) -> None:
    """Обе границы включены, нули и пробелы стоят на нужных местах."""
    result = card_number_generator(start=start, stop=stop)
    assert iter(result) is result
    assert list(result) == expected
    with pytest.raises(StopIteration):
        next(result)


@pytest.mark.parametrize("start, stop", [(0, 1), (-1, 5), (1, 0), (1, 10**16), (10**16, 10**16)])
def test_invalid_card_bounds(start: int, stop: int) -> None:
    """Не допускаются номера за пределами 16 цифр и нулевой номер."""
    with pytest.raises(ValueError, match="Границы"):
        list(card_number_generator(start, stop))


def test_full_card_range_is_lazy() -> None:
    """Даже полный диапазон позволяет сразу получить первые два номера."""
    assert list(islice(card_number_generator(1, 9999999999999999), 2)) == [
        "0000 0000 0000 0001", "0000 0000 0000 0002",
    ]
