"""Тесты модели Goal."""

from models import Category, Goal, User
from models.goals import (
    add_goal,
    filter_goals_by_category,
    filter_goals_by_status,
    find_goal_by_id,
    find_goals_by_title,
    find_goals_by_user,
    get_statistics,
)


def make_user(user_id=1, name="Иван"):
    return User(user_id, name, f"user{user_id}@example.com")


def make_category(cat_id=1, name="Работа"):
    return Category(cat_id, name)


def test_goal_creation():
    owner = make_user()
    category = make_category()
    goal = Goal(1, "Выучить Django", "Курс", owner, category, 1,
                "2026-09-01", "2026-09-15")
    assert goal.id == 1
    assert goal.owner is owner
    assert goal.category is category
    assert goal.progress == 0
    assert goal.is_completed is False


def test_goal_str_contains_owner():
    owner = make_user(1, "Иван")
    category = make_category()
    goal = Goal(1, "Цель", "О", owner, category, 1,
                "2026-09-01", "2026-09-15")
    assert "Иван" in str(goal)


def test_goal_update_progress():
    owner = make_user()
    category = make_category()
    goal = Goal(1, "Цель", "О", owner, category, 1,
                "2026-09-01", "2026-09-15")
    goal.update_progress(75)
    assert goal.progress == 75
    assert goal.is_completed is False


def test_goal_complete():
    owner = make_user()
    category = make_category()
    goal = Goal(1, "Цель", "О", owner, category, 1,
                "2026-09-01", "2026-09-15")
    goal.complete()
    assert goal.progress == 100
    assert goal.is_completed is True


def test_goal_from_data():
    owner = make_user(5, "Анна")
    category = make_category()
    data = {
        "id": 5, "title": "Цель", "description": "О",
        "user_id": 5, "category_id": 1, "priority": 2,
        "created_date": "2026-09-01", "deadline": "2026-09-15",
        "progress": 30, "is_completed": False,
    }
    goal = Goal.from_data(data, owner, category)
    assert goal.id == 5
    assert goal.owner is owner


def test_add_goal():
    owner = make_user()
    category = make_category()
    goals = []
    add_goal(goals, "Цель", "О", owner, category, 1,
             "2026-09-01", "2026-09-15")
    assert len(goals) == 1
    assert goals[0].owner is owner


def test_find_goals_by_user():
    user1 = make_user(1, "Иван")
    user2 = make_user(2, "Анна")
    category = make_category()
    goals = []
    add_goal(goals, "Ц1", "О", user1, category, 1,
             "2026-09-01", "2026-09-15")
    add_goal(goals, "Ц2", "О", user1, category, 1,
             "2026-09-02", "2026-09-16")
    add_goal(goals, "Ц3", "О", user2, category, 1,
             "2026-09-03", "2026-09-17")
    assert len(find_goals_by_user(goals, 1)) == 2
    assert len(find_goals_by_user(goals, 2)) == 1


def test_statistics_empty():
    stats = get_statistics([])
    assert stats["total"] == 0
    assert stats["completed"] == 0