from web_app.bl.report.racing_report import build_report_for_db
from web_app.db.models.drivers import Driver
from web_app.db.models.result_race import ResultRace
from web_app.db.models.race import Race
from web_app.db.session import s
from config import FOLDER_PATH

import logging

log = logging.getLogger(__name__)


def load_report_to_db(folder: str = FOLDER_PATH):
    report = build_report_for_db(folder)

    race = Race(name='Monaco', year=2018)
    results = []
    for d in report:
        _driver = Driver(abbr=d.abbr, name=d.name, team=d.team)
        _result = ResultRace(
            driver=_driver,
            race=race,
            stage='Q3',
            end=d.end,
            start=d.start,
            position=d.position
        )
        results.append(_result)
    s.users_db.add_all(results)
    s.users_db.commit()
    log.info('Data loaded successfully.')
