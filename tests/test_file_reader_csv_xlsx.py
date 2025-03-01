import os
import unittest
from unittest.mock import mock_open, patch

import pandas as pd

from config import DATA_DIR
from src.file_reader_csv_xlsx import read_csv, read_excel


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="650703;Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации",
)
@patch("csv.reader")
def test_read_csv_valid_data(mock_csv_reader, mock_file) -> None:
    """1. Тест чтения CSV-файла с валидными данными."""
    read_csv("test.csv")
    mock_file.assert_called_once_with(
        os.path.join(DATA_DIR, "test.csv"), encoding="utf-8"
    )
    mock_csv_reader.assert_called_once_with(mock_file(), delimiter=";")


@patch("builtins.open", new_callable=mock_open, read_data="")
@patch("csv.reader")
def test_read_csv_empty_file(mock_csv_reader, mock_file) -> None:
    """2. Тест чтения пустого CSV-файла."""
    read_csv("empty.csv")
    mock_file.assert_called_once_with(
        os.path.join(DATA_DIR, "empty.csv"), encoding="utf-8"
    )
    mock_csv_reader.assert_called_once_with(mock_file(), delimiter=";")


@patch("builtins.open", side_effect=FileNotFoundError)
def test_read_csv_file_not_found(mock_file) -> None:
    """3. Тест обработки отсутствия CSV-файла."""
    with unittest.TestCase().assertRaises(FileNotFoundError):
        read_csv("missing.csv")
    mock_file.assert_called_once_with(
        os.path.join(DATA_DIR, "missing.csv"), encoding="utf-8"
    )


@patch("pandas.read_excel")
def test_read_excel_valid_data(mock_read_excel) -> None:
    """4. Тест чтения Excel-файла с валидными данными."""
    mock_data = pd.DataFrame({"Column1": [1, 2], "Column2": ["A", "B"]})
    mock_read_excel.return_value = mock_data

    read_excel("test.xlsx")
    mock_read_excel.assert_called_once_with(os.path.join(DATA_DIR, "test.xlsx"))
    # Проверяем, что данные выводятся корректно
    assert mock_read_excel.call_count == 1


@patch("pandas.read_excel", return_value=pd.DataFrame())
def test_read_excel_empty_file(mock_read_excel) -> None:
    """5. Тест чтения пустого Excel-файла."""
    read_excel("empty.xlsx")
    mock_read_excel.assert_called_once_with(os.path.join(DATA_DIR, "empty.xlsx"))
    # Проверяем, что файл открыт, но данных нет
    assert mock_read_excel.call_count == 1


@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_read_excel_file_not_found(mock_read_excel) -> None:
    """6. Тест обработки отсутствия Excel-файла."""
    with unittest.TestCase().assertRaises(FileNotFoundError):
        read_excel("missing.xlsx")
    mock_read_excel.assert_called_once_with(os.path.join(DATA_DIR, "missing.xlsx"))


# if __name__ == "__main__":
#     # Запуск тестов
#     test_read_csv_valid_data()
#     test_read_csv_empty_file()
#     test_read_csv_file_not_found()
#     test_read_excel_valid_data()
#     test_read_excel_empty_file()
#     test_read_excel_file_not_found()
