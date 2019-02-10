import sqlite3
from sqlite3 import Error

from pyrotools import console
from pyrotools.console import cprint

import constants


class Model:

    def __init__(self, conn):
        self.conn = conn
        self.conn.row_factory = sqlite3.Row

    @staticmethod
    def create_table(conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            cprint(console.COLORS.BRIGHT_RED, e)
            exit(constants.ERROR_CODES.DB_CANNOT_CREATE_TABLE)
