import json
import re
from typing import List, Union
from urllib.parse import urlparse


class Vacancy:
    """
    Класс для работы с вакансиями.

    Отвечает за создание и обработку объектов вакансий, включая валидацию данных,
    парсинг зарплаты и проверку URL.
    """

    __slots__ = ["name", "url", "salary_from", "salary_to", "requirements"]

    def __init__(self, name: str, url: str, salary: Union[str, int], requirements: str):
        """
        Инициализация объекта вакансии.

        :param name: название вакансии
        :param url: ссылка на вакансию
        :param salary: информация о зарплате (строка или число)
        :param requirements: требования к кандидату
        """
        self.name = Vacancy.__validate_str(name)

        if not self.__is_valid_url(url):
            raise ValueError("Неверный URL")
        self.url = url

        self.salary_from, self.salary_to = Vacancy.salary_split(salary)

        self.requirements = Vacancy.__validate_str(requirements)

    @property
    def amount(self) -> float:
        """
        Возвращает среднюю зарплату.

        :return: среднее значение между минимальной и максимальной зарплатой
        """
        return (self.salary_from + self.salary_to) / 2

    def __eq__(self, other: object) -> bool:
        """
        Сравнение вакансий по средней зарплате.

        :param other: объект для сравнения
        :return: True если зарплаты равны, иначе False
        """
        if isinstance(other, Vacancy):
            return self.amount == other.amount
        return False

    def __lt__(self, other: object) -> bool:
        """
        Сравнение вакансий по средней зарплате (меньше).

        :param other: объект для сравнения
        :return: True если зарплата меньше, иначе False
        """
        if isinstance(other, Vacancy):
            return self.amount < other.amount
        return NotImplemented

    def __le__(self, other: object) -> bool:
        """
        Сравнение вакансий по средней зарплате (меньше или равно).

        :param other: объект для сравнения
        :return: True если зарплата меньше или равна, иначе False
        """
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: object) -> bool:
        """
        Сравнение вакансий по средней зарплате (больше).

        :param other: объект для сравнения
        :return: True если зарплата больше, иначе False
        """
        return not self.__le__(other)

    def __ge__(self, other: object) -> bool:
        """
        Сравнение вакансий по средней зарплате (больше или равно).

        :param other: объект для сравнения
        :return: True если зарплата больше или равна, иначе False
        """
        return not self.__lt__(other)

    def __ne__(self, other: object) -> bool:
        """
        Сравнение вакансий по средней зарплате (не равно).

        :param other: объект для сравнения
        :return: True если зарплаты не равны, иначе False
        """
        return not self.__eq__(other)

    @classmethod
    def cast_to_object_list(cls, data: str) -> List["Vacancy"]:
        """
        Преобразует JSON-строку в список объектов Vacancy

        :param data: JSON-строка с данными о вакансиях
        :return: список объектов Vacancy
        """
        vacancy_list: List[Vacancy] = []
        try:
            result = json.loads(data)

            for item in result:
                try:
                    if item.get("salary") is not None:
                        salary_info = item.get("salary", {})
                        salary_from = salary_info.get("from", 0)
                        salary_to = salary_info.get("to", 0)
                    else:
                        salary_from = 0
                        salary_to = 0

                    formatted_salary = f"{salary_from} - {salary_to}"

                    # Получение требований
                    snippet = item.get("snippet", {})
                    raw_requirements = snippet.get("requirement", "")  # Получаем требования

                    # Проверка на None и очистка HTML
                    if raw_requirements is None:
                        clean_requirements = ""
                    else:
                        clean_requirements = re.sub(r"<[^>]+>", "", raw_requirements)
                        clean_requirements = clean_requirements.replace("\n", " ").strip()

                    # Создание объекта вакансии
                    vacancy = cls(
                        name=item.get("name", ""),
                        url=item.get("alternate_url", item.get("url", "")),
                        salary=formatted_salary,
                        requirements=clean_requirements,
                    )
                    vacancy_list.append(vacancy)
                except ValueError as e:
                    print(f"Ошибка при создании вакансии: {e}")
                except Exception as e:
                    print(f"Произошла ошибка: {e}")
        except json.JSONDecodeError:
            print("Ошибка при парсинге JSON данных")
        except Exception as e:
            print(f"Критическая ошибка: {e}")

        return vacancy_list

    @staticmethod
    def __is_valid_url(url: str) -> bool:
        """
        Проверяет валидность URL-адреса

        :param url: URL для проверки
        :return: True если URL валиден, иначе False
        """
        try:
            result = urlparse(url)
            # Базовая проверка схемы и сетевого расположения
            if not result.scheme or not result.netloc:
                return False

            # Проверка схемы на допустимые значения
            if result.scheme not in ["http", "https"]:
                return False

            # Регулярное выражение для проверки формата домена
            domain_regex = re.compile(r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")

            # Проверка домена
            if not domain_regex.match(result.netloc.split(":")[0]):
                return False

            # Проверка на пробелы в URL
            if " " in url:
                return False

            return True
        except ValueError:
            return False

    @staticmethod
    def __validate_str(some_str: str) -> str:
        """
        Проверяет, что переданная переменная является строкой

        :param some_str: проверяемая строка
        :return: исходная строка
        :raises ValueError: если параметр не является строкой
        """
        if not isinstance(some_str, str):
            raise ValueError("Неверно задан параметр.")
        return some_str

    @staticmethod
    def salary_split(salary: Union[str, int]) -> tuple[int, int]:
        """
        Разбивает строку с зарплатой на минимальное и максимальное значение

        :param salary: строка или число с информацией о зарплате
        :return: кортеж с минимальной и максимальной зарплатой
        """
        if isinstance(salary, str):
            try:
                cleaned = re.sub(r"[^\d-]", "", salary)
                parts = cleaned.split("-")
                parts = [p for p in parts if p]

                if len(parts) == 1:
                    salary_from = int(parts[0])
                    salary_to = salary_from
                    return salary_from, salary_to

                if len(parts) >= 2:
                    salary_from = int(parts[0])
                    salary_to = int(parts[-1])
                    return salary_from, salary_to

                raise ValueError("Недостаточно числовых значений")

            except ValueError as e:
                print(f"Произошла ошибка: {e}")
                print("Значение зарплаты установлено 0")
                return 0, 0
        return 0, 0

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта вакансии

        :return: форматированная строка с данными о вакансии
        """
        return (
            f'"{self.name}"\n'
            f'"{self.url}"\n'
            f'"{self.salary_from} - {self.salary_to}"\n'
            f'"Требования: {self.requirements}"'
        )

    def to_dict(self) -> dict:
        """
        Преобразует объект вакансии в словарь

        :return: словарь с данными о вакансии
        """
        return {
            "name": self.name,
            "url": self.url,
            "salary": {"from": self.salary_from, "to": self.salary_to},
            "requirements": self.requirements,
        }
