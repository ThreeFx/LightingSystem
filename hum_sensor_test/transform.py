import datetime, serial, sys

from serialcomm import *

ser = serial.Serial(
	port = '/dev/ttyACM0',\
	baudrate = 115200)

currentdate = getdatefilename()

f = open('log-{}.csv'.format(currentdate), 'w')

while True:
	data = readnums(ser)
	writenumsto(f, data)
	f.flush()
