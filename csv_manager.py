import csv

def read(file):
    output = []
    with open(file, "r", encoding="utf16") as file:
        reader = csv.reader(file)
        for rows in reader:
            row=[]
            for i in row:
                row.append(i)
                print(row)
            output.append(row)
            print(output)
    return output

def write(file, data):
    with open(file, "w", encoding="utf16") as file:
        writer = cvs.writer(file)
        for r in data:
            writer.writerow(r)

def findIndexInFile(file, text):
    data = read(file)
    data_row = 0
    for i in range(len(data)):
        row = data[i]
        for j in row:
            if j == text:
                data_row = i
    return data_row

def findInFile(file, text):
    data = read(file)
    data_row = 0
    for i in range(len(data)):
        row = data[i]
        for j in row:
            if j == text:
                data_row = i
    return data[data_row]