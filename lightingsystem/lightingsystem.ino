#include <Wire.h>
//#define DEBUG

unsigned long start;

const int samplesPerCycle = 250; // five sine waves

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


void setup() {  
  // Init the light sensor
  pinMode(GND_PIN, OUTPUT);
  pinMode(VOLT_PIN, OUTPUT);
  pinMode(S0_PIN, OUTPUT);
  pinMode(S1_PIN, OUTPUT);

  pinMode(FREQ_PIN, INPUT);

  digitalWrite(GND_PIN, LOW);
  digitalWrite(VOLT_PIN, HIGH);
  digitalWrite(S0_PIN, LOW);
  digitalWrite(S1_PIN, HIGH);

  // Init the I2C bus
  Wire.begin();

  // Open the data connection
  Serial.begin(115200);

  // wait at startup for power to flow
  delay(100);

  // Determine initial values;
  long darkFreq = getFrequency();
  float initTemp = getTemperature();

  // write initial data
  writeData(0, darkFreq, initTemp);

  // wait for lamp to get turned on
  delay(10 * 1000L);

  start = micros();
}

void loop() {
  // get the current temperature only once per cycle
  float temp = getTemperature();

  long freqs[samplesPerCycle];
  unsigned long timee[samplesPerCycle];
  // gather data (ca. samplesPerCycle / 10 sine waves)
  for (int i = 0; i < samplesPerCycle; i++) {
    freqs[i] = getFrequency();
    timee[i] = micros() - start;
  }

  // write data
  for (int i = 0; i < samplesPerCycle; i++) {
    writeData(timee[i], freqs[i], temp);
  }

  delay(20L * 1000L);
}

long getFrequency() {
  int duration = pulseIn(FREQ_PIN, HIGH, 100000);
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

void writeData(unsigned long timeInMs, long frequency, float temperature) {
  Serial.print(timeInMs);
  Serial.write(',');
  Serial.print(frequency);
  Serial.write(',');
  Serial.println(temperature);
}

