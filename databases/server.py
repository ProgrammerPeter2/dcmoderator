import socket
import _thread
import json
import os

def on_new_client(client: socket.socket, addr):
    print("Connecting from:", addr)
    while True:
        cmd = client.recv(10240).decode('utf8')
        _return = None
        if cmd == "get":
            arg = cmd[4:]
            if arg == "mutes":
                with open("datas/tables/mutes.txt", "r", encoding="utf8") as file:
                    content = file.read()
                    _return = content
            elif arg == "users":
                file = open("datas/users.json", "r", encoding="utf8")
                _return = json.load(file)
            elif arg == "badwords":
                with open("datas/tables/badwords.txt", "r", encoding="utf8") as file:
                    content = file.read()
                    _return = content
        elif cmd == "update":
            arg = cmd[9:]
            if "mutes" in arg:
                file = open("datas/tables/mutes.txt", "w", encoding="utf8")
                content = cmd[16:]
                file.write(content)
            elif "badwords" in arg:
                file = open("datas/tables/badwords.txt", "w", encoding="utf8")
                content = cmd[18:]
                file.write(content)
        if _return is not None:
            client.send(_return.encode())

if os.getcwd() == "/app/":
    os.chdir("/app/databases")

server = socket.socket()
host = socket.gethostname()
port = 3306
server.bind((host, port))

while True:
    client, addr = server.accept()
    _thread.start_new_thread(on_new_client, (client, addr))