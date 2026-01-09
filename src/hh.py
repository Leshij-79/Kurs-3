from abc import ABC, abstractmethod

import requests


class AbstraktHH(ABC):

    @abstractmethod
    def __load_vacancies(self):
        pass

    @abstractmethod
    def processing_vacancies(self, keyword, search_field, area, period, salary, only_with_salary):
        pass


class HeadHunterAPI(AbstraktHH):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        """
        Инициализация класса HeadHunterAPI
        """
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {}
        self.__vacancies = []

    def _AbstraktHH__load_vacancies(self) -> list:
        """
        Метод запроса вакансий с портала hh.ru в соотвествии с настройками пользователя
        Реализация приватного абстрактного метода
        :return: Список словарей с вакансиями
        """
        try:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        except Exception as e:
            print(f"Проверьте соединение. Ошибка - {e}")
            return []
        if response.status_code == 200:
            return response
        else:
            print(f"Ошибка подключения - {response.status_code}")
            return []

    def processing_vacancies(
        self,
        keyword: str = "",
        search_field: str = "",
        area: str = "",
        period: int = 0,
        salary: int = 0,
        only_with_salary: bool = False,
    ) -> list:
        """
        Метод формирования и обработки полученного ответа на запрос по вакансим с портала hh.ru
        :param keyword: Ключевое слово для поиска
        :param search_field: Поле по которому производится поиск
        :param area: Регион поиска
        :param period: Количество дней отбора
        :param salary: Предполагаемая заработная плата
        :param only_with_salary: Вывод вакансий в которых указана заработная плата
        :return: Список словарей с вакансиями
        """
        if keyword != "":
            self.__params["text"] = keyword
        if search_field != "":
            self.__params["search_field"] = search_field
        if area != "":
            self.__params["area"] = area
        if period != 0:
            self.__params["period"] = period
        if salary != 0:
            self.__params["salary"] = salary
        self.__params["page"] = 0
        self.__params["per_page"] = 10
        self.__params["only_with_salary"] = only_with_salary
        self.__params["currency"] = "RUR"
        while self.__params.get("page") != 1:
            response = self._AbstraktHH__load_vacancies()
            if response == []:
                return self.__vacancies
            vacancies = response.json()["items"]
            self.__vacancies.extend(vacancies)
            self.__params["page"] += 1
        return self.__vacancies
