/*
  Water Pollution Monitoring - ESP32 Firmware (Phase 1 Skeleton)
  ----------------------------------------------------------------
  This version uses SIMULATED sensor values so the full pipeline
  (ESP32 -> WiFi -> FastAPI backend -> Postgres) can be proven end
  to end before physical sensors arrive.

  When hardware arrives, replace the readSimulated___() functions
  with real sensor reads. The rest of the code (WiFi, HTTP POST,
  JSON payload, timing) stays the same.

  Required libraries (install via Arduino Library Manager):
    - ArduinoJson (by Benoit Blanchon)
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ---------- CONFIGURE THESE ----------
const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// Use your computer's local IP address on the same WiFi network,
// e.g. "http://192.168.1.42:8000/api/readings"
// (localhost/127.0.0.1 will NOT work from the ESP32's perspective)
const char* SERVER_URL = "http://YOUR_COMPUTER_IP:8000/api/readings";

const char* NODE_ID = "node-01";
const unsigned long SEND_INTERVAL_MS = 60000; // 60 seconds, matches methodology spec

// --------------------------------------

unsigned long lastSendTime = 0;

void setup() {
  Serial.begin(115200);
  connectToWiFi();
}

void loop() {
  if (millis() - lastSendTime >= SEND_INTERVAL_MS) {
    lastSendTime = millis();

    float turbidity = readSimulatedTurbidity();
    float ph = readSimulatedPH();
    float tds = readSimulatedTDS();
    float temperature = readSimulatedTemperature();

    Serial.println("---- Reading ----");
    Serial.printf("Turbidity: %.2f NTU\n", turbidity);
    Serial.printf("pH: %.2f\n", ph);
    Serial.printf("TDS: %.2f ppm\n", tds);
    Serial.printf("Temperature: %.2f C\n", temperature);

    sendReading(turbidity, ph, tds, temperature);
  }
}

void connectToWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected. IP address: ");
  Serial.println(WiFi.localIP());
}

void sendReading(float turbidity, float ph, float tds, float temperature) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected, skipping send and retrying connection.");
    connectToWiFi();
    return;
  }

  HTTPClient http;
  http.begin(SERVER_URL);
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<256> doc;
  doc["node_id"] = NODE_ID;
  doc["turbidity_ntu"] = turbidity;
  doc["ph"] = ph;
  doc["tds_ppm"] = tds;
  doc["temperature_c"] = temperature;
  doc["is_simulated"] = true; // set to false once real sensors are wired in

  String payload;
  serializeJson(doc, payload);

  int responseCode = http.POST(payload);

  if (responseCode > 0) {
    Serial.printf("Server responded: %d\n", responseCode);
    Serial.println(http.getString());
  } else {
    Serial.printf("POST failed, error: %s\n", http.errorToString(responseCode).c_str());
  }

  http.end();
}

// ---------- SIMULATED SENSOR FUNCTIONS ----------
// TODO Phase 2: replace each of these with real analogRead() based
// sensor logic and calibration formulas once hardware arrives.

float readSimulatedTurbidity() {
  // Simulate values mostly in safe range (0-5 NTU), occasionally higher
  return random(0, 800) / 100.0; // 0.00 - 8.00 NTU
}

float readSimulatedPH() {
  // Simulate values mostly in safe range (6.5-8.5)
  return 6.0 + (random(0, 350) / 100.0); // 6.00 - 9.50
}

float readSimulatedTDS() {
  // Simulate values mostly safe (0-500 ppm), occasionally higher
  return random(0, 120000) / 100.0; // 0.00 - 1200.00 ppm
}

float readSimulatedTemperature() {
  return 24.0 + (random(0, 600) / 100.0); // 24.00 - 30.00 C
}
