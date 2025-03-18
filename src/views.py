import json
import os
from typing import Any

from dotenv import load_dotenv

from src.utils import (
    filter_transactions,
    get_cards_data,
    get_exchange_rates,
    get_stocks_cost,
    get_top_5_transactions,
    greeting,
    read_transaction_excel,
)

# Получаем путь к директории, где находится текущий файл
current_dir = os.path.dirname(os.path.abspath(__file__))
# Формируем путь к файлу user_settings.json
settings_path = os.path.join(current_dir, "../data/user_settings.json")

# Открываем файл
with open(settings_path, "r") as file:
    user_choice = json.load(file)

load_dotenv()
api_key_currency = os.getenv("API_KEY_CURRENCY")
api_key_stocks = os.getenv("API_KEY_STOCKS")


def main(input_date: str) -> Any:
    """Основная функция для генерации JSON-ответа."""
    # path = r"../data/operations.xlsx"
    path = r"data/operations.xlsx"
    transactions = read_transaction_excel(path)
    filtered_transactions = filter_transactions(transactions, input_date)
    cards_data = get_cards_data(filtered_transactions)
    exchange_rates = get_exchange_rates(user_choice["user_currencies"], api_key_currency)
    stocks_cost = get_stocks_cost(user_choice["user_stocks"], api_key_stocks)
    top_transactions = get_top_5_transactions(filtered_transactions)
    greetings = greeting()

    user_data = {
        "greeting": greetings,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "exchange_rates": exchange_rates,
        "stocks": stocks_cost,
    }

    return json.dumps(user_data, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    input_date_str = "2020-03-20 00:00:00"  # Пример даты в нужном формате
    result = main(input_date_str)
    print(result)
