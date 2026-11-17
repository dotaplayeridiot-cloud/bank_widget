"""Проверки маскирования реквизитов и некорректного ввода."""

import pytest

from src.masks import get_mask_account, get_mask_card_nubmer


@pytest.mark.parametrize(
    "number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("9999999999999999", "9999 99** **** 9999"),
    ],
)
def test_card_mask(number: str, expected: str) -> None:
    """Сохранить первые шесть и последние четыре цифры карты."""
    assert get_mask_card_nubmer(number) == expected


@pytest.mark.parametrize(
    "number", ["", "123", "1" * 15, "1" * 17, "123456789012345x", "1234 5678 9012 3456", "-123456789012345"]
)
def test_invalid_card(number: str) -> None:
    """Отклонить пустые, нецифровые и неверные по длине номера."""
    with pytest.raises(ValueError, match="16 цифр"):
        get_mask_card_nubmer(number)


@pytest.mark.parametrize(
    "number, expected",
    [("73654108430135874305", "**4305"), ("1234", "**1234"), ("0000", "**0000"), ("12345", "**2345")],
)
def test_account_mask(number: str, expected: str) -> None:
    """Маскировать счет, включая минимальную допустимую длину."""
    assert get_mask_account(number) == expected


@pytest.mark.parametrize("number", ["", "1", "123", "12ab", "123 456", "-1234"])
def test_invalid_account(number: str) -> None:
    """Отклонить номера короче четырех цифр и нецифровой ввод."""
    with pytest.raises(ValueError, match="минимум 4 цифры"):
        get_mask_account(number)
