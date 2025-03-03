import unittest
from unittest.mock import patch
import pandas as pd
import os

from config import DATA_DIR
from src.file_reader_csv_xlsx import read_csv, read_excel


@patch("pandas.read_csv")
def test_read_csv_valid_data(mock_read_csv):
    """1. Тест чтения CSV-файла с валидными данными."""
    mock_data = pd.DataFrame({"id": [650703, 5380041], "state": ["EXECUTED", "CANCELED"]})
    mock_read_csv.return_value = mock_data

    result = read_csv("test.csv", ";")

    mock_read_csv.assert_called_once_with(os.path.join(DATA_DIR, "test.csv"), delimiter=";")
    expected_result = [{"id": 650703, "state": "EXECUTED"}, {"id": 5380041, "state": "CANCELED"}]
    assert result == expected_result


@patch("pandas.read_csv")
def test_read_csv_empty_file(mock_read_csv):
    """2. Тест чтения пустого CSV-файла."""
    # Мокируем пустой DataFrame
    mock_data = pd.DataFrame()
    mock_read_csv.return_value = mock_data

    result = read_csv("empty.csv", ";")
    mock_read_csv.assert_called_once_with(os.path.join(DATA_DIR, "empty.csv"), delimiter=";")
    assert result == []


@patch("pandas.read_csv", side_effect=FileNotFoundError)
def test_read_csv_file_not_found(mock_read_csv):
    """4. Тест обработки отсутствия CSV-файла."""
    try:
        read_csv("missing.csv", ";")
    except FileNotFoundError:
        pass
    else:
        assert False, "Файл не найден. Ошибка FileNotFoundError"

    mock_read_csv.assert_called_once_with(os.path.join(DATA_DIR, "missing.csv"), delimiter=";")


@patch("pandas.read_excel")
def test_read_excel_valid_data(mock_read_excel) -> None:
    """4. Тест чтения Excel-файла с валидными данными."""
    mock_data = pd.DataFrame({"Column1": [1, 2], "Column2": ["A", "B"]})
    mock_read_excel.return_value = mock_data

    read_excel("test.xlsx")
    mock_read_excel.assert_called_once_with(os.path.join(DATA_DIR, "test.xlsx"))
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
