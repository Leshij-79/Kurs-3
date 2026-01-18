import psycopg2


class DBManager:
    """
    Класс работы с записями БД
    """
    def __init__(self, database: str, params: list[dict]) -> None:
        self.__database = database
        self.__params = params

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Метод получения списка всех компаний и количества вакансий у каждой компании
        :return: Список кортежей с данными
        """
        conn = psycopg2.connect(dbname=self.__database, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                "SELECT e.name, COUNT(v.vacancy_id) FROM employers e "
                "JOIN vacancies v ON e.employers_id = v.employers_id "
                "GROUP BY e.name"
            )
            companies_and_vacancies = cur.fetchall()
        conn.close()
        return companies_and_vacancies

    def get_all_vacancies(self) -> list[tuple]:
        """
        Метод получения списка всех вакансий с указанием названия компании, названия вакансии
        и зарплаты, а также ссылки на вакансию
        :return: Списко кортежей с данными
        """
        conn = psycopg2.connect(dbname=self.__database, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                "SELECT e.name, v.name, v.salary_from, v.salary_to, v.alternate_url "
                "FROM employers e JOIN vacancies v ON e.employers_id = v.employers_id"
            )
            companies_and_vacancies = cur.fetchall()
        conn.close()
        return companies_and_vacancies

    def get_avg_salary(self) -> list[tuple]:
        """
        Метод получения средней зарплаты по вакансиям
        :return: Список кортежей с данными
        """
        conn = psycopg2.connect(dbname=self.__database, **self.__params)
        with conn.cursor() as cur:
            cur.execute("SELECT AVG(salary_from), AVG(salary_to) FROM vacancies")
            avg_salary = cur.fetchall()
        conn.close()
        return avg_salary

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Метод получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return: Список кортежей с данными
        """
        conn = psycopg2.connect(dbname=self.__database, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                "SELECT name FROM vacancies "
                "WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies) "
                "AND salary_to > (SELECT AVG(salary_to) FROM vacancies)"
            )
            vacancies_with_higher_salary = cur.fetchall()
        conn.close()
        return vacancies_with_higher_salary

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """
        Метод получения списка всех вакансий, в названии которых содержатся переданные в метод слова
        :param keyword: Искомые в названии вакансий слова
        :return: Список кортежей с данными
        """
        #  получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        conn = psycopg2.connect(dbname=self.__database, **self.__params)
        with conn.cursor() as cur:
            cur.execute(f"SELECT name FROM vacancies WHERE name LIKE '%{keyword}%'")
            vacancies_with_keyword = cur.fetchall()
        conn.close()
        return vacancies_with_keyword
