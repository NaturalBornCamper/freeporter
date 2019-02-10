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


    def quit_trigger(self):
        qApp.quit()

    def selected(self, q):
        print(q.text() + ' selected')

    def init_main_window(self, ui):
        cprint(console.COLORS.BRIGHT_BLUE, "init_main_window()")
        self.main_ui = ui
        self.main_ui.yearListWidget.clear()
        for year in self.journal.get_years():
            item = QtWidgets.QListWidgetItem()
            item.setText(year["year"])
            print("year", year["year"])
            self.main_ui.yearListWidget.addItem(item)

        self.main_ui.yearListWidget.selectAll()

    def filter_actives(self):
        pass

    def filter_passives(self):
        pass

    def select_all_years(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_all_years()")
        self.main_ui.yearListWidget.selectAll()

    # Triggered every time the year list's selection changed
    def select_years(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_years()")
        selected_years = []
        for year in self.main_ui.yearListWidget.selectedItems():
            selected_years.append(year.text())

        months = self.journal.get_months(selected_years=selected_years)
        self.main_ui.monthListWidget.clear()
        for month in months:
            item = QtWidgets.QListWidgetItem()
            item.setText(month["month"])
            print("month", month["month"])
            self.main_ui.monthListWidget.addItem(item)

        self.select_all_months()

    def select_months(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_months()")

    def select_actives(self):
        pass

    def select_passives(self):
        pass

    def select_none_years(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_none_years()")
        self.main_ui.yearListWidget.clearSelection()

    def select_all_months(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_all_months()")
        self.main_ui.monthListWidget.selectAll()

    def select_none_months(self):
        cprint(console.COLORS.BRIGHT_BLUE, "select_none_months()")
        self.main_ui.monthListWidget.clearSelection()

    def select_all_actives(self):
        pass

    def select_none_actives(self):
        pass

    def select_all_passives(self):
        pass

    def select_none_passives(self):
        pass

    def select_actives_folder(self):
        pass

    def select_passives_folder(self):
        pass

    def include_actives_subfolders(self):
        pass

    def include_passives_subfolders(self):
        pass

    def open_actives_folder_selection_dialog(self):
        pass

    def open_passives_folder_selection_dialog(self):
        pass
