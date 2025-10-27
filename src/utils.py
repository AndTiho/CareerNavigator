def parse_salary(vacancy: dict) -> int | float:
    """
    Парсит информацию о зарплате из вакансии и возвращает минимальное значение в рублях
    """
    try:
        # Проверяем наличие вложенного словаря salary
        if 'salary' in vacancy and isinstance(vacancy['salary'], dict):
            salary_info = vacancy['salary']
            currency = salary_info.get('currency', 'RUB')
            amount = salary_info.get('from', 0)

            # Проверяем корректность данных
            if not isinstance(amount, (int, float)):
                print(f"Ошибка: некорректное значение зарплаты {amount}")
                return 0

            # Добавляем курс для UZS
            exchange_rates = {
                'UZS': 0.0085  # пример курса узбекского сума к рублю
            }

            rate = exchange_rates.get(currency, 1)
            converted_amount = amount * rate

            return converted_amount

        # Проверяем наличие отдельных полей salary_from и salary_to
        elif 'salary_from' in vacancy:
            currency = vacancy.get('currency', 'RUB')
            amount = vacancy.get('salary_from', 0)

            if not isinstance(amount, (int, float)):
                print(f"Ошибка: некорректное значение зарплаты {amount}")
                return 0

            exchange_rates = {
                'UZS': 0.0085  # добавляем курс для UZS
            }

            rate = exchange_rates.get(currency, 1)
            converted_amount = amount * rate

            return converted_amount

        return 0

    except (TypeError, ValueError) as e:
        print(f"Ошибка при парсинге зарплаты: {e}")
        return 0