class Employers:

    __slots__ = ('id', 'name', 'description', 'site_url', 'alternate_url', 'vacancies_url', 'open_vacancies')

    def __init__(self, id, name, description, site_url, alternate_url, vacancies_url, open_vacancies):
        self.id = id
        self.name = name
        self.description = description
        self.site_url = site_url
        self.alternate_url = alternate_url
        self.vacancies_url = vacancies_url
        self.open_vacancies = open_vacancies


    def __str__(self):
        return (f'ID работодателя - {self.id},\n'
                f'Наименование раотодателя - {self.name},\n'
                f'Описание работодателя - {self.description},\n'
                f'Сайт работодателя - {self.site_url},\n'
                f'Сайт работодателя на портале hh.ru - {self.alternate_url},\n'
                f'Список вакансий на портале hh.ru - {self.open_vacancies},\n'
                f'Количество открытых вакансий -  {self.vacancies_url}')


    @staticmethod
    def cast_to_object_list(employers: list) -> list[dict]:
        temp_list = []
        for employer in employers:
            temp_dict = {}
            temp_dict['id'] = employer.id
            temp_dict['name'] = employer.name
            temp_dict['description'] = employer.description
            temp_dict['site_url'] = employer.site_url
            temp_dict['alternate_url'] = employer.alternate_url
            temp_dict['vacancies_url'] = employer.vacancies_url
            temp_dict['open_vacancies'] = employer.open_vacancies
            temp_list.append(temp_dict)
        return temp_list