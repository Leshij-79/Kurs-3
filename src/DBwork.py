import psycopg2


def create_database(database_name: str, params: dict) -> None:
    try:
        conn = psycopg2.connect(database="postgres", **params, connect_timeout=5)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                """
                            SELECT 1
                            FROM pg_database
                            WHERE datname = %s
                            """,
                (database_name,),
            )
            is_DB = cur.fetchone() is not None
            if not is_DB:
                cur.execute(f"CREATE DATABASE {database_name}")
    except psycopg2.Error as e:
        print(f"Ошибка при проверке базы данных: {e}")
        return False
    finally:
        if "conn" in locals():
            conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        if is_DB:
            cur.execute("""DROP SCHEMA public CASCADE""")
            cur.execute("""CREATE SCHEMA public""")
        cur.execute(
            """
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
        """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE vacancies (
                vacancies_id SERIAL PRIMARY KEY,
                vacancy_id VARCHAR(10) NOT NULL,
                employers_id int NOT NULL,
                employer_id INT NOT NULL ,
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
                FOREIGN KEY (employers_id) REFERENCES employers (employers_id) ON DELETE CASCADE
            )
        """
        )
    conn.commit()
    conn.close()


def save_data_to_database(list_object_employers: list, list_object_vacancies: list, database_name: str,
                          params: dict) -> None:
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in list_object_employers:
            emp_id = employer["id"]
            cur.execute(
                """
                INSERT INTO employers (employer_id, name, description, site_url, alternate_url, vacancies_url,
                                       open_vacancies)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING employers_id
                """,
                (
                    employer["id"],
                    employer["name"],
                    employer["description"],
                    employer["site_url"],
                    employer["alternate_url"],
                    employer["vacancies_url"],
                    employer["open_vacancies"],
                ),
            )
            employers_id = cur.fetchone()[0]
            for vacancy in list_object_vacancies:
                if vacancy["employer_id"] == emp_id:
                    cur.execute(
                        """
                        INSERT INTO vacancies (vacancy_id, employers_id, employer_id, name, salary_from, salary_to,
                                               salary_currency, area_name, published_at, alternate_url,
                                               snippet_requirement, snippet_responsibility, schedule_name,
                                               work_format_name, experience_name)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            vacancy["id"],
                            employers_id,
                            vacancy["employer_id"],
                            vacancy["name"],
                            vacancy["salary_from"],
                            vacancy["salary_to"],
                            vacancy["salary_currency"],
                            vacancy["area_name"],
                            vacancy["published_at"],
                            vacancy["alternate_url"],
                            vacancy["snippet_requirement"],
                            vacancy["snippet_responsibility"],
                            vacancy["schedule_name"],
                            vacancy["work_format_name"],
                            vacancy["experience_name"],
                        ),
                    )

    conn.commit()
    conn.close()
