"""Вспомогательные функции для ввода данных с обработкой ошибок."""

from datetime import datetime


def input_int(prompt: str, min_value: int = None, max_value: int = None) -> int:
    """Запросить у пользователя целое число с повторным вводом при ошибке."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Значение должно быть не меньше {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Значение должно быть не больше {max_value}.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите целое число.")


def input_str(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: строка не может быть пустой.")


def input_date(prompt: str) -> str:
    """Запросить дату в формате ДД.ММ.ГГГГ и вернуть в формате ГГГГ-ММ-ДД."""
    while True:
        raw = input(prompt).strip()
        try:
            parsed = datetime.strptime(raw, "%d.%m.%Y")
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            print("Ошибка: неверный формат даты. Используйте ДД.ММ.ГГГГ.")


def input_progress(prompt: str) -> int:
    """Запросить прогресс от 0 до 100."""
    return input_int(prompt, min_value=0, max_value=100)