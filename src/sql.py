import sqlite3 as sql

def create_db(file):
    con = sql.connect("file:{0}?mode=rwc".format(file), uri=True)
    cur = con.cursor()
    exec_file(cur, 'db/create_table.sqlscript')
    con.commit()
    con.close()

def exec_file(cursor, file, *args):
    with open(file) as f:
        script = f.read()
        cursor.executescript(script)

def insert(message):
    if not message.get('id'):
        raise ValueError('id field not found')
    if not message.get('status'):
        raise ValueError('status field not found')
    con = sql.connect("db/default.db")
    cur = con.cursor()
    cur = cur.execute("INSERT INTO message_status VALUES(?, ?)", (message['id'], message['status']))
    con.commit()

def get(message_id):
    con = sql.connect("db/default.db")
    cur = con.cursor()
    result = cur.execute("SELECT status FROM message_status WHERE id=?", (message_id,))
    status = result.fetchone()
    if status is None:
        status = ('not found',)
    return status[0]