import pytest

from src.utils import parse_salary


def test_parse_salary():
    # Тестовые данные
    vacancy_with_salary_dict = {
        'salary': {
            'currency': 'RUB',
            'from': 100000
        }
    }

    vacancy_with_salary_from = {
        'salary_from': 150000,
        'currency': 'RUB'
    }

    vacancy_with_uzs = {
        'salary': {
            'currency': 'UZS',
            'from': 1000000
        }
    }

    vacancy_with_invalid_salary = {
        'salary': {
            'currency': 'RUB',
            'from': 'сто тысяч'  # Некорректное значение
        }
    }

    vacancy_without_salary = {}

    # Тест с вложенным словарем salary
    assert parse_salary(vacancy_with_salary_dict) == 100000

    # Тест с отдельными полями salary_from и currency
    assert parse_salary(vacancy_with_salary_from) == 150000

    # Тест с конвертацией UZS в RUB
    assert parse_salary(vacancy_with_uzs) == 8500  # 1000000 * 0.0085

    # Тест с некорректным значением зарплаты
    assert parse_salary(vacancy_with_invalid_salary) == 0

    # Тест с отсутствующей информацией о зарплате
    assert parse_salary(vacancy_without_salary) == 0

    # Тест с отсутствующим полем currency
    vacancy_no_currency = {
        'salary': {
            'from': 200000
        }
    }
    assert parse_salary(vacancy_no_currency) == 200000  # Должен использовать RUB по умолчанию

    # Тест с неизвестной валютой
    vacancy_unknown_currency = {
        'salary': {
            'currency': 'USD',
            'from': 1000
        }
    }
    assert parse_salary(vacancy_unknown_currency) == 1000  # Должен использовать курс 1


# Можно также добавить параметризованные тесты
@pytest.mark.parametrize("input_data, expected", [
    ({'salary': {'currency': 'RUB', 'from': 50000}}, 50000),
    ({'salary_from': 75000, 'currency': 'RUB'}, 75000),
    ({'salary': {'currency': 'UZS', 'from': 500000}}, 4250),  # 500000 * 0.0085
    ({'salary': {'currency': 'RUB', 'from': 'abc'}}, 0),
    ({}, 0),
    ({'salary': {'from': 300000}}, 300000),  # currency по умолчанию RUB
    ({'salary': {'currency': 'EUR', 'from': 1000}}, 1000)  # неизвестный курс
])
def test_parse_salary_parametrized(input_data, expected):
    assert parse_salary(input_data) == expected
