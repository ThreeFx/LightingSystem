//#define TEMP 1;
//#define FREQ 0;

/* The light sensor */
const int GND_PIN = 35;
const int VOLT_PIN = 25;
const int OUT_PIN = 23;
const int S0_PIN = 36;
const int S1_PIN = 34;

#include <Wire.h>

void setup() {
  Serial.begin(115200);

  /* -------------------------------------- */

  pinMode(GND_PIN, OUTPUT);
  pinMode(VOLT_PIN, OUTPUT);
  pinMode(S0_PIN, OUTPUT);
  pinMode(S1_PIN, OUTPUT);

  pinMode(OUT_PIN, INPUT);

  digitalWrite(GND_PIN, LOW);
  digitalWrite(VOLT_PIN, HIGH);
  digitalWrite(S0_PIN, LOW);
  digitalWrite(S1_PIN, HIGH);

  Wire.begin();
}

void loop() {
//  long l = getFrequency();
//  Serial.print("Frequency: ");
//  Serial.println(l);

  float a = getTemperature();
  Serial.print("Temperature: ");
  Serial.println(a);

  delay(2000);
}

float getTemperature() {
  Wire.beginTransmission(0x40);
  Wire.write(0xE3);
  Wire.endTransmission();
  Wire.requestFrom(0x40, 2);
  byte upper = Wire.read();
  byte lower = Wire.read();
  Serial.print(upper); Serial.print(" "); Serial.print(lower);
  float temp = ((uint16_t)(upper << 8) | lower) * 175.72 / 65535 - 46.85;

  return temp;
}

long getFrequency() {
  int duration = pulseIn(OUT_PIN, HIGH);
  if (duration != 0) {
    return 1000000L / duration;
  }
  return 0;
}
