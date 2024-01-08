from sqlalchemy import create_engine, Engine, select
from sqlalchemy.orm import sessionmaker, Session, SessionTransaction
from contextvars import ContextVar
import dataclasses
import typing as t
import logging

from web_app.config import BASE_URL, ENGINE_OPTIONS, DB_NAME


log = logging.getLogger(__name__)


@dataclasses.dataclass
class Pool:
    engine: Engine
    maker: sessionmaker


pools: dict[str, Pool] = {}


users_db = ContextVar[Session]('users_db')
users_db_transaction = ContextVar[SessionTransaction | None](
    'users_db_transaction', default=None
)


class EngineCreationException(Exception):
    pass


def get_pool_sync(db_url: str, options: dict[str, t.Any]) -> Pool:
    current = pools.get(db_url)
    if not current:
        autocommit_engine = create_engine(db_url, **options)
        check_connection(autocommit_engine)
        autocommit_maker = _create_sessionmaker(autocommit_engine)

        current = Pool(
            engine=autocommit_engine,
            maker=autocommit_maker,
        )
        pools[db_url] = current

    return current


def _create_sessionmaker(engine: Engine) -> sessionmaker:
    return sessionmaker(
        bind=engine,
        expire_on_commit=False,
        future=True,
    )


def check_connection(engine: Engine) -> None:
    try:
        with engine.connect() as conn:
            conn.execute(select(1))
        log.error('Connect is success')
    except Exception as exc:
        raise EngineCreationException(
            'Cannot connect to database provided'
        ) from exc


def close_dbs() -> None:
    log.info('Closing engines')
    for p in pools.values():
        p.engine.dispose()
    log.info('Engines closed')


def set_session() -> None:
    current_pool = get_pool_sync(f'{BASE_URL}/{DB_NAME}', ENGINE_OPTIONS)
    s.users_db = current_pool.maker()
    s.users_db.connection(execution_options={'isolation_level': 'AUTOCOMMIT'})


def pop_session() -> None:
    try:
        s.users_db.commit()
    except Exception:
        s.users_db.rollback()
    finally:
        s.users_db.close()


class Sessions:
    @property
    def users_db(self) -> Session:
        return users_db.get()

    @users_db.setter
    def users_db(self, value: Session) -> None:
        users_db.set(value)

    @property
    def users_db_transaction(self) -> SessionTransaction | None:
        return users_db_transaction.get()

    @users_db_transaction.setter
    def users_db_transaction(self, value: SessionTransaction) -> None:
        users_db_transaction.set(value)


s = Sessions()
