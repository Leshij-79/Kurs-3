from src.DBwork import create_database, save_data_to_database
from src.db_config import db_config
from src.hh import load_employers, load_vacancies
from src.utils import list_to_object_employers, list_to_object_vacancies


def main(list_employers=None):
    list_employers =['2180','2748','3529','8884','1959252','68587','1740','3192913','9498112','2523']
    params = db_config()
    create_database('vacancies', params)
    list_of_employers = load_employers(list_employers)
    list_of_vacancies = load_vacancies(list_employers)
    list_object_employers = list_to_object_employers(list_of_employers)
    list_object_vacancies = list_to_object_vacancies(list_of_vacancies)
    save_data_to_database(list_object_employers, list_object_vacancies, 'vacancies', params)


if __name__ == '__main__':
    main()