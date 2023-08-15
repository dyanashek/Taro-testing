import sqlite3
import logging

database = sqlite3.connect("db.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cursor = database.cursor()

try:
    # creates table users who have filled up the form
    cursor.execute('''CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        user_id TEXT,
        username TEXT,
        name TEXT,
        check_id TEXT,
        check_type TEXT,
        photo TEXT,
        request TEXT,
        input BOOLEAN DEFAULT True,
        input_data TEXT
    )''')
except Exception as ex:
    logging.error(f'Users table already exists. {ex}')

# cursor.execute("DELETE FROM users WHERE id<>10000")
# database.commit()