from web_app.bl.report.racing_report import print_report
from web_app.cli.my_parser import parser_data


if __name__ == '__main__':
    files, order, driver = parser_data()
    print_report(folder_path=files, driver=driver, order=order)
