/***************************************************
  This is an example for the HTU21D-F Humidity & Temp Sensor

  Designed specifically to work with the HTU21D-F sensor from Adafruit
  ----> https://www.adafruit.com/products/1899

  These displays use I2C to communicate, 2 pins are required to
  interface
 ****************************************************/

#include <Wire.h>

// Connect Vin to 3-5VDC
// Connect GND to ground
// Connect SCL to I2C clock pin (A5 on UNO)
// Connect SDA to I2C data pin (A4 on UNO)

void setup() {
  Wire.begin();
  Serial.begin(115200);
  Serial.println("Temperature,Humidity");
}


void loop() {
  Wire.beginTransmission(0x40);
  Wire.write(0xE3);
  Wire.endTransmission();
  Wire.requestFrom(0x40, 2);
  byte upper = Wire.read();
  byte lower = Wire.read();
  float temp = ((upper << 8) | lower) * 175.72 / 65535 - 46.85;

  Wire.beginTransmission(0x40);
  Wire.write(0xE5);
  Wire.endTransmission();
  Wire.requestFrom(0x40, 2);

  uint16_t a;

  upper = Wire.read();
  lower = Wire.read();
  float hum = ((uint16_t)(upper << 8) | lower) * 125.0 / 65536 - 6;

  Serial.print(temp); Serial.write(','); Serial.println(hum);

  delay(5000);
}
