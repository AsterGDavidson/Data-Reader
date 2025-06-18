// TeensyLivePlot.ino
const int potPin = A0;     // change to whichever analog pin you use
const unsigned long interval = 50;  // ms between readings

unsigned long lastTime = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) ;  // wait for host
}

void loop() {
  unsigned long now = millis();
  if (now - lastTime >= interval) {
    lastTime = now;
    int raw = analogRead(potPin);
    float voltage = raw * (3.3f / 1023.0f);  // for 10-bit ADC on 3.3V Teensy
    // Send as "<millis>,<voltage>\n"
    Serial.print(now);
    Serial.print(',');
    Serial.println(voltage, 3);
  }
}
