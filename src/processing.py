from typing import List

def filter_by_state(data_logs: List[dict], state: str='EXECUTED') -> List[dict]:
    """ Возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению. """

    data_filter = []

    for item in data_logs:
        if 'state' in item and item['state'] == state:
            data_filter.append(item)

    return data_filter


def sort_by_date(data_logs: List[dict], reverse='True') -> List[dict]:
    """ Возвращает новый список, отсортированный по дате """

    return sorted(data_logs, key=lambda x: x['date'], reverse=reverse)
