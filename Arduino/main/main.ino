#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266httpUpdate.h>
#include <ArduinoJson.h>

// MQTT message will be in form JSON format 

// need parsing function to parse MQTT message
// Parse incoming JSON string
// iterate through parsed message

// parse JSON MQTT message
StaticJsonDocument<200> doc;

// function frequencies
const int LOOP_DELAY = 1000;
const int UPDATE_FREQ = 60 * 10; // 60 second * 10 * LOOP_DELAY : once every ten minutes 
int updateCounter = 0;

// WiFi
const char* ssid = "twistedfields";
const char* password = "alwaysbekind";

// MQTT
const char* mqttServer = "192.168.1.123";
const int mqttPort = 1883;
WiFiClient espClient;
PubSubClient client(espClient);

// OTA
HTTPClient httpClient;
const int FW_VERSION = 1;

// hardware pins
const int RELAY = 12;
const int LED = 13;

char* ID;
String MAC;

struct entry
 {
     String MAC;
     char* ID;
 };

entry entries[] = {
    { "C8:2B:96:4F:DC:A6", "p00d00"   },
    { "testMAC"          , "testID" }
};


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
 
  Serial.begin(115200);

  // Wifi
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  // set MAC
  MAC = WiFi.macAddress();

  // set ID
  for (int i = 0; i <= sizeof(entries); i++) {
    if (entries[i].MAC == MAC) { 
      ID = entries[i].ID;
    }
  }
  Serial.println(ID);

  // MQTT
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("valves")) {
 
      Serial.println("connected");  
      client.subscribe("valves");
      Serial.println("subscribed");  
 
    } else {
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
   }
 
} 

void checkForUpdates() {

  // get version
  Serial.println("checking for version update");
  httpClient.begin("http://192.168.1.123/t.version");
  int httpCode = httpClient.GET();

  if( httpCode == 200 ) {
    Serial.println("200");
    String newFWVersion = httpClient.getString();
    Serial.print("version on server: ");
    Serial.print(newFWVersion);
    int newVersion = newFWVersion.toInt();

    if( newVersion > FW_VERSION ) {
      Serial.println( "Preparing to update" );
      // get binary
      t_httpUpdate_return ret = ESPhttpUpdate.update("192.168.1.123", 80,"/newVersion.bin");  
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

int callback(char* topic, byte* payload, unsigned int length) {
  payload[length] = '\0';
  //char json[] = "{\"sensor\":\"gps\",\"time\":1351824120,\"data\":[48.756080,2.302038]}";

  // Deserialize the JSON document
  DeserializationError error = deserializeJson(doc, payload);

  // Test if parsing succeeds.
  if (error) {
    Serial.print(F("deserializeJson() failed: "));
    Serial.println(error.f_str());
    return 1;
  }
 
  const String command = doc[ID];
  Serial.print("command: ");
  Serial.println(command);
  if (command == "on") {
    Serial.println("command is on");
    digitalWrite(RELAY, HIGH);
    digitalWrite(LED, LOW);
  } else {
    Serial.println("command is NOT on");
    digitalWrite(RELAY, LOW);
    digitalWrite(LED, HIGH);
  }


///------
/*
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
*/
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
     client.subscribe("valves");
   } else {
     Serial.print("failed, rc=");
     Serial.print(client.state());
     Serial.println(" try again in 5 seconds");
     // Wait 5 seconds before retrying
     delay(5000);
   }
  }
}

String getMAC()
{
  uint8_t mac[6];
  char result[14];

 snprintf( result, sizeof( result ), "%02x%02x%02x%02x%02x%02x", mac[ 0 ], mac[ 1 ], mac[ 2 ], mac[ 3 ], mac[ 4 ], mac[ 5 ] );
 Serial.println("getMAC():");
 Serial.println(String(result));
 Serial.println("------------");
 Serial.println(WiFi.macAddress());

  return String( result );
}



void loop() {


  // MQTT
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // OTA
  updateCounter = updateCounter + 1;
  if (updateCounter == UPDATE_FREQ) {
    checkForUpdates();
    updateCounter = 0;
  }
  delay(1000);
  getMAC();

}
