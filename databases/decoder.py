def toString(matrix: list):
    _return: str
    for row in matrix:
        _row: str
        for cell in row:
            addtext = cell + ", "
            _row += addtext
        _row += "\n"
        _return += _row
    return _return

def toMatrix(input: str):
    _return = []
    _rows = input.split("\n")
    for row in _rows:
        _row = row.split(", ")
        _return.append(_row)
    return _return