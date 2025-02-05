def filter_by_currency(transactions, currency_code):
    """ Функция фильтрует входящий список транзакций по коду валюты """
    return (i for i in transactions if currency_code == i.get("operationAmount", {}).get("currency", {}).get("code"))


def transaction_descriptions(transactions):
    for trans in transactions:
        if trans.get("description"):
            yield trans["description"]


def card_number_generator(start, stop):
    for i in range(start, stop+1):
        full_number = str(i).zfill(16) # 0000000000010001
        card_num_line = f"{full_number[0:4]} {full_number[4:8]} {full_number[8:12]} {full_number[12:16]}"
        yield card_num_line

print(next(filter_by_currency(transactions, 'RUR')))