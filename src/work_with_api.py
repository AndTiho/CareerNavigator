import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import requests


class Parser(ABC):
    """
    Абстрактный базовый класс для парсеров вакансий
    """

    @abstractmethod
    def _load_vacancies(self, keyword: str) -> None:
        """
        Загружает вакансии по заданному ключевому слову

        :param keyword: ключевое слово для поиска вакансий
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> str:
        """
        Возвращает список вакансий в формате JSON

        :param keyword: ключевое слово для поиска вакансий
        :return: JSON-строка с вакансиями
        """
        pass


class HeadHunterAPI(Parser):
    """
    Класс для работы с API HeadHunter

    Предоставляет методы для получения вакансий с платформы HeadHunter
    """

    def __init__(self):
        self.__url: str = "https://api.hh.ru/vacancies"
        self.__headers: Dict[str, str] = {"User-Agent": "HH-User-Agent"}
        self.__params: Dict[str, Any] = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies: List[Dict[str, Any]] = []

    def _load_vacancies(self, keyword: str) -> None:
        """
        Загружает вакансии с HeadHunter по заданному ключевому слову
        """

        self.__params["text"] = keyword
        while self.__params.get("page") != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code == 200:
                vacancies = response.json()["items"]
                self.__vacancies.extend(vacancies)
                self.__params["page"] += 1
            else:
                raise Exception(f"Ошибка при подключении к API: {response.status_code}")

    def get_vacancies(self, keyword: str) -> str:
        """
        Получает и возвращает вакансии в формате JSON

        :param keyword: ключевое слово для поиска вакансий
        :return: JSON-строка с найденными вакансиями
        """
        self._load_vacancies(keyword)
        return json.dumps(self.__vacancies)
