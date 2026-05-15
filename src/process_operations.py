import os
import re
import json
from typing import List, Dict, Any
from collections import Counter
from config import DATA_DIR
# from tests.conftest import transactions

# Определяем адрес файла с данными относительно текущего файла
OPERATIONS_FILE_PATH = os.path.join(DATA_DIR, 'operations.json')


def load_operations() -> List[Dict[str, Any]]:
    """Загружает список операций из файла operations.json"""
    try:
        with open(OPERATIONS_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Фильтруем пустые словари, как в исходных данных
            return [item for item in data if item]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {OPERATIONS_FILE_PATH}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Файл содержит некорректный JSON: {e}")


def filter_transactions_by_description(
        transactions: List[Dict[str, Any]],
        search_string: str
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по наличию строки в описании, используя регулярные выражения,
    и возвращает список словарей, у которых в описании есть искомая строка
    """

    if not search_string or not search_string.strip():
        raise ValueError("Строка поиска не может быть пустой")

    try:
        pattern = re.compile(re.escape(search_string), re.IGNORECASE)

        # Формируем список отфильтрованных транзакций
        result = [
            trans for trans in transactions
            if isinstance(trans, dict) and  # проверка, что транзакция - словарь
               'description' in trans and  # проверка наличия ключа description
               isinstance(trans['description'], str) and  # проверка, что описание - строка
               pattern.search(trans['description'])  # поиск подстроки в описании
        ]

        return result

    except re.error as e:
        raise ValueError(f"Ошибка в регулярном выражении: {e}")


def count_operations_by_categories(
        transactions: List[Dict[str, Any]],
        categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество банковских операций по заданным категориям.
    """

    if not transactions:
        return {category: 0 for category in categories}

    if not categories:
        return {}

    counter = Counter()

    # Проходим по каждой транзакции
    for transaction in transactions:
        # Пропускаем некорректные транзакции
        if not isinstance(transaction, dict):
            continue

        # Получаем описание транзакции
        description = transaction.get('description', '')

        if not isinstance(description, str):
            continue

        # Проверяем каждую категорию
        for category in categories:
            if re.search(re.escape(category), description, re.IGNORECASE):
                counter[category] += 1

    # Возвращаем словарь со всеми категориями, включая нулевые значения
    return {category: counter.get(category, 0) for category in categories}


# Проверка
# categories = ["Перевод", "Открытие вклада", "Оплата", "Карта"]
# print(count_operations_by_categories(load_operations(), categories))

# print(*filter_transactions_by_description(load_operations(), "Перевод"), sep="\n")
