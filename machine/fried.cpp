#include "HX711.h"

const int DOUT = 2;
const int SCK = 3;

HX711 scale;

void setup() {
  Serial.begin(57600);
  Serial.println("Checking HX711...");
  scale.begin(DOUT, SCK);

  if (scale.is_ready()) {
    Serial.println("HX711 is ready.");
    Serial.print("Raw reading: ");
    Serial.println(scale.read());
  } else {
    Serial.println("HX711 not found or not responding.");
  }
}

void loop() {
  // Leave empty for now
}
