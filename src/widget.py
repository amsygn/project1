from masks import get_mask_card_number, get_mask_account


def mask_account_card(user_input: str) -> str:
    """ Возвращает строку с замаскированным номером карты или счета"""

    input_split = user_input.split()
    # определяем формат номера - карта или счет
    if len(input_split[-1]) == 16:
        return get_mask_card_number(input_split[-1])
    else:
        return get_mask_account(input_split[-1])


def get_date(user_date: str) -> str:
    """ Возвращает строку с датой в формате ДД.ММ.ГГГГ """
    pass

user_input: str = input('>')
print(mask_account_card(user_input))