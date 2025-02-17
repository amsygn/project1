import os
from json import JSONDecodeError

import requests
import json

from dotenv import load_dotenv
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
            print("Нет данных")
            return []

    except json.JSONDecodeError:
        print("Невозможно обработать данные")
        return []
    except Exception as e:
        print(f"Ошибка чтения данных: {e}")
        return []


def convert_operations(data):
    """ Возвращает сумму транзакции в рублях, при необходимости с конвертацией валюты через API внешнего сервиса """
    load_dotenv(".env")
    apikey = os.getenv("API_KEY")
    headers = {"apikey": apikey}

    with open(data, 'r', encoding='utf-8') as file:
        try:
            operations = json.load(file)  # Загружаем данные из файла
        except JSONDecodeError:
            return []

    results = []

    for op in operations:
        op_id = op["id"]
        op_code = op["operationAmount"]["currency"]["code"]
        op_amount = op["operationAmount"]["amount"]

        if op_code == "RUB":
            results.append({"id": op_id, "amount_rub": op_amount})  # Добавляем сумму в рублях
        else:
            # Конвертируем валюту в рубли через API
            url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={op_code}&amount={op_amount}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                results.append({"id": op_id, "amount_rub": result["result"]})  # Добавляем конвертированную сумму
            else:
                results.append({"id": op_id, "error": "Не удалось конвертировать"})  # Обработка ошибки API

    return results



# Пример использования get_file
# opers = get_file('operations.json')
# print(opers)

# Пример использования convert_operations
result = convert_operations(get_file("operations.json"))
print(result)
