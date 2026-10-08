"""Сохранение и загрузка объектов проекта в JSON-файлы."""

import json
import os

from models import Category, Goal, Result, Stage, User

DATA_DIR = "data"


def _ensure_data_dir() -> None:
    """Создать каталог data, если он отсутствует."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def _load_json(filename: str) -> list:
    """Загрузить список из JSON-файла."""
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


def _save_json(filename: str, data: list) -> None:
    """Сохранить список в JSON-файл."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_users() -> list[User]:
    """Загрузить пользователей."""
    return [User.from_data(d) for d in _load_json("users.json")]


def save_users(users: list[User]) -> None:
    """Сохранить пользователей."""
    _save_json("users.json", [u.to_data() for u in users])


def load_categories() -> list[Category]:
    """Загрузить категории."""
    return [Category.from_data(d) for d in _load_json("categories.json")]


def save_categories(categories: list[Category]) -> None:
    """Сохранить категории."""
    _save_json("categories.json", [c.to_data() for c in categories])


def load_goals(
    users: list[User], categories: list[Category]
) -> list[Goal]:
    """Загрузить цели, восстановив связи с User и Category."""
    goals = []
    for data in _load_json("goals.json"):
        owner = next(
            (u for u in users if u.id == data["user_id"]), None
        )
        category = next(
            (c for c in categories if c.id == data["category_id"]), None
        )
        if owner is None or category is None:
            continue
        goals.append(Goal.from_data(data, owner, category))
    return goals


def save_goals(goals: list[Goal]) -> None:
    """Сохранить цели."""
    _save_json("goals.json", [g.to_data() for g in goals])


def load_stages(goals: list[Goal]) -> list[Stage]:
    """Загрузить этапы, восстановив связи с целями."""
    stages = []
    for data in _load_json("stages.json"):
        goal = next((g for g in goals if g.id == data["goal_id"]), None)
        if goal is None:
            continue
        stages.append(Stage.from_data(data, goal))
    return stages


def save_stages(stages: list[Stage]) -> None:
    """Сохранить этапы."""
    _save_json("stages.json", [s.to_data() for s in stages])


def load_results(goals: list[Goal]) -> list[Result]:
    """Загрузить результаты, восстановив связи с целями."""
    results = []
    for data in _load_json("results.json"):
        goal = next((g for g in goals if g.id == data["goal_id"]), None)
        if goal is None:
            continue
        results.append(Result.from_data(data, goal))
    return results


def save_results(results: list[Result]) -> None:
    """Сохранить результаты."""
    _save_json("results.json", [r.to_data() for r in results])