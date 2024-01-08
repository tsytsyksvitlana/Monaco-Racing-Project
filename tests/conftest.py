import pytest

import typing as t

from flask import Flask

from web_app.app import create_app
from web_app.db.utils import drop_database, create_database, init_database
from web_app.config import BASE_URL, POSTGRESS_DB, DB_NAME
from web_app.db.session import close_dbs, set_session, pop_session
from web_app.bl.utils import load_report_to_db
from config import FOLDER_PATH_FOR_DB


DB_URL = f'{BASE_URL}/{POSTGRESS_DB}'
TEST_DB = f'{BASE_URL}/{DB_NAME}'


@pytest.fixture(scope='session')
def app() -> t.Generator[Flask, t.Any, None]:
    app = create_app()
    yield app


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    create_database(db_url=DB_URL, db_name=DB_NAME)
    print('CREATE DB')
    init_database(TEST_DB, db_name=DB_NAME)
    set_session()
    load_report_to_db(FOLDER_PATH_FOR_DB)
    pop_session()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    try:
        close_dbs()
    finally:
        print('\nCLOSE DB')
    try:
        drop_database(db_url=DB_URL, db_name=DB_NAME)
    finally:
        print('DROP DB')
