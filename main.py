"""Система отслеживания целей. Точка запуска приложения."""

from datetime import datetime
from typing import Optional

from models import Category, Goal, Result, Stage, User
from models.categories import (
    add_category,
    get_category_name,
    show_categories,
)
from models.goals import (
    add_goal,
    filter_goals_by_category,
    filter_goals_by_status,
    find_goal_by_id,
    find_goals_by_title,
    get_statistics,
    show_goals,
    sort_goals_by_deadline,
)
from models.results import (
    add_result,
    find_results_by_goal,
    mark_result_achieved,
    show_results,
)
from models.stages import (
    add_stage,
    complete_stage,
    find_stages_by_goal,
    get_goal_progress_from_stages,
    show_stages,
)
from models.users import add_user, find_user_by_id, show_users
from storage import (
    load_categories,
    load_goals,
    load_results,
    load_stages,
    load_users,
    save_categories,
    save_goals,
    save_results,
    save_stages,
    save_users,
)
from utils import input_date, input_int, input_str


def menu_add_goal(
    goals: list[Goal], categories: list[Category]
) -> None:
    """Сценарий добавления цели."""
    if not categories:
        print("Сначала добавьте хотя бы одну категорию.")
        return
    title = input_str("Название цели: ")
    description = input_str("Описание: ")
    show_categories(categories)
    category_id = input_int("ID категории: ")
    category = next(
        (c for c in categories if c.id == category_id), None
    )
    if category is None:
        print("Категория не найдена.")
        return
    priority = input_int(
        "Приоритет (1 — высокий, 2 — средний, 3 — низкий): ",
        min_value=1, max_value=3,
    )
    deadline = input_date("Дедлайн (ДД.ММ.ГГГГ): ")
    created = datetime.now().strftime("%Y-%m-%d")
    add_goal(goals, title, description, category, priority,
             created, deadline)
    print("Цель добавлена.")


def menu_add_user(users: list[User]) -> None:
    """Сценарий добавления пользователя."""
    name = input_str("Имя: ")
    email = input_str("Email: ")
    add_user(users, name, email)
    print("Пользователь добавлен.")


def menu_add_category(categories: list[Category]) -> None:
    """Сценарий добавления категории."""
    name = input_str("Название категории: ")
    add_category(categories, name)
    print("Категория добавлена.")


def menu_add_stage(
    stages: list[Stage], goals: list[Goal]
) -> None:
    """Сценарий добавления этапа."""
    if not goals:
        print("Сначала добавьте хотя бы одну цель.")
        return
    show_goals(goals)
    goal_id = input_int("ID цели: ")
    goal = find_goal_by_id(goals, goal_id)
    if goal is None:
        print("Цель не найдена.")
        return
    title = input_str("Название этапа: ")
    add_stage(stages, title, goal)
    print("Этап добавлен.")


def menu_complete_stage(
    stages: list[Stage], goals: list[Goal]
) -> None:
    """Сценарий отметки этапа выполненным."""
    show_stages(stages)
    stage_id = input_int("ID этапа: ")
    if complete_stage(stages, stage_id):
        stage = next(s for s in stages if s.id == stage_id)
        new_progress = get_goal_progress_from_stages(
            stages, stage.goal.id
        )
        stage.goal.update_progress(new_progress)
        print(f"Этап выполнен. Прогресс цели: {new_progress}%")
    else:
        print("Этап не найден.")


def menu_add_result(
    results: list[Result], goals: list[Goal]
) -> None:
    """Сценарий добавления результата."""
    if not goals:
        print("Сначала добавьте хотя бы одну цель.")
        return
    show_goals(goals)
    goal_id = input_int("ID цели: ")
    goal = find_goal_by_id(goals, goal_id)
    if goal is None:
        print("Цель не найдена.")
        return
    description = input_str("Описание результата: ")
    add_result(results, description, goal)
    print("Результат добавлен.")


def menu_mark_result(
    results: list[Result], goals: list[Goal]
) -> None:
    """Сценарий отметки результата достигнутым."""
    show_results(results)
    result_id = input_int("ID результата: ")
    if mark_result_achieved(results, result_id):
        print("Результат отмечен как достигнутый.")
    else:
        print("Результат не найден.")


