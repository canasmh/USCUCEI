import sqlite3
from sqlite3 import Error
from datetime import datetime
import os


class EventsDB:

    def __init__(self, events):
        self.db_name = os.getcwd() + 'events.db'
        self.table_name = 'events'
        self.events = events

    def connect(self):

        try:
            connection = sqlite3.connect(self.db_name)
            print("Connection was successful")
        except Error as err:
            connection = None
            print(f"There was an error:\n{err}")

        return connection
