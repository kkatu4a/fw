"""Модель пользователя системы."""

from typing import Optional


class User:
    """Пользователь — владелец целей."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Создать объект пользователя."""
        self.id = user_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        """Вернуть строковое представление пользователя."""
        return f"User #{self.id}: {self.name} <{self.email}>"

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из словаря."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def to_data(self) -> dict:
        """Преобразовать пользователя в словарь."""
        return {"id": self.id, "name": self.name, "email": self.email}


def add_user(users: list[User], name: str, email: str) -> User:
    """Создать пользователя и добавить его в коллекцию."""
    new_id = max((u.id for u in users), default=0) + 1
    user = User(new_id, name, email)
    users.append(user)
    return user


def find_user_by_id(users: list[User], user_id: int) -> Optional[User]:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_users_by_name(users: list[User], query: str) -> list[User]:
    """Найти пользователей по подстроке имени."""
    q = query.lower()
    return [u for u in users if q in u.name.lower()]


def show_users(users: list[User]) -> None:
    """Вывести список пользователей."""
    if not users:
        print("Список пользователей пуст.")
        return
    for user in users:
        print(f"  {user}")
