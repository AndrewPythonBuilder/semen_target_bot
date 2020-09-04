import sqlite3


def register_user(external_id, user_name):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (external_id, user_name) VALUES(?,?)',
                   (external_id, user_name))
    conn.commit()
    cursor.close()
    conn.close()


def get_all_ids():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT external_id FROM users')
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    res = []
    for i in result:
        res.append(i[0])
    return res


def edit_message(hello_text):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE hello_texts SET hello_text=:hello_text WHERE id=:id',
                   {'id': 1, 'hello_text': hello_text})
    conn.commit()
    cursor.close()
    conn.close()


def get_message():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT hello_text FROM hello_texts WHERE id=:id', {'id': 1})
    result = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return result


def get_last_message(external_id):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT hello_text FROM hello_text WHERE id=:id', {'id': 1})
    result = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return result


def get_endl_message():
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('SELECT hello_text FROM hello_texts WHERE id=:id', {'id': 2})
    result = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return result


def edit_endl_message(hello_text):
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE hello_texts SET hello_text=:hello_text WHERE id=:id',
                   {'id': 2, 'hello_text': hello_text})
    conn.commit()
    cursor.close()
    conn.close()
