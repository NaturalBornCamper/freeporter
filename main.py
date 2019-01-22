import json
from locale import *

from report import Report

'''
All that needs to be installed for kivy (dependencies)
pip wheel setuptools pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
docutils (Seems to work without)
kivy.deps.gstreamer (For audio and video)
https://kivy.org/doc/stable/installation/installation-windows.html#kivy-dependencies
'''

# Set locale for number format (Empty string means computer default)
# setlocale(LC_NUMERIC, 'English_Canada.1252')
# setlocale(LC_NUMERIC, 'French_Canada.1252')
setlocale(LC_NUMERIC, '')


def pprint(var):
    print(json.dumps(var, sort_keys=True, indent=3))


# Just a method to output a report to the console
def print_console_results(report):
    pprint(report.active)
    pprint(report.passive)

    print("Brute Revenue: ", report.brute_revenue, "CAD")
    print("Total Expenses: ", report.total_expenses, "CAD")
    print("Net Revenue: ", report.net_revenue, "CAD")

    print("Provincial Income Tax: ", report.provincial_income_tax, "CAD")
    print("Federal Income Tax: ", report.federal_income_tax, "CAD")
    print("Total Income Tax To Pay: ", report.provincial_income_tax + report.federal_income_tax, "CAD")


report = Report()
report.generate_report()
print_console_results(report)
