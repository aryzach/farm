#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Connect to the WiFi
const char* ssid = "twistedfields";
const char* password = "alwaysbekind";

const char* mqttServer = "192.168.1.123";
const int mqttPort = 1883;
 
WiFiClient espClient;
PubSubClient client(espClient);

const int RELAY = 12;
const int LED = 13;
const char* NAME = "valve5";

void setupPins() {
  for(int i = 12; i < 15; i++)
      {
          Serial.println("setting up: ");
          Serial.println(i);
          pinMode(i, OUTPUT);
      }
}

 
void setup() {

  setupPins();
 
  Serial.begin(9600);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
 
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
 
  client.subscribe(NAME);
 
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
    delay(1000);
    digitalWrite(LED, LOW);
    delay(1000);
  } else {
    Serial.println("no");
    digitalWrite(RELAY, LOW);
    delay(1000);
    digitalWrite(LED, HIGH);
    delay(1000);
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
}
