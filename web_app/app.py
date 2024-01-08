from flask_restful import Api
from flask import Flask
from web_app.report.routes import my_routes
from web_app.web_api.api import Report, ReportDrivers
from web_app.db.session import set_session, pop_session, close_dbs
import typing as t


def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.register_blueprint(my_routes)

    app.before_request(set_session)

    @app.teardown_request
    def handle_session(args) -> t.Any:
        pop_session()
        return args

    @app.teardown_appcontext
    def close_db(args) -> t.Any:
        close_dbs()
        return args

    api.add_resource(Report, '/api/report/')
    api.add_resource(ReportDrivers, '/api/report/drivers/')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
