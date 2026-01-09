from src.db_config import db_config
from src.utils import create_database


def main():
    params = db_config()
    create_database('vacancies', params)