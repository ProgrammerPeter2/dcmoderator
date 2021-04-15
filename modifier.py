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
    elements = str.split("-")
    year = int(elements[0])
    month = int(elements[1])
    day = int(elements[2])
    return date(year,month,day)