import dict2xml
import xml.etree.ElementTree as ET
from flask import json
import pytest
from sqlalchemy import select

from web_app.db.session import s
from web_app.db.models.drivers import Driver


def test_api_json_drivers_report(client):
    drivers = s.users_db.scalars(select(Driver)).all()
    report_data = {}
    for driver in drivers:
        report_data[driver.abbr] = {'driver': driver.name, 'team': driver.team}
    api_data = client.get("/api/report/drivers/").get_json()
    assert len(report_data) == len(api_data)


def test_api_xml_drivers_report(client):
    drivers = s.users_db.scalars(select(Driver)).all()
    codes = {}
    for driver in drivers:
        codes[driver.abbr] = {'driver': driver.name, 'team': driver.team}
    api_response = client.get("/api/report/drivers/?format=XML")
    api_data = api_response.data
    xml_tree = ET.fromstring(api_data)
    assert len(set(codes)) == len(set(xml_tree))


def test_api_json_report(client):
    data = s.users_db.scalars(select(Driver)).all()
    codes = {}
    for driver in data:
        codes[driver.id] = {'driver': driver.name, 'team': driver.team}
    api_data = client.get("/api/report/").get_json()
    assert len(codes) == len(api_data)


def test_api_xml_report(client):
    data = s.users_db.scalars(select(Driver)).all()
    report_data = {}
    for driver in data:
        report_data[driver.id] = {'driver': driver.name, 'team': driver.team}
    api_response = client.get("/api/report/?format=XML").data
    xml_tree = ET.fromstring(api_response)
    assert len(set(report_data)) == len(set(xml_tree))


api_driver_id_cases = [
    ('SVF', {'SVF': {
        'abbr': 'SVF',
        "driver": "Sebastian Vettel",
        "position": 1,
        "team": "FERRARI",
        "time": 65}}),
]


@pytest.mark.parametrize('abbr, result', (api_driver_id_cases))
def test_api_json_driver_id(abbr, result, client):
    api_data = client.get(f"/api/report/drivers/?driver_id={abbr}").get_json()
    assert json.dumps(result) == json.dumps(api_data)


@pytest.mark.parametrize('abbr, result', (api_driver_id_cases))
def test_api_xml_driver_id(abbr, result, client):
    api_data = client.get(
        f"/api/report/drivers/?driver_id={abbr}&format=XML").data
    xml_tree = ET.fromstring(api_data)
    result = dict2xml.dict2xml(result, wrap='root')
    xml_str = ET.tostring(xml_tree, encoding="unicode")
    assert result.strip() == xml_str.strip()
