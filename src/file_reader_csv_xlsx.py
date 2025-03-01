import csv
import os
import pandas as pd
from config import DATA_DIR


def read_csv(data: str) -> None:
    file_path = os.path.join(DATA_DIR, data)
    with open(file_path, encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            print(row)


def read_excel(data: str) -> pd.DataFrame:
    file_path = os.path.join(DATA_DIR, data)
    excel_data = pd.read_excel(file_path)
    print(f"Размерность файла: {excel_data.shape}")
    print(excel_data.head(3))
    return excel_data


# print(read_csv("transactions.csv"))
print(read_excel("transactions_excel.xlsx"))
