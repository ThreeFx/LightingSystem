import datetime, serial

ser = serial.Serial(
	port = 'COM5',\ # Change this to whatever port the arduino is using
	baudrate = 115200)

currentdate = datetime.datetime.utcnow()
              .replace(" ", "-").replace(":", "-")

rawdata = open('log-{}-raw.csv'.format(currentdate), 'w')
f = open('log-{}.csv'.format(currentdate), 'w')

# Configuration of the light sensor
configuration = readinp()
# The first set of data reveals the initial conditions
# No light, "complete" darkness
intialdata = readinp()

while True:
	data = readinp()
	writeTo(rawdata, data)
	data[0] = getLightFromFrequency(data, initialdata)
	writeTo(f, data)
	rawdata.flush()
	f.flush()

def getLightFromFrequency(data, initdata):
	frequency = data[0]
	darkfrequency = initdata[0]
	temp = data[1]

	frequencydiff = frequency - darkfrequency
	irradiance = frequencydiff * 100 / 100; # convert to µW/cm^2 and then to W/m^2
	lightoutput = irradiance * 1^2; # figure distance out (in m)
	junctiontemp = 80 # figure junction temp out
	actuallightoutput = lightoutput / ((-0.3 * (junctiontemp - 25) + 100) / 100)
	return actuallightoutput

def writeTo(f, data):
	f.write(';'.join(map(str, data)) + '\n')

def readinp():
	return map(int, ser.readline().split(';'))
