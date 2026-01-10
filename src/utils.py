import psycopg2


def create_database(database_name: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о каналах и видео."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
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
