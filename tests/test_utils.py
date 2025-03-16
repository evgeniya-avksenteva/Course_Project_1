from datetime import datetime
from pathlib import Path
from unittest.mock import patch, Mock
from typing import List, Dict

import pandas as pd
import pytest

from src.utils import (filter_transactions, get_cards_data, get_top_5_transactions, greeting,
                       read_transaction_excel, get_exchange_rates, get_stocks_cost)


ROOT_PATH = Path(__file__).resolve().parent.parent


def test_get_data_from_xlsx() -> None:
    test_data = [
        {
            "Дата операции": "01.06.2023 12:00:00",
            "Сумма операции": "-100.50",
            "Категория": "Покупки",
            "Описание": "Магазин",
        },
        {
            "Дата операции": "15.06.2023 18:30:00",
            "Сумма операции": "-250.00",
            "Категория": "Ресторан",
            "Описание": "Ужин",
        },
    ]
    df = pd.DataFrame(test_data)
    with patch("pandas.read_excel", return_value=df):
        result = read_transaction_excel(r"../data/operations.xlsx")
        assert result == test_data

@patch('pandas.read_excel')
def test_get_excel_df_2(mock_get):
    mock_get.return_value =pd.DataFrame({})
    assert read_transaction_excel('filename.xlsx') == []

@patch('pandas.read_excel')
def test_read_transaction_failure(mock_get_2):
    mock_get_2.side_effect = Exception("Ошибка чтения файла")
    assert read_transaction_excel('filename.xlsx') == []


@pytest.fixture
def test_transactions() -> None:
    return [
        {
            "Дата операции": "01.06.2023 12:00:00",
            "Сумма операции": "-100.50",
            "Категория": "Покупки",
            "Описание": "Магазин",
        },
        {
            "Дата операции": "15.06.2023 18:30:00",
            "Сумма операции": "-250.00",
            "Категория": "Ресторан",
            "Описание": "Ужин",
        },
        {
            "Дата операции": "20.06.2023 10:00:00",
            "Сумма операции": "-75.00",
            "Категория": "Транспорт",
            "Описание": "Такси",
        },
        {
            "Дата операции": "05.05.2023 08:15:00",
            "Сумма операции": "-500.00",
            "Категория": "Медицина",
            "Описание": "Аптека",
        },
        {
            "Дата операции": "25.05.2023 14:45:00",
            "Сумма операции": "-120.00",
            "Категория": "Покупки",
            "Описание": "Одежда",
        },
    ]


@pytest.mark.parametrize(
    "input_date_str, expected_result",
    [
        (
            "20.06.2023",
            [
                {
                    "Дата операции": "01.06.2023 12:00:00",
                    "Сумма операции": "-100.50",
                    "Категория": "Покупки",
                    "Описание": "Магазин",
                },
                {
                    "Дата операции": "15.06.2023 18:30:00",
                    "Сумма операции": "-250.00",
                    "Категория": "Ресторан",
                    "Описание": "Ужин",
                },
                {
                    "Дата операции": "20.06.2023 10:00:00",
                    "Сумма операции": "-75.00",
                    "Категория": "Транспорт",
                    "Описание": "Такси",
                },
            ],
        ),
        (
            "15.05.2023",
            [
                {
                    "Дата операции": "05.05.2023 08:15:00",
                    "Сумма операции": "-500.00",
                    "Категория": "Медицина",
                    "Описание": "Аптека",
                },
            ],
        ),
    ],
)
def test_filter_transactions(test_transactions, input_date_str, expected_result):
    result = filter_transactions(test_transactions, input_date_str)
    assert result == expected_result


@patch("src.utils.datetime")
@pytest.mark.parametrize(
    "current_hour, expected_greeting",
    [
        (7, "Доброе утро"),
        (13, "Добрый день"),
        (19, "Добрый вечер"),
        (2, "Доброй ночи"),
    ],
)
def test_greeting(mock_datetime, current_hour, expected_greeting):
    mock_now = datetime(2023, 6, 20, current_hour, 0, 0)
    mock_datetime.now.return_value = mock_now
    result = greeting()
    assert result == expected_greeting


def test_get_cards_data_empty():
    transactions = []
    expected_result = []
    assert get_cards_data(transactions) == expected_result


def test_get_cards_data_single_transaction() -> None:
    transactions = [{"Номер карты": "1234", "Сумма операции": "-100.0", "Кэшбэк": "1.0", "Категория": "Продукты"}]
    expected_result = [{"last_digits": "1234", "total_spent": 100.0, "cashback": 1.0}]
    assert get_cards_data(transactions) == expected_result


