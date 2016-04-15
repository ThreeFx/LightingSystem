#include "Wire.h"
#define DEBUG

/* The RGB-diode */
const int RED_PIN = A0;
const int GREEN_PIN = A1;
const int BLUE_PIN = A2;

/* Frequency counter */
const int FREQ_S2_PIN = 2;
const int FREQ_S3_PIN = 3;
const int FREQ_PIN = 4;

/* 
 *  Stores the configuration for the sensor in the form
 *  <S2 bit> <S3 bit>
 *  as a short integer.
 */
const short SENS_RED = 0;
const short SENS_GREEN = 3;
const short SENS_BLUE = 1;
const short SENS_ALL = 2;

/* Temperature sensor */
const int TEMP_ADDR = 0x90 >> 1;

void setup() {
  // Initialise the LED pins
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  // Init the sensor pins
  pinMode(FREQ_S2_PIN, OUTPUT);
  pinMode(FREQ_S3_PIN, OUTPUT);
  pinMode(FREQ_PIN, INPUT);

  // Init the I2C Bus
  Wire.begin();

  // Init the communication
  Serial.begin(115200);
}

void loop() {
  // get the current temperature
  int temp = getTemperature();

  // test red light
  setLED(255, 0, 0);
  int freq_red = getFrequency(SENS_RED);

  // test green light
  setLED(0, 255, 0);
  int freq_green = getFrequency(SENS_GREEN);

  // test blue light
  setLED(0, 0, 255);
  int freq_blue = getFrequency(SENS_BLUE);

  // shut down led
  setLED(0, 0, 0);

  // write data, wait and repeat
  writeData(freq_red, freq_green, freq_blue, temp);
  delay(60L * 1000L);
}

// Sets the LED to the specified RGB color
void setLED(byte red, byte green, byte blue) {
  analogWrite(RED_PIN, red);
  analogWrite(GREEN_PIN, green);
  analogWrite(BLUE_PIN, blue);
}

// Determines the current frequency for the color
// passed as parameter (SENS_*)
long getFrequency(short color) {
  setSensor(color);
  int duration = pulseIn(FREQ_PIN, HIGH);
  if (duration != 0) {
    return 1000000L / duration;
  }
  return 0;
}

// Sets the sensor to react to the color specified
// in the corresponding SENS_* constant
void setSensor(short conf) {
  digitalWrite(FREQ_S2_PIN, conf & 0x2);
  digitalWrite(FREQ_S3_PIN, conf & 0x1);
}

// Calculates the current temperature in °C (error: 1°C)
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

void writeData(long freq_r, long freq_g, long freq_b, int temperature) {
  Serial.print(freq_r);
  Serial.write(';');
  Serial.print(freq_g);
  Serial.write(';');
  Serial.print(freq_b);
  Serial.write(';');
  Serial.println(temperature);
}

