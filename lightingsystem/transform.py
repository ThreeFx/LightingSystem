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

rawdata = open('rawlog-{}.csv'.format(currentdate), 'w')
f = open('log-{}.csv'.format(currentdate), 'w')

prev3 = readnums();
prev2 = readnums();
prev = readnums();

map(lambda x: writenumsto(rawdata, x), [prev3, prev2, prev])

# Compare the data to the data 3 minutes prior
# If there is no significant frequency change in
# the light, the led junction has warmed up
while True:
    data = readnums(ser)
    writenumsto(rawdata, data)

    if abs(prev3[0] - data[0]) < 100: # in Hz
        break;

    prev = data
    prev2 = prev
    prev3 = prev2

while True:
    data = readnums(ser)
    writenumsto(rawdata, data)
    data[0] = getLightFromFrequency(data, initialdata)
    writenumsto(f, data)
    rawdata.flush()
    f.flush()
