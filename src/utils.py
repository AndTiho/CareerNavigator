from typing import Dict, Union


def parse_salary(vacancy: Dict[str, Union[Dict[str, Union[int, float, str]], int, float, str]]) -> Union[int, float]:
    """
    Парсит информацию о зарплате из вакансии и возвращает минимальное значение в рублях.

    Обрабатывает два формата данных:
    1. Вложенный словарь salary с полями from и currency
    2. Отдельные поля salary_from и currency

    При некорректных данных возвращает 0.
    """
    try:
        # Проверяем наличие вложенного словаря salary
        if "salary" in vacancy and isinstance(vacancy["salary"], dict):
            salary_info: Dict[str, Union[int, float, str]] = vacancy["salary"]
            currency: str = salary_info.get("currency", "RUB")
            amount: Union[int, float] = salary_info.get("from", 0)

            # Проверяем корректность данных
            if not isinstance(amount, (int, float)):
                print(f"Ошибка: некорректное значение зарплаты {amount}")
                return 0

            # Добавляем курс для UZS
            exchange_rates: Dict[str, float] = {"UZS": 0.0085}  # пример курса без API к ресурсу

            rate: float = exchange_rates.get(currency, 1)
            converted_amount: Union[int, float] = amount * rate

            return converted_amount

        # Проверяем наличие отдельных полей salary_from и salary_to
        elif "salary_from" in vacancy:
            currency: str = vacancy.get("currency", "RUB")
            amount: Union[int, float] = vacancy.get("salary_from", 0)

            if not isinstance(amount, (int, float)):
                print(f"Ошибка: некорректное значение зарплаты {amount}")
                return 0

            exchange_rates: Dict[str, float] = {"UZS": 0.0085}  # пример курса без API к ресурсу

            rate: float = exchange_rates.get(currency, 1)
            converted_amount: Union[int, float] = amount * rate

            return converted_amount

        return 0

    except (TypeError, ValueError) as e:
        print(f"Ошибка при парсинге зарплаты: {e}")
        return 0
