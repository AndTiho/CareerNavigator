import json
from abc import abstractmethod, ABC
from typing import List
import os

from src.work_with_vacanсy import Vacancy


class AllToFiles(ABC):

    @abstractmethod
    def add_vacancy(self,keyword):
        pass

    @abstractmethod
    def delete_vacancy(self, keyword):
        pass

    @abstractmethod
    def get_vacancy(self, keyword):
        pass

class JSONSaver(AllToFiles):

    def __init__(self, filename: str = "vacancies.json"):
        self._data_dir = "data"
        self.__filename = os.path.join(self._data_dir, filename)
        self._data = []

    def _save_to_file(self) -> None:
        """Сохраняет данные в JSON-файл"""
        with open(self.__filename, 'a', encoding='utf-8') as file:
            json.dump(
                [v.to_dict() for v in self._data],
                file,
                ensure_ascii=False,
                indent=4
            )


    # def _save_to_file(self) -> None:
    #     """Сохраняет данные в JSON-файл"""
    #     with open(self.__filename, 'a', encoding='utf-8') as file:
    #         json.dump(
    #             self._data,
    #             file,
    #             ensure_ascii=False,
    #             indent=4
    #         )

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл, избегая дубликатов"""
        if not any(v.url == vacancy.url for v in self._data):
            self._data.append(vacancy)
            self._save_to_file()

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию по URL"""
        self._data = [v for v in self._data if v.url != vacancy.url]
        self._save_to_file()


    def get_all_vacancies(self) -> List[dict]:
        """Возвращает все вакансии"""
        return self._data

    def get_vacancy(self, keyword):
        pass