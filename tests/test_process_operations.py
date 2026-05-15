import pytest

from src.process_operations import count_operations_by_categories, filter_transactions_by_description

# Тесты для функции filter_transactions_by_description

def test_search_found():
    """Поиск существующей строки."""
    transactions = [{"description": "Перевод организации"}]
    result = filter_transactions_by_description(transactions, "Перевод")
    assert len(result) == 1


def test_search_not_found():
    """Поиск отсутствующей строки."""
    transactions = [{"description": "Перевод организации"}]
    result = filter_transactions_by_description(transactions, "Вклад")
    assert len(result) == 0


def test_search_case_insensitive():
    """Регистронезависимый поиск."""
    transactions = [{"description": "ПЕРЕВОД"}]
    result = filter_transactions_by_description(transactions, "перевод")
    assert len(result) == 1


def test_search_empty_string():
    """Пустая строка поиска вызывает ошибку."""
    with pytest.raises(ValueError):
        filter_transactions_by_description([{"description": "test"}], "")


def test_search_empty_transactions():
    """Пустой список транзакций."""
    result = filter_transactions_by_description([], "test")
    assert result == []


def test_search_missing_description():
    """Транзакция без ключа description."""
    transactions = [{"id": 1}, {"description": "Перевод"}]
    result = filter_transactions_by_description(transactions, "Перевод")
    assert len(result) == 1


def test_search_special_characters():
    """Поиск со специальными символами."""
    transactions = [{"description": "Перевод (срочный)"}]
    result = filter_transactions_by_description(transactions, "(срочный)")
    assert len(result) == 1


# Тесты для функции count_operations_by_categories


def test_count_single_category():
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты"},
    ]
    result = count_operations_by_categories(transactions, ["Перевод"])
    assert result["Перевод"] == 2


def test_count_multiple_categories():
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
        {"description": "Перевод с карты"},
        {"description": "Оплата услуг"},
    ]
    categories = ["Перевод", "Вклад", "Оплата"]
    result = count_operations_by_categories(transactions, categories)
    assert result["Перевод"] == 2
    assert result["Вклад"] == 1
    assert result["Оплата"] == 1


def test_count_case_insensitive():
    transactions = [
        {"description": "ПЕРЕВОД организации"},
        {"description": "перевод с карты"},
    ]
    result = count_operations_by_categories(transactions, ["Перевод"])
    assert result["Перевод"] == 2


def test_count_empty_transactions():
    result = count_operations_by_categories([], ["Перевод"])
    assert result["Перевод"] == 0


def test_count_empty_categories():
    transactions = [{"description": "Перевод"}]
    result = count_operations_by_categories(transactions, [])
    assert result == {}


def test_count_category_not_found():
    transactions = [{"description": "Перевод"}]
    result = count_operations_by_categories(transactions, ["Вклад"])
    assert result["Вклад"] == 0


def test_count_with_invalid_transactions():
    transactions = [
        {},
        {"description": "Перевод"},
        None,
        "not a dict",
        {"description": "Оплата"},
    ]
    result = count_operations_by_categories(transactions, ["Перевод", "Оплата"])
    assert result["Перевод"] == 1
    assert result["Оплата"] == 1
