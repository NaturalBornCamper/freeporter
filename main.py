import os
import sqlite3
import sys
from locale import *
from sqlite3 import Error

from PyQt5 import QtWidgets
from pyrotools import console
from pyrotools.console import cprint

import constants
from Controllers.MainWindow import MainWindow
from Models.journal import Journal
from Views.UI_MainWindow import Ui_MainWindow
from report import Report

# Set locale for number format (Empty string means computer default)
# setlocale(LC_NUMERIC, 'English_Canada.1252')
# setlocale(LC_NUMERIC, 'French_Canada.1252')
setlocale(LC_NUMERIC, '')


# Just a method to output a report to the console
def print_console_results(report):
    # pprint(report.active)
    # pprint(report.passive)

    cprint(console.COLORS.GREEN, "Brute Revenue: ", report.brute_revenue, "CAD")
    cprint(console.COLORS.BRIGHT_RED, "Total Expenses: ", report.total_expenses, "CAD")
    cprint(console.COLORS.BRIGHT_GREEN, "Net Revenue: ", report.net_revenue, "CAD")

    cprint(console.COLORS.BRIGHT_RED, "Provincial Income Tax: ", report.provincial_income_tax, "CAD")
    cprint(console.COLORS.BRIGHT_RED, "Federal Income Tax: ", report.federal_income_tax, "CAD")
    cprint(console.COLORS.BRIGHT_RED, "Total Income Tax To Pay: ",
           report.provincial_income_tax + report.federal_income_tax, "CAD")


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


if __name__ == "__main__":
    DEBUG = True

    conn = create_connection(constants.DB_DEBUG_FILE if DEBUG else ":memory:")
    journal = Journal(conn)

    report = Report(journal)
    report.generate_report()
    # print_console_results(report)

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    main_window = MainWindow(journal=journal, report=report)
    ui.setupUi(main_window)
    main_window.init_main_window(ui=ui)
    main_window.show()
    app.exec()

    conn.close()
    if os.path.exists(constants.DB_DEBUG_FILE):
        try:
            os.remove(constants.DB_DEBUG_FILE)
        except PermissionError as e:
            cprint(console.COLORS.BRIGHT_RED, e)

    # sys.exit()
