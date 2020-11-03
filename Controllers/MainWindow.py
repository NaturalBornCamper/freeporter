import locale
from pprint import pprint

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, qApp
from PyQt5 import QtWidgets
from pyrotools import console
from pyrotools.console import cprint


class MainWindow(QMainWindow):

    def __init__(self, journal, report):
        super().__init__()
        self.journal = journal
        self.report = report
        self.main_ui = None

        self.selected_years = []
        self.selected_months = []
        self.selected_inputs = []
        self.selected_outputs = []

        self.use_share_only = False

    def quit_trigger(self):
        qApp.quit()

    def selected(self, q):
        print(q.text() + ' selected')

    def init_main_window(self, ui):
        cprint(console.COLORS.BRIGHT_BLUE, "init_main_window()")
        self.main_ui = ui

        self.main_ui.YearListWidget.clear()
        for year in self.journal.get_years():
            item = QtWidgets.QListWidgetItem()
            item.setText(year["year"])
            self.main_ui.YearListWidget.addItem(item)

        self.main_ui.YearListWidget.selectAll()

    # Code repetition with following method with slight change.. fix that
    def get_selected_list_items_text(self, list_widget):
        selected_list_items = []

        for item in getattr(self.main_ui, list_widget).selectedItems():
            selected_list_items.append(item.text())

        cprint(console.COLORS.BRIGHT_BLUE, "Selected list items:", selected_list_items)
        # return tuple(selected_list_items)
        return selected_list_items

    # Code repetition with previous method with slight change.. fix that
    def get_selected_list_items(self, list_widget):
        selected_list_items = []

        for item in getattr(self.main_ui, list_widget).selectedItems():
            selected_list_items.append(item)

        cprint(console.COLORS.BRIGHT_BLUE, "Selected list items:", selected_list_items)
        # return tuple(selected_list_items)
        return selected_list_items

    def filter_actives(self):
        pass

    def filter_passives(self):
        pass

    def select_all_years(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_all_years()")
        self.main_ui.YearListWidget.selectAll()

    # Triggered every time the year list's selection changed
    def select_years(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_years()")
        self.main_ui.MonthListWidget.clear()
        selected_years = self.get_selected_list_items_text(list_widget="YearListWidget")
        for month in self.journal.get_months(selected_years=selected_years):
            item = QtWidgets.QListWidgetItem()
            item.setText(month["month"])
            self.main_ui.MonthListWidget.addItem(item)

        self.select_all_months()

    def select_months(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_months()")
        self.main_ui.ActivesListWidget.clear()
        self.main_ui.PassivesListWidget.clear()
        selected_years = self.get_selected_list_items_text(list_widget="YearListWidget")
        selected_months = self.get_selected_list_items_text(list_widget="MonthListWidget")
        for journal_item in self.journal.get_items(selected_years=selected_years, selected_months=selected_months):
            item = QtWidgets.QListWidgetItem()

            # 100, 101 and 102 are just arbitrary numbers, will set constants with, not sure in constants.py or MainWindow.py
            item.setData(100, journal_item["amount"])
            item.setData(101, journal_item["gst"])
            item.setData(102, journal_item["pst"])
            item.setData(103, journal_item["share"])
            item.setText(journal_item["name"] or journal_item["date"])

            if journal_item["direction"] == "in":
                self.main_ui.ActivesListWidget.addItem(item)
            else:
                self.main_ui.PassivesListWidget.addItem(item)

        self.select_all_actives()
        self.select_all_passives()

    def select_actives(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_actives()")

        amount_total = 0.0
        gst_total = 0.0
        pst_total = 0.0

        # for item in self.main_ui.ActivesListWidget.selectedItems():
        for item in getattr(self.main_ui, "ActivesListWidget").selectedItems():
            # selected_actives = self.get_selected_list_items(list_widget="ActivesListWidget")
            share = item.data(103) if self.use_share_only else 1.0
            amount_total += item.data(100) * share
            gst_total += item.data(101) * share
            pst_total += item.data(102) * share
            # pprint(item)

        # locale.setlocale(locale.LC_ALL, '')
        locale.setlocale(locale.LC_ALL, 'en_CA')
        self.main_ui.TotalIncomeLineEdit.setText(locale.currency(amount_total, grouping=True))
        self.main_ui.TotalIncomePstLineEdit.setText(locale.currency(pst_total, grouping=True))
        self.main_ui.TotalIncomeGstLineEdit.setText(locale.currency(gst_total, grouping=True))
        self.main_ui.TotalIncomeGstPstLineEdit.setText(locale.currency(gst_total + pst_total, grouping=True))

        # for journal_item in self.journal.get_items(selected_years=selected_years, selected_months=selected_months):
        #     item = QtWidgets.QListWidgetItem()
        #     item.setText(journal_item["name"] or journal_item["date"])
        #     if journal_item["direction"] == "in":
        #         self.main_ui.ActivesListWidget.addItem(item)
        #     else:
        #         self.main_ui.PassivesListWidget.addItem(item)

    def select_passives(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_passives()")

        amount_total = 0.0
        gst_total = 0.0
        pst_total = 0.0

        # for item in self.main_ui.ActivesListWidget.selectedItems():
        for item in getattr(self.main_ui, "PassivesListWidget").selectedItems():
            share = item.data(103) if self.use_share_only else 1.0
            amount_total += item.data(100) * share
            gst_total += item.data(101) * share
            pst_total += item.data(102) * share

        locale.setlocale(locale.LC_ALL, 'en_CA')
        self.main_ui.TotalExpensesLineEdit.setText(locale.currency(amount_total, grouping=True))
        self.main_ui.TotalExpensesPstLineEdit.setText(locale.currency(pst_total, grouping=True))
        self.main_ui.TotalExpensesGstLineEdit.setText(locale.currency(gst_total, grouping=True))
        self.main_ui.TotalExpensesGstPstLineEdit.setText(locale.currency(gst_total + pst_total, grouping=True))

    def select_none_years(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_none_years()")
        self.main_ui.YearListWidget.clearSelection()

    def select_all_months(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_all_months()")
        self.main_ui.MonthListWidget.selectAll()

    def select_none_months(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_none_months()")
        self.main_ui.MonthListWidget.clearSelection()

    def select_all_actives(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_none_actives()")
        self.main_ui.ActivesListWidget.selectAll()

    def select_none_actives(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_none_actives()")
        self.main_ui.ActivesListWidget.clearSelection()

    def select_all_passives(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_none_actives()")
        self.main_ui.PassivesListWidget.selectAll()

    def select_none_passives(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_none_passives()")
        self.main_ui.PassivesListWidget.clearSelection()

    def select_actives_folder(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_actives_folder()")
        pass

    def select_passives_folder(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_passives_folder()")
        pass

    def include_actives_subfolders(self):
        cprint(console.COLORS.BRIGHT_BLUE, "include_actives_subfolders()")
        pass

    def include_passives_subfolders(self):
        cprint(console.COLORS.BRIGHT_BLUE, "include_passives_subfolders()")
        pass

    def open_actives_folder_selection_dialog(self):
        cprint(console.COLORS.BRIGHT_BLUE, "open_actives_folder_selection_dialog()")
        pass

    def open_passives_folder_selection_dialog(self):
        cprint(console.COLORS.BRIGHT_BLUE, "open_passives_folder_selection_dialog()")
        pass

    def use_deductible_percentage_only(self, checkbox_widget):
        cprint(console.COLORS.BRIGHT_BLUE, "use_deductible_percentage_only()")
        self.use_share_only = checkbox_widget == Qt.Checked
        self.select_actives()
        self.select_passives()

    def filter_passive_equipment(self):
        cprint(console.COLORS.BRIGHT_BLUE, "filter_passive_equipment()")
        pass

    def filter_passive_services(self):
        cprint(console.COLORS.BRIGHT_BLUE, "filter_passive_services()")
        pass

    def filter_passive_travel(self):
        cprint(console.COLORS.BRIGHT_BLUE, "filter_passive_travel()")
        pass

    def filter_passive_adhesion_fees(self):
        cprint(console.COLORS.BRIGHT_BLUE, "filter_passive_adhesion_fees()")
        pass

    def filter_passive_others(self):
        cprint(console.COLORS.BRIGHT_BLUE, "filter_passive_others()")
        pass

    def filter_passive_office_furnitures(self):
        cprint(console.COLORS.BRIGHT_BLUE, "filter_passive_office_furnitures()")
        pass
