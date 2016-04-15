#include "Wire.h"
#define DEBUG

/* Digital pins */
const int FREQ_PIN = 2;

/*
 *  Temperature sensor address
 *  Device is 0x90 >> 1 == 0x48
 */
const int TEMP_ADDR = 0x90 >> 1;

/* The relay */
const int RELAY_PIN = 3;

void setup() {
  // Initialise the pins
  pinMode(FREQ_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);

  // Init the I2C bus
  Wire.begin();

  // Open the data connection
  Serial.begin(115200);

  // Activate the lamp, go in loop
  digitalWrite(RELAY_PIN, HIGH);
}

void loop() {
  // get the current data
  long freq = getFrequency();
  int temp = getTemperature();

  // write it and repeat
  writeData(freq, temp);
  delay(60L * 1000L);
}

long getFrequency() {
  int duration = pulseIn(FREQ_PIN, HIGH);
  if (duration != 0) {
    return 1000000L / duration;
  }
  return 0;
}

int getTemperature() {
  byte* upper;
  byte* lower;
  readBytesFromSensor(upper, lower);
  return ((*upper) << 8) + (*lower);
}

void readBytesFromSensor(byte* upper, byte* lower) {
  Wire.beginTransmission(TEMP_ADDR);
  Wire.write(0x0);
  Wire.endTransmission();

  Wire.requestFrom(TEMP_ADDR, 2);
  *upper = Wire.read();
  *lower = Wire.read();

#ifdef DEBUG
  Serial.println(*upper);
  Serial.println(*lower);
#endif
}

void writeData(long frequency, int temperature) {
  Serial.print(frequency);
  Serial.write(',');
  Serial.println(temperature);
}

