"""Параметризованные проверки виджета и преобразования даты."""

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
        ("Visa Classic 0000000000000000", "Visa Classic 0000 00** **** 0000"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("счет 1234", "счет **1234"),
        ("СЧЕТ 000012345", "СЧЕТ **2345"),
        ("  Visa Platinum   7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ],
)
def test_mask_account_card(value: str, expected: str) -> None:
    """Выбрать маску карты или счета и сохранить название."""
    assert mask_account_card(value) == expected


@pytest.mark.parametrize("value", ["", "Visa Platinum", "Счет", "Visa 1234x", "   "])
def test_missing_number(value: str) -> None:
    """Строка без конечного номера вызывает понятную ошибку."""
    with pytest.raises(ValueError, match="Строка должна содержать"):
        mask_account_card(value)


@pytest.mark.parametrize("value", ["Visa 123", "Maestro 12345678901234567", "Счет 123"])
def test_invalid_number_length(value: str) -> None:
    """Проверка длины номера выполняется и через интерфейс виджета."""
    with pytest.raises(ValueError):
        mask_account_card(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-12-01T10:05:00", "01.12.2024"),
        ("2024-02-29", "29.02.2024"),
        ("2024-01-01T00:00:00", "01.01.2024"),
        ("2024-12-31T23:59:59+03:00", "31.12.2024"),
        ("2024-03-11T02:26:18Z", "11.03.2024"),
        ("2024-03-11 02:26:18", "11.03.2024"),
    ],
)
def test_get_date(value: str, expected: str) -> None:
    """Преобразовать допустимые ISO-даты, включая високосный день."""
    assert get_date(value) == expected


@pytest.mark.parametrize("value", ["", "not-a-date", "11.03.2024", "2023-02-29", "2024-13-01", "2024-01-32"])
def test_invalid_date(value: str) -> None:
    """Отклонить пустые, невозможные даты и неподдерживаемый формат."""
    with pytest.raises(ValueError):
        get_date(value)
