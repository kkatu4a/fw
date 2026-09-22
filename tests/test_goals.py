"""Тесты функций работы с целями."""

from goals import (
    add_goal,
    complete_goal,
    delete_goal,
    filter_goals_by_category,
    find_goal_by_id,
    find_goals_by_title,
    get_statistics,
    update_goal_progress,
)


def test_add_goal():
    goals = []
    add_goal(goals, "Выучить Django", "Курс", 1, 1, "2026-09-01", "2026-09-15")
    assert len(goals) == 1
    assert goals[0]["title"] == "Выучить Django"


def test_find_goal_by_id():
    goals = []
    add_goal(goals, "Цель 1", "Описание", 1, 1, "2026-09-01", "2026-09-15")
    add_goal(goals, "Цель 2", "Описание", 2, 2, "2026-09-02", "2026-09-16")
    assert find_goal_by_id(goals, 2)["title"] == "Цель 2"


def test_find_goals_by_title():
    goals = []
    add_goal(goals, "Выучить Django", "Курс", 1, 1, "2026-09-01", "2026-09-15")
    add_goal(goals, "Выучить Python", "Курс", 1, 1, "2026-09-01", "2026-09-15")
    assert len(find_goals_by_title(goals, "python")) == 1


def test_filter_goals_by_category():
    goals = []
    add_goal(goals, "Цель 1", "Описание", 1, 1, "2026-09-01", "2026-09-15")
    add_goal(goals, "Цель 2", "Описание", 2, 2, "2026-09-02", "2026-09-16")
    assert len(filter_goals_by_category(goals, 1)) == 1


def test_update_and_complete_goal():
    goals = []
    add_goal(goals, "Цель", "Описание", 1, 1, "2026-09-01", "2026-09-15")
    update_goal_progress(goals, 1, 50)
    assert goals[0]["progress"] == 50
    assert goals[0]["is_completed"] is False
    complete_goal(goals, 1)
    assert goals[0]["is_completed"] is True


def test_delete_goal():
    goals = []
    add_goal(goals, "Цель", "Описание", 1, 1, "2026-09-01", "2026-09-15")
    assert delete_goal(goals, 1) is True
    assert len(goals) == 0


def test_statistics_empty():
    stats = get_statistics([])
    assert stats["total"] == 0
    assert stats["completed"] == 0