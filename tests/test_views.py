from unittest.mock import mock_open
import json
import pytest

from src.views import (main, filter_transactions, get_cards_data, get_exchange_rates, get_stocks_cost,
                       get_top_5_transactions, greeting, read_transaction_excel)


@pytest.fixture
def mock_file(mocker):
    mock_data = '{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}'
    mocker.patch("builtins.open", mock_open(read_data=mock_data))


@pytest.fixture
def mock_dependencies(mocker):
    mocker.patch("src.views.read_transaction_excel", return_value=[])
    mocker.patch("src.views.filter_transactions", return_value=[])
    mocker.patch("src.views.get_cards_data", return_value=[{'card_name': 'Visa', 'balance': 100}])
    mocker.patch("src.views.get_exchange_rates", return_value={'USD': 73.5, 'EUR': 86.5})
    mocker.patch("src.views.get_stocks_cost", return_value={'AAPL': 150, 'GOOGL': 2800})
    mocker.patch("src.views.get_top_5_transactions", return_value=[{'transaction_name': 'Buy', 'amount': 50}])
    mocker.patch("src.views.greeting", return_value='Hello!')
    mocker.patch("os.getenv",
                 side_effect=lambda key: 'fake_api_key' if key in {"API_KEY_CURRENCY", "API_KEY_STOCKS"} else None)


def test_main(mock_file, mock_dependencies):
    input_date = "20.03.2020"
    with open('mock_user_settings.json') as f:
        user_settings = json.load(f)
    # Здесь должен быть вызов вашей функции
    result = main(input_date, user_settings, "API_KEY_CURRENCY", "API_KEY_STOCKS")
    # Преобразование результата из строки JSON в словарь Python
    result = json.loads(result)  # Добавить это для преобразования строки в словарь

    expected_output = {
        "greeting": "Hello!",
        "cards": [{'card_name': 'Visa', 'balance': 100}],
        "top_transactions": [{'transaction_name': 'Buy', 'amount': 50}],
        "exchange_rates": {'USD': 73.5, 'EUR': 86.5},
        "stocks": {'AAPL': 150, 'GOOGL': 2800}
    }

    assert result == expected_output
