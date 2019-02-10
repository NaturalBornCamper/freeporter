from pyrotools import console
from pyrotools.console import cprint

import constants
from Models.model import Model

sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS journal (
                                        id INTEGER PRIMARY KEY,
                                        date TEXT DEFAULT '2018-01-01',
                                        year TEXT DEFAULT 2018,
                                        month TEXT DEFAULT "01",
                                        day TEXT DEFAULT "01",
                                        name TEXT NOT NULL,
                                        amount REAL DEFAULT 0.0,
                                        gst REAL DEFAULT 0.0,
                                        pst REAL DEFAULT 0.0,
                                        direction TEXT DEFAULT 'ingress'
                                    ); """


class Journal(Model):
    def __init__(self, conn):
        super().__init__(conn)

        if self.conn is not None:
            self.create_table(self.conn, sql_create_projects_table)
        else:
            cprint(console.COLORS.BRIGHT_RED, "Error! cannot create the database connection.")
            exit(constants.ERROR_CODES.DB_CANNOT_CONNECT)

    def commit_changes(self):
        """
        Save Inserts/Updates/Deletes to database file
        """
        self.conn.commit()

    def insert(self, journal_entry, commit=False):
        """
        Create a new journal entry
        :param commit:
        :param journal_entry:
        :return:
        """

        sql = """INSERT INTO journal(date, year, month, day, name, amount, gst, pst, direction)
                  VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        cur = self.conn.cursor()
        cur.execute(sql, journal_entry)

        if commit:
            self.conn.commit()

        return cur.lastrowid

    def select_all_tasks(self):
        """
        Query all rows in the table
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM journal")

        rows = cur.fetchall()

        for row in rows:
            print(row)

    def get_years(self):
        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT year FROM journal")
        return cur.fetchall()

    def get_months(self, selected_years):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT DISTINCT month FROM journal WHERE year IN (%s) ORDER BY month" % ','.join(
                '?' * len(selected_years)
            ),
            selected_years
        )
        return cur.fetchall()

    def select_task_by_priority(self, year):
        """
        Query tasks by priority
        :param year:
        :return:
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE year=?", (year,))

        rows = cur.fetchall()

        for row in rows:
            print(row)
