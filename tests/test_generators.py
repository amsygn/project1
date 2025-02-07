import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

def test_filter_by_currency(transactions):
    assert (next(filter_by_currency(transactions, 'RUR'))) == {
    "id": 142264268,
    "state": "EXECUTED",
    "date": "2019-04-04T23:20:05.206878",
    "operationAmount": {
        "amount": "79114.93",
        "currency": {
            "name": "RUR",
            "code": "RUR"}
        },
    "description": "Перевод со счета на счет",
    "from": "Счет 19708645243227258542",
    "to": "Счет 75651667383060284188"
    }
    assert (next(filter_by_currency(transactions, 'USD'))) == {
        "id": 939719570,
    "state": "EXECUTED",
    "date": "2018-06-30T02:08:58.425572",
    "operationAmount": {
        "amount": "9824.07",
        "currency": {
            "name": "USD",
            "code": "USD"}
        },
    "description": "Перевод организации",
    "from": "Счет 75106830613657916952",
    "to": "Счет 11776614605963066702"
      }

def test_transaction_descriptions(transactions):
    transaction_descr_gen = transaction_descriptions(transactions)
    assert next(transaction_descr_gen) == "Перевод организации"
    assert next(transaction_descr_gen) == "Перевод со счета на счет"


def test_transaction_descriptions_empty(transactions):
    transaction_descr_gen = transaction_descriptions(transactions)
    next(transaction_descr_gen)
    next(transaction_descr_gen)
    with pytest.raises(Exception, match="Нет данных по описанию"):
        next(transaction_descr_gen)


def test_card_number_generator():
    card_num_gen = card_number_generator(10001, 10004)
    assert next(card_num_gen) == "0000 0000 0001 0001"
    assert next(card_num_gen) == "0000 0000 0001 0002"


