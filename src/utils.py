from src.employers import Employers
from src.vacancies import Vacancy


def list_to_object_vacancies(vacancies: list[list[dict]]) -> list[Vacancy]:
    list_of_vacancies = []
    for vacancy in vacancies:
        for vacancy_ in vacancy:
            if vacancy_["salary"] is None:
                vacancy_["salary"] = {"from": None, "to": None, "currency": "RUR", "gross": False}
            list_of_vacancies.append(
                Vacancy(
                    vacancy_["id"],
                    vacancy_["employer"],
                    vacancy_["name"],
                    vacancy_["salary"],
                    vacancy_["area"],
                    vacancy_["published_at"],
                    vacancy_["alternate_url"],
                    vacancy_["snippet"],
                    vacancy_["work_format"],
                    vacancy_["experience"],
                    vacancy_["schedule"]
                )
            )
    return list_of_vacancies


def list_to_object_employers(employers: list[dict]) -> list[Employers]:
    list_of_employers = []
    for employer in employers:
        list_of_employers.append(
            Employers(
                employer["id"],
                employer["name"],
                employer["description"],
                employer["site_url"],
                employer["alternate_url"],
                employer["vacancies_url"],
                employer["open_vacancies"]
            )
        )
    return list_of_employers


