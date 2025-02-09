import json
import os
from config import DATA_DIR


def get_file(file_name: str):
    """ Забирает список операций из JSON-файла и выводит его в консоль """
    file_path = os.path.join(DATA_DIR, file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            return data
        else:
            return []

    except json.JSONDecodeError:
        # Если файл пустой или содержит некорректный JSON
        return []
    except Exception as e:
        # Обработка других возможных исключений
        print(f"Ошибка чтения данных: {e}")
        return []

# Пример использования
opers = get_file('operations.json')
print(opers)