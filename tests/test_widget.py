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
