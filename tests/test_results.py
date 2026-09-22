"""Тесты модели Result."""

from models import Category, Goal, Result
from models.results import (
    add_result,
    find_result_by_id,
    find_results_by_goal,
    mark_result_achieved,
)


def make_goal(goal_id=1):
    category = Category(1, "Работа")
    return Goal(goal_id, "Цель", "Описание", category, 1,
                "2026-09-01", "2026-09-15")


def test_result_creation():
    goal = make_goal()
    result = Result(1, "Работающее приложение", goal)
    assert result.id == 1
    assert result.description == "Работающее приложение"
    assert result.goal is goal
    assert result.achieved is False


def test_result_str():
    goal = make_goal()
    result = Result(1, "Работающее приложение", goal)
    assert "Работающее приложение" in str(result)
    assert "не достигнут" in str(result)


def test_result_mark_achieved():
    goal = make_goal()
    result = Result(1, "Работающее приложение", goal)
    result.mark_achieved()
    assert result.achieved is True
    assert "достигнут" in str(result)


def test_add_result():
    goal = make_goal()
    results = []
    add_result(results, "Результат", goal)
    assert len(results) == 1


def test_find_result_by_id():
    goal = make_goal()
    results = []
    add_result(results, "Р1", goal)
    add_result(results, "Р2", goal)
    assert find_result_by_id(results, 2).description == "Р2"


def test_find_results_by_goal():
    goal1 = make_goal(1)
    goal2 = make_goal(2)
    results = []
    add_result(results, "Р1", goal1)
    add_result(results, "Р2", goal1)
    add_result(results, "Р3", goal2)
    assert len(find_results_by_goal(results, 1)) == 2


def test_mark_result_achieved():
    goal = make_goal()
    results = []
    add_result(results, "Результат", goal)
    assert mark_result_achieved(results, 1) is True
    assert results[0].achieved is True
