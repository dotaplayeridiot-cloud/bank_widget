"""Проверки логирования в консоль и файл при успехе и ошибке."""

from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from src.decorators import log


@pytest.mark.parametrize("is_file", [False, True])
def test_success(is_file: bool, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Сохранить результат и аргументы, записать время и успешный исход."""
    log_path = tmp_path / "success.log"
    filename = str(log_path) if is_file else None

    @log(filename=filename)
    def add(left: int, *, right: int) -> int:
        """Сложить два числа."""
        return left + right

    before = datetime.now().astimezone()
    assert add(1, right=2) == 3
    after = datetime.now().astimezone()
    captured = capsys.readouterr()
    output = log_path.read_text(encoding="utf-8") if is_file else captured.out
    lines = output.splitlines()
    assert len(lines) == 4
    assert lines[0].startswith("add start: ")
    assert ". Inputs: (1,), {'right': 2}" in lines[0]
    assert lines[1:3] == ["add ok", "add result: 3"]
    assert lines[3].startswith("add end: ")
    started_at = datetime.fromisoformat(lines[0].split("start: ", 1)[1].split(". Inputs:")[0])
    finished_at = datetime.fromisoformat(lines[3].split("end: ", 1)[1])
    assert before <= started_at <= finished_at <= after
    assert captured.err == ""
    if is_file:
        assert captured.out == ""


@pytest.mark.parametrize("is_file", [False, True])
@pytest.mark.parametrize("error_type", [ValueError, TypeError, ZeroDivisionError])
def test_errors(
    is_file: bool, error_type: type[Exception], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Записать тип, текст и входные данные, затем передать то же исключение."""
    log_path = tmp_path / "errors.log"
    expected_error = error_type("Ошибка операции")

    @log(filename=str(log_path) if is_file else None)
    def fail(value: int, *, currency: str) -> None:
        """Имитировать ошибку обрабатываемой функции."""
        raise expected_error

    with pytest.raises(error_type) as caught:
        fail(7, currency="RUB")
    assert caught.value is expected_error
    captured = capsys.readouterr()
    output = log_path.read_text(encoding="utf-8") if is_file else captured.out
    lines = output.splitlines()
    assert len(lines) == 3
    assert lines[0].startswith("fail start: ")
    assert lines[1] == (
        f"fail error: {error_type.__name__}. Inputs: (7,), {{'currency': 'RUB'}}. Error: Ошибка операции"
    )
    assert lines[2].startswith("fail end: ")
    assert "fail ok" not in output
    assert "fail result:" not in output
    assert captured.err == ""
    if is_file:
        assert captured.out == ""


def test_file_append_and_unicode(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """Не затирать существующие записи, корректно сохранять кириллицу."""
    log_path = tmp_path / "история.log"
    log_path.write_text("Существующая запись\n", encoding="utf-8")

    @log(filename=str(log_path))
    def echo(text: str) -> str:
        """Вернуть переданную строку."""
        return text

    assert echo("Привет") == "Привет"
    assert echo("Мир") == "Мир"
    output = log_path.read_text(encoding="utf-8")
    assert output.startswith("Существующая запись\n")
    assert output.count("echo ok\n") == 2
    assert "echo result: 'Привет'" in output
    assert "echo result: 'Мир'" in output
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("result", [None, False, 0, "", {"items": [1, 2]}])
def test_result_unchanged(result: Any, capsys: pytest.CaptureFixture[str]) -> None:
    """Возвращать исходный объект, включая пустые и ложные значения."""
    @log()
    def value() -> Any:
        """Вернуть объект без преобразований."""
        return result

    assert value() is result
    output = capsys.readouterr().out
    assert "Inputs: (), {}" in output
    assert f"value result: {result!r}" in output
    assert "value ok" in output


def test_metadata_and_single_call(capsys: pytest.CaptureFixture[str]) -> None:
    """Сохранить метаданные и вызывать функцию ровно один раз между start/end."""
    calls: list[int] = []

    def original(number: int) -> int:
        """Документация исходной функции."""
        calls.append(number)
        print("function body")
        return number

    decorated = log()(original)
    assert decorated.__name__ == original.__name__
    assert decorated.__doc__ == original.__doc__
    assert decorated.__annotations__ == original.__annotations__
    assert getattr(decorated, "__wrapped__") is original
    assert decorated(5) == 5
    assert calls == [5]
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith("original start:")
    assert lines[1] == "function body"
    assert lines[-1].startswith("original end:")
