"""Модель цели."""

from datetime import datetime
from typing import Optional

from .categories import Category


class Goal:
    """Цель пользователя."""

    def __init__(
        self,
        goal_id: int,
        title: str,
        description: str,
        category: Category,
        priority: int,
        created_date: str,
        deadline: str,
        progress: int = 0,
        is_completed: bool = False,
    ) -> None:
        """Создать объект цели."""
        self.id = goal_id
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.created_date = created_date
        self.deadline = deadline
        self.progress = progress
        self.is_completed = is_completed

    def get_priority_label(self) -> str:
        """Вернуть текстовое описание приоритета."""
        if self.priority == 1:
            return "Высокий"
        elif self.priority == 2:
            return "Средний"
        elif self.priority == 3:
            return "Низкий"
        return "Неизвестно"

    def get_progress_status(self) -> str:
        """Оценить состояние прогресса."""
        if self.progress == 100:
            return "Цель достигнута"
        elif self.progress >= 75:
            return "Почти готово!"
        elif self.progress >= 50:
            return "Половина пути сделана"
        elif self.progress >= 25:
            return "Продолжайте"
        return "Начало"

    def update_progress(self, progress: int) -> None:
        """Обновить прогресс цели."""
        self.progress = progress
        self.is_completed = progress >= 100

    def complete(self) -> None:
        """Отметить цель как выполненную."""
        self.update_progress(100)

    def days_left(self) -> int:
        """Сколько дней осталось до дедлайна."""
        deadline_date = datetime.strptime(self.deadline, "%Y-%m-%d").date()
        today = datetime.now().date()
        return (deadline_date - today).days

    def __str__(self) -> str:
        """Вернуть строковое представление цели."""
        status = "выполнена" if self.is_completed else "в работе"
        return (
            f"Goal #{self.id}: {self.title} "
            f"[{self.category.name}, {self.get_priority_label()}, "
            f"{self.progress}%, {status}]"
        )

    @classmethod
    def from_data(cls, data: dict, category: Category) -> "Goal":
        """Создать цель из словаря и объекта Category."""
        return cls(
            goal_id=data["id"],
            title=data["title"],
            description=data["description"],
            category=category,
            priority=data["priority"],
            created_date=data["created_date"],
            deadline=data["deadline"],
            progress=data.get("progress", 0),
            is_completed=data.get("is_completed", False),
        )

    def to_data(self) -> dict:
        """Преобразовать цель в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category_id": self.category.id,
            "priority": self.priority,
            "created_date": self.created_date,
            "deadline": self.deadline,
            "progress": self.progress,
            "is_completed": self.is_completed,
        }


def add_goal(
    goals: list[Goal],
    title: str,
    description: str,
    category: Category,
    priority: int,
    created_date: str,
    deadline: str,
) -> Goal:
    """Создать цель и добавить её в коллекцию."""
    new_id = max((g.id for g in goals), default=0) + 1
    goal = Goal(new_id, title, description, category, priority,
                created_date, deadline)
    goals.append(goal)
    return goal


def find_goal_by_id(goals: list[Goal], goal_id: int) -> Optional[Goal]:
    """Найти цель по идентификатору."""
    for goal in goals:
        if goal.id == goal_id:
            return goal
    return None


def find_goals_by_title(goals: list[Goal], query: str) -> list[Goal]:
    """Найти цели по подстроке названия."""
    q = query.lower()
    return [g for g in goals if q in g.title.lower()]


def filter_goals_by_category(
    goals: list[Goal], category_id: int
) -> list[Goal]:
    """Отобрать цели по категории."""
    return [g for g in goals if g.category.id == category_id]


def filter_goals_by_status(
    goals: list[Goal], is_completed: bool
) -> list[Goal]:
    """Отобрать цели по статусу."""
    return [g for g in goals if g.is_completed == is_completed]


def sort_goals_by_deadline(goals: list[Goal]) -> list[Goal]:
    """Отсортировать цели по дедлайну."""
    return sorted(goals, key=lambda g: g.deadline)


def get_statistics(goals: list[Goal]) -> dict:
    """Вернуть статистику по целям."""
    if not goals:
        return {"total": 0, "completed": 0, "average_progress": 0.0}
    completed = sum(1 for g in goals if g.is_completed)
    average = sum(g.progress for g in goals) / len(goals)
    return {
        "total": len(goals),
        "completed": completed,
        "average_progress": round(average, 1),
    }


def show_goals(goals: list[Goal]) -> None:
    """Вывести список целей."""
    if not goals:
        print("Список целей пуст.")
        return
    for goal in goals:
        print(f"  {goal}")
        print(f"      Дедлайн: {goal.deadline} "
              f"(дней: {goal.days_left()})")
        print(f"      Статус: {goal.get_progress_status()}")
        print("-" * 40)
