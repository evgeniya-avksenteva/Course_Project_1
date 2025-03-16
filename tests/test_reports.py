import json

import pandas as pd
import pytest

from src.reports import report_to_file, spending_by_weekday, spending_by_workday


@pytest.fixture
def spending_data() -> pd.DataFrame:
    # Пример тестовых данных
    data_2 = {
        "День операции": [
            "Понедельник",
            "Вторник",
            "Среда" "Четверг",
        ],
        "Сумма": [-217.24634920634915, -57.81921568627451, -139.2568253968254, -320.05508196721314],
    }
    df = pd.DataFrame(data_2)
    return df


def test_spending_by_weekday() -> None:
    # Тестирование функции с категорией, для которой нет транзакций
    result = spending_by_weekday(spending_by_weekday, "Пятница")
    assert len(result) == 0


def create_test_dataframe() -> pd.DataFrame:
    data = {
        "Дата операции": [
            "01.10.2023 10:00:00",
            "02.10.2023 14:00:00",
            "03.10.2023 12:00:00",
            "04.10.2023 16:00:00",
            "05.10.2023 18:00:00",
            "06.10.2023 11:00:00",
            "07.10.2023 19:00:00",
            "08.10.2023 20:00:00",
            "09.10.2023 09:00:00",
            "10.10.2023 10:00:00",
        ],
        "Сумма операции": [100, 200, 150, 400, 300, 500, 900, 600, 700, 800],
    }
    return pd.DataFrame(data)


# Тест для проверки работы с конкретной датой
def test_spending_by_weekday_with_date() -> None:
    df = create_test_dataframe()
    test_date = "2023.10.10"  # Формат: YYYY-MM-DD
    result = spending_by_weekday(df, test_date)

    result_dict = json.loads(result)

    # Проверка, что в результате есть все дни недели
    weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    for day in weekdays:
        assert day in result_dict


# Тест для проверки обработки ошибки
def test_spending_by_weekday_with_invalid_date() -> None:
    df = create_test_dataframe()
    result = spending_by_weekday(df, "invalid_date_string")  # Неправильная дата

    # Проверка, что результат пустой
    assert result == ""


@pytest.fixture
def spending_workday_data() -> pd.DataFrame:
    data_3 = {
        "День операции": [
            "Выходной",
            "Рабочий",
        ],
        "Сумма": [-374.46868686868686, -180.06194805194806],
    }
    df = pd.DataFrame(data_3)
    return df


def test_spending_by_workday() -> None:
    # Тестирование функции с категорией, для которой нет транзакций
    spending_by_workday_result = spending_by_workday(spending_by_workday, "Выходной")
    assert spending_by_workday_result == ""


def create_test_dataframe_1() -> pd.DataFrame:
    data = {
        "Дата операции": [
            "01.10.2023 10:00:00",  # Понедельник
            "02.10.2023 14:00:00",  # Вторник
            "03.10.2023 12:00:00",  # Среда
            "04.10.2023 16:00:00",  # Четверг
            "05.10.2023 18:00:00",  # Пятница
            "06.10.2023 11:00:00",  # Суббота
            "07.10.2023 19:00:00",  # Воскресенье
            "08.10.2023 20:00:00",  # Понедельник
            "09.10.2023 09:00:00",  # Вторник
            "10.10.2023 10:00:00",  # Среда
        ],
        "Сумма операции": [100, 200, 150, 400, 300, 500, 900, 600, 700, 800],
    }
    return pd.DataFrame(data)


# Тест для проверки работы с конкретной датой
def test_spending_by_workday_with_date() -> None:
    df = create_test_dataframe_1()
    test_date = "2023.10.10"  # Формат: YYYY-MM-DD
    result = spending_by_workday(df, test_date)

    result_dict = json.loads(result)

    # Проверка на наличие ключей и типов
    assert "Рабочий" in result_dict
    assert "Выходной" in result_dict
    assert isinstance(result_dict["Рабочий"], float)
    assert isinstance(result_dict["Выходной"], float)


# Тест для проверки обработки ошибки
def test_spending_by_workday_with_invalid_date() -> None:
    df = create_test_dataframe_1()
    result = spending_by_workday(df, "invalid_date_string")  # Неправильная дата

    # Проверка, что результат пустой
    assert result == ""


def test_report_to_file_default() -> None:
    @report_to_file(filename="test_report.txt")
    def report_to_file_default(x: str, y: str) -> str:
        """Тестирует корректное выполнение функции"""
        return x + y

    result = report_to_file_default(1, 2)
    assert result == 3


# if __name__ == "__main__":
#     pytest.main()
