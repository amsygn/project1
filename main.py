from src.file_reader_csv_xlsx import read_excel, read_csv
from src.generators import filter_by_currency
from src.process_operations import filter_transactions_by_description
from src.utils import get_file
from src.processing import filter_by_state, sort_by_date


def format_transaction(transaction):
    """Форматирует одну транзакцию для вывода"""
    # Извлекаем дату и форматируем её
    date = transaction.get("date", "")
    if " " in date:
        date = date.split("T")[0]  # Берём только дату
    date_parts = date.split("-")
    if len(date_parts) == 3:
        date = f"{date_parts[2]}.{date_parts[1]}.{date_parts[0]}"

    description = transaction.get("description", "Нет описания")

    # Форматируем информацию о карте/счёте
    from_account = transaction.get("from", "Счет")
    to_account = transaction.get("to", "")
    if from_account and to_account:
        account_info = f"{from_account} -> {to_account}"
    elif from_account:
        account_info = from_account
    else:
        account_info = to_account

    # Сумма и валюта
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

    # Выбор типа файла
    while True:
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        user_choice = input("Введите цифру: ").strip()

        if user_choice == "1":
            file_json_path = 'operations.json'
            transactions = get_file(file_json_path)
            print("Для обработки выбран JSON-файл.")
            break
        elif user_choice == "2":
            file_csv_path: str = 'transactions.csv'
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

    # Фильтрация по статусу
    while True:
        print("\nВыберите статус, по которому необходимо выполнить фильтрацию.")
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        user_status_choice = input("Введите статус: ").upper().strip()

        if user_status_choice in ['EXECUTED', 'CANCELED', 'PENDING']:
            status_filter = user_status_choice
            ft = filter_by_state(transactions, status_filter)
            print(f'Операции отфильтрованы по статусу "{status_filter}"')
            break
        else:
            print(f'Статус операции "{user_status_choice}" недоступен.')
            continue

    # Сортировка по дате
    sort_choice = input("\nОтсортировать операции по дате? Да/Нет\n").strip().lower()

    if sort_choice == 'да':
        order_choice = input('Отсортировать по возрастанию (1) или по убыванию (2)?\nВведите цифру: ').strip().lower()
        if order_choice == '1':
            ft = sort_by_date(ft, reverse=False)
            print("Операции отсортированы по возрастанию даты")
        elif order_choice == '2':
            ft = sort_by_date(ft, reverse=True)
            print("Операции отсортированы по убыванию даты")
        else:
            print("Некорректный ввод, сортировка не применена")

    # Фильтрация по валюте
    currency_choice = input("\nВыводить только рублевые транзакции? Да/Нет\n").strip().lower()

    if currency_choice == "да":
        if user_choice in ['2', '3']:
            ft = [t for t in ft if t.get("currency_code") == 'RUB']
        elif user_choice == '1':
            ft = list(filter_by_currency(ft, 'RUB'))
        print("Выбраны только рублёвые транзакции")
    else:
        print("Рублёвая фильтрация не применена")

    # Фильтрация по слову в описании
    word_filter_choice = input(
        "\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет\n").strip().lower()

    if word_filter_choice == 'да':
        filter_word = input('Введите слово:\n').strip()
        ft = filter_transactions_by_description(ft, filter_word)
        print(f"Транзакции отфильтрованы по слову '{filter_word}'")
    else:
        print("Фильтрация по слову не применена")

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...")

    if not ft:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
    else:
        print(f"Всего банковских операций в выборке: {len(ft)}\n")
        # for transaction in ft:
        #     print(format_transaction(transaction))
        #     print()


if __name__ == "__main__":
    main()
