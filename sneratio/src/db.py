import sqlite3
import os
import sys

db_name = "sneratio.db"
db_path = os.path.join(os.path.dirname(os.path.realpath(sys.path[0])), "src/sneratio.db")
print(db_path)


def _create_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS loop_info
                (id integer primary key, task_done bool, img_data text)''')

    conn.commit()
    conn.close()


def _reset_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''DELETE FROM loop_info''')

    conn.commit()
    conn.close()


def _insert_empty_row_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    task_done = False
    img_data= ""

    c.execute("INSERT INTO loop_info (task_done, img_data) VALUES(?, ?)", (task_done, img_data))

    conn.commit()
    conn.close()


def initialize_db(db_path):
    _create_db(db_path)
    _reset_db(db_path)
    _insert_empty_row_db(db_path)


def select_db(db_path, id=None):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    if id is None:
        c.execute('''SELECT * FROM loop_info''')
    else:
        c.execute('''SELECT * FROM loop_info WHERE id=?''', (id,))

    rows = c.fetchall()

    for row in rows:
    	print(row)

    data = {
        "id": rows[0][0],
        "task_done": rows[0][1],
        "img_data": rows[0][2]
    }

    conn.commit()
    conn.close()

    return data


def update_db(db_path, data):
    id = 1

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    task_done = data["task_done"]
    img_data = data["img_data"]

    c.execute('''UPDATE loop_info set (task_done, img_data)=(?, ?) where id=?''', (task_done, img_data, id))

    conn.commit()
    conn.close()
