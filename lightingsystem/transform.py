import datetime, os, serial, sys, traceback
from subprocess import call
from time import sleep
import numpy as np
import math

# -- Sliding window length -- #

configurelimit = 3 * 250
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

from serialcomm import *


# -- The light calculation function, adapt to sensor sensitivity and parameters -- #

def getLightFromFrequency(data, init):
#    return data[1]

    frequency = data[1]
    darkfrequency = init[1]
    temp = data[2]

    frequencydiff = frequency - darkfrequency
    irradiance = frequencydiff * 10 / 100; # convert to microW/cm^2 and then to W/m^2
    lightoutput = irradiance * 0.21 * 0.21; # Watt per sternradian
    return lightoutput # watt per sterntradian


def fixpermissions(path):
    uid = int(os.environ.get('SUDO_UID'))
    gid = int(os.environ.get('SUDO_GID'))
    os.chown(os.path.abspath(path), uid, gid)

def fixall(cd):
    fixpermissions('logs/log-{}.csv'.format(cd))
    fixpermissions('rawlogs/rawlog-{}.csv'.format(cd))
    plotfile = os.path.abspath('plots/plot-{}.csv'.format(cd))
    if (os.path.exists(plotfile)):
        fixpermissions(plotfile)


def makeDirIfExists(path):
    if not os.path.exists(os.path.abspath(path)):
        os.makedirs(os.path.abspath(path))
        fixpermissions(path)

# --------- Main begins here ----------- #


sys.stdout.write("Beginning setup ... ")

makeDirIfExists('logs')
makeDirIfExists('rawlogs')
makeDirIfExists('avg')

ser = serial.Serial(
        port = '/dev/ttyACM0',\
        baudrate = 115200)


currentdate = getdatefilename()
rawdata = open('rawlogs/rawlog-{}.csv'.format(currentdate), 'w')
f = open('logs/log-{}.csv'.format(currentdate), 'w')
avg = open('avg/avg-{}.csv'.format(currentdate), 'w')

print("done")


sys.stdout.write("Acquiring initial data ... ")
init = readnums(ser)
print("done")

sys.stdout.write("You have ten seconds to plug in the LED ...")
sleep(8)
print


print("configurelimit is set to {}".format(configurelimit))
sys.stdout.write("Acquiring initial reference data ... ")
prevdata = [init]
for x in xrange(0, configurelimit):
    prevdata.append(readnums(ser))
print("done")


map(lambda x: writenumsto(rawdata, x), prevdata)

# Compare the data to the data 3 minutes prior
# If there is no significant frequency change in
# the light, the led junction has warmed up
sys.stdout.write("Configuring ... ")
while True:
    data = readnums(ser)
    writenumsto(rawdata, data)

    if abs(prevdata[-configurelimit][1] - data[1]) < 100: # in Hz
        break;

    prevdata.append(data)

print("done")

print("Acquiring real data (^C to end) ... ")
try:
    c = 0;
    avgdata = [];
    while True:
        data = readnums(ser)
        writenumsto(rawdata, data)

        data[1] = getLightFromFrequency(data, init)

        # log the average separately
        avgdata.append(data)
        c = c + 1
        if c >= 250:
            average = [np.mean(map(lambda x: x[1], avgdata)), data[2]]
            print("{}, {}".format(average[0], average[1]));
            writenumsto(avg, average)
            avgdata = []
            c = 0

        writenumsto(f, data)
        rawdata.flush()
        f.flush()

except KeyboardInterrupt:
    print
    print("Stopping ...  ")

finally:
    rawdata.close();
    f.close();
    fixall(currentdate);

    #sys.stdout.write("Do you want a plot of the data? (requires gnuplot) [y/N]: ")
    #resp = raw_input();


    #if (resp == 'y' or resp == 'Y'):
    #    makeDirIfExists('plots')
    #    try:
    #        with open('plots/plot-{}.png'.format(currentdate), 'w') as plot:
    #                call([ "gnuplot -e \"datafile='./logs/log-{0}.csv'\" script.plg" ], stdout=plot)
    #    except Exception, e:
    #        print("An error occurred:")
    #        print traceback.format_exc(e)
    print("Exiting ... ")
