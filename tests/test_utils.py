from unittest.mock import mock_open, patch

from src.utils import get_file


@patch("builtins.open", new_callable=mock_open, read_data='[{"id": "1"}]')
def test_get_info(mock_file, transactions):
    transactions = get_file("test.json")
    assert transactions == [{"id": "1"}]


@patch("os.path.join")
@patch("builtins.open", side_effect=FileNotFoundError("Файл не найден"))
def test_get_file_not_found(mock_file, mock_join):
    """Тест ошибки, если файл не найден."""

    mock_join.return_value = "fake_path.json"
    result = get_file("fake_file.json")
    assert result == []
    mock_file.assert_called_once_with("fake_path.json", "r", encoding="utf-8")
