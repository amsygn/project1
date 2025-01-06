from src.processing import filter_by_state, sort_by_date

data_logs = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

print('\n### Sorted by status:\nDefault: EXECUTED')
state_filter = filter_by_state(data_logs)
for state in state_filter:
    print(state)

print('\n### Sorted by date:')
date_sorted = sort_by_date(data_logs)
for d in date_sorted:
    print(d)
print()



#from src.widget import mask_account_card
#print(mask_account_card('Счет 12345678901234567890'))
#print(mask_account_card('Visa Super Puper 1234567890123456'))
#print(mask_account_card('Visa Super 1234567890123456'))
#print(mask_account_card('Visa 1234567890123456'))
