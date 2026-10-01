#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define VOLTAGE_PIN 32
#define FAN_PIN 33
#define TV_PIN 34
#define FRIDGE_PIN 35
#define AC_PIN 39

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";
const char* MQTT_BROKER = "broker.hivemq.com";
const int MQTT_PORT = 1883;
const char* MQTT_TOPIC = "smart_home_energy";

WiFiClient espClient;
PubSubClient mqttClient(espClient);

int oled_state = 0;

void connectWiFi() {
    Serial.print("Connecting to WiFi");
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD, 6);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi Connected");
    Serial.println(WiFi.localIP());
}

void connectMQTT() {
    while (!mqttClient.connected()) {
        Serial.print("Connecting to MQTT...");
        String clientId = "ESP32-Energy-";
        clientId += String((uint32_t)ESP.getEfuseMac(), HEX);

        if (mqttClient.connect(clientId.c_str())) {
            Serial.println("Connected");
        } else {
            Serial.print("Failed, rc=");
            Serial.println(mqttClient.state());
            delay(2000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    connectWiFi();
    mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
    mqttClient.setBufferSize(512); // Increase buffer size for larger JSON payload

    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println("OLED initialization failed");
    } else {
        display.clearDisplay();
        display.setTextColor(WHITE);
        display.setTextSize(1);
        display.setCursor(0, 0);
        display.println("SMART ENERGY");
        display.display();
    }
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) {
        connectWiFi();
    }
    if (!mqttClient.connected()) {
        connectMQTT();
    }
    mqttClient.loop();

    int vRaw = analogRead(VOLTAGE_PIN);
    int fanRaw = analogRead(FAN_PIN);
    int tvRaw = analogRead(TV_PIN);
    int fridgeRaw = analogRead(FRIDGE_PIN);
    int acRaw = analogRead(AC_PIN);

    float voltage = 200.0 + ((float)vRaw / 4095.0) * 50.0;
    float fan_c = ((float)fanRaw / 4095.0) * 2.0;
    float tv_c = ((float)tvRaw / 4095.0) * 1.5;
    float fridge_c = ((float)fridgeRaw / 4095.0) * 3.0;
    float ac_c = ((float)acRaw / 4095.0) * 8.0;

    float fan_p = voltage * fan_c;
    float tv_p = voltage * tv_c;
    float fridge_p = voltage * fridge_c;
    float ac_p = voltage * ac_c;

    float total_power = fan_p + tv_p + fridge_p + ac_p;

    char payload[400];
    snprintf(payload, sizeof(payload), 
        "{\"device\":\"ESP32_LivingRoom\",\"voltage\":%.2f,"
        "\"appliances\":{"
        "\"fan\":{\"current\":%.2f,\"power\":%.2f},"
        "\"tv\":{\"current\":%.2f,\"power\":%.2f},"
        "\"refrigerator\":{\"current\":%.2f,\"power\":%.2f},"
        "\"ac\":{\"current\":%.2f,\"power\":%.2f}"
        "},\"total_power\":%.2f}",
        voltage, fan_c, fan_p, tv_c, tv_p, fridge_c, fridge_p, ac_c, ac_p, total_power
    );

    bool published = mqttClient.publish(MQTT_TOPIC, payload);

    Serial.println();
    Serial.println("================================");
    Serial.println("SMART HOME ENERGY");
    Serial.println("================================");
    Serial.println();
    Serial.println("Supply Voltage:");
    Serial.printf("%.2f V\r\n\r\n", voltage);
    Serial.printf("Fan\r\nCurrent: %.2f A\r\nPower:   %.2f W\r\n\r\n", fan_c, fan_p);
    Serial.printf("TV\r\nCurrent: %.2f A\r\nPower:   %.2f W\r\n\r\n", tv_c, tv_p);
    Serial.printf("Refrigerator\r\nCurrent: %.2f A\r\nPower:   %.2f W\r\n\r\n", fridge_c, fridge_p);
    Serial.printf("AC\r\nCurrent: %.2f A\r\nPower:   %.2f W\r\n\r\n", ac_c, ac_p);
    Serial.println("--------------------------------");
    Serial.printf("Total Power: %.2f W\r\n", total_power);
    Serial.printf("MQTT: %s\r\n", published ? "Published" : "Publish Failed");
    Serial.println("--------------------------------");

    // OLED Update
    display.clearDisplay();
    display.setCursor(0, 0);
    display.setTextSize(1);
    
    if (oled_state == 0) {
        display.println("SMART HOME ENERGY");
        display.println();
        display.println("Voltage:");
        display.printf("%.1f V\n\n", voltage);
        display.println("Total:");
        display.printf("%.0f W", total_power);
    } else if (oled_state == 1) {
        display.println("FAN");
        display.printf("%.2f A\n", fan_c);
        display.printf("%.0f W\n\n", fan_p);
        display.println("TV");
        display.printf("%.2f A\n", tv_c);
        display.printf("%.0f W\n", tv_p);
    } else {
        display.println("REFRIGERATOR");
        display.printf("%.2f A\n", fridge_c);
        display.printf("%.0f W\n\n", fridge_p);
        display.println("AC");
        display.printf("%.2f A\n", ac_c);
        display.printf("%.0f W\n", ac_p);
    }
    
    display.display();
    
    oled_state = (oled_state + 1) % 3;
    delay(5000);
}
