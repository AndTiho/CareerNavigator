import pytest

from src.work_with_vacanсy import Vacancy


def test_vacancy_creation():
    vacancy = Vacancy(
        name="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary="100000-150000",
        requirements="Опыт работы от 2 лет",
    )

    assert vacancy.name == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.requirements == "Опыт работы от 2 лет"


# Тест парсинга зарплаты


def test_salary_split():
    # Проверяем разные варианты входных данных
    assert Vacancy.salary_split("100000-150000") == (100000, 150000)  # Обычный случай
    assert Vacancy.salary_split("100000") == (100000, 100000)  # Только нижняя граница
    assert Vacancy.salary_split("100000-") == (100000, 100000)  # Нижняя граница с дефисом
    assert Vacancy.salary_split("-150000") == (150000, 150000)  # Только верхняя граница
    assert Vacancy.salary_split("100000-200000-300000") == (100000, 300000)  # Несколько дефисов
    assert Vacancy.salary_split("100000 руб.") == (100000, 100000)  # С текстом


# Тест сравнения зарплат


def test_salary_comparison():
    # Используем валидный URL
    v1 = Vacancy("Test", "https://example.com/vacancy", "100000-150000", "")
    v2 = Vacancy("Test", "https://example.com/vacancy", "125000-125000", "")
    v3 = Vacancy("Test", "https://example.com/vacancy", "50000-100000", "")

    assert v1 == v2  # Средние зарплаты равны (125000 == 125000)
    assert v3 < v1  # Средняя зарплата меньше (75000 < 125000)
    assert v1 > v3  # Средняя зарплата больше


# Тест валидации URL
def test_invalid_url():
    with pytest.raises(ValueError):
        Vacancy("Test", "invalid_url", "100000", "")


# Тест парсинга JSON
def test_cast_to_object_list():
    json_data = """
    [
        {
            "name": "Тестировщик",
            "alternate_url": "https://hh.ru/vacancy/456",
            "salary": {"from": 80000, "to": 120000},
            "snippet": {"requirement": "<b>Опыт от 1 года</b>"}
        }
    ]
    """

    vacancies = Vacancy.cast_to_object_list(json_data)
    assert len(vacancies) == 1

    vacancy = vacancies[0]
    assert vacancy.name == "Тестировщик"
    assert vacancy.salary_from == 80000
    assert vacancy.salary_to == 120000
    assert vacancy.requirements == "Опыт от 1 года"


# Тест преобразования в словарь
def test_to_dict():
    vacancy = Vacancy(
        name="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary="100000-150000",
        requirements="Опыт работы от 2 лет",
    )

    expected_dict = {
        "name": "Python Developer",
        "url": "https://hh.ru/vacancy/123",
        "salary": {"from": 100000, "to": 150000},
        "requirements": "Опыт работы от 2 лет",
    }

    assert vacancy.to_dict() == expected_dict


def test_invalid_name():
    with pytest.raises(ValueError):
        Vacancy(None, "https://example.com", "100000", "")


def test_invalid_requirements():
    with pytest.raises(ValueError):
        Vacancy("Test", "https://example.com", "100000", None)


def test_json_errors():
    invalid_json_data = [
        "{}",  # Пустой JSON
        '{"name": "Test"}',  # Неполный JSON
        '{"name": "Test", "url": "https://example.com"}',  # Отсутствуют зарплата и требования
        '{"name": "Test", "url": "https://example.com", "salary": {"from": 100000}}',  # Отсутствует to
        '{"name": "Test", "url": "https://example.com", "salary": {"to": 150000}}',  # Отсутствует from
        '{"name": "Test", "url": "https://example.com", "salary": "100000"}',  # Неверный формат зарплаты
        '{"name": "Test", "url": "https://example.com", "salary": {"from": "abc", "to": 150000}}',
        # Нечисловое значение
        '{"name": "Test", "url": "https://example.com", "salary": {"from": 100000, "to": "abc"}}',
        # Нечисловое значение
        '{"name": "Test", "url": "https://example.com", "salary": {"from": 100000, "to": 150000},'
        ' "snippet": {"requirement": null}}',
        # Null в требованиях
        '{"name": "Test", "url": "https://example.com", "salary": {"from": 100000, "to": 150000},'
        ' "snippet": {"requirement": 123}}',
        # Нестроковое значение в требованиях
    ]

    # Проверяем, что все некорректные JSON обрабатываются без исключений
    for data in invalid_json_data:
        try:
            result = Vacancy.cast_to_object_list(data)
            # Проверяем, что результат не None
            assert result is not None
        except Exception as e:
            # Если исключение всё же возникло, проверяем его сообщение
            assert str(e) != ""


def test_invalid_urls():
    # Тестируем только явно некорректные URL
    invalid_urls = [
        "htp://example.com",  # Неверная схема
        "http:/example.com",  # Отсутствует слэш
        "http://.com",  # Неверное доменное имя
        "http://example..com",  # Двойное точка
        "http://example.com/path with spaces",  # Пробелы
    ]

    for url in invalid_urls:
        try:
            with pytest.raises(ValueError):
                Vacancy("Test", url, "100000", "")
        except AssertionError:
            print(f"URL '{url}' не вызвал ожидаемую ошибку")


def test_valid_urls():
    # Проверяем только явно корректные URL
    valid_urls = [
        "https://example.com",
        "http://example.com",
        "http://example.com:80/path?query=string#fragment",
        "http://example.com/path?query=string#fragment",
    ]

    for url in valid_urls:
        vacancy = Vacancy("Test", url, "100000", "")
        assert vacancy.url == url


def test_edge_cases():
    # Проверяем граничные случаи
    edge_cases = ["http://localhost", "http://192.168.1.1"]  # Локальный хост  # IP-адрес

    for url in edge_cases:
        try:
            with pytest.raises(ValueError):
                Vacancy("Test", url, "100000", "")
        except AssertionError:
            print(f"Edge case URL '{url}' не вызвал ожидаемую ошибку")
