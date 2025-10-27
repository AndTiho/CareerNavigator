import json
from abc import abstractmethod, ABC
import requests

class Parser(ABC):

    @abstractmethod
    def _load_vacancies(self,keyword):
        pass

    @abstractmethod
    def get_vacancies(self, keyword):
        pass


class HeadHunterAPI(Parser):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = []

    def _load_vacancies(self, keyword):
        self.__params['text'] = keyword
        while self.__params.get('page') != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            if response.status_code == 200:
                vacancies = response.json()['items']
                self.__vacancies.extend(vacancies)
                self.__params['page'] += 1
            else:
                raise Exception(f"Ошибка при подключении к API: {response.status_code}")


    def get_vacancies(self, keyword):
        self._load_vacancies(keyword)
        return json.dumps(self.__vacancies)
