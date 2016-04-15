import datetime, serial

from serialcomm import *

ser = serial.Serial(
	port = '/dev/ttyACM0',\
	baudrate = 115200)

currentdate = str(datetime.datetime.utcnow()).replace(" ", "-")

f = open('log-{}.csv'.format(currentdate), 'w')

# Configuration of the light sensor
configuration = readinp(ser)
f.write(','.join(configuration) + '\n')

while True:
	data = readnums(ser)
	writenumsto(f, data)
	f.flush()
