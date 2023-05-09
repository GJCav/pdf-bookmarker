
def read():
    rst = []
    while True:
        try:
            s = input()
        except:
            break
        rst.append(s)
    return rst

def isInt(s: str):
    try:
        int(s)
        return True
    except:
        return False