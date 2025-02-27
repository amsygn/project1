import json
import os

from config import DATA_DIR


def get_file(file_name: str) -> list:
    """Забирает список операций из JSON-файла и выводит его в консоль"""
    file_path = os.path.join(DATA_DIR, file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            return data
        else:
            print("Нет данных")
            return []


    except FileNotFoundError:
        print(f"Файл {file_name} не найден")
        return []
    except json.JSONDecodeError:
        print("Невозможно обработать данные")
        return []
    except Exception as e:
        print(f"Ошибка чтения данных: {e}")
        return []
