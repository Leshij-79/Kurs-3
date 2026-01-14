from configparser import ConfigParser


def db_config(filename: str = "database.ini", section: str = "postgresql") -> dict:
    """
    Функция чтения файла настройки подключения к БД
    :param filename:  Имя файла настройки доступа к БД
    :param section: Искомая секция файла настройки
    :return: Словарь параметров подключения к БД
    """
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Секция {0} не найдена в {1} файле.".format(section, filename))
    return db
