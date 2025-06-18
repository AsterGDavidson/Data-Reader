// TeensyDualPot.ino

const int potPin0   = A0;     // first potentiometer
const int potPin1   = A1;     // second potentiometer
const unsigned long interval = 5;   // ms between readings

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
    
    // read raw ADC counts
    int raw0 = analogRead(potPin0);
    int raw1 = analogRead(potPin1);
    
    // convert to voltage (adjust divisor if you’ve changed resolution/reference)
    float voltage0 = raw0 * (3.3f / 1023.0f);
    float voltage1 = raw1 * (3.3f / 1023.0f);
    
    // send as "time,voltage0,voltage1\n"
    Serial.print(now);
    Serial.print(',');
    Serial.print(voltage0, 3);
    Serial.print(',');
    Serial.println(voltage1, 3);
  }
}