def menu_search_goals(goals: list[Goal]) -> None:
    """Сценарий поиска целей по названию."""
    query = input_str("Подстрока для поиска: ")
    found = find_goals_by_title(goals, query)
    if not found:
        print("Ничего не найдено.")
        return
    show_goals(found)


def menu_filter_by_category(
    goals: list[Goal], categories: list[Category]
) -> None:
    """Сценарий фильтрации по категории."""
    show_categories(categories)
    category_id = input_int("ID категории: ")
    show_goals(filter_goals_by_category(goals, category_id))


def menu_show_sorted(goals: list[Goal]) -> None:
    """Сценарий вывода целей по дедлайну."""
    show_goals(sort_goals_by_deadline(goals))


def menu_show_statistics(goals: list[Goal]) -> None:
    """Сценарий вывода статистики."""
    stats = get_statistics(goals)
    print(f"Всего целей:       {stats['total']}")
    print(f"Выполнено:         {stats['completed']}")
    print(f"Средний прогресс:  {stats['average_progress']}%")


def menu_show_stages_for_goal(stages: list[Stage]) -> None:
    """Сценарий показа этапов конкретной цели."""
    goal_id = input_int("ID цели: ")
    found = find_stages_by_goal(stages, goal_id)
    if not found:
        print("Этапы не найдены.")
        return
    show_stages(found)


def menu_show_results_for_goal(results: list[Result]) -> None:
    """Сценарий показа результатов конкретной цели."""
    goal_id = input_int("ID цели: ")
    found = find_results_by_goal(results, goal_id)
    if not found:
        print("Результаты не найдены.")
        return
    show_results(found)


def main() -> None:
    """Точка запуска: главное меню приложения."""
    users = load_users()
    categories = load_categories()
    goals = load_goals(categories)
    stages = load_stages(goals)
    results = load_results(goals)

    while True:
        print()
        print("=" * 40)
        print("СИСТЕМА ОТСЛЕЖИВАНИЯ ЦЕЛЕЙ")
        print("=" * 40)
        print("1.  Показать пользователей")
        print("2.  Добавить пользователя")
        print("3.  Показать категории")
        print("4.  Добавить категорию")
        print("5.  Показать все цели")
        print("6.  Добавить цель")
        print("7.  Найти цель по названию")
        print("8.  Показать цели по категории")
        print("9.  Показать цели (сортировка по дедлайну)")
        print("10. Показать только выполненные")
        print("11. Показать статистику")
        print("12. Показать этапы")
        print("13. Добавить этап")
        print("14. Отметить этап выполненным")
        print("15. Показать результаты")
        print("16. Добавить результат")
        print("17. Отметить результат достигнутым")
        print("0.  Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_users(users)
        elif choice == "2":
            menu_add_user(users)
        elif choice == "3":
            show_categories(categories)
        elif choice == "4":
            menu_add_category(categories)
        elif choice == "5":
            show_goals(goals)
        elif choice == "6":
            menu_add_goal(goals, categories)
        elif choice == "7":
            menu_search_goals(goals)
        elif choice == "8":
            menu_filter_by_category(goals, categories)
        elif choice == "9":
            menu_show_sorted(goals)
        elif choice == "10":
            show_goals(filter_goals_by_status(goals, True))
        elif choice == "11":
            menu_show_statistics(goals)
        elif choice == "12":
            menu_show_stages_for_goal(stages)
        elif choice == "13":
            menu_add_stage(stages, goals)
        elif choice == "14":
            menu_complete_stage(stages, goals)
        elif choice == "15":
            menu_show_results_for_goal(results)
        elif choice == "16":
            menu_add_result(results, goals)
        elif choice == "17":
            menu_mark_result(results, goals)
        elif choice == "0":
            save_users(users)
            save_categories(categories)
            save_goals(goals)
            save_stages(stages)
            save_results(results)
            print("Данные сохранены. До свидания!")
            break
        else:
            print("Неверный пункт меню. Попробуйте снова.")


if __name__ == "__main__":
    main()
