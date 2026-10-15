import re

from src.masks import get_mask_account, get_mask_card_nubmer


def mask_account_card(account_card: str) -> str:
    """Маскирует номер банковской карты или счета."""
    match = re.search(r"\d+$", account_card)

    if match is None:
        raise ValueError("Строка должна содержать номер карты или счета")

    name = account_card[: match.start()].strip()
    number = match.group()

    if name.lower().startswith("счет"):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_nubmer(number)

    return f"{name} {masked_number}"
from datetime import datetime


def get_date(date_string: str) -> str:
    """Преобразует дату из ISO-формата в формат ДД.ММ.ГГГГ."""
    date_object = datetime.fromisoformat(date_string)
    return date_object.strftime("%d.%m.%Y")
