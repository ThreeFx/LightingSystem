import datetime, os, serial, sys
from subprocess import call

# -- Sliding window length -- #

configurelimit = 3
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

from serialcomm import *


# -- The light calculation function, adapt to sensor sensitivity and parameters -- #

def getLightFromFrequency(data, init):
    return data[0]

    frequency = data[0]
    darkfrequency = initdata[0]
    temp = data[1]

    frequencydiff = frequency - darkfrequency
    irradiance = frequencydiff * 100 / 100; # convert to microW/cm^2 and then to W/m^2
    lightoutput = irradiance * 1^2; # figure distance out (in m)
    junctiontemp = 80 # figure junction temp out
    actuallightoutput = lightoutput / ((-0.3 * (junctiontemp - 25) + 100) / 100)
    return actuallightoutput


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


def makedir(path):
    if not os.path.exists(os.path.abspath(path)):
        os.makedirs(os.path.abspath(path))
        fixpermissions(path)

# --------- Main begins here ----------- #


sys.stdout.write("Beginning setup ... ")

makedir('logs')
makedir('rawlogs')

ser = serial.Serial(
        port = '/dev/ttyACM0',\
        baudrate = 115200)


currentdate = getdatefilename()
rawdata = open('rawlogs/rawlog-{}.csv'.format(currentdate), 'w')
f = open('logs/log-{}.csv'.format(currentdate), 'w')

print("done")


sys.stdout.write("Acquiring initial data ... ")
init = readnums(ser)
print("done")

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

    if abs(prevdata[-configurelimit][0] - data[0]) < 100: # in Hz
        break;

    prevdata.append(data)

print("done")

sys.stdout.write("Acquiring real data (^C to end) ... .")
try:
    while True:
        data = readnums(ser)
        freq = data[0];
        data[0] = getLightFromFrequency(data, init)

        writenumsto(rawdata, data)
        writenumsto(f, data)
        rawdata.flush()
        f.flush()
except KeyboardInterrupt:
    print("Stopping ...  ")
finally:
    sys.stdout.write("Do you want a plot of the data? (requires gnuplot) [y/N]: ")
    resp = raw_input();
    if (resp == 'y' or resp == 'Y'):
        makedir('plots')
        try:
            call([ "gnuplot", "-e datafile='logs/log-{0}.csv'".format(currentdate), "script.plg", "> plots/plot-{0}.png".format(currentdate) ])
        except:
            print("An error occurred")
        rawdata.close();
        f.close();
    fixall(currentdate);
    print("Exiting ... ")
