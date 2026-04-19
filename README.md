# Домашняя работа 13.1 #
### Цель проекта:
Разработка виджета для банка

### Установка и запуск проекта:
1. Клонировать проект **Homework** на локальный компьютер.
2. Активировать интерпретатор *Poetry* в проекте командой `poetry init`.
3. В случае его отсутствия выполнить установку необходимых пакетов через менеджер загрузок `pipx` 
из списка зависимостей в файле `pyproject.toml` или скачать его с [сайта разработчика](https://python-poetry.org/docs/#installation/).
4. С помощью шаблона `.env.example` создать файл `.env` для хранения чувствительных данных 
(ключи API, пароли и т.п.) и обязательно добавить его в список исключений `.gitignore`.  


### Содержание проекта:
В текущей версии в пакете `src` доступны следующие функции и декораторы:
1. Модуль `decorators.py` с декоратором `log`
2. Модуль `external_api.py` с функцией конвертации валюты транзакции с помощью внешнего API
3. Модуль `generators.py`
* `card_number_generator` - генерирует номер карты в заданном диапазоне
* `filter_by_currency` - фильтрует входящий список транзакций по коду валюты
* `transaction_descriptions` - возвращает список описаний транзакций
4. Модуль `masks.py`
* `get_mask_account` - маскировка номера банковского счета
* `get_mask_card_number` - маскировка номера банковской карты 
5. Модуль `processing.py`
* `filter_by_state` - возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению
* `sort_by_date` - возвращает новый список, отсортированный по дате
6. Модуль `utils.py` с функцией чтения JSON-файла 
7. Модуль `widget.py`
* `get_date` - возвращает строку с датой в формате ДД.ММ.ГГГГ
* `mask_account_card` - объединенная функция маскировки номера карты или счета

В домашнем задании 13.1:
* добавлен модуль `file_reader_csv_xlsx.py` с функциями чтения файлов 
форматов `.csv` и `.xlsx`.
* Для использования этих функций требуется установка библиотек `csv` и `pandas`.
* В папку `data/` добавлены файлы `transactions.csv` и `transactions_excel.xlsx`.


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
Логирование функции `utils.py`
```
2025-02-27 21:59:14 get_file: INFO: Файл operations.json успешно открыт и данные загружены
2025-02-27 22:02:42 get_file: ERROR: Файл operations.json содержит некорректный JSON
```
`file_reader_csv_xlsx.py`: чтение файлов формата `.xlsx`
```
Размерность файла: (1000, 9)
          id     state  ...                         to               description
0   650703.0  EXECUTED  ...  Счет 39745660563456619397       Перевод организации
1  3598919.0  EXECUTED  ...  Discover 0720428384694643  Перевод с карты на карту
2   593027.0  CANCELED  ...      Visa 6804119550473710  Перевод с карты на карту

[3 rows x 9 columns]
```


### Тестирование проекта
Проект содержит тесты всех модулей в папке `tests`.
Статистика по покрытию согласно отчету `pytest-cov`:
```
---------- coverage: platform win32, python 3.13.0-final-0 -----------
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
config.py                                4      0   100%
src\__init__.py                          0      0   100%
src\decorators.py                       20      4    80%
src\external_api.py                     26      1    96%
src\file_reader_csv_xlsx.py             17      1    94%
src\generators.py                       13      0   100%
src\masks.py                            23      0   100%
src\processing.py                       12      0   100%
src\utils.py                            32      8    75%
src\widget.py                           11      0   100%
tests\__init__.py                        0      0   100%
tests\conftest.py                        4      0   100%
tests\test_decorators.py                14      3    79%
tests\test_external_api.py              29      1    97%
tests\test_file_reader_csv_xlsx.py      40      0   100%
tests\test_generators.py                24      3    88%
tests\test_masks.py                      6      0   100%
tests\test_processing.py                21      1    95%
tests\test_utils.py                     13      0   100%
tests\test_widget.py                    17      0   100%
--------------------------------------------------------
TOTAL                                  326     22    93%
```