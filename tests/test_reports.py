import pandas as pd
import pytest

from src.reports import spending_by_weekday, spending_by_workday


@pytest.fixture
def spending_data() -> None:
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


@pytest.fixture
def spending_workday_data() -> None:
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


if __name__ == "__main__":
    pytest.main()
