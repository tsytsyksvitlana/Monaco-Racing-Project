from argparse import ArgumentParser
import os

from web_app.config import DB_NAME, BASE_URL, POSTGRESS_DB
from config import FOLDER_PATH
from web_app.db.utils import create_database, init_database, drop_database
from web_app.bl.utils import load_report_to_db
from web_app.db.session import set_session, close_dbs

import logging

log = logging.getLogger(__name__)


def my_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Prepare for DB")
    parser.add_argument(
        "--files",
        required=False,
        help="Folder containing data files",
        default=FOLDER_PATH
    )
    parser.add_argument(
        "--db_name",
        required=False,
        help="Database name",
        default=DB_NAME
    )
    parser.add_argument(
        '--load',
        action='store_true',
        help='Insert Data DB'
    )
    parser.add_argument(
        '--init',
        action='store_true',
        help='Init DB'
    )
    parser.add_argument(
        'action',
        choices=['create', 'init', 'recreate', 'drop'],
        help='Choice action DB')
    return parser


def check_files_exist(folder_path: str, required_files: list) -> bool:
    for file_name in required_files:
        file_path = os.path.join(folder_path, file_name)
        if not os.path.isfile(file_path):
            return False
    return True


def main():
    args = my_parser().parse_args()

    if args.action == 'drop':
        drop_database(
            db_url=f'{BASE_URL}/{POSTGRESS_DB}',
            db_name=args.db_name
        )
        return

    if args.action == 'create':
        create_database(
            db_url=f'{BASE_URL}/{POSTGRESS_DB}',
            db_name=args.db_name
        )

    if args.action == 'recreate':
        drop_database(
            db_url=f'{BASE_URL}/{POSTGRESS_DB}',
            db_name=args.db_name
        )
        create_database(
            db_url=f'{BASE_URL}/{POSTGRESS_DB}',
            db_name=args.db_name
        )

    if args.action == 'init' or args.init:
        init_database(db_url=BASE_URL, db_name=args.db_name)

    if args.load:
        set_session()
        load_report_to_db(args.files)
        close_dbs()


if __name__ == '__main__':
    main()
