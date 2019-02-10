import os

DB_DEBUG_FILE = "Freeeporter.db"

FOLDERS = {
    "passive": os.path.join("C:", "Users", "Marco", "Dropbox", "Array51", "Passif"),
    # "passive": "C:/Users/Marco/Dropbox/Array51/Passif/",
    "active": os.path.join("C:", "Users", "Marco", "Dropbox", "Array51", "Actif"),
    # "active": "C:/Users/Marco/Dropbox/Array51/Actif/"
}

PASSIVES_FILE_TYPES = "*.pdf"
ACTIVES_FILE_TYPES = "*.pdf"
DEFAULT_CURRENCY = "CAD"

REGEXES = {
    "date": r'(\d{4}-\d{2}-\d{2})',  # Change it to accept 2018-07 for example (monthly invoice)
    "year": r'(\d{4})',
    "month": r'\d{4}-(\d{2})',
    "day": r'\d{4}-\d{2}-(\d{2})',
    "subtotal": r'\(\W*([a-zA-Z]{3})?\D*?([0-9,\.]+)\D*?\)',
    "gst": r'\[\W*([a-zA-Z]{3})?\D*?([0-9,\.]+)\D*?\]',
    "pst": r'\{\W*([a-zA-Z]{3})?\D*?([0-9,\.]+)\D*?\}',
    "description": r'([^\)^\]^\}]*)$',
}

# 2018 - 2018 - 2018 - 2018 - 2018 - 2018 - 2018 - 2018 - 2018 - 2018
# Income tax rates per slice
# https://www.canada.ca/en/revenue-agency/services/tax/individuals/frequently-asked-questions-individuals/canadian-income-tax-rates-individuals-current-previous-years.html
# https://www.revenuquebec.ca/en/citizens/your-situation/new-residents/the-quebec-taxation-system/income-tax-rates/
INCOME_TAX_RATE_SLICES = {
    "canada": [
        {"amount": 46605, "rate": 0.15},
        {"amount": 46603, "rate": 0.205},
        {"amount": 51281, "rate": 0.26},
        {"amount": 61353, "rate": 0.29},
        {"amount": 9999999999, "rate": 0.33},
    ],
    "quebec": [
        {"amount": 42705, "rate": 0.15},
        {"amount": 42700, "rate": 0.20},
        {"amount": 18510, "rate": 0.24},
        {"amount": 9999999999, "rate": 0.2575},
    ]
}


class STRINGS:
    APP_TITLE = "Freeporter"


class ERROR_CODES:
    DB_CANNOT_CONNECT = -1
    DB_CANNOT_CREATE_TABLE = -2
