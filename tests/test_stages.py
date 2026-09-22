"""Тесты модели Stage."""

from models import Category, Goal, Stage
from models.stages import (
    add_stage,
    complete_stage,
    find_stage_by_id,
    find_stages_by_goal,
    get_goal_progress_from_stages,
)


def make_goal(goal_id=1):
    category = Category(1, "Работа")
    return Goal(goal_id, "Цель", "Описание", category, 1,
                "2026-09-01", "2026-09-15")


def test_stage_creation():
    goal = make_goal()
    stage = Stage(1, "Пройти раздел", goal)
    assert stage.id == 1
    assert stage.title == "Пройти раздел"
    assert stage.goal is goal
    assert stage.is_done is False


def test_stage_str():
    goal = make_goal()
    stage = Stage(1, "Пройти раздел", goal)
    assert "Пройти раздел" in str(stage)
    assert "[ ]" in str(stage)


def test_stage_complete():
    goal = make_goal()
    stage = Stage(1, "Пройти раздел", goal)
    stage.complete()
    assert stage.is_done is True
    assert "[x]" in str(stage)


def test_add_stage():
    goal = make_goal()
    stages = []
    add_stage(stages, "Этап", goal)
    assert len(stages) == 1


def test_find_stage_by_id():
    goal = make_goal()
    stages = []
    add_stage(stages, "Этап 1", goal)
    add_stage(stages, "Этап 2", goal)
    assert find_stage_by_id(stages, 2).title == "Этап 2"


def test_find_stages_by_goal():
    goal1 = make_goal(1)
    goal2 = make_goal(2)
    stages = []
    add_stage(stages, "Этап 1", goal1)
    add_stage(stages, "Этап 2", goal1)
    add_stage(stages, "Этап 3", goal2)
    assert len(find_stages_by_goal(stages, 1)) == 2


def test_complete_stage():
    goal = make_goal()
    stages = []
    add_stage(stages, "Этап", goal)
    assert complete_stage(stages, 1) is True
    assert stages[0].is_done is True


def test_progress_from_stages():
    goal = make_goal()
    stages = []
    add_stage(stages, "Этап 1", goal)
    add_stage(stages, "Этап 2", goal)
    complete_stage(stages, 1)
    assert get_goal_progress_from_stages(stages, 1) == 50


def test_progress_from_stages_empty():
    assert get_goal_progress_from_stages([], 1) == 0
