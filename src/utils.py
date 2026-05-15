import json
import logging
import os
from typing import Any

import pandas as pd

from config import DATA_DIR, LOGS_DIR

logger = logging.getLogger()
logfile_path = os.path.join(LOGS_DIR, 'utils.log')
file_handler = logging.FileHandler(logfile_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(funcName)s: %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_file(file_name: str) -> list:
    """Функция забирает список операций из JSON-файла и выводит его в консоль"""
    file_path = os.path.join(DATA_DIR, file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные являются списком
        if isinstance(data, list):
            logger.info(f"Файл {file_name} успешно открыт и данные загружены")
            return data
        else:
            logger.error(f"Файл {file_name} не содержит список данных")
            return []

    except FileNotFoundError:
        logger.error(f"Файл {file_name} не найден")
        return []
    except json.JSONDecodeError:
        logger.error(f"Файл {file_name} содержит некорректный JSON")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_name}: {e}")
        return []


def reading_excel(file_name: str) -> list[dict[Any, Any]]:
    """Функция для чтения файлов XLSX"""

    file_path = os.path.join(DATA_DIR, file_name)
    dict_df_excel = pd.read_excel(file_path).to_dict(orient='records')
    return dict_df_excel


# Проверка
# file_open = get_file("operations.json")
# print(file_open)
