import pytest

from src.widget import mask_account_card


def test_mask_visa_card() -> None:
    assert mask_account_card("Visa Platinum 7000792289606361") == ("Visa Platinum 7000 79** **** 6361")


def test_mask_maestro_card() -> None:
    assert mask_account_card("Maestro 7000792289606361") == ("Maestro 7000 79** **** 6361")


def test_mask_account() -> None:
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"


def test_invalid_input() -> None:
    with pytest.raises(ValueError):
        mask_account_card("Visa Platinum")


from src.widget import get_date


def test_get_date() -> None:
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


def test_get_date_without_microseconds() -> None:
    assert get_date("2024-12-01T10:05:00") == "01.12.2024"

