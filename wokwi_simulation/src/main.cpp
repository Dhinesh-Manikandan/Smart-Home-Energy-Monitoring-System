#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ArduinoJson.h>

#define VOLTAGE_PIN 32
#define FAN_PIN 33
#define TV_PIN 34
#define FRIDGE_PIN 35
#define AC_PIN 39

#define RELAY_FAN 16
#define RELAY_TV 17
#define RELAY_FRIDGE 18
#define RELAY_AC 19

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";
const char* MQTT_BROKER = "broker.hivemq.com";
const int MQTT_PORT = 1883;
const char* MQTT_TOPIC = "smart_home_energy";
const char* MQTT_COMMAND_TOPIC = "smart_home_energy/command";
const char* MQTT_STATUS_TOPIC = "smart_home_energy/status";

WiFiClient espClient;
PubSubClient mqttClient(espClient);

int oled_state = 0;
unsigned long last_update = 0;

bool fan_state = true;
bool tv_state = true;
bool fridge_state = true;
bool ac_state = true;

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

void processReadingsAndPublish(bool is_command = false) {
    int vRaw = analogRead(VOLTAGE_PIN);
    int fanRaw = analogRead(FAN_PIN);
    int tvRaw = analogRead(TV_PIN);
    int fridgeRaw = analogRead(FRIDGE_PIN);
    int acRaw = analogRead(AC_PIN);

    float voltage = 200.0 + ((float)vRaw / 4095.0) * 50.0;
    
    float fan_c = fan_state ? ((float)fanRaw / 4095.0) * 2.0 : 0.0;
    float tv_c = tv_state ? ((float)tvRaw / 4095.0) * 1.5 : 0.0;
    float fridge_c = fridge_state ? ((float)fridgeRaw / 4095.0) * 3.0 : 0.0;
    float ac_c = ac_state ? ((float)acRaw / 4095.0) * 8.0 : 0.0;

    float fan_p = voltage * fan_c;
    float tv_p = voltage * tv_c;
    float fridge_p = voltage * fridge_c;
    float ac_p = voltage * ac_c;

    float total_power = fan_p + tv_p + fridge_p + ac_p;

    StaticJsonDocument<512> doc;
    doc["device"] = "ESP32_LivingRoom";
    doc["voltage"] = round(voltage * 100) / 100.0;
    
    JsonObject apps = doc.createNestedObject("appliances");
    
    JsonObject f = apps.createNestedObject("fan");
    f["current"] = round(fan_c * 100) / 100.0;
    f["power"] = round(fan_p * 100) / 100.0;
    f["state"] = fan_state ? "ON" : "OFF";
    
    JsonObject t = apps.createNestedObject("tv");
    t["current"] = round(tv_c * 100) / 100.0;
    t["power"] = round(tv_p * 100) / 100.0;
    t["state"] = tv_state ? "ON" : "OFF";
    
    JsonObject r = apps.createNestedObject("refrigerator");
    r["current"] = round(fridge_c * 100) / 100.0;
    r["power"] = round(fridge_p * 100) / 100.0;
    r["state"] = fridge_state ? "ON" : "OFF";
    
    JsonObject a = apps.createNestedObject("ac");
    a["current"] = round(ac_c * 100) / 100.0;
    a["power"] = round(ac_p * 100) / 100.0;
    a["state"] = ac_state ? "ON" : "OFF";
    
    doc["total_power"] = round(total_power * 100) / 100.0;

    char payload[512];
    serializeJson(doc, payload);
    bool published = mqttClient.publish(MQTT_TOPIC, payload);

    if (is_command) {
        StaticJsonDocument<256> statDoc;
        statDoc["device"] = "ESP32_LivingRoom";
        statDoc["fan"] = fan_state ? "ON" : "OFF";
        statDoc["tv"] = tv_state ? "ON" : "OFF";
        statDoc["refrigerator"] = fridge_state ? "ON" : "OFF";
        statDoc["ac"] = ac_state ? "ON" : "OFF";
        char statPayload[256];
        serializeJson(statDoc, statPayload);
        mqttClient.publish(MQTT_STATUS_TOPIC, statPayload);
    }

    Serial.println();
    Serial.println("================================");
    if (is_command) {
        Serial.println("RELAY COMMAND EXECUTED");
    } else {
        Serial.println("SMART HOME ENERGY");
    }
    Serial.println("================================");
    Serial.println();
    Serial.println("Supply Voltage:");
    Serial.printf("%.2f V\r\n\r\n", voltage);
    
    Serial.printf("Fan\r\nState: %s\r\nCurrent: %.2f A\r\nPower:   %.2f W\r\n\r\n", fan_state ? "ON" : "OFF", fan_c, fan_p);
    Serial.printf("TV\r\nState: %s\r\nCurrent: %.2f A\r\nPower:   %.2f W\r\n\r\n", tv_state ? "ON" : "OFF", tv_c, tv_p);
    Serial.printf("Refrigerator\r\nState: %s\r\nCurrent: %.2f A\r\nPower:   %.2f W\r\n\r\n", fridge_state ? "ON" : "OFF", fridge_c, fridge_p);
    Serial.printf("AC\r\nState: %s\r\nCurrent: %.2f A\r\nPower:   %.2f W\r\n\r\n", ac_state ? "ON" : "OFF", ac_c, ac_p);
    
    Serial.println("--------------------------------");
    Serial.printf("Total Power: %.2f W\r\n", total_power);
    Serial.printf("MQTT: %s\r\n", published ? (is_command ? "Status Published" : "Published") : "Publish Failed");
    Serial.println("--------------------------------");

    display.clearDisplay();
    display.setCursor(0, 0);
    display.setTextSize(1);
    
    if (oled_state == 0) {
        display.println("SMART HOME ENERGY");
        display.println();
        display.printf("Voltage: %.1f V\n", voltage);
        display.println();
        display.println("TOTAL:");
        display.printf("%.0f W", total_power);
    } else if (oled_state == 1) {
        display.printf("FAN  %c %s\n", fan_state ? '*' : 'o', fan_state ? "ON" : "OFF");
        display.printf("%.0f W\n\n", fan_p);
        display.printf("TV   %c %s\n", tv_state ? '*' : 'o', tv_state ? "ON" : "OFF");
        display.printf("%.0f W\n", tv_p);
    } else {
        display.printf("FRIDGE %c %s\n", fridge_state ? '*' : 'o', fridge_state ? "ON" : "OFF");
        display.printf("%.0f W\n\n", fridge_p);
        display.printf("AC     %c %s\n", ac_state ? '*' : 'o', ac_state ? "ON" : "OFF");
        display.printf("%.0f W\n", ac_p);
    }
    
    display.display();
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
    if (String(topic) == MQTT_COMMAND_TOPIC) {
        StaticJsonDocument<256> doc;
        DeserializationError error = deserializeJson(doc, payload, length);
        if (!error) {
            String app = doc["appliance"].as<String>();
            String cmd = doc["command"].as<String>();
            
            bool new_state = (cmd == "ON");
            
            if (app == "fan") {
                fan_state = new_state;
                digitalWrite(RELAY_FAN, fan_state ? HIGH : LOW);
            } else if (app == "tv") {
                tv_state = new_state;
                digitalWrite(RELAY_TV, tv_state ? HIGH : LOW);
            } else if (app == "refrigerator") {
                fridge_state = new_state;
                digitalWrite(RELAY_FRIDGE, fridge_state ? HIGH : LOW);
            } else if (app == "ac") {
                ac_state = new_state;
                digitalWrite(RELAY_AC, ac_state ? HIGH : LOW);
            }
            
            processReadingsAndPublish(true);
        }
    }
}

void connectMQTT() {
    while (!mqttClient.connected()) {
        Serial.print("Connecting to MQTT...");
        String clientId = "ESP32-Energy-";
        clientId += String((uint32_t)ESP.getEfuseMac(), HEX);

        if (mqttClient.connect(clientId.c_str())) {
            Serial.println("Connected");
            mqttClient.subscribe(MQTT_COMMAND_TOPIC);
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
    
    pinMode(RELAY_FAN, OUTPUT);
    pinMode(RELAY_TV, OUTPUT);
    pinMode(RELAY_FRIDGE, OUTPUT);
    pinMode(RELAY_AC, OUTPUT);
    
    digitalWrite(RELAY_FAN, HIGH);
    digitalWrite(RELAY_TV, HIGH);
    digitalWrite(RELAY_FRIDGE, HIGH);
    digitalWrite(RELAY_AC, HIGH);

    connectWiFi();
    mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
    mqttClient.setCallback(mqttCallback);
    mqttClient.setBufferSize(512);

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

    unsigned long currentMillis = millis();
    if (currentMillis - last_update >= 5000) {
        last_update = currentMillis;
        processReadingsAndPublish(false);
        oled_state = (oled_state + 1) % 3;
    }
}
