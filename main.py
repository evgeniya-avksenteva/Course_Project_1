import pandas as pd

import config
from src.reports import spending_by_weekday, spending_by_workday
from src.services import (
    analyze_cashback,
    find_person_to_person_transactions,
    investment_bank,
    search_transaction_by_mobile_phone,
    search_transactions_by_user_choice,
)
from src.views import main, user_choice

# Веб страницы
main_page = main(config.input_date_str, user_choice, config.api_key_currency, config.api_key_stocks)
print(main_page)

# Сервисы
cashback_analysis_result = analyze_cashback(config.transactions, config.year, config.month)
investment_bank_result = investment_bank(config.transactions, config.date, config.limit)
search_transactions_by_user_choice_result = search_transactions_by_user_choice(config.transactions, config.search)
search_transaction_by_mobile_phone_result = search_transaction_by_mobile_phone(config.transactions)
find_person_to_person_transactions_result = find_person_to_person_transactions(config.transactions)
print(cashback_analysis_result)  # Принимает список словарей транзакций и считает сумму кэшбека по категориям
print(investment_bank_result)  # Cчитает сколько можно было отложить в инвесткопилку
print(search_transactions_by_user_choice_result)  # Функция выполняет поиск в транзакциях по переданной строке
print(search_transaction_by_mobile_phone_result)  # Возвращает транзакции в описании которых есть мобильный номер
print(find_person_to_person_transactions_result)  # В описании есть имя кому или от кого выполнен перевод


# Отчёты
df = pd.read_excel(r"../data/operations.xlsx")
spending_by_weekday_result = spending_by_weekday(df, "2020.05.20")
spending_by_workday_result = spending_by_workday(df, "2020.05.20")
print(spending_by_weekday_result)  # Возвращает средние траты в каждый из дней недели за последние три месяца
print(spending_by_workday_result)  # Выводит средние траты в рабочий и в выходной день за последние три месяца
