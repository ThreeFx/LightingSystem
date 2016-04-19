import datetime, os, serial, sys

configurelimit = 3
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

from serialcomm import *

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

# --------- Main begins here ----------- #

sys.stdout.write("Beginning setup ... ")

if not os.path.exists(os.path.abspath('./logs')):
    os.makedirs(os.path.abspath('./logs'))

if not os.path.exists(os.path.abspath('./rawlogs')):
    os.makedirs(os.path.abspath('./rawlogs'))

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

sys.stdout.write("Acquiring real data (C-c to end) ...")
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
#finally:
#    sys.stdout.write("Do you want a plot of the data? (requires gnuplot) [y/N]: ")
#    resp = raw_input();
#    if (resp == 'y' || resp == 'Y'):
#        try:
#            call(["gnuplot", "-e script.plg"])
#        except:
#            print("An error occurred")
#    print("Terminating);
