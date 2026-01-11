from datetime import datetime


class Vacancy:
    """
    Класс вакансий
    """

    __slots__ = ('id', 'employer_id', 'name', 'salary_from', 'salary_to', 'area', 'published_at', 'alternate_url',
                 'snippet_requirement', 'snippet_responsibility', 'work_format', 'experience')

    def __init__(
        self, id: str, employer: dict, name: str, salary: dict, area: dict, published_at: datetime, alternate_url: str,
            snippet: dict, work_format: list, experience: dict):

        self.id = id
        self.employer_id = employer['id']
        self.name = name
        self.salary_from = self.__salary_from(salary)
        self.salary_to = self.__salary_to(salary)
        self.area = area["name"]
        self.published_at = published_at
        self.alternate_url = alternate_url
        self.snippet_requirement = snippet['requirement']
        self.snippet_responsibility = snippet['responsibility']
        self.work_format = self.__work_format(work_format)
        self.experience = experience['name']


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
            temp_dict["area"] = item.area
            temp_dict["published_at"] = item.published_at
            temp_dict["alternate_url"] = item.alternate_url
            temp_dict["snippet_requirement"] = item.snippet_requirement
            temp_dict["snippet_responsibility"] = item.snippet_responsibility
            temp_dict["work_format"] = item.work_format
            temp_dict["experience"] = item.experience
            list_of_vacancies.append(temp_dict)
        return list_of_vacancies


    def __salary_from(self, salary: dict) -> int:
        """
        Приватный метод обработки заработной платы от
        :param salary: Заработная плата в формате словаря
        :return: Заработная плата в формате целого числа
        """
        if salary["from"]:
            return salary["from"]
        else:
            return 0


    def __salary_to(self, salary: dict) -> int:
        """
        Приватный метод обработки заработной платы от
        :param salary: Заработная плата в формате словаря
        :return: Заработная плата в формате целого числа
        """
        if salary["to"]:
            return salary["to"]
        else:
            return 9999999

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

    def __lt__(self, other):
        return (self.salary_from < other.salary_from) or (self.salary_to < other.salary_to)

    def __gt__(self, other):
        return (self.salary_from > other.salary_from) or (self.salary_to > other.salary_to)

    def __eq__(self, other):
        return (self.salary_from == other.salary_from) or (self.salary_to == other.salary_to)

    def __ne__(self, other):
        return (self.salary_from != other.salary_from) or (self.salary_to != other.salary_to)

    def __le__(self, other):
        return (self.salary_from <= other.salary_from) or (self.salary_to <= other.salary_to)

    def __ge__(self, other):
        return (self.salary_from >= other.salary_from) or (self.salary_to >= other.salary_to)

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
            f"Формат работы - {self.work_format}, Опыт работы - {self.experience}"
        )
