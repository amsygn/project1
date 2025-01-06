from typing import List

data_logs = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

def filter_by_state(data_logs: List[dict], state: str='EXECUTED') -> List[dict]:
    """ Возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению. """

    data_filter = []

    for item in data_logs:
        if 'state' in item and item['state'] == state:
            data_filter.append(item)

    return data_filter


def sort_by_date(date_logs: dict):
    """ Возвращает новый список, отсортированный по дате """
    pass


print(filter_by_state(data_logs), sep='\n')