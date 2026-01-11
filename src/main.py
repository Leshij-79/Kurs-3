from src.DBManager import DBManager
from src.DBwork import create_database, save_data_to_database
from src.db_config import db_config
from src.employers import Employers
from src.hh import load_employers, load_vacancies
from src.utils import list_to_object_employers, list_to_object_vacancies
from src.vacancies import Vacancy


def main(list_employers=None):
    list_employers =['2180','2748','3529','8884','1959252','68587','1740','3192913','9498112','2523']
    params = db_config()
    create_database('vacancies', params)
    list_of_employers = load_employers(list_employers)
    list_of_vacancies = load_vacancies(list_employers)
    list_object_employers = list_to_object_employers(list_of_employers)
    list_object_vacancies = list_to_object_vacancies(list_of_vacancies)
    save_data_to_database(Employers.cast_to_object_list(list_object_employers),
                          Vacancy.cast_to_object_list(list_object_vacancies),
                          'vacancies', params)

    employers = DBManager('vacancies', params)

    companies_and_vacancies_count = employers.get_companies_and_vacancies_count()
    for item in companies_and_vacancies_count:
        print(f'Компания: {item[0]}, Количество вакансий: {item[1]}')

    all_vacancies = employers.get_all_vacancies()
    for item in all_vacancies:
        print(f'Работодатель - {item[0]},\nВакансия - {item[1]},\nЗарплата от - {item[2]},\nЗарплата до - {item[3]},\n'
              f'Ссылка на вакансию - {item[4]}\n')

    avg_salary = employers.get_avg_salary()
    for item in avg_salary:
        print(f'Средняя зарплата от - {round(item[0],2)}, Средсняя зарплата до - {round(item[1],2)}')

    vacancies_with_higher_salary = employers.get_vacancies_with_higher_salary()
    for item in vacancies_with_higher_salary:
        print(item[0])

    keyword = input('Введите искомое слово в названии вакансии: ')
    vacancies_with_keyword = employers.get_vacancies_with_keyword(keyword)
    if len(vacancies_with_keyword) == 0:
        print("Таких вакансий нет")
    else:
        for item in vacancies_with_keyword:
            print(item[0])


if __name__ == '__main__':
    main()