import mysql.connector as connector

def get_connection(host, user, password, db):
    mydb = None
    try:
        mydb = connector.connect(host=host, user=user, password=password, database=db)
    except:
        pass
    return mydb

base_conn = get_connection("db4free.net", "rootadmin07", "1234abcd", "dcmoderation")

def make_columnsText(columns: list, chars: str):
    columnsText = columns[0] + chars
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
    _columns = make_columnsText(columns, ", ")
    if columns[0] == "*":
        _columns = "*"
    sql = "SELECT " + _columns + " FROM " + table + " " + extras
    ret = []
    try:
        cur = get_cursor(conn)
        cur.execute(sql)
        ret = cur.fetchall()
    except connector.Error as err:
        print(sql, format(err))
    if isPrintSQL:
        print(sql)
    return ret

def insert(table: str, columns: list, values: str, conn=base_conn):
    _columns = make_columnsText(columns, ",")
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
            print("Msql error, " + sql, cerr)