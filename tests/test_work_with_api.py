from unittest.mock import MagicMock, patch

import pytest

from src.work_with_api import HeadHunterAPI


# Создаем фикстуру для создания объекта парсера
@pytest.fixture
def hh_parser():
    return HeadHunterAPI()


def test_init_params(hh_parser):
    # Проверяем URL
    assert hh_parser._HeadHunterAPI__url == "https://api.hh.ru/vacancies"

    # Проверяем headers
    assert hh_parser._HeadHunterAPI__headers == {"User-Agent": "HH-User-Agent"}

    # Проверяем параметры запроса
    assert hh_parser._HeadHunterAPI__params == {"text": "", "page": 0, "per_page": 100}

    # Проверяем пустой список вакансий
    assert hh_parser._HeadHunterAPI__vacancies == []


# @patch('requests.get')
# def test_load_vacancies(mock_get, hh_parser):
#     # Создаем тестовый ответ
#     mock_response = MagicMock()
#     mock_response.status_code = 200
#     mock_response.json.return_value = {'items': [{'id': 1}, {'id': 2}]}
#
#     # Заставляем mock возвращать наш тестовый ответ
#     mock_get.return_value = mock_response
#
#     # Вызываем метод
#     hh_parser._load_vacancies('Python')
#
#     # Проверяем параметры запроса
#     mock_get.assert_called_with(
#         'https://api.hh.ru/vacancies',
#         headers={'User-Agent': 'HH-User-Agent'},
#         params={'text': 'Python', 'page': 0, 'per_page': 100}
#     )
#
#     # Проверяем результат
#     assert hh_parser._HeadHunterAPI__vacancies == [{'id': 1}, {'id': 2}]
#
#
@patch("requests.get")
def test_load_vacancies_error(mock_get, hh_parser):
    # Создаем ответ с ошибкой
    mock_response = MagicMock()
    mock_response.status_code = 404

    mock_get.return_value = mock_response

    # Проверяем, что поднимается исключение
    with pytest.raises(Exception) as excinfo:
        hh_parser._load_vacancies("Python")

    # Проверяем сообщение об ошибке
    assert str(excinfo.value) == "Ошибка при подключении к API: 404"
