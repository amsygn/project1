import os
import requests
from dotenv import load_dotenv

transaction_rub = {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"
}
transaction_usd = {
    "id": 41428829,
    "state": "EXECUTED",
    "date": "2019-07-03T18:35:29.512364",
    "operationAmount": {
      "amount": "8221.37",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Перевод организации",
    "from": "MasterCard 7158300734726758",
    "to": "Счет 35383033474447895560"
}


def convert_to_rub(transaction):
    """ Конвертирует сумму транзакции в рубли. """
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    API_URL = "https://api.apilayer.com/exchangerates_data/convert"

    amount = transaction["operationAmount"]["amount"]
    currency = transaction["operationAmount"]["currency"]["code"]

    # Если валюта уже в рублях, возвращаем сумму без изменений
    if currency == "RUB":
        return round(float(amount), 2)

    # Параметры запроса к API
    params = {
        "to": "RUB",
        "from": currency,
        "amount": amount,
    }
    headers = {
        "apikey": API_KEY,
    }

    try:
        # Выполняем запрос к API
        response = requests.get(API_URL, params=params, headers=headers)
        response.raise_for_status()  # Проверяем, что запрос успешен

        # Получаем результат конвертации
        result = response.json()
        if "result" not in result:
            raise ValueError("Некорректный ответ от API.")

        return round(float(result["result"]), 2)

    except requests.exceptions.RequestException as e:
        # Обрабатываем ошибки запроса
        raise RuntimeError(f"Ошибка при запросе к API: {e}")

    except (KeyError, ValueError) as e:
        # Обрабатываем ошибки в данных
        raise ValueError(f"Ошибка при обработке данных: {e}")


# Пример использования convert_to_rub для RUB и USD
# result_ = convert_to_rub(transaction_rub)
# print(result_)
# result_ = convert_to_rub(transaction_usd)
# print(result_)
