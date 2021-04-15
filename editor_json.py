import json

def decode(file):
    data = ""
    try:
        f = open(file, "r", encoding="utf8")
        data = json.load(f)
    except IOError:
        data = str(IOError)
    return data

def encode(file, data):
    try:
        f = open(file, "w", encoding="utf8")
        datas = json.dumps(data)
        f.write(datas)
    except IOError:
        print(format(IOError))