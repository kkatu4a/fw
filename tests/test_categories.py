"""Тесты модели Category."""

from models import Category
from models.categories import (
    add_category,
    find_category_by_id,
    get_category_name,
    sort_categories_by_name,
)


def test_category_creation():
    category = Category(1, "Работа")
    assert category.id == 1
    assert category.name == "Работа"


def test_category_str():
    category = Category(2, "Здоровье")
    assert "Здоровье" in str(category)


def test_add_category():
    categories = []
    add_category(categories, "Работа")
    assert len(categories) == 1


def test_find_category_by_id():
    categories = []
    add_category(categories, "Работа")
    add_category(categories, "Здоровье")
    assert find_category_by_id(categories, 2).name == "Здоровье"


def test_get_category_name_missing():
    assert get_category_name([], 99) == "Без категории"


def test_sort_categories_by_name():
    categories = []
    add_category(categories, "Здоровье")
    add_category(categories, "Работа")
    sorted_cats = sort_categories_by_name(categories)
    assert sorted_cats[0].name == "Здоровье"
