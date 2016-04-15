sepchar = ','

def readinp(conn):
    return conn.readline().rstrip().split(sepchar)

def readnums(conn):
    return map(float, readinp(conn))

def writeto(file, data):
    return (sepchar.join(data) + '\n')

def writenumsto(file, data):
    return writeto(file, map(str, data))
