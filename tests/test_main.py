import pytest
from datetime import datetime
from unittest.mock import patch

from main import parse_dates_in_transactions, format_transaction, main


def test_parse_dates_with_z_format():
    """Тест: парсинг даты с форматом Z (UTC)"""
    transactions = [
        {"id": 1, "date": "2025-12-08T18:00:00Z", "description": "Test"}
    ]

    result = parse_dates_in_transactions(transactions)

    assert isinstance(result[0]["date"], datetime)
    assert result[0]["date"].year == 2025
    assert result[0]["date"].month == 12
    assert result[0]["date"].day == 8
    assert result[0]["date"].hour == 18
    assert result[0]["date"].minute == 0


def test_parse_dates_with_milliseconds():
    """Тест: парсинг даты с миллисекундами (ветка elif)"""
    transactions = [
        {"id": 1, "date": "2025-12-08T18:00:00.123456", "description": "Test"}
    ]

    result = parse_dates_in_transactions(transactions)

    assert isinstance(result[0]["date"], datetime)
    assert result[0]["date"].year == 2025
    assert result[0]["date"].month == 12
    assert result[0]["date"].day == 8
    assert result[0]["date"].microsecond == 123456


def test_parse_dates_without_milliseconds():
    """Тест: парсинг даты без миллисекунд и без Z (ветка else)"""
    transactions = [
        {"id": 1, "date": "2025-12-08T18:00:00", "description": "Test"}
    ]

    result = parse_dates_in_transactions(transactions)

    assert isinstance(result[0]["date"], datetime)
    assert result[0]["date"].year == 2025
    assert result[0]["date"].month == 12
    assert result[0]["date"].day == 8


def test_parse_dates_handles_value_error():
    """Тест: обработка ValueError (ошибка парсинга)"""
    transactions = [
        {"id": 1, "date": "invalid-date-format", "description": "Test"}
    ]

    # Функция не должна выбрасывать исключение
    result = parse_dates_in_transactions(transactions)

    # Дата должна остаться исходной строкой
    assert result[0]["date"] == "invalid-date-format"


def test_parse_dates_multiple_transactions():
    """Тест: несколько транзакций с разными форматами"""
    transactions = [
        {"id": 1, "date": "2025-12-08T18:00:00Z"},
        {"id": 2, "date": "2020-01-01T10:00:00.123456"},
        {"id": 3, "date": "2021-02-15T09:30:00"},
        {"id": 4, "date": "bad-date"},
        {"id": 5},  # нет даты
    ]

    result = parse_dates_in_transactions(transactions)

    assert isinstance(result[0]["date"], datetime)
    assert isinstance(result[1]["date"], datetime)
    assert isinstance(result[2]["date"], datetime)
    assert result[3]["date"] == "bad-date"
    assert "date" not in result[4] or result[4].get("date") == ""


def test_parse_dates_empty_list():
    """Тест: пустой список транзакций"""
    result = parse_dates_in_transactions([])

    assert result == []


def test_parse_dates_with_exception_handling():
    """Тест: проверка блока except через mock"""
    with patch('main.datetime') as mock_datetime:
        # Заставляем datetime.strptime выбросить исключение
        mock_datetime.strptime.side_effect = ValueError("Test error")

        transactions = [
            {"id": 1, "date": "2020-01-01T10:00:00Z", "description": "Test"}
        ]

        # Функция не должна выбросить исключение
        result = parse_dates_in_transactions(transactions)

        # Дата осталась исходной строкой
        assert result[0]["date"] == "2020-01-01T10:00:00Z"


def test_format_transaction_with_datetime():
    """Тест: форматирование транзакции с объектом datetime"""
    transaction = {
        "date": datetime(2026, 5, 8, 18, 0, 0),
        "description": "Открытие вклада",
        "from": "Счет",
        "to": "Счет 4321",
        "amount": 40542,
        "currency": {"name": "руб.", "code": "RUB"}
    }

    result = format_transaction(transaction)

    expected = "08.05.2026 Открытие вклада\nСчет -> Счет 4321\nСумма: 40542 руб."
    assert result == expected


def test_format_transaction_with_string_date():
    """Тест: форматирование транзакции со строковой датой"""
    transaction = {
        "date": "2026-05-08T18:00:00Z",
        "description": "Перевод с карты на карту",
        "from": "MasterCard 7771 27** **** 3727",
        "to": "Visa Platinum 1293 38** **** 9203",
        "amount": 130,
        "currency": {"name": "USD", "code": "USD"}
    }

    result = format_transaction(transaction)

    expected = "08.05.2026 Перевод с карты на карту\nMasterCard 7771 27** **** 3727 -> Visa Platinum 1293 38** **** 9203\nСумма: 130 USD"
    assert result == expected


def test_format_transaction_missing_fields():
    """Тест: форматирование транзакции с отсутствующими полями"""
    transaction = {
        "date": "2020-01-01T10:00:00Z",
        "amount": 1000
    }

    result = format_transaction(transaction)

    assert "Нет описания" in result
    assert "Сумма: 1000 руб." in result


# тесты для main

@patch('builtins.print')
@patch('builtins.input')
@patch('main.get_file')
def test_main_empty_result(mock_get_file, mock_input, mock_print):
    """Тест: пустой результат после фильтрации"""
    mock_get_file.return_value = []

    mock_input.side_effect = [
        "1",  # Выбор JSON
        "EXECUTED",  # Статус
        "2",  # Не сортировать
        "2",  # Не фильтровать по валюте
        "2",  # Не фильтровать по слову
    ]

    main()

    # Проверяем сообщение о пустом результате
    empty_result_found = False
    for call in mock_print.call_args_list:
        if "Не найдено ни одной транзакции" in str(call):
            empty_result_found = True
            break

    assert empty_result_found


@patch('builtins.print')
@patch('builtins.input')
@patch('main.get_file')
def test_main_invalid_status_then_valid(mock_get_file, mock_input, mock_print):
    """Тест: сначала неверный статус, потом верный"""
    mock_get_file.return_value = [
        {"id": 1, "date": "2020-01-01T10:00:00Z", "state": "EXECUTED", "description": "Test"}
    ]

    mock_input.side_effect = [
        "1",  # Выбор JSON
        "INVALID",  # Неверный статус
        "EXECUTED",  # Верный статус
        "2",  # Не сортировать
        "2",  # Не фильтровать по валюте
        "2",  # Не фильтровать по слову
    ]

    main()

    # Проверяем сообщение о неверном статусе
    error_found = False
    for call in mock_print.call_args_list:
        if 'Статус операции "INVALID" недоступен' in str(call):
            error_found = True
            break

    assert error_found


# ==================== ЗАПУСК ТЕСТОВ ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])