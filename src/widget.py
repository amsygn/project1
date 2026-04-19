from src.masks import get_mask_account, get_mask_card_number

def mask_account_card(user_input: str) -> str:
    """ Возвращает строку с замаскированным номером карты или счета """
    input_split = user_input.split()

    # определяем формат номера - карта или счет
    if len(input_split[-1]) == 16:
        input_split[-1] = get_mask_card_number(input_split[-1])
    elif len(input_split[-1]) == 20:
        input_split[-1] = get_mask_account(input_split[-1])
    else:
        raise ValueError('Неверный формат данных')
    return ' '.join(input_split)


def get_date(user_date: str) -> str:
    """ Возвращает строку с датой в формате ДД.ММ.ГГГГ """
    return user_date[8:10] + '.' + user_date[5:7] + '.' + user_date[0:4]
