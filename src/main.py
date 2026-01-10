from src.db_config import db_config
from src.utils import create_database


def main():
    list_employers =['2180','2748','3529','8884','1858119','68587','1740','3192913','9498112','2523']
    params = db_config()
    create_database('vacancies', params)


if __name__ == '__main__':
    main()