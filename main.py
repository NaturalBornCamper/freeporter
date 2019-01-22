import glob
import json
import os
import re
from collections import defaultdict
from locale import *
from os.path import basename, dirname

import constants
from log import Log



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

all = {
    "passive": {},
    "active": {
        "clients": {},
        "total": {
            "subtotal": defaultdict(float),
            "gst": defaultdict(float),
            "pst": defaultdict(float),
        }
    }
}


def pprint(var):
    print(json.dumps(var, sort_keys=True, indent=3))


def extract_price(filename, category):
    matches = re.search(constants.REGEXES[category], filename)
    # matches = re.search(r'(\D+)?(\d+\.?\d+)', price_string)
    if matches is not None:
        return {
            "currency": matches[1] if matches[1] else constants.DEFAULT_CURRENCY,
            "amount": atof(matches[2]) if matches[2] else 0.0,
            # "amount": float(matches[2].replace(',', '')) if matches[2] else 0.0,
        }
    else:
        return {"currency": constants.DEFAULT_CURRENCY, "amount": 0.0}


def extract_single_element(filename, category):
    matches = re.search(constants.REGEXES[category], filename)
    # matches = re.search(r'(\D+)?(\d+\.?\d+)', price_string)
    if matches is not None:
        return matches[1].strip()
    else:
        Log.w(message=(category + "amount not formatted correctly in " + filename))
        return False


def process_filename(filename):
    journal_entry = {
        "date": extract_single_element(filename, "date"),
        "subtotal": extract_price(filename, "subtotal"),
        "gst": extract_price(filename, "gst"),
        "pst": extract_price(filename, "pst"),
        "description": extract_single_element(filename, "description")
    }

    if any([journal_entry["subtotal"], journal_entry["gst"], journal_entry["pst"]]):
        if not journal_entry["date"]:
            Log.w(message=("Date not formatted correctly in " + filename))
        elif not journal_entry["description"]:
            Log.w(message=("Description not formatted correctly in " + filename))
        return journal_entry
    else:
        Log.w(message=("No amounts found in " + filename))
        return False


print(process_filename("2018-06-17 Auncun "))
print(process_filename("2018-06-17 (35.46) Un seul "))
print(process_filename("2018-06-17 (35.46) [ USD 1.77] { TWD3.54 } Cellulaire allo "))


def extract_data(folder):
    bob = {
        "journal": defaultdict(list),
        "total": {
            "subtotal": defaultdict(float),
            "gst": defaultdict(float),
            "pst": defaultdict(float),
        }
    }
    for filepath in glob.glob(os.path.join(folder, constants.PASSIVES_FILE_TYPES)):
        file_basename = os.path.splitext(basename(filepath))[0]

        journal_entry = process_filename(file_basename)
        if journal_entry:
            bob["journal"][journal_entry["date"]].append(journal_entry)
            for x in ("subtotal", "gst", "pst"):
                bob["total"][x][journal_entry[x]["currency"]] += journal_entry[x]["amount"]

    return bob


def calculate_income_tax(revenue_to_calculate, territory):
    income_tax = 0.0
    for tax_slice in constants.INCOME_TAX_RATE_SLICES[territory]:
        if revenue_to_calculate > tax_slice["amount"]:
            income_tax += tax_slice["amount"] * tax_slice["rate"]
            revenue_to_calculate -= tax_slice["amount"]
        else:
            income_tax += revenue_to_calculate * tax_slice["rate"]
            break

    return income_tax


# Extract "passive" folder
all["passive"] = extract_data(constants.FOLDERS["passive"])

# Extract "actives" subfolders
for folder in glob.glob(os.path.join(constants.FOLDERS["active"], '*/')):
    all["active"]["clients"][basename(dirname(folder))] = client_data = extract_data(folder)

    for section in ["subtotal", "gst", "pst"]:
        for currency in client_data["total"][section]:
            all["active"]["total"][section][currency] += client_data["total"][section][currency]

pprint(all)

brute_revenue = all["active"]["total"]["subtotal"][constants.DEFAULT_CURRENCY]
total_expenses = all["passive"]["total"]["subtotal"][constants.DEFAULT_CURRENCY]
net_revenue = brute_revenue - total_expenses
print("Brute Revenue: ", brute_revenue, "CAD")
print("Total Expenses: ", total_expenses, "CAD")
print("Net Revenue: ", net_revenue, "CAD")

provincial_income_tax = calculate_income_tax(net_revenue, "quebec")
federal_income_tax = calculate_income_tax(net_revenue, "canada")
print("Provincial Income Tax: ", provincial_income_tax, "CAD")
print("Federal Income Tax: ", federal_income_tax, "CAD")
print("Total Income Tax To Pay: ", provincial_income_tax + federal_income_tax, "CAD")

