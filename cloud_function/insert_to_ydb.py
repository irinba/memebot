import ydb
from typing import Dict, Any
from ydb import Session


def format_kwargs(**kwargs: Any) -> Dict[str, Any]:
    """
    Форматирует ключи словаря для использования в запросах к базе данных.

    Данная функция преобразует ключи аргументов, добавляя к ним префикс '$', что необходимо для их использования
    в качестве переменных в SQL-запросах к YDB.

    :param kwargs: Произвольный набор пар ключ-значение.
    :return: Словарь с ключами, отформатированными для использования в SQL-запросах.
    """
    return {"${}".format(key): value for key, value in kwargs.items()}


def insert_data_to_ydb(session: Session, query: str, **kwargs: Any) -> None:
    """
    Выполняет вставку данных в базу данных Yandex Database (YDB).

    Функция готовит SQL-запрос, используя предоставленную строку запроса и аргументы, и выполняет его в рамках
    транзакции, обеспечивая надежное и консистентное обновление данных.

    :param session: Сессия подключения к YDB.
    :param query: Строка SQL-запроса для выполнения.
    :param kwargs: Аргументы, которые будут использоваться в SQL-запросе.
    """
    prepared_query = session.prepare(query)
    session.transaction(ydb.SerializableReadWrite()).execute(
        prepared_query, format_kwargs(**kwargs),
        commit_tx=True
    )
