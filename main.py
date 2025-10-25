import json

from src.utils import parse_salary
from src.work_with_api import HeadHunterAPI
# from src.work_with_files import JSONSaver
from src.work_with_vacanсy import Vacancy


def user_interaction():
    print("Добро пожаловать в систему поиска вакансий!")

    # Шаг 1: Ввод поискового запроса
    search_query = 'Python' #input("Введите поисковый запрос для поиска вакансий: ")

    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    vacancies = [vacancy.to_dict() for vacancy in vacancies_list]

    # Шаг 2: Выбор действия
    while True:
        print("\nВыберите действие:")
        print("1. Получить топ N вакансий по зарплате")
        print("2. Найти вакансии по ключевому слову в описании")
        print("3. Выйти")

        choice = input("Ваш выбор: ")

        if choice == '1':
            try:
                top_n = int(input("Введите количество вакансий для топа: "))
                # Сортируем по зарплате в рублях
                sorted_vacancies = sorted(
                    vacancies,
                    key=lambda x: parse_salary(x),
                    reverse=True
                )
                print("\nТоп вакансий по зарплате в рублях:")
                for vac in sorted_vacancies[:top_n]:
                    salary_info = vac.get('salary', {})
                    currency = salary_info.get('currency', 'RUB')
                    print(f"Вакансия: {vac.get('name')}\n"
                          f"Зарплата: {salary_info.get('from', 'не указана')} {currency}\n"
                          f"URL: {vac.get('url')}\n"
                          f"Требования: {vac.get('requirements')}\n"
                      )
            except ValueError:
                print("Ошибка: введите число")

        elif choice == '2':
            keyword = input("Введите ключевое слово для поиска в описании: ")
            filtered_vacancies = [
                vac for vac in vacancies
                if keyword.lower() in vac['requirements'].lower()
            ]
            print(f"\nНайдено {len(filtered_vacancies)} вакансий:")
            for vac in filtered_vacancies:
                salary_info = vac.get('salary', {})
                currency = salary_info.get('currency', 'RUB')
                print(f"Вакансия: {vac.get('name')}\n"
                      f"Зарплата: {salary_info.get('from', 'не указана')} {currency}\n"
                      f"URL: {vac.get('url')}\n"
                      f"Требования: {vac.get('requirements')}\n"
                      )

        elif choice == '3':
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте еще раз.")




if __name__ == "__main__":
    user_interaction()


