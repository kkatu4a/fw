from datetime import datetime, timedelta

goal_title = "Выучить Django"
goal_description = "Завершить курс по бэкенд-разработке"
priority = 1
days_to_complete = 14

today = datetime.now().date()
deadline = today + timedelta(days=days_to_complete)

progress_percent = 25
is_completed = False

def get_priority_label(priority_value):
    if priority_value == 1:
        return "Высокий"
    elif priority_value == 2:
        return "Средний"
    elif priority_value == 3:
        return "Низкий"
    else:
        return "Неизвестно"

def get_progress_status(percent):
    if percent == 100:
        return "Цель достигнута"
    elif percent >= 75:
        return "Почти готово!"
    elif percent >= 50:
        return "Половина пути сделана"
    elif percent >= 25:
        return "Продолжайте"
    else:
        return "Начало"

print("Система отслеживания целей")

print(f"Цель: {goal_title}")
print(f"Описание: {goal_description}")
print(f"Приоритет: {get_priority_label(priority)}")
print(f"Дедлайн: {deadline}")
print(f"Дней осталось: {days_to_complete}")
print("-" * 40)

print(f"Прогресс: {progress_percent}%")
print(get_progress_status(progress_percent))