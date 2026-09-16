import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> list[dict[str, Any]]:
    """Загрузить данные из JSON-файла."""
    file_path = Path(path)

    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    if isinstance(data, list):
        return data
    return []


def save_json(path: str, data: list[dict[str, Any]]) -> None:
    """Сохранить данные в JSON-файл."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
