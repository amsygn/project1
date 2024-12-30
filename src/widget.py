from .masks import get_mask_account, get_mask_card_number


def mask_account_card(user_input: str) -> str:
    """Возвращает строку с замаскированным номером карты или счета"""

    input_split = user_input.split()
    # определяем формат номера - карта или счет
    if len(input_split[-1]) == 16:
        input_split[-1] = get_mask_card_number(input_split[-1])
    else:
        input_split[-1] = get_mask_account(int(input_split[-1]))
    return " ".join(input_split)


def get_date(user_date: str) -> str:
    """Возвращает строку с датой в формате ДД.ММ.ГГГГ"""
    return user_date[8:10] + "." + user_date[5:7] + "." + user_date[0:4]


# user_input: str = input('>')
# print(mask_account_card(user_input))

# print(get_date('2024-03-11T02:26:18.671407'))
