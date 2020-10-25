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


    @staticmethod
    def empty_table(conn, table):
        c = conn.cursor()
        c.execute(f"DELETE FROM {table}")

    @staticmethod
    def list_to_where_in(where_in_list):
        return '(' + str(where_in_list)[1:-1] + ')'
        # return str(where_in_list).replace('[', '(').replace(']', ')')
