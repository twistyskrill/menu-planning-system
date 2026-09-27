from menu_planning.models import User


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.user_id == user_id:
            return user

    return None


def find_user_by_name(users: list[User], name: str) -> User | None:
    """Найти пользователя по имени."""
    for user in users:
        if user.name.lower() == name.lower():
            return user

    return None
