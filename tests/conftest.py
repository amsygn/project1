import pytest


@pytest.fixture
def transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "RUR",
                    "code": "RUR"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 144264270,
            "state": "EXECUTED",
            "date": "2019-05-09T13:25:50.2063998",
            "operationAmount": {
                "amount": "23444.03",
                "currency": {
                    "name": "RUR",
                    "code": ""},
            },
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]
