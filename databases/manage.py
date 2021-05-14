import socket
import decoder
host = socket.gethostname()
port = 3306
client_socket = socket.socket()
client_socket.connect((host, port))

def get(table = ""):
    if table != "":
        cmd = f"get {table}"
        client_socket.send(cmd.encode())
        _return = client_socket.recv(10240).decode(encoding="utf8")
        _return = decoder.toMatrix(_return)
        return _return
    else:
        pass

def set(table = "", matrix = []):
    if table != "" and len(matrix) > 0:
        _table = decoder.toString(matrix)
        statement = f"set {table} {_table}"
        client_socket.send(statement.encode())