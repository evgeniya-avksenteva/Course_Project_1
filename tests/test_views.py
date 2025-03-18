import json
import os
from unittest.mock import mock_open, patch

import pytest

from src.views import main


@pytest.fixture
def mock_user_settings():
    # Мокируем файл user_settings.json
    mock_data = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        yield


@pytest.fixture
def mock_environment_variables():
    with patch.dict(
        os.environ, {"API_KEY_CURRENCY": "mock_currency_api_key", "API_KEY_STOCKS": "mock_stocks_api_key"}
    ):
        yield


@pytest.fixture
def mock_read_transaction_excel():
    with patch("src.views.read_transaction_excel") as mock:
        mock.return_value = [
            {"date": "2020-03-20", "amount": 100, "currency": "USD"},
            {"date": "2020-03-21", "amount": 50, "currency": "EUR"},
        ]
        yield mock


@pytest.fixture
def mock_filter_transactions():
    with patch("src.views.filter_transactions") as mock:
        mock.return_value = [
            {"date": "2020-03-20", "amount": 100, "currency": "USD"},
        ]
        yield mock


@pytest.fixture
def mock_get_cards_data():
    with patch("src.views.get_cards_data") as mock:
        mock.return_value = [{"card_name": "Visa", "balance": 100}]
        yield mock


@pytest.fixture
def mock_get_exchange_rates():
    with patch("src.views.get_exchange_rates") as mock:
        mock.return_value = {"USD": 73.5, "EUR": 86.5}
        yield mock


@pytest.fixture
def mock_get_stocks_cost():
    with patch("src.views.get_stocks_cost") as mock:
        mock.return_value = {"AAPL": 150, "GOOGL": 2800}
        yield mock


@pytest.fixture
def mock_get_top_5_transactions():
    with patch("src.views.get_top_5_transactions") as mock:
        mock.return_value = [{"transaction_name": "Buy", "amount": 50}]
        yield mock


@pytest.fixture
def mock_greeting():
    with patch("src.views.greeting") as mock:
        mock.return_value = "Hello!"
        yield mock


def test_main(
    mock_user_settings,
    mock_environment_variables,
    mock_read_transaction_excel,
    mock_filter_transactions,
    mock_get_cards_data,
    mock_get_exchange_rates,
    mock_get_stocks_cost,
    mock_get_top_5_transactions,
    mock_greeting,
):
    input_date = "2020-03-20"

    # Вызов вашей функции
    result = main(input_date)

    # Преобразование результата из строки JSON в словарь Python
    result_dict = json.loads(result)

    expected_output = {
        "greeting": "Hello!",
        "cards": [{"card_name": "Visa", "balance": 100}],
        "top_transactions": [{"transaction_name": "Buy", "amount": 50}],
        "exchange_rates": {"USD": 73.5, "EUR": 86.5},
        "stocks": {"AAPL": 150, "GOOGL": 2800},
    }

    assert result_dict == expected_output
