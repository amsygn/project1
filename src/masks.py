# card_num = int(input("Введите номер карты (16 цифр)\n"))
# account_num = int(input("Введите номер счета (20 цифр)\n"))


def get_mask_card_number(card_num: str) -> str:
    """ Функция маскировки номера банковской карты """

    # накладываем маску на номер карты
    card_mask = card_num[:6] + ('*' * 6) + card_num[-4:]

    # разбиваем маску на группы по 4 цифры
    card_num_sep = []
    for i in range(0, len(card_mask), 4):
        card_num_sep.append(card_mask[i: (i + 4)])

    return ' '.join(card_num_sep)


def get_mask_account(account_num: str) -> str:
    """ Функция маскировки номера банковского счета """
    return "**" + account_num[-4:]
