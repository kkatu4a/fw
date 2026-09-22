"""Тесты модели Goal."""

from models import Category, Goal
from models.goals import (
    add_goal,
    filter_goals_by_category,
    filter_goals_by_status,
    find_goal_by_id,
    find_goals_by_title,
    get_statistics,
)


def make_category(cat_id=1, name="Работа"):
    return Category(cat_id, name)


def test_goal_creation():
    category = make_category()
    goal = Goal(1, "Выучить Django", "Курс", category, 1,
                "2026-09-01", "2026-09-15")
    assert goal.id == 1
    assert goal.title == "Выучить Django"
    assert goal.category is category
    assert goal.progress == 0
    assert goal.is_completed is False


def test_goal_str():
    category = make_category()
    goal = Goal(1, "Выучить Django", "Курс", category, 1,
                "2026-09-01", "2026-09-15")
    assert "Выучить Django" in str(goal)
    assert "Работа" in str(goal)


def test_goal_priority_label():
    category = make_category()
    goal = Goal(1, "Цель", "Описание", category, 1,
                "2026-09-01", "2026-09-15")
    assert goal.get_priority_label() == "Высокий"


def test_goal_progress_status():
    category = make_category()
    goal = Goal(1, "Цель", "Описание", category, 1,
                "2026-09-01", "2026-09-15")
    goal.update_progress(50)
    assert goal.get_progress_status() == "Половина пути сделана"


def test_goal_update_progress():
    category = make_category()
    goal = Goal(1, "Цель", "Описание", category, 1,
                "2026-09-01", "2026-09-15")
    goal.update_progress(75)
    assert goal.progress == 75
    assert goal.is_completed is False


def test_goal_complete():
    category = make_category()
    goal = Goal(1, "Цель", "Описание", category, 1,
                "2026-09-01", "2026-09-15")
    goal.complete()
    assert goal.progress == 100
    assert goal.is_completed is True


def test_goal_from_data():
    category = make_category()
    data = {
        "id": 5, "title": "Цель", "description": "Описание",
        "category_id": 1, "priority": 2, "created_date": "2026-09-01",
        "deadline": "2026-09-15", "progress": 30, "is_completed": False,
    }
    goal = Goal.from_data(data, category)
    assert goal.id == 5
    assert goal.category is category


def test_add_goal():
    category = make_category()
    goals = []
    add_goal(goals, "Цель", "Описание", category, 1,
             "2026-09-01", "2026-09-15")
    assert len(goals) == 1


def test_find_goal_by_id():
    category = make_category()
    goals = []
    add_goal(goals, "Цель 1", "О", category, 1, "2026-09-01", "2026-09-15")
    add_goal(goals, "Цель 2", "О", category, 2, "2026-09-02", "2026-09-16")
    assert find_goal_by_id(goals, 2).title == "Цель 2"


def test_find_goals_by_title():
    category = make_category()
    goals = []
    add_goal(goals, "Выучить Django", "О", category, 1,
             "2026-09-01", "2026-09-15")
    add_goal(goals, "Выучить Python", "О", category, 1,
             "2026-09-01", "2026-09-15")
    assert len(find_goals_by_title(goals, "python")) == 1


def test_filter_goals_by_category():
    cat1 = make_category(1, "Работа")
    cat2 = make_category(2, "Здоровье")
    goals = []
    add_goal(goals, "Ц1", "О", cat1, 1, "2026-09-01", "2026-09-15")
    add_goal(goals, "Ц2", "О", cat2, 2, "2026-09-02", "2026-09-16")
    assert len(filter_goals_by_category(goals, 1)) == 1


def test_filter_goals_by_status():
    category = make_category()
    goals = []
    add_goal(goals, "Ц1", "О", category, 1, "2026-09-01", "2026-09-15")
    add_goal(goals, "Ц2", "О", category, 1, "2026-09-02", "2026-09-16")
    goals[0].complete()
    assert len(filter_goals_by_status(goals, True)) == 1


def test_statistics_empty():
    stats = get_statistics([])
    assert stats["total"] == 0
    assert stats["completed"] == 0
