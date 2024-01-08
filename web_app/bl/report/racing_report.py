import re
from dataclasses import asdict
from datetime import datetime
from functools import cmp_to_key
from pathlib import Path

from web_app.bl.report.models import DriverTimeTeamType, MessageData
from web_app.bl.report.models import DriverData
from typing import Literal

from config import (
    FILE_NAME_START, FILE_NAME_END, FILE_NAME_ABBREVIATIONS)

DATE_FMT = '%Y-%m-%d_%H:%M:%S.%f'
PATTERN = re.compile(r"([A-Z]*)(.*)")


ITEM_TYPE = dict[str, DriverTimeTeamType]
REPORT_TYPE = list[tuple[str, DriverTimeTeamType]]

CMP_TYPE = tuple[str, DriverTimeTeamType]

FORMAT_MESSAGE = "{pos} | {name} | {team} | {time}"

FAVORITE_GRADE = 15


def parser_abbr(
    folder_path: str, file_name: str = FILE_NAME_ABBREVIATIONS
) -> dict[str, dict[str, str]]:
    """Function creates a dict
    {driver_abbr: {'driver': 'full_name', 'team': 'driver_team'}, ...}
    from a string
    '{driver_abbr}_{full_name}_{driver_team}'.

    Example SVF_Sebastian Vettel_FERRARI ->
    {'SVF': {'driver': 'Sebastian Vettel', 'team': 'FERRARI'}}.
    """

    file_path = Path(folder_path, file_name)
    with open(file_path, "r") as f:
        data = f.readlines()
    result = {}
    for _data in data:
        abbr, driver, team = _data.rstrip().split('_')
        result[abbr] = {'driver': driver, 'team': team}
    return result


def parser_log(folder_path: str, file_name: str) -> dict[str, datetime]:
    """Function returns a dict
    {driver_abbr: time} from a string '{driver_abbr}_{time}'
    """

    file_path = Path(folder_path, file_name)
    with open(file_path, "r") as f:
        data = f.readlines()
    result = {}
    for line in data:
        res = PATTERN.match(line)
        assert res is not None
        abbr, time = res.groups()
        result[abbr] = datetime.strptime(time.rstrip(), DATE_FMT)
    return result


def parser_log_start(
    folder_path: str, file_name: str = FILE_NAME_START
) -> dict[str, datetime]:
    return parser_log(folder_path=folder_path, file_name=file_name)


def parser_log_end(
    folder_path: str, file_name: str = FILE_NAME_END
) -> dict[str, datetime]:
    return parser_log(folder_path=folder_path, file_name=file_name)


def build_report(folder_path: str) -> ITEM_TYPE:
    """Function builds report, returns a dict
    {driver_name: {
        'time': t_secons,
        'team': team,
        'driver_id': abbr,
        'driver': driver_name
        },
    }
    """

    dict_abbr = parser_abbr(folder_path)
    start_log = parser_log_start(folder_path)
    end_log = parser_log_end(folder_path)
    report_dict: ITEM_TYPE = {}
    for abbr, data in dict_abbr.items():
        driver = data['driver']
        team = data['team']
        time = (end_log[abbr] - start_log[abbr]).total_seconds()
        report_dict[driver] = DriverTimeTeamType(
            time=time, team=team, driver_id=abbr, driver=driver
        )
    return report_dict


def format_time(seconds: float) -> str:
    """Function formats time given in seconds into minutes:seconds.3digits.
    Minus is used for drivers which was rejected.
    """

    _minutes, _sec = divmod(seconds, 60)
    return f'{"-" if _minutes < 0 else ""}{abs(_minutes):02.0f}:{_sec:06.3f}'


def cmp_result(next_item: CMP_TYPE, prev_item: CMP_TYPE) -> int:
    """Function sorts 2 items, for positive in asc, for negative in desc.
    """

    _next, _prev = next_item[1]['time'], prev_item[1]['time']
    if _next > 0 and _prev > 0:
        return int(_next - _prev)
    return int(_prev - _next)


def get_report(folder_path: str) -> REPORT_TYPE:
    """Function returns sorted report,
    [(driver_name: {'time': t_secons,'team': team}),]
    """

    report_dict = build_report(folder_path)
    result = sorted(report_dict.items(), key=cmp_to_key(cmp_result))
    return result


def _full_report_with_id(folder_path: str) -> dict[str, dict[str, object]]:
    result = {}
    for pos, (_, data) in enumerate(get_report(folder_path), 1):
        result[data['driver_id']] = data | {'position': pos}

    return result


def result_driver(report: REPORT_TYPE, driver: str) -> str:
    """Function returns statistic for single driver as a string
    'pos | driver_name | t_secons | team'
    """
    if (_driver := _result_driver(report, driver)) is None:
        return f"Driver {driver} not found"
    return FORMAT_MESSAGE.format(**asdict(_driver))


def _result_driver(report: REPORT_TYPE, driver: str) -> MessageData | None:
    """Function returns statistic for single driver as a MessageData
    """
    for pos, (name, data) in enumerate(report, 1):
        team = data['team']
        time = format_time(data['time'])
        if driver == name:
            return MessageData(pos=pos, name=name, team=team, time=time)
    return None


def result_drivers(
    report: REPORT_TYPE, order: Literal['asc', 'desc']
) -> list[str]:
    """Function returns statistic for all driver as list strings
    ['pos | driver_name | t_secons | team',]
    """

    messages = []
    for data in _result_drivers(report, order):
        messages.append(FORMAT_MESSAGE.format(**asdict(data)))
        if data.pos == FAVORITE_GRADE:
            messages.append('_' * len(messages[-1]))
    return messages


def _result_drivers(
    report: REPORT_TYPE, order: Literal['asc', 'desc']
) -> list[MessageData]:
    """Function returns statistic for all driver as list MessageData
    """
    drivers = []
    for pos, (name, data) in enumerate(report, 1):
        team = data['team']
        time = format_time(data['time'])
        drivers.append(MessageData(pos=pos, name=name, team=team, time=time))

    if order == 'desc':
        drivers.reverse()
    return drivers


def print_report(
    folder_path: str, driver: str | None, order: Literal['asc', 'desc']
) -> None:
    """Function print to console statistic
    about single driver or report of racing for all drivers.
    """

    report = get_report(folder_path)
    if driver is not None:
        print(result_driver(report, driver))
    else:
        messages = result_drivers(report, order)
        print('\n'.join(messages))


def build_report_for_db(path: str) -> list[DriverData]:
    report_data = {}
    abbrs = parser_abbr(path)
    starts = parser_log_start(path)
    ends = parser_log_end(path)
    for abbr, driver_data in abbrs.items():
        name = driver_data["driver"]
        team = driver_data['team']
        _result = (ends[abbr] - starts[abbr]).total_seconds()
        _start = int(starts[abbr].timestamp())
        _end = int(ends[abbr].timestamp())
        report_data[abbr] = DriverData(
            abbr=abbr, name=name, team=team, start=_start, end=_end,
            result=_result
        )
    sorted_report = sorted(
        report_data.values(),
        key=lambda item: (item.result <= 0, abs(item.result)),
    )
    for pos, driver in enumerate(sorted_report, 1):
        driver.position = pos

    return sorted_report
