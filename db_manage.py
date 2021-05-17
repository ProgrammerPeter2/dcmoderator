import mysql.connector as connector

def get_connection(host, user, password, db):
    mydb = None
    try:
        mydb = connector.connect(host=host, user=user, password=password, database=db)
    except:
        pass
    return mydb

base_conn = get_connection("remotemysql.com", "LMhwjDOQr9", "iIykidkeEl", "LMhwjDOQr9")

def make_columnsText(columns: list, chars: str):
    columnsText = ""
    if len(columns) == 1:
        columnsText = columns[0]
    elif len(columns) > 1:
        columnsText = columns[0] + chars
        print(columns)
        for c in range(1, (len(columns) - 1)):
            column = columns[c]
            columnText = column + chars
            columnsText += columnText
    columnsText += columns[(len(columns) - 1)]
    return columnsText

def get_cursor(conn):
    return conn.cursor()

def execute(sql, conn=base_conn):
    cur = get_cursor(conn)
    cur.execute(sql)

def table_exists(table: str, conn=base_conn):
    cur = get_cursor(conn)
    cur.execute("SHOW TABLES")
    exists = False
    for i in cur:
        if table in i:
            exists = True
    return exists

def select(table: str, columns: list, extras: str, isPrintSQL = False, conn=base_conn):
    _columns = ""
    sql = ""
    cur = get_cursor(conn)
    ret = []
    if table == "config":
        sql = "select * from config"
        cur.execute(sql)
        datas = cur.fetchall()
        for d in datas:
            key = d[0]
            value = d[1]
            _type = d[2]
            if _type == "int":
                value = int(value)
            elif _type == "str":
                value = str(value)
            ret.append({key, value})
    elif table == "badWords":
        sql = "select * from badWords"
        cur.execute(sql)
        datas = cur.fetchall()
        for d in datas:
            ret.append(d[0])
    else:
        if columns[0] == "*":
            _columns = "*"
        else:
            _columns = make_columnsText(columns, ", ")
        sql = "SELECT " + _columns + " FROM " + table + " " + extras
        try:
            cur.execute(sql)
            ret = cur.fetchall()
        except connector.Error as err:
            print(sql, format(err))
    if isPrintSQL:
        print(sql)
    return ret

def insert(table: str, columns: list, values: str, conn=base_conn):
    _columns = make_columnsText(columns, ",")
    if table == "badwords":
        _columns = "badword"
    sql = "INSERT INTO " + table + " (" + _columns + ") VALUES (" + values + ")"
    try:
        cur = get_cursor(conn)
        cur.execute(sql)
        conn.commit()
    except connector.Error as e:
        print(sql, format(e))

def remove(table: str, whereDeleteFrom: str, conn=base_conn):
    sql = "DELETE FROM %s WHERE %s" % (str(table), str(whereDeleteFrom))
    if table_exists(table, conn):
        try:
            cursor = get_cursor(conn)
            cursor.execute(sql)
            conn.commit()
        except connector.Error as cerr:
            print(sql, "\nMsql error, " + sql, cerr)