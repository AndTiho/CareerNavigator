import os
import pytest
import json

from src.work_with_files import JSONSaver
from src.work_with_vacanсy import Vacancy


# Создаем тестовые вакансии
vacancy1 = Vacancy("Тестировщик", "https://test.com", "100000", "Опыт от 1 года")
vacancy2 = Vacancy("Разработчик", "https://dev.com", "150000", "Опыт от 2 лет")
vacancy3 = Vacancy("Аналитик", "https://test.com", "120000", "Опыт от 3 лет")  # Дубликат URL


@pytest.fixture
def saver():
    """Фикстура для создания временного экземпляра JSONSaver"""
    saver = JSONSaver("test_vacancies.json")
    filename = os.path.join(saver._data_dir, "test_vacancies.json")
    if os.path.exists(filename):
        os.remove(filename)
    return saver


def test_add_vacancy(saver):
    """Проверка добавления вакансии"""
    saver.add_vacancy(vacancy1)
    assert len(saver._data) == 1
    assert saver._data[0].name == vacancy1.name  # Сравниваем объекты Vacancy

    # Проверка на дубликаты
    saver.add_vacancy(vacancy3)  # Тот же URL
    assert len(saver._data) == 1  # Должен игнорироваться


def test_add_multiple_vacancies(saver):
    """Проверка добавления нескольких вакансий"""
    saver.add_vacancy(vacancy1)
    saver.add_vacancy(vacancy2)
    assert len(saver._data) == 2
    urls = [v.url for v in saver._data]  # Получаем URL из объектов Vacancy
    assert "https://test.com" in urls
    assert "https://dev.com" in urls


def test_delete_vacancy(saver):
    """Проверка удаления вакансии"""
    saver.add_vacancy(vacancy1)
    saver.add_vacancy(vacancy2)

    # Удаляем одну вакансию
    saver.delete_vacancy(vacancy1)
    assert len(saver._data) == 1
    assert saver._data[0].url == vacancy2.url  # Сравниваем объекты Vacancy

    # Пытаемся удалить несуществующую
    saver.delete_vacancy(vacancy3)
    assert len(saver._data) == 1


def test_get_all_vacancies(saver):
    """Проверка получения всех вакансий"""
    saver.add_vacancy(vacancy1)
    saver.add_vacancy(vacancy2)
    vacancies = saver.get_all_vacancies()
    assert len(vacancies) == 2
    urls = [v.url for v in vacancies]  # Получаем URL из объектов Vacancy
    assert "https://test.com" in urls
    assert "https://dev.com" in urls


def test_file_creation(saver):
    """Проверка создания файла"""
    filename = os.path.join(saver._data_dir, "test_vacancies.json")

    # Создаем директорию, если её нет
    if not os.path.exists(saver._data_dir):
        os.makedirs(saver._data_dir)

    saver.add_vacancy(vacancy1)
    assert os.path.exists(filename)