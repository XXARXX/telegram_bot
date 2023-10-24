import sqlite3 as sql

def create_db(file):
    """
    Create database

    Parameters
    ----------
    file : str
        db file path
    """
    con = sql.connect("file:{0}?mode=rwc".format(file), uri=True)
    cur = con.cursor()
    exec_file(cur, 'db/create_table.sqlscript')
    con.commit()
    con.close()

def exec_file(cursor, file):
    """
    Utility function for sql script execution from file

    Parameters
    ----------
    cursor
        database cursor
    file
        script path
    """
    with open(file) as f:
        script = f.read()
        cursor.executescript(script)

def insert(message, db_path = 'db/default.db'):
    """
    Insert row into database

    Parameters
    ----------
    message : dictionary
        id : str
            message id
        status : str
            status description
    """
    if not message.get('id'):
        raise ValueError('id field not found')
    if not message.get('status'):
        raise ValueError('status field not found')
    con = sql.connect(db_path)
    cur = con.cursor()
    cur = cur.execute("INSERT INTO message_status VALUES(?, ?)", (message['id'], message['status']))
    con.commit()
    con.close()

def get(message_id, db_path = 'db/default.db'):
    """
    Returns message by id

    Parameters
    ----------
    message_id : str

    Returns
    -------
    status
        returns message status or not found in case if message with such id not found
    """
    con = sql.connect(db_path)
    cur = con.cursor()
    result = cur.execute("SELECT status FROM message_status WHERE id=?", (message_id,))
    status = result.fetchone()
    if status is None:
        status = ('not found',)
    con.close()
    return status[0]