import psycopg2


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
                cur.execute(f"CREATE DATABASE {database_name}")
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
                vacancy_id VARCHAR(10) NOT NULL,
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
                FOREIGN KEY (employer_id) REFERENCES employers (employers_id) ON DELETE CASCADE
            )
        """)
    conn.commit()
    conn.close()


def save_data_to_database(list_object_employers: list, list_object_vacancies: list, database_name: str, params: dict):
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in list_object_employers:
            cur.execute(
                """
                INSERT INTO employers (title, views, subscribers, videos, channel_url)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING channel_id
                """,
                (channel_data['title'], channel_stats['viewCount'], channel_stats['subscriberCount'],
                 channel_stats['videoCount'], f"https://www.youtube.com/channel/{channel['channel']['id']}")
            )
            channel_id = cur.fetchone()[0]
            videos_data = channel['videos']
            for video in videos_data:
                video_data = video['snippet']
                cur.execute(
                    """
                    INSERT INTO videos (channel_id, title, publish_date, video_url)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (channel_id, video_data['title'], video_data['publishedAt'],
                     f"https://www.youtube.com/watch?v={video['id']['videoId']}")
                )

    conn.commit()
    conn.close()
