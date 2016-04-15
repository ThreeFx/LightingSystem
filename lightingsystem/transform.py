import datetime, serial

from serialcomm import *

def getLightFromFrequency(data, initdata):
    frequency = data[0]
    darkfrequency = initdata[0]
    temp = data[1]

    frequencydiff = frequency - darkfrequency
    irradiance = frequencydiff * 100 / 100; # convert to microW/cm^2 and then to W/m^2
    lightoutput = irradiance * 1^2; # figure distance out (in m)
    junctiontemp = 80 # figure junction temp out
    actuallightoutput = lightoutput / ((-0.3 * (junctiontemp - 25) + 100) / 100)
    return actuallightoutput

# --------- Main begins here ----------- #

ser = serial.Serial(
        port = 'COM5',\
        baudrate = 115200)

currentdate = getdatefilename()

rawdata = open('log-{}-raw.csv'.format(currentdate), 'w')
f = open('log-{}.csv'.format(currentdate), 'w')

# Configuration of the light sensor
configuration = readinp(ser)
# The first set of data reveals the initial conditions
# No light, "complete" darkness
intialdata = readnums(ser)
writenumsto(rawdata, initialdata)

while True:
    data = readnums(ser)
    writenumsto(rawdata, data)
    data[0] = getLightFromFrequency(data, initialdata)
    writenumsto(f, data)
    rawdata.flush()
    f.flush()

