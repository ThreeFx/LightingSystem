#include <Wire.h>
//#define DEBUG

/* The light sensor */
const int GND_PIN = 35;
const int VOLT_PIN = 25;
const int FREQ_PIN = 23;
const int S0_PIN = 36;
const int S1_PIN = 34;

/*
    Temperature sensor address
    Device is 0x40 - AdaFruit HTU21D-F
*/
const int TEMP_ADDR = 0x40;

/* The relay */
//const int RELAY_PIN = 3;
//const int TEST_LED = 12;

void setup() {
//  pinMode(RELAY_PIN, OUTPUT);
//  pinMode(TEST_LED, INPUT);
  
  // Init the light sensor
  pinMode(GND_PIN, OUTPUT);
  pinMode(VOLT_PIN, OUTPUT);
  pinMode(S0_PIN, OUTPUT);
  pinMode(S1_PIN, OUTPUT);

  pinMode(FREQ_PIN, INPUT);

  digitalWrite(GND_PIN, LOW);
  digitalWrite(VOLT_PIN, HIGH);
  digitalWrite(S0_PIN, HIGH);
  digitalWrite(S1_PIN, LOW);

  // Init the I2C bus
  Wire.begin();

  // Open the data connection
  Serial.begin(115200);

  // Determine initial values;
  long darkFreq = getFrequency();
  float initTemp = getTemperature();

  // write initial data
  writeData(darkFreq, initTemp);

  // wait for lamp to get turned on
  delay(10L * 1000L);

  // Activate the lamp, go in loop
  //digitalWrite(RELAY_PIN, HIGH);
  //delay(10);
  //Serial.println(digitalRead(TEST_LED));
}

void loop() {
  // get the current data
  long freq = getFrequency();
  float temp = getTemperature();

  // write it and repeat
  writeData(freq, temp);

  delay(30L * 1000L);
}

long getFrequency() {
  int duration = pulseIn(FREQ_PIN, HIGH, 1000000);
  if (duration != 0) {
    return 1000000L / duration;
  }
  return 0;
}

float getTemperature() {
  // Standard I2C
  Wire.beginTransmission(0x40);
  // 0xE3 is the temperature register
  Wire.write(0xE3);
  Wire.endTransmission();

  Wire.requestFrom(0x40, 2);
  byte upper = Wire.read();
  byte lower = Wire.read();
  // Magic?
  float temp = ((uint16_t)(upper << 8) | lower) * 175.72 / 65535 - 46.85;

  return temp;
}

void writeData(long frequency, float temperature) {
  Serial.print(frequency);
  Serial.write(',');
  Serial.println(temperature);
}

