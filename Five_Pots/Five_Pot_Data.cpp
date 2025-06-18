// TeensyMultiPot.ino

// Pins for the five potentiometers
const int potPins[] = { A0, A1, A2, A3, A4 };
const int numPots    = sizeof(potPins) / sizeof(potPins[0]);

// How often to sample (ms)
const unsigned long interval = 5;

unsigned long lastTime = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    // wait for host to open the port
  }
}

void loop() {
  unsigned long now = millis();
  if (now - lastTime >= interval) {
    lastTime = now;

    // Print timestamp
    Serial.print(now);

    // Read, convert, and print each potentiometer voltage
    for (int i = 0; i < numPots; i++) {
      int raw = analogRead(potPins[i]);
      float voltage = raw * (3.3f / 1023.0f);
      Serial.print(',');
      Serial.print(voltage, 3);
    }

    // end line
    Serial.println();
  }
}
