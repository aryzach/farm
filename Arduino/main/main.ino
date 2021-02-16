#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266httpUpdate.h>

const int API_TIMEOUT = 10000;  //keep it long if you want to receive headers from client


// WiFi
const char* ssid = "twistedfields";
const char* password = "alwaysbekind";

// MQTT
const char* mqttServer = "192.168.1.123";
const int mqttPort = 1883;
WiFiClient espClient;
PubSubClient client(espClient);

// OTA
const char* host = "raw.githubusercontent.com";
const int httpsPort = 443;
BearSSL::WiFiClientSecure otaClient;


// hardware pins
const int RELAY = 12;
const int LED = 13;


const char* NAME = "valve1";

void setupPins() {
  for(int i = 12; i < 15; i++)
      {
          Serial.println("setting up: ");
          Serial.println(i);
          pinMode(i, OUTPUT);
      }
}

void setupWifiMQTT() {
  // Wifi
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  // MQTT
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect(NAME)) {
 
      Serial.println("connected");  
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
 
}

void setup() {

  setupPins();
 
  Serial.begin(9600);

  setupWifiMQTT();

  otaClient.setInsecure(); //the magic line, use with caution
  //otaClient.setTimeout(API_TIMEOUT);
} 

void checkForUpdates() {

 if (!otaClient.connect(host, httpsPort)) {
    Serial.println("OTA connection failed");
    return;
  }
  Serial.println("3");

  String url = "/aryzach/OTA/main/20401c592040.version";
  Serial.print("Requesting URL: ");
  Serial.println(url);
  otaClient.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "User-Agent: BuildFailureDetectorESP8266\r\n" +
               "Connection: close\r\n\r\n");

  Serial.println("Request sent");
  while (otaClient.connected()) {
    String line = otaClient.readStringUntil('\n');
    if (line == "\r") {
      Serial.println("Headers received");
      break;
    }
  }
  String line = otaClient.readStringUntil('\n');
  if (line.startsWith("{\"state\":\"success\"")) {
    Serial.println("esp8266/Arduino CI successfull!");
  } else {
    Serial.println("esp8266/Arduino CI has failed");
  }
  Serial.println("Reply was:");
  Serial.println("==========");
  Serial.println(line);
  Serial.println("==========");
  Serial.println("Closing connection");
  otaClient.stop();
}

String getMAC()
{
  uint8_t mac[6];
  char result[14];

 snprintf( result, sizeof( result ), "%02x%02x%02x%02x%02x%02x", mac[ 0 ], mac[ 1 ], mac[ 2 ], mac[ 3 ], mac[ 4 ], mac[ 5 ] );

  return String( result );
}

int callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println("payload 0");
  Serial.println((char)payload[0]);
  Serial.println((char)payload[0] == '1');
  if ((char)payload[0] == '1') {
    Serial.println("yeah");
    digitalWrite(RELAY, HIGH);
    digitalWrite(LED, LOW);
  } else {
    Serial.println("no");
    digitalWrite(RELAY, LOW);
    delay(200);
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
    delay(200);
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
    delay(200);
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
    delay(200);
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
    delay(200);
    digitalWrite(LED, HIGH);
  }
   
  

  Serial.println();
  Serial.println("-----------------------");

}

void reconnect() {
  while (!client.connected()) {
   Serial.print("Attempting MQTT connection...");
   // Create a random client ID
   String clientId = "ESP8266Client-";
   clientId += String(random(0xffff), HEX);
   // Attempt to connect
   if (client.connect(clientId.c_str())) {
     Serial.println("connected");
     // Once connected, publish an announcement...
     //client.publish("server", "reconnected");
     // ... and resubscribe
     client.subscribe(NAME);
   } else {
     Serial.print("failed, rc=");
     Serial.print(client.state());
     Serial.println(" try again in 5 seconds");
     // Wait 5 seconds before retrying
     delay(5000);
   }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  checkForUpdates();
}
