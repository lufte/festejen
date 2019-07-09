import sqlite3
import os


def get_connection():
    connection = sqlite3.connect(os.path.join(os.path.dirname(__file__),
                                              '../../festejen.db'))
    connection.row_factory = sqlite3.Row
    connection.commit()
    return connection
