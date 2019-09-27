# Copyright © 2019 Javier Ayres
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the LICENSE file for more details.

import sqlite3
import os


def get_connection():
    connection = sqlite3.connect(os.path.join(os.path.dirname(__file__),
                                              '../../festejen.db'))
    connection.row_factory = sqlite3.Row
    connection.commit()
    return connection
