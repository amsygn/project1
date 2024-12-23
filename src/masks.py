card_num = int(input("Введите номер карты (16 цифр)\n"))
account_num = int(input("Введите номер счета (20 цифр)\n"))


def get_mask_card_number(card_num: int) -> str:
    """ Функция маскировки номера банковской карты """

    card_number = str(card_num)

    # Проверяем формат карты: число из 16 цифр
    if not len(card_number) == 16:
        return " Неверный формат номера карты"

    card_mask = card_number[:6] + ('*' * 6) + card_number[-4:]

    # Разбиваем маску на блоки
    card_parts = []
    for i in range(0, len(card_mask), 4):
        card_parts.append(card_mask[i : (i + 4)])

    return ' '.join(card_parts)


def get_mask_account(account_num: int) -> str:
    """ Функция маскировки номера банковского счета """
    
    account_number = str(account_num)

    # Проверяем формат счета: число из 20 цифр
    if not len(account_number) == 20:
        return "  Неверный формат номера счета"

    account_mask = "**" + account_number[-4:]

    return account_mask
