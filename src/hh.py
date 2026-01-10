from typing import Any

import requests

def load_employers(employers) -> list[dict[str, Any]]:
    temp_list_employers =[]
    headers = {"User-Agent": "HH-User-Agent"}
    url_employers = "https://api.hh.ru/employers"
    for item in employers:
        url_employer = url_employers + "/" + item
        try:
            response = requests.get(url_employer, headers=headers)
        except Exception as e:
            print(f"Проверьте соединение. Ошибка - {e}")
            return []
        if response.status_code == 200:
            temp_list_employers.append(response.json())
        else:
            print(f"Работодатели - Ошибка подключения - {response.status_code}")
            return []
    return temp_list_employers


def load_vacancies(employers) -> list:
    url = "https://api.hh.ru/vacancies"
    vacancies = []
    headers = {"User-Agent": "HH-User-Agent"}
    params = {"page": 0, "per_page": 10, "only_with_salary": True, "currency": "RUR", "employer_id": ""}
    for_item = 0
    for item in employers:
        for_item += 1
        params["page"] = 0
        params["employer_id"] = item
        while params["page"] != 1:
            try:
                response = requests.get(url, headers=headers, params=params)
            except Exception as e:
                print(f"Проверьте соединение. Ошибка - {e}")
                return []
            if response == []:
                break
            if response.status_code == 200:
                vacancies.append(response.json()["items"])
            else:
                print(f"Вакансии - Ошибка подключения - {response.status_code} - {response.text}")
                return []
            params["page"] += 1
    return vacancies







#   https://api.hh.ru/employers/1959252  -- запрос данных по работодателю
#   https://api.hh.ru/vacancies?employer_id=1959252  -- запрос вакансий по организации