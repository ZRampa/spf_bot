import sqlite3


def query_sel_all_id():
    query = f"SELECT user_id FROM students;"
    return query


def query_name_db(user_id):
    query = f"SELECT * FROM students WHERE user_id = '{user_id}';"
    return query


def sel_all_id():
    ans = sql_query(query_sel_all_id())
    return ans


def query_ins_active(user_id, name, telegram, phone, course):
    query = f"INSERT INTO students VALUES ('{name}', '{telegram}', '{phone}', '{course}', '{user_id}');"
    return query


def query_ins_anon_mes(message):
    query = f"INSERT INTO anon_msg VALUES ('{message}');"
    return query


def name_db(user_id):
    ans = sql_query(query_name_db(user_id))
    if len(ans) > 0:
        return True, ans
    else:
        return False, ans


def sql_query(query):
    conn = sqlite3.connect('SPF_BOT_SQL.db')
    cursor = conn.cursor()

    ans = cursor.execute(query)
    ans = ans.fetchall()

    conn.commit()
    conn.close()

    return ans

