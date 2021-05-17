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
    dateindex = 0
    if len(elements) == 3 and (elements[0] == "" or elements[0] == chr(32)):
        dateindex = 1
    datesplit = "."
    if not "." in elements[dateindex] and "-" in elements[dateindex]:
        datesplit = "-"
    date = elements[dateindex].split(datesplit)
    time = elements[dateindex+1].split(":")
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    hour = int(time[0])
    minute = int(time[1])
    seconds = int(time[2])
    return datetime(year, month, day, hour, minute, seconds)

def listToText(list, char):
    outstring = list[0]
    for li in range(1, len(list)):
        text = list[li] + char
        outstring += text
    return outstring

def getDictintFromList(list: list, key):
    value = 0
    for dic in list:
        try:
            test = dic[key]
            value = test[key]
            break
        except Exception:
            continue
    return value

def includeMatrix(matrix: list, key: str):
    included = False
    for array in matrix:
            if key in array:
                included = True
    return included