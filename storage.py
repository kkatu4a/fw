"""Сохранение и загрузка данных проекта в JSON-файлы."""

import json
import os

DATA_DIR = "data"


def _ensure_data_dir() -> None:
    """Создать каталог data, если он отсутствует."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_json(filename: str) -> list:
    """Загрузить список из JSON-файла. При ошибке вернуть пустой список."""
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {path} не найден. Будет создан при сохранении.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {path} содержит некорректный JSON.")
        return []


def save_json(filename: str, data: list) -> None:
    """Сохранить список в JSON-файл."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_goals() -> list:
    """Загрузить цели."""
    return load_json("goals.json")


def save_goals(goals: list) -> None:
    """Сохранить цели."""
    save_json("goals.json", goals)


def load_categories() -> list:
    """Загрузить категории."""
    return load_json("categories.json")


def save_categories(categories: list) -> None:
    """Сохранить категории."""
    save_json("categories.json", categories)