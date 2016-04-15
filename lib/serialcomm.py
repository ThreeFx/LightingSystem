import datetime

sepchar = ','

def readinp(conn):
    return conn.readline().rstrip().split(sepchar)

def readnums(conn):
    return map(float, readinp(conn))

def writeto(f, data):
    return f.write(sepchar.join(data) + '\n')

def writenumsto(f, data):
    return writeto(f, map(str, data))

def getdatefilename():
    return str(datetime.datetime.utcnow()).replace(" ", "-").replace(":", "-").replace(".", "-")
