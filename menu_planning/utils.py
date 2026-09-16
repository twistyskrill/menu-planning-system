def input_int(prompt: str) -> int:
    """Запросить целое число у пользователя."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите число.")
