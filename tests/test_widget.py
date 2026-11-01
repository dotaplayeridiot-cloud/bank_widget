import pytest

from src.widget import get_date, mask_account_card


def test_mask_visa_card() -> None:
    """Проверить маску карты Visa."""
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"


def test_mask_maestro_card() -> None:
    """Проверить маску карты Maestro."""
    assert mask_account_card("Maestro 7000792289606361") == "Maestro 7000 79** **** 6361"


def test_mask_account() -> None:
    """Проверить маску банковского счета."""
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"


def test_invalid_input() -> None:
    """Строка без номера должна вызывать ошибку."""
    with pytest.raises(ValueError):
        mask_account_card("Visa Platinum")


def test_get_date() -> None:
    """Проверить преобразование даты с микросекундами."""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


def test_get_date_without_microseconds() -> None:
    """Проверить преобразование даты без микросекунд."""
    assert get_date("2024-12-01T10:05:00") == "01.12.2024"