def test_get_cards_data_multiple_transactions() -> None:
    transactions = [
        {"Номер карты": "1234", "Сумма операции": "-100.0", "Кэшбэк": "1.0", "Категория": "Продукты"},
        {"Номер карты": "1234", "Сумма операции": "-200.0", "Кэшбэк": "2.0", "Категория": "Продукты"},
        {"Номер карты": "5678", "Сумма операции": "-50.0", "Кэшбэк": "0.5", "Категория": "Продукты"},
    ]
    expected_result = [
        {"last_digits": "1234", "total_spent": 300.0, "cashback": 3.0},
        {"last_digits": "5678", "total_spent": 50.0, "cashback": 0.5},
    ]
    assert get_cards_data(transactions) == expected_result


def test_get_cards_data_nan_card_number() -> None:
    transactions = [
        {"Номер карты": "1234", "Сумма операции": "-100.0", "Кэшбэк": "1.0", "Категория": "Продукты"},
        {"Номер карты": "nan", "Сумма операции": "-200.0", "Кэшбэк": "2.0", "Категория": "Продукты"},
        {"Номер карты": "5678", "Сумма операции": "-50.0", "Кэшбэк": "0.5", "Категория": "Продукты"},
    ]
    expected_result = [
        {"last_digits": "1234", "total_spent": 100.0, "cashback": 1.0},
        {"last_digits": "5678", "total_spent": 50.0, "cashback": 0.5},
    ]
    assert get_cards_data(transactions) == expected_result


def test_get_cards_data_cashback() -> None:
    transactions = [
        {"Номер карты": "1234", "Сумма операции": "-100.0", "Категория": "Продукты"},
        {"Номер карты": "5678", "Сумма операции": "-50.0", "Категория": "Продукты"},
    ]
    expected_result = [
        {"last_digits": "1234", "total_spent": 100.0, "cashback": 1.0},
        {"last_digits": "5678", "total_spent": 50.0, "cashback": 0.5},
    ]
    assert get_cards_data(transactions) == expected_result


def test_get_top_5_transactions_empty():
    transactions = []
    expected_result = []
    assert get_top_5_transactions(transactions) == expected_result


def test_get_top_5_transactions_single_transaction() -> None:
    transactions = [
        {
            "Дата операции": "20.06.2023 12:00:00",
            "Сумма операции": "-100.0",
            "Категория": "Еда",
            "Описание": "Покупка еды",
        }
    ]
    expected_result = [{"date": "20.06.2023", "amount": "-100.0", "category": "Еда", "description": "Покупка еды"}]
    assert get_top_5_transactions(transactions) == expected_result


def test_get_top_5_transactions_multiple_transactions() -> None:
    transactions = [
        {
            "Дата операции": "20.06.2023 12:00:00",
            "Сумма операции": "-100.0",
            "Категория": "Еда",
            "Описание": "Покупка еды",
        },
        {
            "Дата операции": "21.06.2023 12:00:00",
            "Сумма операции": "-200.0",
            "Категория": "Транспорт",
            "Описание": "Оплата проезда",
        },
        {
            "Дата операции": "22.06.2023 12:00:00",
            "Сумма операции": "-50.0",
            "Категория": "Развлечения",
            "Описание": "Кино",
        },
        {
            "Дата операции": "23.06.2023 12:00:00",
            "Сумма операции": "-300.0",
            "Категория": "Магазины",
            "Описание": "Покупка одежды",
        },
        {
            "Дата операции": "24.06.2023 12:00:00",
            "Сумма операции": "-20.0",
            "Категория": "Кофе",
            "Описание": "Кофе на вынос",
        },
        {
            "Дата операции": "25.06.2023 12:00:00",
            "Сумма операции": "-400.0",
            "Категория": "Магазины",
            "Описание": "Покупка техники",
        },
    ]
    expected_result = [
        {"date": "25.06.2023", "amount": "-400.0", "category": "Магазины", "description": "Покупка техники"},
        {"date": "23.06.2023", "amount": "-300.0", "category": "Магазины", "description": "Покупка одежды"},
        {"date": "21.06.2023", "amount": "-200.0", "category": "Транспорт", "description": "Оплата проезда"},
        {"date": "20.06.2023", "amount": "-100.0", "category": "Еда", "description": "Покупка еды"},
        {"date": "22.06.2023", "amount": "-50.0", "category": "Развлечения", "description": "Кино"},
    ]
    assert get_top_5_transactions(transactions) == expected_result


