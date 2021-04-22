mutes = []

def get_mutes():
    global mutes
    return mutes

def set_mutes(inp):
    global mutes
    mutes = inp

def add_to_mutes(inp):
    global mutes
    mutes.append(mutes)

def clear_mutes():
    global mutes
    mutes.clear()

def print_mutes():
    global mutes
    print(mutes)