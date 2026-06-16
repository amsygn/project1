from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(user_input) -> str:
    """Функция возвращает строку с замаскированным номером карты или счета."""

    # Приводим к строке, обрабатывая float
    if isinstance(user_input, float):
        # Преобразуем float в int, если это целое число
        if user_input.is_integer():
            user_input = str(int(user_input))
        else:
            user_input = str(user_input)
    else:
        user_input = str(user_input)

    # Разбиваем на слова
    parts = user_input.split()

    # Если только одно слово - это номер
    if len(parts) == 1:
        number = parts[0]
        # Очищаем от возможных нецифровых символов
        number = ''.join(filter(str.isdigit, number))

        if len(number) == 16:
            return get_mask_card_number(number)
        elif len(number) == 20:
            return get_mask_account(number)
        else:
            raise ValueError(f'Неверный формат номера: длина {len(number)}')

    # Если есть название и номер
    # Название может состоять из нескольких слов
    name_parts = parts[:-1]
    number = parts[-1]

    # Очищаем номер от нецифровых символов
    number = ''.join(filter(str.isdigit, number))

    if len(number) == 16:
        masked_number = get_mask_card_number(number)
    elif len(number) == 20:
        masked_number = get_mask_account(number)
    else:
        raise ValueError(f'Неверный формат номера: длина {len(number)}')

    # Собираем результат
    return ' '.join(name_parts + [masked_number])


# def mask_account_card(user_input: str) -> str:
#     """Функция возвращает строку с замаскированным номером карты или счета.
#     Старая версия"""
#     user_input = str(user_input)
#     input_split = user_input.split()
#
#     # определяем формат номера - карта или счет
#     if len(input_split[-1]) == 16:
#         input_split[-1] = get_mask_card_number(input_split[-1])
#     elif len(input_split[-1]) == 20:
#         input_split[-1] = get_mask_account(input_split[-1])
#     else:
#         raise ValueError('Неверный формат данных')
#     return ' '.join(input_split)


def get_date(user_date: str) -> str:
    """Функция возвращает строку с датой в формате ДД.ММ.ГГГГ """
    return user_date[8:10] + '.' + user_date[5:7] + '.' + user_date[0:4]
