// Teensy5PotPlot.ino

// Pot pins
const int potPins[5] = { A0, A1, A2, A3, A4 };
// Sample every 5 ms → 200 Hz
const unsigned long interval = 5;

void setup() {
  Serial.begin(115200);
  while (!Serial) ;  // wait for USB Serial
}

void loop() {
  static unsigned long lastTime = 0;
  unsigned long now = millis();
  if (now - lastTime >= interval) {
    lastTime = now;
    // Read & send five voltages
    for (int i = 0; i < 5; i++) {
      int raw = analogRead(potPins[i]);
      float volts = raw * (3.3f / 1023.0f);
      Serial.print(volts, 3);
      if (i < 4) Serial.print(' ');
    }
    Serial.println();
  }
}
