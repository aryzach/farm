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
//int callback(char* topic, byte* payload, unsigned int length); 

// OTA
HTTPClient httpClient;
const int FW_VERSION = 2;

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


void setup() {

  setupPins();
 
  Serial.begin(9600);

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
 
} 

void checkForUpdates() {

  // get version
  Serial.println("begin check");
  httpClient.begin("http://192.168.1.123/t.version");
  Serial.println("after httpClient.begin");

  int httpCode = httpClient.GET();
  Serial.println("GET");
  Serial.println(httpCode);

  if( httpCode == 200 ) {
    Serial.println("200");
    String newFWVersion = httpClient.getString();
    Serial.print("version on server: ");
    Serial.print(newFWVersion);
    int newVersion = newFWVersion.toInt();

    if( newVersion > FW_VERSION ) {
      Serial.println( "Preparing to update" );
      // get binary
      t_httpUpdate_return ret = ESPhttpUpdate.update("192.168.1.123", 80,"/t.bin");  
      switch(ret) {
        case HTTP_UPDATE_FAILED:
          Serial.printf("HTTP_UPDATE_FAILD Error (%d): %s", ESPhttpUpdate.getLastError(), ESPhttpUpdate.getLastErrorString().c_str());
          break;

        case HTTP_UPDATE_NO_UPDATES:
          Serial.println("HTTP_UPDATE_NO_UPDATES");
          break;
       }
     }
   }
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
  digitalWrite(LED, HIGH);
  delay(300);
  digitalWrite(LED, LOW);
  delay(300);
  digitalWrite(LED, HIGH);
  delay(300);
  digitalWrite(LED, LOW);
  delay(300);
  digitalWrite(LED, HIGH);
  delay(300);
  digitalWrite(LED, LOW);
}
