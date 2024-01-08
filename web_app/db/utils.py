from sqlalchemy import (
    text,
    create_engine
)
from sqlalchemy.exc import ProgrammingError
import logging

log = logging.getLogger(__name__)


def create_database(db_url: str, db_name: str) -> None:
    try:
        with create_engine(
            db_url, isolation_level='AUTOCOMMIT'
        ).begin() as conn:
            conn.execute(text(f'CREATE DATABASE {db_name};'))
    except ProgrammingError:
        log.info(f'DataBase {db_name} EXISTS')
    else:
        log.info(f'Database {db_name} created successfully')


def drop_database(db_url: str, db_name: str) -> None:
    try:
        with create_engine(
            db_url, isolation_level='AUTOCOMMIT'
        ).begin() as conn:
            conn.execute(text(f'DROP DATABASE {db_name} WITH (FORCE);'))
    except ProgrammingError:
        log.info(f'DataBase {db_name} NOT EXISTS')
    else:
        log.info(f'Database {db_name} deleted successfully')


def init_database(db_url: str, db_name: str) -> None:
    import alembic.config
    import alembic.command
    alembic_config = alembic.config.Config('alembic.ini')
    alembic_config.set_main_option('sqlalchemy.url', f'{db_url}/{db_name}')
    alembic.command.upgrade(alembic_config, 'head')
    log.info(f'alembic upgrade db: {db_url}/{db_name}')
