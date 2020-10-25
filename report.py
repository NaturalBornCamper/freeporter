import glob
import os
import re
from collections import defaultdict
from locale import *
from os.path import basename, dirname

import constants
from pyrotools.log import Log

# "class" to permit arrays/dictionaries/lists like this:
# x = nested_dict()
# x[3][1]["dfdf"]["allo"][4] = "created on the fly"
nested_dict = lambda: defaultdict(nested_dict)


def nd(nes):
    return defaultdict(nes)


class Report:
    def __init__(self, journal):
        self.journal = journal

        self.passive = {}

        self.active = {
            "clients": {},
            "total": {
                "subtotal": defaultdict(float),
                "gst": defaultdict(float),
                "pst": defaultdict(float),
            }
        }

        self.brute_revenue = 0.0
        self.total_expenses = 0.0
        self.net_revenue = 0.0
        self.provincial_income_tax = 0.0
        self.federal_income_tax = 0.0

    def __extract_price(self, filename, category):
        matches = re.search(constants.REGEXES[category], filename)
        # matches = re.search(r'(\D+)?(\d+\.?\d+)', price_string)
        if matches is not None:
            return atof(matches[2]) if matches[2] else 0.0
            return {
                "currency": matches[1] if matches[1] else constants.DEFAULT_CURRENCY,
                "amount": atof(matches[2]) if matches[2] else 0.0,
                # "amount": float(matches[2].replace(',', '')) if matches[2] else 0.0,
            }
        else:
            return 0.0
            return {"currency": constants.DEFAULT_CURRENCY, "amount": 0.0}

    def __extract_single_element(self, string, category):
        matches = re.search(constants.REGEXES[category], string)
        # matches = re.search(r'(\D+)?(\d+\.?\d+)', price_string)
        if matches is not None:
            return matches[1].strip()
        else:
            Log.w(message=(category + "is not formatted correctly in " + string))
            return False

    def __process_filename(self, filename):
        journal_entry = {
            "date": self.__extract_single_element(filename, "date"),
            "subtotal": self.__extract_price(filename, "subtotal"),
            "gst": self.__extract_price(filename, "gst"),
            "pst": self.__extract_price(filename, "pst"),
            "description": self.__extract_single_element(filename, "description")
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

    def __extract_data(self, folder, direction):
        data = {
            "journal": nested_dict(),
            # "journal": defaultdict(dict),
            "total": {
                "subtotal": defaultdict(float),
                "gst": defaultdict(float),
                "pst": defaultdict(float),
            }
        }

        for filepath in glob.iglob(os.path.join(folder, constants.PASSIVES_FILE_TYPES), recursive=True):
            # Folder is the file's parent folder, unless it's a year, then use another folder up the hierarchy
            # TODO Instead of backtracking from filename for category (Phone expenses, equipment, ATW, Voxtel),
            #  use the folders inside the passives and actives folders. Two ways of doing this:
            #   1- Loop inside loop, scan all folders inside the passives/actives then for each folder scan recursively
            #     This means a loop inside a loop, so code more indented to the right..
            #   2- Scan recursively inside the passives/actives and extract the next folder from the scan path
            #     This means do the same operation on every file in the same category folder (code re-executing)
            folder = os.path.basename(os.path.dirname(filepath))
            if (bool(re.match('^\d\d\d\d$', folder))):
                folder = os.path.basename(os.path.dirname(os.path.dirname(filepath)))




            # for filepath in glob.glob(os.path.join(folder, constants.PASSIVES_FILE_TYPES)):
            file_basename = os.path.splitext(basename(filepath))[0]

            journal_entry = self.__process_filename(file_basename)
            if journal_entry:
                year = self.__extract_single_element(journal_entry["date"], "year")
                month = self.__extract_single_element(journal_entry["date"], "month") or "01"
                day = self.__extract_single_element(journal_entry["date"], "day") or "01"
                if not data["journal"][year][month][day]:
                    data["journal"][year][month][day] = []
                data["journal"][year][month][day].append(journal_entry)
                # data["journal"][journal_entry["date"]].append(journal_entry)
                # date, year, month, day, name, category, amount, gst, pst, direction
                self.journal.insert((
                    journal_entry["date"],
                    year,
                    month,
                    day,
                    journal_entry["description"],
                    folder,
                    float(journal_entry["subtotal"]),
                    float(journal_entry["gst"]),
                    float(journal_entry["pst"]),
                    direction
                ))

                # Just for printing in console then copy-pasting in cav or Excel file for manual calculations
                print(
                    '"' + folder + '",',
                    '"' + journal_entry["date"] + '",',
                    '"' + journal_entry["description"] + '",',
                    '"' + str(journal_entry["subtotal"]) + '",',
                    '"' + str(journal_entry["gst"]) + '",',
                    '"' + str(journal_entry["pst"]) + '"'
                )

                # for x in ("subtotal", "gst", "pst"):
                #     data["total"][x][journal_entry[x]["currency"]] += journal_entry[x]["amount"]

        return data

    def __calculate_income_tax(self, revenue_to_calculate, territory):
        income_tax = 0.0
        for tax_slice in constants.INCOME_TAX_RATE_SLICES[territory]:
            if revenue_to_calculate > tax_slice["amount"]:
                income_tax += tax_slice["amount"] * tax_slice["rate"]
                revenue_to_calculate -= tax_slice["amount"]
            else:
                income_tax += revenue_to_calculate * tax_slice["rate"]
                break

        return income_tax

    def generate_report(self):
        self.__extract_data(constants.FOLDERS["passive"], constants.MONEY_OUTPUT)

        self.__extract_data(constants.FOLDERS["active"], constants.MONEY_INPUT)

        # Extract "actives" subfolders
        # for folder in glob.glob(os.path.join(constants.FOLDERS["active"], '*/')):
        #     self.active["clients"][basename(dirname(folder))] = self.__extract_data(folder, constants.MONEY_INPUT)

        self.journal.commit_changes()

        #     for section in ["subtotal", "gst", "pst"]:
        #         for currency in client_data["total"][section]:
        #             self.active["total"][section][currency] += client_data["total"][section][currency]
        #
        # self.brute_revenue = self.active["total"]["subtotal"][constants.DEFAULT_CURRENCY]
        # self.total_expenses = self.passive["total"]["subtotal"][constants.DEFAULT_CURRENCY]
        # self.net_revenue = self.brute_revenue - self.total_expenses
        #
        # self.provincial_income_tax = self.__calculate_income_tax(self.net_revenue, "quebec")
        # self.federal_income_tax = self.__calculate_income_tax(self.net_revenue, "canada")
