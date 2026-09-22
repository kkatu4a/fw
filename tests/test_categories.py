"""Тесты функций работы с категориями."""

from categories import (
    add_category,
    find_categories_by_name,
    find_category_by_id,
    get_category_name,
    sort_categories_by_name,
)


def test_add_category():
    categories = []
    add_category(categories, "Работа")
    assert len(categories) == 1
    assert categories[0]["name"] == "Работа"


def test_find_category_by_id():
    categories = []
    add_category(categories, "Работа")
    add_category(categories, "Здоровье")
    assert find_category_by_id(categories, 2)["name"] == "Здоровье"


def test_find_categories_by_name():
    categories = []
    add_category(categories, "Работа")
    add_category(categories, "Рабочие проекты")
    add_category(categories, "Здоровье")
    assert len(find_categories_by_name(categories, "рабоч")) == 1


def test_get_category_name_missing():
    assert get_category_name([], 99) == "Без категории"


def test_sort_categories_by_name():
    categories = []
    add_category(categories, "Здоровье")
    add_category(categories, "Работа")
    sorted_cats = sort_categories_by_name(categories)
    assert sorted_cats[0]["name"] == "Здоровье"