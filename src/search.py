import re
import json
import os
from typing import List, Dict, Any
from collections import Counter
from config import DATA_DIR

OPERATIONS_FILE_PATH = os.path.join(DATA_DIR, 'operations.json')


def load_operations() -> List[Dict[str, Any]]:
    """ Загружает список операций из файла operations.json """
    try:
        with open(OPERATIONS_FILE_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден")
    except json.JSONDecodeError:
        raise ValueError(f"Файл содержит некорректный JSON")


def filter_transactions_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """ Фильтрует транзакции по наличию строки в описании, используя регулярные выражения. """
    if not search_string or not search_string.strip():
        raise ValueError("Строка поиска не может быть пустой")

    try:
        pattern = re.compile(re.escape(search_string), re.IGNORECASE)
        return [
            trans for trans in transactions
            if isinstance(trans, dict) and
               'description' in trans and
               isinstance(trans['description'], str) and
               pattern.search(trans['description'])
        ]
    except re.error as e:
        raise ValueError(f"Ошибка в регулярном выражении: {e}")


def count_operations_by_category(operations: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.

    Args:
        operations: Список словарей с банковскими операциями (должен содержать 'description')
        categories: Список категорий для поиска в описаниях операций

    Returns:
        Словарь с количеством операций по каждой категории

    Raises:
        TypeError: Если входные аргументы неверного типа
        ValueError: Если список категорий пуст

    Пример:
        >>> ops = [
        ...     {'description': 'Grocery store', 'amount': 100},
        ...     {'description': 'Pharmacy', 'amount': 50},
        ...     {'description': 'Grocery store', 'amount': 75}
        ... ]
        >>> count_operations_by_category(ops, ['Grocery', 'Pharmacy'])
        {'Grocery': 2, 'Pharmacy': 1}
    """
    # Проверка входных данных
    if not isinstance(operations, list):
        raise TypeError("operations должен быть списком")
    if not isinstance(categories, list):
        raise TypeError("categories должен быть списком")
    if not categories:
        raise ValueError("Список категорий не может быть пустым")

    category_counts = Counter()

    for op in operations:
        if not isinstance(op, dict) or 'description' not in op:
            continue

        description = op['description'].lower()
        for category in categories:
            if category.lower() in description:
                category_counts[category] += 1

    return dict(category_counts)

# Пример использования
if __name__ == "__main__":
    # try:
    #     operations_file = load_operations()
    #     filtered = filter_transactions_by_description(operations_file, "перевод")
    #     print(f"Найдено {len(filtered)} операций\nПримеры:")
    #     for op in filtered[:5]:  # Выводим первые 5 результатов
    #         print(f"  {op['description']}")
    #
    # except Exception as e:
    #     print(f"Ошибка: {e}")

    oper_count = count_operations_by_category(OPERATIONS_FILE_PATH, ["Перевод организации"])
    print(oper_count)

