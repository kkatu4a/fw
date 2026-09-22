"""Модель результата выполнения цели."""

from typing import Optional

from .goals import Goal


class Result:
    """Результат — итог выполнения цели."""

    def __init__(
        self,
        result_id: int,
        description: str,
        goal: Goal,
        achieved: bool = False,
    ) -> None:
        """Создать объект результата."""
        self.id = result_id
        self.description = description
        self.goal = goal
        self.achieved = achieved

    def mark_achieved(self) -> None:
        """Отметить результат как достигнутый."""
        self.achieved = True

    def __str__(self) -> str:
        """Вернуть строковое представление результата."""
        mark = "достигнут" if self.achieved else "не достигнут"
        return f"Result #{self.id}: {self.description} ({mark})"

    @classmethod
    def from_data(cls, data: dict, goal: Goal) -> "Result":
        """Создать результат из словаря и объекта Goal."""
        return cls(
            result_id=data["id"],
            description=data["description"],
            goal=goal,
            achieved=data.get("achieved", False),
        )

    def to_data(self) -> dict:
        """Преобразовать результат в словарь."""
        return {
            "id": self.id,
            "description": self.description,
            "goal_id": self.goal.id,
            "achieved": self.achieved,
        }


def add_result(
    results: list[Result], description: str, goal: Goal
) -> Result:
    """Создать результат и добавить его в коллекцию."""
    new_id = max((r.id for r in results), default=0) + 1
    result = Result(new_id, description, goal)
    results.append(result)
    return result


def find_result_by_id(
    results: list[Result], result_id: int
) -> Optional[Result]:
    """Найти результат по идентификатору."""
    for result in results:
        if result.id == result_id:
            return result
    return None


def find_results_by_goal(
    results: list[Result], goal_id: int
) -> list[Result]:
    """Найти результаты по цели."""
    return [r for r in results if r.goal.id == goal_id]


def mark_result_achieved(results: list[Result], result_id: int) -> bool:
    """Отметить результат достигнутым."""
    result = find_result_by_id(results, result_id)
    if result is None:
        return False
    result.mark_achieved()
    return True


def show_results(results: list[Result]) -> None:
    """Вывести список результатов."""
    if not results:
        print("Список результатов пуст.")
        return
    for result in results:
        print(f"  {result}")