def test_get_top_5_transactions_less_than_5() -> None:
    transactions = [
        {
            "Дата операции": "20.06.2023 12:00:00",
            "Сумма операции": "-100.0",
            "Категория": "Еда",
            "Описание": "Покупка еды",
        },
        {
            "Дата операции": "21.06.2023 12:00:00",
            "Сумма операции": "-200.0",
            "Категория": "Транспорт",
            "Описание": "Оплата проезда",
        },
    ]
    expected_result = [
        {"date": "21.06.2023", "amount": "-200.0", "category": "Транспорт", "description": "Оплата проезда"},
        {"date": "20.06.2023", "amount": "-100.0", "category": "Еда", "description": "Покупка еды"},
    ]
    assert get_top_5_transactions(transactions) == expected_result


def test_get_top_5_transactions_with_equal_amounts() -> None:
    transactions = [
        {
            "Дата операции": "20.06.2023 12:00:00",
            "Сумма операции": "-100.0",
            "Категория": "Еда",
            "Описание": "Покупка еды",
        },
        {
            "Дата операции": "21.06.2023 12:00:00",
            "Сумма операции": "-100.0",
            "Категория": "Транспорт",
            "Описание": "Оплата проезда",
        },
        {
            "Дата операции": "22.06.2023 12:00:00",
            "Сумма операции": "-100.0",
            "Категория": "Развлечения",
            "Описание": "Кино",
        },
        {
            "Дата операции": "23.06.2023 12:00:00",
            "Сумма операции": "-100.0",
            "Категория": "Магазины",
            "Описание": "Покупка одежды",
        },
        {
            "Дата операции": "24.06.2023 12:00:00",
            "Сумма операции": "-100.0",
            "Категория": "Кофе",
            "Описание": "Кофе на вынос",
        },
        {
            "Дата операции": "25.06.2023 12:00:00",
            "Сумма операции": "-100.0",
            "Категория": "Магазины",
            "Описание": "Покупка техники",
        },
    ]
    expected_result = [
        {"date": "20.06.2023", "amount": "-100.0", "category": "Еда", "description": "Покупка еды"},
        {"date": "21.06.2023", "amount": "-100.0", "category": "Транспорт", "description": "Оплата проезда"},
        {"date": "22.06.2023", "amount": "-100.0", "category": "Развлечения", "description": "Кино"},
        {"date": "23.06.2023", "amount": "-100.0", "category": "Магазины", "description": "Покупка одежды"},
        {"date": "24.06.2023", "amount": "-100.0", "category": "Кофе", "description": "Кофе на вынос"},
    ]
    assert get_top_5_transactions(transactions) == expected_result


API_KEY = "test_api_key"
CURRENCIES = ["USD", "EUR"]


def test_get_exchange_rates_success():
    with patch('requests.get') as mock_get:
        # Имитация успешного ответа API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "conversion_rates": {
                "RUB": 70.0
            }
        }
        mock_get.return_value = mock_response

        expected_result = [
            {"currency": "USD", "rate": 70.0},
            {"currency": "EUR", "rate": 70.0}
        ]

        result = get_exchange_rates(CURRENCIES, API_KEY)
        assert result == expected_result


def test_get_exchange_rates_api_error():
    with patch('requests.get') as mock_get:
        # Имитация ошибки API
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_get.return_value = mock_response

        expected_result = [
            {"currency": "USD", "rate": None},
            {"currency": "EUR", "rate": None}
        ]

        result = get_exchange_rates(CURRENCIES, API_KEY)
        assert result == expected_result


def test_get_exchange_rates_partial_success():
    with patch('requests.get') as mock_get:
        # Имитация частичного успеха
        mock_response_usd = Mock()
        mock_response_usd.status_code = 200
        mock_response_usd.json.return_value = {
            "conversion_rates": {
                "RUB": 70.0
            }
        }

        mock_response_eur = Mock()
        mock_response_eur.status_code = 400
        mock_response_eur.text = "Bad Request"

        mock_get.side_effect = [mock_response_usd, mock_response_eur]  # Устанавливаем разные ответы для разных вызовов

        expected_result = [
            {"currency": "USD", "rate": 70.0},
            {"currency": "EUR", "rate": None}
        ]

        result = get_exchange_rates(CURRENCIES, API_KEY)
        assert result == expected_result


def test_get_exchange_rates_empty_list():
    result = get_exchange_rates([], API_KEY)
    assert result == []  # Ожидаем пустой список при передаче пустого списка валют
