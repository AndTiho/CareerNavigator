import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List

from src.work_with_vacanсy import Vacancy


class AllToFiles(ABC):
    """
    Абстрактный базовый класс для работы с файлами вакансий
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в хранилище

        :param vacancy: объект вакансии для добавления
        """
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из хранилища

        :param vacancy: объект вакансии для удаления
        """
        pass

    @abstractmethod
    def get_vacancy(self, keyword: str) -> List[Dict]:
        """
        Получает вакансии по ключевому слову

        :param keyword: ключевое слово для поиска
        :return: список найденных вакансий
        """
        pass


class JSONSaver(AllToFiles):
    """
    Класс для работы с JSON-файлами вакансий
    """

    def __init__(self, filename: str = "vacancies.json"):
        """
        Инициализация класса

        :param filename: имя файла для хранения данных
        """
        self._data_dir: str = "data"
        self.__filename: str = os.path.join(self._data_dir, filename)
        self._data: List[Vacancy] = []

    def _save_to_file(self) -> None:
        """
        Сохраняет данные в JSON-файл

        Создает файл в указанной директории и записывает данные
        """
        with open(self.__filename, "a", encoding="utf-8") as file:
            json.dump([v.to_dict() for v in self._data], file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавляет вакансию в файл, избегая дубликатов

        Проверяет наличие вакансии по URL перед добавлением

        :param vacancy: объект вакансии для добавления
        """
        if not any(v.url == vacancy.url for v in self._data):
            self._data.append(vacancy)
            self._save_to_file()

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию по URL

        Обновляет список вакансий, исключая указанную вакансию

        :param vacancy: объект вакансии для удаления
        """
        self._data = [v for v in self._data if v.url != vacancy.url]
        self._save_to_file()

    def get_all_vacancies(self) -> List[Dict]:
        """
        Возвращает все вакансии

        :return: список всех вакансий в формате словаря
        """
        return [v.to_dict() for v in self._data]

    def get_vacancy(self, keyword: str) -> List[Dict]:
        """
        Метод для получения вакансии по ключевому слову

        :param keyword: ключевое слово для поиска
        :return: список найденных вакансий
        """
        pass
