"""Функции для работы с категориями целей."""

from typing import Optional


def add_category(categories: list[dict], name: str) -> dict:
    """Добавить новую категорию и вернуть её."""
    new_id = max((c["id"] for c in categories), default=0) + 1
    category = {"id": new_id, "name": name}
    categories.append(category)
    return category


def find_category_by_id(categories: list[dict], category_id: int) -> Optional[dict]:
    """Найти категорию по идентификатору."""
    for category in categories:
        if category["id"] == category_id:
            return category
    return None


def find_categories_by_name(categories: list[dict], query: str) -> list[dict]:
    """Найти категории по подстроке названия (без учёта регистра)."""
    query_lower = query.lower()
    return [c for c in categories if query_lower in c["name"].lower()]


def get_category_name(categories: list[dict], category_id: int) -> str:
    """Вернуть название категории или 'Без категории'."""
    category = find_category_by_id(categories, category_id)
    return category["name"] if category else "Без категории"


def sort_categories_by_name(categories: list[dict]) -> list[dict]:
    """Отсортировать категории по названию."""
    return sorted(categories, key=lambda c: c["name"].lower())