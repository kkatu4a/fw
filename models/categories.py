"""Модель категории целей."""

from typing import Optional


class Category:
    """Категория — группа для целей (Работа, Здоровье и т.д.)."""

    def __init__(self, category_id: int, name: str) -> None:
        """Создать объект категории."""
        self.id = category_id
        self.name = name

    def __str__(self) -> str:
        """Вернуть строковое представление категории."""
        return f"Category #{self.id}: {self.name}"

    @classmethod
    def from_data(cls, data: dict) -> "Category":
        """Создать категорию из словаря."""
        return cls(category_id=data["id"], name=data["name"])

    def to_data(self) -> dict:
        """Преобразовать категорию в словарь."""
        return {"id": self.id, "name": self.name}


def add_category(categories: list[Category], name: str) -> Category:
    """Создать категорию и добавить её в коллекцию."""
    new_id = max((c.id for c in categories), default=0) + 1
    category = Category(new_id, name)
    categories.append(category)
    return category


def find_category_by_id(
    categories: list[Category], category_id: int
) -> Optional[Category]:
    """Найти категорию по идентификатору."""
    for category in categories:
        if category.id == category_id:
            return category
    return None


def get_category_name(
    categories: list[Category], category_id: int
) -> str:
    """Вернуть название категории или 'Без категории'."""
    category = find_category_by_id(categories, category_id)
    return category.name if category else "Без категории"


def sort_categories_by_name(
    categories: list[Category],
) -> list[Category]:
    """Отсортировать категории по названию."""
    return sorted(categories, key=lambda c: c.name.lower())


def show_categories(categories: list[Category]) -> None:
    """Вывести список категорий."""
    if not categories:
        print("Список категорий пуст.")
        return
    for category in sort_categories_by_name(categories):
        print(f"  {category}")
