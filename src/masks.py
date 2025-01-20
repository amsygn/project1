# card_num = int(input("Введите номер карты (16 цифр)\n"))
# account_num = int(input("Введите номер счета (20 цифр)\n"))


def get_mask_card_number(card_data: str) -> str:
    """ Функция маскировки номера банковской карты """

    card_data_split: list = card_data.split()
    card_num = card_data_split[-1]

    if len(card_num) == 16:
        # накладываем маску на номер карты
        card_mask = card_num[:6] + ('*' * 6) + card_num[-4:]
    else:
        raise ValueError('Неверный формат карты')

    # разбиваем маску на группы по 4 цифры
    card_num_sep = []
    for i in range(0, len(card_mask), 4):
        card_num_sep.append(card_mask[i: (i + 4)])

    card_num_mask = ' '.join(card_num_sep)
    card_data_split[-1] = card_num_mask

    return ' '.join(card_data_split)


def get_mask_account(account_data: str) -> str:
    """ Функция маскировки номера банковского счета """

    account_data_split: list = account_data.split()
    account_num = account_data_split[1]
    if len(account_num) == 20:
        account_mask = "**" + account_num[-4:]
        account_mask_full = account_data_split[0] + ' ' + account_mask
    else:
        raise ValueError('Неверный формат счета')

    return account_mask_full
