import logging
import os

from config import LOGS_DIR

logging.basicConfig(
    format="%(asctime)s %(funcName)s: %(levelname)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger()
logfile_path = os.path.join(LOGS_DIR, 'masks.log')
file_handler = logging.FileHandler(logfile_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(funcName)s: %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# создаем именованный логер по имени функции
func_logger = logging.getLogger(__name__)



def get_mask_card_number(card_num: str) -> str:
    """ Функция маскировки номера банковской карты """

    # накладываем маску на номер карты
    card_mask = card_num[:6] + ('*' * 6) + card_num[-4:]

    # разбиваем маску на группы по 4 цифры
    card_num_sep = []
    for i in range(0, len(card_mask), 4):
        card_num_sep.append(card_mask[i: (i + 4)])

    func_logger.info("Номер карты замаскирован")
    return ' '.join(card_num_sep)


def get_mask_account(account_num: str) -> str:
    """ Функция маскировки номера банковского счета """
    func_logger.info("Номер счета замаскирован")
    return "**" + account_num[-4:]

# Примеры использования
# print(get_mask_card_number("1234567890123456"))
# print(get_mask_account("12345678901234567890"))
