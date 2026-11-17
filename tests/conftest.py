"""Общие независимые данные для тестов обработки операций."""

from typing import Any

import pytest


@pytest.fixture
def operations() -> list[dict[str, Any]]:
    """Создать новый набор операций для каждого теста."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def equal_date_operations() -> list[dict[str, Any]]:
    """Создать операции с одинаковой датой и разными идентификаторами."""
    return [
        {"id": 2, "date": "2024-01-01T12:00:00"},
        {"id": 1, "date": "2024-01-01T12:00:00"},
    ]


@pytest.fixture
def incomplete_operations() -> list[dict[str, Any]]:
    """Создать записи без статуса и со статусом в другом регистре."""
    return [{"id": 1}, {"id": 2, "state": "executed"}]
