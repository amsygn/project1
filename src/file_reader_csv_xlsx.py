import os
from typing import Any, Hashable

import pandas as pd

from config import DATA_DIR


def read_csv(file_name: str, delimiter: str) -> list[dict[Hashable, Any]]:
    """Функция для чтения файлов CSV"""
    file_path = os.path.join(DATA_DIR, file_name)
    from_csv = pd.read_csv(file_path, delimiter=delimiter)
    return from_csv.to_dict(orient="records")


def read_excel(file_name: str) -> list[dict[Hashable, Any]]:
    """Функция для чтения файлов XLSX"""
    file_path = os.path.join(DATA_DIR, file_name)
    from_excel = pd.read_excel(file_path)
    # print(f"Размерность файла: {from_excel.shape}")
    # print(from_excel.head(3))
    return from_excel.to_dict(orient="records")


# print(read_csv("transactions.csv", ";"))
# print(read_excel("transactions_excel.xlsx"))
