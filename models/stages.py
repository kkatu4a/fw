"""Модель этапа цели."""

from typing import Optional

from .goals import Goal


class Stage:
    """Этап — промежуточный шаг на пути к цели."""

    def __init__(
        self,
        stage_id: int,
        title: str,
        goal: Goal,
        is_done: bool = False,
    ) -> None:
        """Создать объект этапа."""
        self.id = stage_id
        self.title = title
        self.goal = goal
        self.is_done = is_done

    def complete(self) -> None:
        """Отметить этап выполненным."""
        self.is_done = True

    def __str__(self) -> str:
        """Вернуть строковое представление этапа."""
        mark = "[x]" if self.is_done else "[ ]"
        return f"Stage #{self.id}: {mark} {self.title} (цель: {self.goal.title})"

    @classmethod
    def from_data(cls, data: dict, goal: Goal) -> "Stage":
        """Создать этап из словаря и объекта Goal."""
        return cls(
            stage_id=data["id"],
            title=data["title"],
            goal=goal,
            is_done=data.get("is_done", False),
        )

    def to_data(self) -> dict:
        """Преобразовать этап в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "goal_id": self.goal.id,
            "is_done": self.is_done,
        }


def add_stage(
    stages: list[Stage], title: str, goal: Goal
) -> Stage:
    """Создать этап и добавить его в коллекцию."""
    new_id = max((s.id for s in stages), default=0) + 1
    stage = Stage(new_id, title, goal)
    stages.append(stage)
    return stage


def find_stage_by_id(
    stages: list[Stage], stage_id: int
) -> Optional[Stage]:
    """Найти этап по идентификатору."""
    for stage in stages:
        if stage.id == stage_id:
            return stage
    return None


def find_stages_by_goal(
    stages: list[Stage], goal_id: int
) -> list[Stage]:
    """Найти этапы по цели."""
    return [s for s in stages if s.goal.id == goal_id]


def complete_stage(stages: list[Stage], stage_id: int) -> bool:
    """Отметить этап выполненным."""
    stage = find_stage_by_id(stages, stage_id)
    if stage is None:
        return False
    stage.complete()
    return True


def get_goal_progress_from_stages(
    stages: list[Stage], goal_id: int
) -> int:
    """Рассчитать прогресс цели по её этапам."""
    goal_stages = find_stages_by_goal(stages, goal_id)
    if not goal_stages:
        return 0
    done = sum(1 for s in goal_stages if s.is_done)
    return int(done / len(goal_stages) * 100)


def show_stages(stages: list[Stage]) -> None:
    """Вывести список этапов."""
    if not stages:
        print("Список этапов пуст.")
        return
    for stage in stages:
        print(f"  {stage}")
