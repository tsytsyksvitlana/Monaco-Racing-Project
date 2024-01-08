from sqlalchemy import select

from web_app.db.models.drivers import Driver
from web_app.db.models.result_race import ResultRace
from web_app.db.models.race import Race
from web_app.db.session import s


def get_report_from_db(
        driver_id: str | None, order: str = 'asc',  year: int = 2018,
        stage: str = 'Q3'
) -> list[dict[str, str | str]] | list[object]:
    stage = 'Q3'
    year = 2018

    query = (
        select(ResultRace, Driver)
        .join(Driver)
        .join(Race)
        .where(Race.year == year)
        .where(ResultRace.stage == stage)
    )
    if order == 'asc':
        query = query.order_by(ResultRace.position.asc())
    else:
        query = query.order_by(ResultRace.position.desc())
    if driver_id:
        query = query.where(Driver.abbr == driver_id)
    result_race = s.users_db.scalars(query).all()
    try:
        report = [
            {
                'abbr': result.driver.abbr,
                'driver': result.driver.name,
                'position': result.position,
                'team': result.driver.team,
                'time': (result.end - result.start),
            }
            for result in result_race
        ]
    except IndexError:
        return result_race
    return report


def get_report_as_dict(
    driver_id: str | None,
    order: str = 'asc',
    year: int = 2018,
    stage: str = 'Q3',
) -> list[dict[str, str]]:
    report = [
        {
            'abbr': result['abbr'],
            'driver': result['driver'],
            'position': result['position'],
            'team': result['team'],
            'time': result['time'],
        }
        for result in get_report_from_db(
            driver_id=driver_id, order=order, year=year, stage=stage
        )
    ]
    return report
