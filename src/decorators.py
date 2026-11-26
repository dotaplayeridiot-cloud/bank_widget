"""Декоратор для записи вызовов функций в консоль или UTF-8 файл."""

from collections.abc import Callable
from datetime import datetime
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def _write_log(message: str, filename: str | None) -> None:
    """Вывести запись в консоль или добавить её в файл без перезаписи."""
    if filename is None:
        print(message)
    else:
        with open(filename, "a", encoding="utf-8") as log_file:
            log_file.write(message + "\n")


def log(filename: str | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Логировать начало, завершение, результат или исключение вызова.

    Использование: @log() для консоли, @log(filename="mylog.txt") для файла.
    Файл создаётся или дополняется в UTF-8; его родительская папка должна
    существовать. Исключения функции записываются и передаются дальше.
    Имя, docstring, аннотации и возвращаемое значение функции сохраняются.
    """
    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        """Обернуть функцию, сохранив её метаданные и типы."""
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """Выполнить один вызов и записать его исход и время."""
            name = function.__name__
            started_at = datetime.now().astimezone().isoformat()
            _write_log(f"{name} start: {started_at}. Inputs: {args!r}, {kwargs!r}", filename)
            try:
                result = function(*args, **kwargs)
            except Exception as error:
                _write_log(
                    f"{name} error: {type(error).__name__}. Inputs: {args!r}, {kwargs!r}. Error: {error}",
                    filename,
                )
                raise
            else:
                _write_log(f"{name} ok", filename)
                _write_log(f"{name} result: {result!r}", filename)
                return result
            finally:
                finished_at = datetime.now().astimezone().isoformat()
                _write_log(f"{name} end: {finished_at}", filename)

        return wrapper

    return decorator
