class Vacancy:
    """
    Класс вакансий
    """

    __slots__ = ("id", "name", "area", "salary_from", "salary_to", "alternate_url", "snippet", "work_format")

    def __init__(
        self, id: str, name: str, area: str, salary: dict, alternate_url: str, snippet: dict, work_format: list
    ):
        """
        Инициализация класса вакансий
        :param id: ID вакансии
        :param name: Наименование вакансии
        :param area: Регион вакансии
        :param salary: Заработная плата по вакансии
        :param alternate_url: URL вакансии
        :param snippet: Описание вакансии
        :param work_format: Формат работы по вакансии
        """
        self.id = id
        self.name = name
        self.area = area["name"]
        self.salary_from = self.__salary_from(salary)
        self.salary_to = self.__salary_to(salary)
        self.alternate_url = alternate_url
        self.snippet = self.__snippet(snippet)
        self.work_format = self.__work_format(work_format)

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

    def __snippet(self, snippet: dict) -> str:
        """
        Формирование Описания вакансии
        :param snippet: Описание вакансии в формате словаря
        :return: Описание вкансии в формате строки
        """

        return f"{snippet['requirement']} {snippet['responsibility']}"

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
            f"ID вакансии - {self.id}, Вакансия - {self.name}, Территория - {self.area}, "
            f"Зарплата - {self.salary_from}-{self.salary_to}, URL вакансии - {self.alternate_url}, "
            f"Описание/требования по вакансии - {self.snippet}, Формат работы - {self.work_format}"
        )

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
            temp_dict["name"] = item.name
            temp_dict["area"] = item.area
            temp_dict["salary_from"] = item.salary_from
            temp_dict["salary_to"] = item.salary_to
            temp_dict["alternate_url"] = item.alternate_url
            temp_dict["snippet"] = item.snippet.replace("<highlighttext>", "").replace("</highlighttext>", "")
            temp_dict["work_format"] = item.work_format
            list_of_vacancies.append(temp_dict)
        return list_of_vacancies
