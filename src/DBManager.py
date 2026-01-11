import psycopg2


class DBManager:
    def __init__(self, database, params):
        self.__database = database
        self.__params = params


    def get_companies_and_vacancies_count(self):
        conn = psycopg2.connect(dbname=self.__database, **self.__params)
        with conn.cursor() as cur:
            cur.execute('SELECT e.name, COUNT(v.vacancy_id) FROM employers e '
                        'JOIN vacancies v ON e.employers_id = v.employers_id '
                        'GROUP BY e.name')
            companies_and_vacancies = cur.fetchall()
        conn.close()
        return companies_and_vacancies


    def get_all_vacancies(self):
        conn = psycopg2.connect(dbname=self.__database, **self.__params)
        with conn.cursor() as cur:
            cur.execute('SELECT e.name, v.name, v.salary_from, v.salary_to, v.alternate_url '
                        'FROM employers e JOIN vacancies v ON e.employers_id = v.employers_id')
            companies_and_vacancies = cur.fetchall()
        conn.close()
        return companies_and_vacancies


    def get_avg_salary(self):
        #  получает среднюю зарплату по вакансиям.
        pass


    def get_vacancies_with_higher_salary(self):
        #  получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        pass


    def get_vacancies_with_keyword(self):
        #  получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        pass