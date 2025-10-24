import json
from abc import abstractmethod, ABC
import requests

class Parser(ABC):

    @abstractmethod
    def load_vacancies(self,keyword):
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
        self.__params = {'text': '', 'page': 0, 'per_page': 1}
        self.__vacancies = []

    def load_vacancies(self, keyword):
        self.__params['text'] = keyword
        while self.__params.get('page') != 5:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            vacancies = response.json()['items']
            self.__vacancies.extend(vacancies)
            self.__params['page'] += 1

    def get_vacancies(self, keyword):
        self.load_vacancies(keyword)
        return json.dumps(self.__vacancies)
