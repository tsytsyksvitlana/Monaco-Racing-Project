import pytest
from sqlalchemy import select

from web_app.db.session import s
from web_app.db.models.drivers import Driver
from web_app.db.models.race import Race
from web_app.db.models.result_race import ResultRace


driver_records_cases = [('Valtteri Bottas', 'MERCEDES', 'VBM', 1, 'asc'),
                        ("Sebastian Vettel", "FERRARI", "SVF", 19, 'desc'),
                        ("Romain Grosjean", "HAAS FERRARI", "RGH", 7, 'asc'),]


@pytest.mark.parametrize('expected_name, expected_team, expected_abbr, id, order',
                         (driver_records_cases)
                         )
def test_driver_records(
    expected_name, expected_team, expected_abbr, id, order, client
):
    if order == 'desc':
        driver = s.users_db.scalars(
            select(Driver).where(Driver.id == id).order_by(Driver.id.desc())
        ).first()
    else:
        driver = s.users_db.scalars(
            select(Driver).where(Driver.id == id)).first()
    assert (driver.name, driver.team, driver.abbr) == (
        expected_name, expected_team, expected_abbr)


race_records_cases = [("Monaco", 2018)]


@pytest.mark.parametrize('expected_name, expected_year', (race_records_cases))
def test_race_records(expected_name, expected_year, client):
    first_race = s.users_db.scalars(select(Race)).first()
    assert (first_race.name, first_race.year) == (expected_name, expected_year)
