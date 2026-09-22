"""Система отслеживания целей. Точка запуска приложения."""

from datetime import datetime
from typing import Optional

from categories import (
    add_category,
    get_category_name,
    sort_categories_by_name,
)
from goals import (
    add_goal,
    complete_goal,
    count_days_left,
    delete_goal,
    filter_goals_by_category,
    filter_goals_by_status,
    find_goal_by_id,
    find_goals_by_title,
    get_goal_status,
    get_priority_label,
    get_statistics,
    sort_goals_by_deadline,
    update_goal_progress,
)
from storage import (
    load_categories,
    load_goals,
    save_categories,
    save_goals,
)
from utils import input_date, input_int, input_progress, input_str


def show_goal(goal: dict, categories: list[dict]) -> None:
    """Вывести информацию о цели."""
    category_name = get_category_name(categories, goal["category_id"])
    days_left = count_days_left(goal["deadline"])
    print(f"  [{goal['id']}] {goal['title']}")
    print(f"      Категория: {category_name}")
    print(f"      Приоритет: {get_priority_label(goal['priority'])}")
    print(f"      Дедлайн:   {goal['deadline']} (дней: {days_left})")
    print(f"      Прогресс:  {goal['progress']}% — {get_goal_status(goal)}")


def show_goals(goals: list[dict], categories: list[dict]) -> None:
    """Вывести список целей."""
    if not goals:
        print("Список целей пуст.")
        return
    for goal in goals:
        show_goal(goal, categories)
        print("-" * 40)


def show_categories(categories: list[dict]) -> None:
    """Вывести список категорий."""
    if not categories:
        print("Список категорий пуст.")
        return
    for category in sort_categories_by_name(categories):
        print(f"  [{category['id']}] {category['name']}")


def show_statistics(goals: list[dict]) -> None:
    """Показать статистику по целям."""
    stats = get_statistics(goals)
    print(f"Всего целей:       {stats['total']}")
    print(f"Выполнено:         {stats['completed']}")
    print(f"Средний прогресс:  {stats['average_progress']}%")


def menu_add_goal(goals: list[dict], categories: list[dict]) -> None:
    """Сценарий добавления цели."""
    if not categories:
        print("Сначала добавьте хотя бы одну категорию.")
        return
    title = input_str("Название цели: ")
    description = input_str("Описание: ")
    show_categories(categories)
    category_id = input_int("ID категории: ")
    priority = input_int("Приоритет (1 — высокий, 2 — средний, 3 — низкий): ",
                         min_value=1, max_value=3)
    deadline = input_date("Дедлайн (ДД.ММ.ГГГГ): ")
    created = datetime.now().strftime("%Y-%m-%d")
    add_goal(goals, title, description, category_id,
             priority, created, deadline)
    print("Цель добавлена.")


def menu_update_progress(goals: list[dict]) -> None:
    """Сценарий обновления прогресса."""
    goal_id = input_int("ID цели: ")
    goal: Optional[dict] = find_goal_by_id(goals, goal_id)
    if goal is None:
        print("Цель не найдена.")
        return
    progress = input_progress("Новый прогресс (0–100): ")
    update_goal_progress(goals, goal_id, progress)
    print("Прогресс обновлён.")


def menu_complete_goal(goals: list[dict]) -> None:
    """Сценарий отметки цели выполненной."""
    goal_id = input_int("ID цели: ")
    if complete_goal(goals, goal_id):
        print("Цель отмечена как выполненная.")
    else:
        print("Цель не найдена.")


def menu_delete_goal(goals: list[dict]) -> None:
    """Сценарий удаления цели."""
    goal_id = input_int("ID цели: ")
    if delete_goal(goals, goal_id):
        print("Цель удалена.")
    else:
        print("Цель не найдена.")


def menu_search_goals(goals: list[dict], categories: list[dict]) -> None:
    """Сценарий поиска целей по названию."""
    query = input_str("Подстрока для поиска: ")
    found = find_goals_by_title(goals, query)
    if not found:
        print("Ничего не найдено.")
        return
    show_goals(found, categories)


def menu_filter_by_category(goals: list[dict], categories: list[dict]) -> None:
    """Сценарий фильтрации по категории."""
    show_categories(categories)
    category_id = input_int("ID категории: ")
    found = filter_goals_by_category(goals, category_id)
    show_goals(found, categories)


def menu_show_sorted(goals: list[dict], categories: list[dict]) -> None:
    """Сценарий вывода целей, отсортированных по дедлайну."""
    show_goals(sort_goals_by_deadline(goals), categories)


def menu_add_category(categories: list[dict]) -> None:
    """Сценарий добавления категории."""
    name = input_str("Название категории: ")
    add_category(categories, name)
    print("Категория добавлена.")


def main() -> None:
    """Точка запуска: главное меню приложения."""
    goals = load_goals()
    categories = load_categories()

    while True:
        print()
        print("=" * 40)
        print("СИСТЕМА ОТСЛЕЖИВАНИЯ ЦЕЛЕЙ")
        print("=" * 40)
        print("1.  Показать все цели")
        print("2.  Добавить цель")
        print("3.  Обновить прогресс")
        print("4.  Отметить цель выполненной")
        print("5.  Удалить цель")
        print("6.  Найти цель по названию")
        print("7.  Показать цели по категории")
        print("8.  Показать цели (сортировка по дедлайну)")
        print("9.  Показать только выполненные")
        print("10. Показать категории")
        print("11. Добавить категорию")
        print("12. Показать статистику")
        print("0.  Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_goals(goals, categories)
        elif choice == "2":
            menu_add_goal(goals, categories)
        elif choice == "3":
            menu_update_progress(goals)
        elif choice == "4":
            menu_complete_goal(goals)
        elif choice == "5":
            menu_delete_goal(goals)
        elif choice == "6":
            menu_search_goals(goals, categories)
        elif choice == "7":
            menu_filter_by_category(goals, categories)
        elif choice == "8":
            menu_show_sorted(goals, categories)
        elif choice == "9":
            show_goals(filter_goals_by_status(goals, True), categories)
        elif choice == "10":
            show_categories(categories)
        elif choice == "11":
            menu_add_category(categories)
        elif choice == "12":
            show_statistics(goals)
        elif choice == "0":
            save_goals(goals)
            save_categories(categories)
            print("Данные сохранены.")
            break
        else:
            print("Неверный пункт меню. Попробуйте снова.")


if __name__ == "__main__":
    main()
