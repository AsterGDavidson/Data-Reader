#include <Wire.h>
#include <Adafruit_MCP9600.h>

// — Pin & Address Defines —
#define I2C_SDA_PIN     18
#define I2C_SCL_PIN     19
#define MCP_I2C_ADDRESS 0x67

Adafruit_MCP9600 mcp;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  // Remap I²C to custom pins
  Wire.setSDA(I2C_SDA_PIN);
  Wire.setSCL(I2C_SCL_PIN);
  Wire.begin();

  // Initialize the MCP9600 at the specified address
  if (!mcp.begin(MCP_I2C_ADDRESS, &Wire)) {
    Serial.println("ERROR: MCP9600 not found!");
    while (1) delay(10);
  }

  // Thermocouple type = K
  mcp.setThermocoupleType(MCP9600_TYPE_K);

  // ADC resolution = 18-bit (highest precision)
  mcp.setADCresolution(MCP9600_ADCRESOLUTION_18);

  // (Optional) sample averaging 0–7
  mcp.setFilterCoefficient(3);

  // Start continuous conversions
  mcp.enable(true);
}

void loop() {
  float tempC = mcp.readThermocouple();
  Serial.println(tempC);    // single numeric line for Serial Plotter
  delay(1000);
}
