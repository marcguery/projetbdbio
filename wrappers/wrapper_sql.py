#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 2018-01-10
# run : python wrapper_sql.py
# =============================================================================
#	Class for interacting with SQL databases stored in SQLite
# =============================================================================

import unittest
import logging
import sqlite3  # https://docs.python.org/3.6/library/sqlite3.html

# configuration and global variables

logging.basicConfig(format='[%(levelname)s] - %(name)s - %(asctime)s : %(message)s')
logger = logging.getLogger("wrapper_sql")
logger.setLevel(logging.DEBUG)

"""
WrapperSQLite class for connecting and querying a SQLite database
"""

class WrapperSQLite:


    def __init__(self, db_name):
        self.conn = None  # connection link to a database to None
        self.connect_db(db_name)  # connect to db

    # connect to another databse
    def connect_db(self, db_name):
        self.db_name = db_name  # name of the database
        self.conn = sqlite3.connect(db_name)

    # executes a sql SELECT query, returns the results as a list of rows
    def query_select(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.ProgrammingError as e:
            logger.exception(e)

    # executes a sql query INSERT / DELETE / UPDATE, returns the number of affected rows
    def query_boolean(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            return cursor.rowcount
        except sqlite3.ProgrammingError as e:
            logger.exception(e)

    # executes a sql SELECT query with params, returns the results as a list of rows
    def query_select_params(self, query, params):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.ProgrammingError as e:
            logger.exception(e)

    # executes a sql script, returns the number of affected rows
    def query_script(self, sql_script):
        try:
            self.conn.executescript(sql_script)
            self.conn.commit()
            return self.conn.total_changes
        except sqlite3.ProgrammingError as e:
            logger.exception(e)

    # create an SQL schema for a database, returns the number of created tables
    def load_schema_sql(self, file_sql):
        fd = open(file_sql, 'r')
        str_schema = fd.read()
        fd.close()
        self.query_script(str_schema)
        nb_tables = len(self.query_select("SELECT * FROM sqlite_master WHERE type='table';"))
        return nb_tables;


'''
unit tests
'''


class TestCase(unittest.TestCase):

    # initialization (run once before all tests)
    @classmethod
    def setUpClass(self):
        print()  # to have first message on a new line
        self.db_tp2 = 'sources/tp2.db'  # path to tp2 data source (SQL)
        self.file_schema_tp2 = 'sources/tp2.sql'  # sql file to create the schema of the tp2 data source
        self.sqlwrap = WrapperSQLite(self.db_tp2)

    def test_load_schema(self):
        self.sqlwrap.connect_db(self.db_tp2)
        self.sqlwrap.load_schema_sql(self.file_schema_tp2)

    def test_query_params(self):
        self.sqlwrap.connect_db(self.db_tp2)
        query = 'SELECT * FROM Genes WHERE gene_id > ?'
        params = (175,)
        res = self.sqlwrap.query_select_params(query, params)
        print(res)
        assert(len(res) == 111)


# a simple example using unit tests

if (__name__ == "__main__"):
    unittest.main(verbosity=2)  # Run all tests with verbose mode
