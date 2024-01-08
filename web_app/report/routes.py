from flask import Blueprint, Response, render_template, request
from sqlalchemy import select

from web_app.bl.report.report_from_db import get_report_from_db
from web_app.bl.report.racing_report import format_time
from web_app.db.models.drivers import Driver
from web_app.db.session import s


my_routes = Blueprint("my_routes", __name__)


@my_routes.route('/report/', methods=['GET'])
def web_report() -> str:
    codes = s.users_db.scalars(select(Driver)).all()
    return render_template('report.html', codes=codes)


@my_routes.route('/report/drivers/', methods=['GET'])
def report_drivers() -> Response | str:
    driver_id = request.args.get('driver_id')
    order = request.args.get('order', 'asc')

    report = get_report_from_db(driver_id, order=order)
    if not report:
        return Response(f"Driver {driver_id} not found", 404)
    for i in report:
        i['time'] = format_time(i['time'])
    return render_template('report_drivers.html', drivers=report)
