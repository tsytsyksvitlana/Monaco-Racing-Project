import dict2xml
from flask import Response, jsonify, request
from flask_restful import Resource
from sqlalchemy import select

from web_app.db.models.drivers import Driver
from web_app.bl.report.report_from_db import get_report_as_dict
from web_app.db.session import s


class Report(Resource):
    def get(self) -> Response:
        '''get common information: abbreviation, driver's name, team.
            format data JSON or XML

        JSON is default format response data

        For XML params format=XML
        example:
            http://127.0.0.1:5000/api/report/?format=XML
            http://127.0.0.1:5000/api/report/
        '''
        _format = request.args.get('format', 'json')
        drivers = s.users_db.scalars(select(Driver)).all()
        codes = {}
        for driver in drivers:
            codes[driver.abbr] = {'driver': driver.name, 'team': driver.team}

        if _format == 'json':
            return jsonify(codes)

        data = dict2xml.dict2xml(codes, wrap='root')
        return Response(
            data,
            content_type='application/xml',
            status=200,
        )


class ReportDrivers(Resource):
    def get(self):
        '''get data a list of driver's names and codes or single driver.
           format data JSON or XML

        JSON is default format response data

        For XML params format=XML
        example:
            http://127.0.0.1:5000/api/report/drivers/?driver_id=BHS&format=XML
            http://127.0.0.1:5000/api/report/drivers/?format=XML
        '''

        _format = request.args.get('format', 'json')
        driver_id = request.args.get('driver_id')

        report_data = get_report_as_dict(driver_id)
        result = {res['abbr']: res for res in report_data}

        if _format == 'json':
            return jsonify(result)

        data = dict2xml.dict2xml(result, wrap='root')
        return Response(
            data,
            content_type='application/xml',
            status=200,
        )
