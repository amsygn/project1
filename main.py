from datetime import datetime

from src.file_reader_csv_xlsx import read_csv, read_excel
from src.generators import filter_by_currency
from src.process_operations import filter_transactions_by_description
from src.processing import filter_by_state, sort_by_date
from src.utils import get_file


def parse_dates_in_transactions(transactions):
    """Функция преобразует строки с датами в объекты datetime для всех транзакций"""
    for transaction in transactions:
        date_str = transaction.get("date", "")
        if date_str:
            try:
                if "Z" in date_str:
                    transaction["date"] = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                elif "." in date_str:
                    transaction["date"] = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    transaction["date"] = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            except (ValueError, TypeError):
                pass
    return transactions


def format_transaction(transaction):
    """Форматирует одну транзакцию для вывода"""
    date_obj = transaction.get("date", "")

    if isinstance(date_obj, datetime):
        date = date_obj.strftime("%d.%m.%Y")
    else:
        date_str = str(date_obj)
        date = date_str[:10] if len(date_str) >= 10 else date_str
        if "-" in date:
            parts = date.split("-")
            if len(parts) == 3:
                date = f"{parts[2]}.{parts[1]}.{parts[0]}"

    description = transaction.get("description", "Нет описания")

    from_account = transaction.get("from", "Счет")
    to_account = transaction.get("to", "")
    if from_account and to_account:
        account_info = f"{from_account} -> {to_account}"
    elif from_account:
        account_info = from_account
    else:
        account_info = to_account

    amount = transaction.get("amount", 0)
    currency = transaction.get("currency", {}).get("name", "руб.")
    currency_code = transaction.get("currency", {}).get("code", "RUB")

    if currency_code == "RUB" or currency == "руб.":
        currency_str = "руб."
    elif currency_code == "USD":
        currency_str = "USD"
    elif currency_code == "EUR":
        currency_str = "EUR"
    else:
        currency_str = currency_code

    return f"{date} {description}\n{account_info}\nСумма: {amount} {currency_str}"


def main():
    """Основная функция, объединяющая функционал разных модулей"""

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Выбор файла-источника
    while True:
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        user_choice = input("Ваш выбор: ").strip()

        if user_choice == "1":
            file_json_path = 'operations.json'
            transactions = get_file(file_json_path)
            print("Для обработки выбран JSON-файл.")
            break
        elif user_choice == "2":
            file_csv_path = 'transactions.csv'
            transactions = read_csv(file_csv_path, delimiter=";")
            print("Для обработки выбран CSV-файл.")
            break
        elif user_choice == "3":
            file_excel_path = 'transactions_excel.xlsx'
            transactions = read_excel(file_excel_path)
            print("Для обработки выбран XLSX-файл.")
            break
        else:
            print(f'Данный выбор "{user_choice}" недоступен')
            continue

    # Формат даты транзакции
    transactions = parse_dates_in_transactions(transactions)

    filter_transactions = []
    # Фильтрация по статусу
    while True:
        print("\nВыберите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        user_status_choice = input("Ваш выбор: ").upper().strip()

        if user_status_choice in ['EXECUTED', 'CANCELED', 'PENDING']:
            status_filter = user_status_choice
            filter_transactions = filter_by_state(transactions, status_filter)
            print(f'Операции отфильтрованы по статусу "{status_filter}"')
            break
        else:
            print(f'Статус операции "{user_status_choice}" недоступен.')
            continue

    # Сортировка по дате
    sort_choice = input("\nОтсортировать операции по дате? Да (1) / Нет (2)\nВаш выбор: ").strip().lower()

    if sort_choice == '1':
        order_choice = input('Отсортировать по возрастанию (1) или по убыванию (2)?\nВаш выбор: ').strip().lower()
        if order_choice == '1':
            filter_transactions = sort_by_date(filter_transactions, reverse=False)
            print("Операции отсортированы по возрастанию даты")
        elif order_choice == '2':
            filter_transactions = sort_by_date(filter_transactions, reverse=True)
            print("Операции отсортированы по убыванию даты")
        else:
            print("Некорректный ввод, сортировка не применена")

    # Фильтрация по валюте
    currency_choice = input("\nВыводить только рублевые транзакции? Да (1) / Нет (2)\nВаш выбор: ").strip().lower()

    if currency_choice == "1":
        if user_choice in ['2', '3']:
            filter_transactions = [t for t in filter_transactions if t.get("currency_code") == 'RUB']
        elif user_choice == '1':
            filter_transactions = list(filter_by_currency(filter_transactions, 'RUB'))
        print("Выбраны только рублёвые транзакции")
    else:
        print("Рублёвая фильтрация не применена")

    # Фильтрация по слову в описании
    word_filter_choice = input(
        "\nОтфильтровать список транзакций по определенному слову в описании? "
        "Да (1) / Нет (2)\nВаш выбор: ").strip().lower()

    if word_filter_choice == '1':
        filter_word = input('Введите слово: ').strip()
        filter_transactions = filter_transactions_by_description(filter_transactions, filter_word)
        print(f"Транзакции отфильтрованы по слову '{filter_word}'")
    else:
        print("Фильтрация по слову не применена")

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")

    if not filter_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print(f"Всего банковских операций в выборке: {len(filter_transactions)}\n")
        for transaction in filter_transactions:
            print(format_transaction(transaction))
            print()


if __name__ == "__main__":
    main()
