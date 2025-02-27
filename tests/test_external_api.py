from os import getenv
from unittest.mock import patch, Mock
from src.external_api import convert_to_rub, transaction_rub, transaction_usd


def test_convert_rub() -> None:
    """Тест транзакции в рублях (RUB)."""
    result = convert_to_rub(transaction_rub)
    assert result == 31957.58


@patch("os.getenv", return_value="fake_api_key")
@patch("requests.get")
def test_convert_usd(mock_requests_get, mock_getenv):
    """Тест транзакции в долларах (USD)."""
    # Мокируем успешный ответ от API
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": 75000.0
    }  # Пример конвертации USD в 75000 RUB
    mock_requests_get.return_value = mock_response

    result = convert_to_rub(transaction_usd)
    assert result == 75000.0  # Проверяем конвертированную сумму

    # Проверяем, что os.getenv был вызван для получения API-ключа
    mock_getenv.assert_called_once_with("API_KEY")

    # Проверяем, что API был вызван с правильными параметрами
    mock_requests_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        params={"to": "RUB", "from": "USD", "amount": "8221.37"},
        headers={"apikey": "fake_api_key"},
    )


@patch("os.getenv", return_value="fake_api_key")
@patch("requests.get")
def test_invalid_api_response(mock_requests_get, mock_getenv):
    """Тест некорректного ответа от API."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"error": "Invalid response"}
    mock_requests_get.return_value = mock_response

    # Проверяем, что функция выбрасывает исключение
    try:
        convert_to_rub(transaction_usd)
    except ValueError as e:
        assert str(e) == "Ошибка при обработке данных: Некорректный ответ от API."
    else:
        assert False, "Ожидалось исключение ValueError"
