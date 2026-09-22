"""Функции для работы с целями пользователя."""

from datetime import datetime
from typing import Optional


def add_goal(
    goals: list[dict],
    title: str,
    description: str,
    category_id: int,
    priority: int,
    created_date: str,
    deadline: str,
) -> dict:
    """Добавить новую цель и вернуть её."""
    new_id = max((g["id"] for g in goals), default=0) + 1
    goal = {
        "id": new_id,
        "title": title,
        "description": description,
        "category_id": category_id,
        "priority": priority,
        "created_date": created_date,
        "deadline": deadline,
        "progress": 0,
        "is_completed": False,
    }
    goals.append(goal)
    return goal


def find_goal_by_id(goals: list[dict], goal_id: int) -> Optional[dict]:
    """Найти цель по идентификатору."""
    for goal in goals:
        if goal["id"] == goal_id:
            return goal
    return None


def find_goals_by_title(goals: list[dict], query: str) -> list[dict]:
    """Найти цели по подстроке названия (без учёта регистра)."""
    query_lower = query.lower()
    return [g for g in goals if query_lower in g["title"].lower()]


def filter_goals_by_category(goals: list[dict], category_id: int) -> list[dict]:
    """Отобрать цели по категории."""
    return [g for g in goals if g["category_id"] == category_id]


def filter_goals_by_status(goals: list[dict], is_completed: bool) -> list[dict]:
    """Отобрать цели по статусу выполнения."""
    return [g for g in goals if g["is_completed"] == is_completed]


def filter_goals_by_priority(goals: list[dict], priority: int) -> list[dict]:
    """Отобрать цели по приоритету."""
    return [g for g in goals if g["priority"] == priority]


def sort_goals_by_deadline(goals: list[dict]) -> list[dict]:
    """Отсортировать цели по дедлайну."""
    return sorted(goals, key=lambda g: g["deadline"])


def sort_goals_by_priority(goals: list[dict]) -> list[dict]:
    """Отсортировать цели по приоритету."""
    return sorted(goals, key=lambda g: g["priority"])


def update_goal_progress(goals: list[dict], goal_id: int, progress: int) -> bool:
    """Обновить прогресс цели. Вернуть True при успехе."""
    goal = find_goal_by_id(goals, goal_id)
    if goal is None:
        return False
    goal["progress"] = progress
    goal["is_completed"] = progress >= 100
    return True


def complete_goal(goals: list[dict], goal_id: int) -> bool:
    """Отметить цель как выполненную."""
    return update_goal_progress(goals, goal_id, 100)


def delete_goal(goals: list[dict], goal_id: int) -> bool:
    """Удалить цель по идентификатору."""
    goal = find_goal_by_id(goals, goal_id)
    if goal is None:
        return False
    goals.remove(goal)
    return True


def get_priority_label(priority_value: int) -> str:
    """Вернуть текстовое описание приоритета."""
    if priority_value == 1:
        return "Высокий"
    elif priority_value == 2:
        return "Средний"
    elif priority_value == 3:
        return "Низкий"
    return "Неизвестно"


def get_progress_status(percent: int) -> str:
    """Оценить состояние прогресса."""
    if percent == 100:
        return "Цель достигнута"
    elif percent >= 75:
        return "Почти готово!"
    elif percent >= 50:
        return "Половина пути сделана"
    elif percent >= 25:
        return "Продолжайте"
    return "Начало"


def get_goal_status(goal: dict) -> str:
    """Вернуть полный статус цели."""
    if goal["is_completed"]:
        return "Цель достигнута"
    return get_progress_status(goal["progress"])


def get_statistics(goals: list[dict]) -> dict:
    """Статистика: всего, выполнено, средний прогресс."""
    if not goals:
        return {"total": 0, "completed": 0, "average_progress": 0.0}
    completed = sum(1 for g in goals if g["is_completed"])
    average = sum(g["progress"] for g in goals) / len(goals)
    return {
        "total": len(goals),
        "completed": completed,
        "average_progress": round(average, 1),
    }


def count_days_left(deadline: str) -> int:
    """Сколько дней осталось до дедлайна."""
    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
    today = datetime.now().date()
    return (deadline_date - today).days
