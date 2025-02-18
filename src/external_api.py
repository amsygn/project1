import os
from json import JSONDecodeError

import requests
import json

from dotenv import load_dotenv
from config import DATA_DIR


def convert_operations(file_name: str):
    """ Возвращает сумму транзакции в рублях, при необходимости с конвертацией валюты через API внешнего сервиса """
    load_dotenv()
    apikey = os.getenv("API_KEY")
    headers = {"apikey": apikey}
    file_path = os.path.join(DATA_DIR, file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            operations = json.load(file)  # Загружаем данные из файла
        except JSONDecodeError:
            return []

    op_results = []

    for op in operations:
        op_id = op["id"]
        op_code = op["operationAmount"]["currency"]["code"]
        op_amount = float(op["operationAmount"]["amount"])

        if op_code == "RUB":
            op_results.append({"id": op_id, "amount_rub": round(op_amount, 2)})  # Добавляем сумму в рублях
        else:
            # Конвертируем валюту в рубли через API
            url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={op_code}&amount={op_amount}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                op_results.append({"id": op_id, "amount_rub": round(result["result"], 2)})
            else:
                op_results.append({"id": op_id, "error": response.status_code})

    file_path = os.path.join(DATA_DIR, "operations_rub.json")
    with open(file_path, 'a', encoding='utf-8') as file:
        json.dump(op_results, file, indent=4, ensure_ascii=False)
    return None

# Пример использования convert_operations
# result_ = convert_operations("operations.json")
# print(result_, sep="\n")

