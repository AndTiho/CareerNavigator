import json
import re


class Vacancy:
    """ Класс занимается откровенной дичью. В его функционал входят:
    создание объекта 'Вакансия' который инициируются через имя, ссыль на вак, З/П, требования, задачи.
    """
    def __init__(self, name, url, salary, requirement):
        """Конструкт....не ну тут вроде понятно всё, кроме З/П собственно....
        З/П создана с учётом если указана строчная передача данных типа '100 000-150 000 руб.'-- эта дичь разбивается
        на две части по дефису, удаляет всё лишнее и закидывает ИНТЫ в две части ОТ и ДО. Почему?
        Я типа готовлюсь к приёму данных от HH.ru где ЗП идёт в виде Salary:{from: 10, to:100}."""

        self.name = Vacancy.__validate_str(name)

        if not self.__is_valid_url(url):
            raise ValueError("Неверный URL")
        self.url = url

        self.salary_from, self.salary_to = Vacancy.salary_split(salary)

        self.requirement = Vacancy.__validate_str(self._clean_html(requirement)) if requirement is not None else ''

    @property
    def amount(self):
        return (self.salary_from + self.salary_to) / 2


    def __eq__(self, other):
        if isinstance(other, Vacancy):
            return self.amount == other.amount
        return False

    def __lt__(self, other):
        if isinstance(other, Vacancy):
            return self.amount < other.amount
        return NotImplemented

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def cast_to_object_list(cls, data: str):
        vacancy_list = []
        try:
            result = json.loads(data)

            for item in result:
                try:

                    if item.get('salary') is not None:
                        salary_info = item.get('salary', {})
                        salary_from = salary_info.get('from', 0)
                        salary_to = salary_info.get('to', 0)
                    else:
                        salary_from = 0
                        salary_to = 0

                    formatted_salary = f"{salary_from} - {salary_to}"

                    # Получаем требования и обязанности
                    snippet = item.get('snippet', {})
                    requirement = snippet.get('requirement', '')
                    responsibility = snippet.get('responsibility', '')

                    vacancy = cls(
                        name=item.get('name', ''),
                        url=item.get('url', ''),
                        salary=formatted_salary,
                        requirement=requirement
                    )
                    vacancy_list.append(vacancy)
                except ValueError as e:
                    print(f"Ошибка при создании вакансии: {e}")

        except json.JSONDecodeError:
            print("Ошибка при парсинге JSON данных")

        return vacancy_list


    @staticmethod
    def __is_valid_url(url):
        from urllib.parse import urlparse
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False


    @staticmethod
    def __validate_str(some_str):
        if not isinstance(some_str, str):
            raise ValueError("Неверно задан параметр.")
        return some_str

    @staticmethod
    def salary_split(salary):
        if Vacancy.__validate_str(salary):
            try:
                salary_from_full = salary.split('-')[0].replace(' ', '')
                salary_from = int(re.sub(r'\D', '', salary_from_full))
                salary_to_full = salary.split('-')[1].replace(' ', '')
                salary_to = int(re.sub(r'\D', '', salary_to_full))
                return salary_from, salary_to
            except ValueError:
                print('Не корректно задан параметр, значение зарплаты установлено 0')
                return 0, 0
        return None

    def __str__(self):
        return f'"{self.name}"\n"{self.url}"\n"{self.salary_from} - {self.salary_to}"\n"Требования: {self.requirement}"'

    def _clean_html(self, text):
        if text is None:
            return ''
        return re.sub(r'<[^>]+>', '', text)