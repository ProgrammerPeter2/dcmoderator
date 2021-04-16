from datetime import  *

def rem_char(text):
    out = ""
    for x in text:
        #x equals with a sepical character then continue else add to output
        if x == "(" or x == "'" or x == "{" or x == "," or x=="}" or x==")":
            continue
        else:
            out += x
    return out

def date_string(date = datetime.now()):
    out = ""
    #get years elements, convert to srting and add to output
    year = date.year
    out = str(year)+"-"
    month = date.month
    out += str(month)+"-"
    day = date.day
    out += str(day)+" "
    hour = date.hour
    out += str(hour)+":"
    min = date.minute
    out += str(min)+":"
    sec = date.second
    out += str(round(sec))
    return out

def string_date(str: str):
    elements = str.split(" ")
    date = elements[0].split("-")
    time = elements[1].split(":")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    hour = int(time[0])
    minute = int(time[1])
    day = int(time[2])
    return datetime(year,month,day,hour,minute,day)