from argparse import ArgumentParser, Namespace
from typing import Literal, Any


def parser_data() -> tuple[Any, Literal['asc', 'desc'], Any]:
    parser = ArgumentParser()
    parser.add_argument(
        '--files', help='Show list of drivers by optional order',
        action='store')
    parser.add_argument('--asc', help='Order by asc', action='store_true')
    parser.add_argument('--desc', help='Order by desc', action='store_true')
    parser.add_argument(
        '--driver', help='Show statistic about driver', action='store')
    args: Namespace = parser.parse_args()

    order: Literal['asc', 'desc'] = 'desc' if args.desc else 'asc'
    return args.files, order, args.driver
