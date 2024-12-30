from src.widget import mask_account_card

print(mask_account_card('Счет 12345678901234567890'))
print(mask_account_card('Visa Super Puper 1234567890123456'))
print(mask_account_card('Visa Super 1234567890123456'))
print(mask_account_card('Visa 1234567890123456'))

