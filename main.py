from src.masks import get_mask_card_number, get_mask_account, card_num, account_num

print('Маска номера карты:')
print(get_mask_card_number(card_num))
print('Маска номера счета:')
print(get_mask_account(account_num))
