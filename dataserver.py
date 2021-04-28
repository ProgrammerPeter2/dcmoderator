import socket

mutes = []
def on_new_client(client: socket.socket):
    global mutes
    while True:
        msg = client.recv(1024).decode()
        msg.split("\n")
        command = msg[0]
        msg.pop(0)
        if command.lower().strip() == "append":
            minp = msg[0].split(", ")
            mutedata = [minp[0], minp[1]]
            mutes.append(mutedata)
        elif command.lower().strip() == "get":
            mutetext = ""
            if msg[0] == "":
                for mute in mutes:
                    addtext = mute[0] + "," + mute[1] + ","
                    mutetext += addtext
            else:
                mutedata = mutes[int(msg[0])]
                mutetext = mutedata[0] + "," + mutedata[1]
            client.send(mutetext.encode())
        elif command.lower().strip() == "delete":
            if not msg[0] == "":
                if not int(msg[0]) >= len(mutes) - 1:
                    mutes.pop[int(msg[0])]
        elif command.lower().strip() == "clear":
            mutes.clear()
