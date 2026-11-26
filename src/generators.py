"""Ленивая обработка транзакций и генерация номеров банковских карт."""

from collections.abc import Iterator
from typing import Any


def filter_by_currency(transactions: list[dict[str, Any]], currency: str) -> Iterator[dict[str, Any]]:
    """Выдать транзакции с указанным кодом валюты, сохраняя порядок.

    Код сравнивается с учетом регистра. Ожидается вложенная структура
    operationAmount/currency/code из задания. Исходные данные не меняются.
    """
    return (
        transaction
        for transaction in transactions
        if transaction["operationAmount"]["currency"]["code"] == currency
    )


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Iterator[str]:
    """Последовательно выдавать описания транзакций, включая повторения.

    Каждая транзакция должна содержать строковое поле description.
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Выдать номера от start до stop включительно в формате XXXX XXXX XXXX XXXX.

    Границы должны быть от 1 до 9999999999999999, иначе при переборе
    возникает ValueError. При start > stop последовательность пустая.
    Номера дополняются нулями слева; весь диапазон в памяти не хранится.
    """
    if not 1 <= start <= 9999999999999999 or not 1 <= stop <= 9999999999999999:
        raise ValueError("Границы должны быть от 1 до 9999999999999999")
    for number in range(start, stop + 1):
        digits = f"{number:016d}"
        yield " ".join(digits[index:index + 4] for index in range(0, 16, 4))
