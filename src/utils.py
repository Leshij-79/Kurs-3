from typing import Any

import psycopg2
import requests


def create_database(database_name: str, params: dict):
    try:
        conn = psycopg2.connect(database="postgres", **params, connect_timeout=5)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("""
                            SELECT 1
                            FROM pg_database
                            WHERE datname = %s
                            """, (database_name,))
            is_DB = cur.fetchone() is not None
            if not is_DB:
                conn_new = psycopg2.connect(dbname='postgres', **params)
                conn_new.autocommit = True
                cur_new = conn_new.cursor()
                cur_new.execute(f"CREATE DATABASE {database_name}")
                cur_new.close()
                conn_new.close()

    except psycopg2.Error as e:
        print(f"Ошибка при проверке базы данных: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        if is_DB:
            cur.execute("""DROP SCHEMA public CASCADE""")
            cur.execute("""CREATE SCHEMA public""")
        cur.execute("""
            CREATE TABLE employers (
                employers_id SERIAL PRIMARY KEY,
                employer_id VARCHAR(7) NOT NULL,
                name VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                site_url VARCHAR(100) NOT NULL,
                alternate_url VARCHAR(255),
                vacancies_url VARCHAR(255),
                open_vacancies INT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                employers_id INT NOT NULL ,
                vacancy_id VARCHAR(10) NOT NULL,
                name VARCHAR NOT NULL,
                salary_from INT,
                salary_to INT,
                salary_currency VARCHAR(3),
                area_name VARCHAR NOT NULL,
                published_at DATE,
                alternate_url TEXT,
                snippet_requirement TEXT,
                snippet_responsibility TEXT,
                schedule_name VARCHAR,
                work_format_name VARCHAR,
                experience_name VARCHAR,
                FOREIGN KEY (employers_id) REFERENCES employers(employers_id) ON DELETE CASCADE
            )
        """)
    conn.commit()
    conn.close()


def list_to_object_vacancies(vacancies: list[dict]) -> list[Vacancy]:
    list_of_vacancies = []
    for vacancy_ in vacancies:
        if vacancy_["salary"] is None:
            vacancy_["salary"] = {"from": None, "to": None, "currency": "RUR", "gross": False}
        list_of_vacancies.append(
            Vacancy(
                vacancy_["id"],
                vacancy_["name"],
                vacancy_["area"],
                vacancy_["salary"],
                vacancy_["alternate_url"],
                vacancy_["snippet"],
                vacancy_["work_format"],
            )
        )
    return list_of_vacancies
