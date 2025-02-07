# Домашняя работа 11.1 #
### Цель проекта:
Разработка виджета для банка

### Установка и запуск проекта:
1. Клонировать проект **Homework 11.1** на локальный компьютер.
2. Активировать интерпретатор *Poetry* в проекте командой `poetry init`.
3. В случае его отсутствия выполнить установку необходимых пакетов через менеджер загрузок `pipx` 
из списка зависимостей в файле `pyproject.toml` или скачать его с [сайта разработчика](https://python-poetry.org/docs/#installation/).


### Содержание проекта:
В текущей версии в модуле `src` доступны следующие функции (в алфавитном порядке):
`card_number_generator` - генератор номеров карт в заданном диапазоне
`filter_by_currency` - сортировка данных по коду валюты 
`filter_by_state` - сортировка данных по статусу транзакции 
`get_date` - переформатирует дату события
`get_mask_account` - маскировка номера счета
`get_mask_card_number` - маскировка номера карты
`mask_account_card` - объединенная функция маскировки номера карты или счета
`sort_by_date` - сортировка данных по дате транзакции
`transaction_descriptions` - вывод описания транзакций

### Примеры работы функций:

`filter_by_state`
```
### Sorted by status:
Default: EXECUTED
{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
```

`sort_by_date`
```
### Sorted by date:
{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
{'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
```

`transaction_descriptions`
```
{"id": 142264268,
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
"to": "Счет 75651667383060284188"}
```

### Тестирование проекта
Проект содержит тесты всех модулей в папке `tests`.
Статистика по покрытию согласно отчету `pytest-cov`:
```
---------- coverage: platform win32, python 3.13.0-final-0 -----------
Name                       Stmts   Miss  Cover
----------------------------------------------
src\__init__.py                0      0   100%
src\generators.py             13      0   100%
src\masks.py                   8      0   100%
src\processing.py             12      0   100%
src\widget.py                 11      0   100%
tests\__init__.py              0      0   100%
tests\conftest.py              4      0   100%
tests\test_generators.py      19      0   100%
tests\test_masks.py            6      0   100%
tests\test_processing.py      21      1    95%
tests\test_widget.py          17      0   100%
----------------------------------------------
TOTAL                        111      1    99%
```

