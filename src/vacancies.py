from datetime import datetime
from typing import Any


class Vacancy:
    """
    Класс вакансий
    """

    __slots__ = (
        "id",
        "employer_id",
        "name",
        "salary_from",
        "salary_to",
        "salary_currency",
        "area",
        "published_at",
        "alternate_url",
        "snippet_requirement",
        "snippet_responsibility",
        "work_format",
        "experience",
        "schedule_name",
    )

    def __init__(
        self,
        id: str,
        employer: dict,
        name: str,
        salary: dict,
        area: dict,
        published_at: datetime,
        alternate_url: str,
        snippet: dict,
        work_format: list,
        experience: dict,
        schedule: dict,
    ) -> None:
        """
        Метод инициализации класса вакансий
        :param id: ID вакансии
        :param employer: ID работодателя
        :param name: Наименование вакансии
        :param salary: Словарь с данными по зарплате по вакансии
        :param area: Территория/регион вакансии
        :param published_at: Дата оупбликования вакансии
        :param alternate_url: Ссылка на вакансию на портале рh.ru
        :param snippet: Словарь с описанием и требованиями по вакансии
        :param work_format: Словарь с форматом работы
        :param experience: Словарь по требованию опыта по вакансии
        :param schedule: Словарь с видом работы
        """

        self.id = id
        self.employer_id = employer["id"]
        self.name = name
        self.salary_from = salary["from"]
        self.salary_to = salary["to"]
        self.salary_currency = salary["currency"]
        self.area = area["name"]
        self.published_at = published_at
        self.alternate_url = alternate_url
        self.snippet_requirement = snippet["requirement"]
        self.snippet_responsibility = snippet["responsibility"]
        self.work_format = self.__work_format(work_format)
        self.experience = experience["name"]
        self.schedule_name = schedule["name"]

    @staticmethod
    def cast_to_object_list(vacancies: list) -> list[dict]:
        """
        Формирование списка вакансий в формате список словарей из списка объектов Vacancy для записи в файл
        :param vacancies: Список объектов Vacancy
        :return: Вакансии в формате список словарей для записи в файл
        """
        list_of_vacancies = []
        for item in vacancies:
            temp_dict = {}
            temp_dict["id"] = item.id
            temp_dict["employer_id"] = item.employer_id
            temp_dict["name"] = item.name
            temp_dict["salary_from"] = item.salary_from
            temp_dict["salary_to"] = item.salary_to
            temp_dict["salary_currency"] = item.salary_currency
            temp_dict["area_name"] = item.area
            temp_dict["published_at"] = item.published_at
            temp_dict["alternate_url"] = item.alternate_url
            temp_dict["snippet_requirement"] = item.snippet_requirement
            temp_dict["snippet_responsibility"] = item.snippet_responsibility
            temp_dict["work_format_name"] = item.work_format
            temp_dict["experience_name"] = item.experience
            temp_dict["schedule_name"] = item.schedule_name
            list_of_vacancies.append(temp_dict)
        return list_of_vacancies

    def __work_format(self, work_format: list[dict]) -> str:
        """
        Формирование формата работы по вакансии
        :param work_format: Формат работы по вакансии в формате список словарей
        :return: Формат работы по вакансии в формате строки
        """
        if work_format == []:
            return "Не определён"
        else:
            return work_format[0]["name"]


    def __str__(self):
        """
        Формирование строки для печати объекта Vacancy
        :return: f-строка данных по вакансии
        """
        return (
            f"ID вакансии - {self.id}, ID работодателя - {self.employer_id},\n"
            f"Вакансия - {self.name}, Территория - {self.area},\n"
            f"Зарплата - {self.salary_from}-{self.salary_to},\n"
            f"URL вакансии - {self.alternate_url}, Опубликовано - {self.published_at},\n"
            f"Описание вакансии - {self.snippet_requirement},\n"
            f"Требование по вакансии - {self.snippet_responsibility},\n"
            f"Формат работы - {self.work_format}, График работы - {self.schedule_name}, "
            f"Опыт работы - {self.experience}"
        )
