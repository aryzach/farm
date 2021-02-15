#include <SPI.h>
#include <ESP8266WiFi.h>        // Include the Wi-Fi library
#include <ESP8266WiFiMulti.h>   // Include the Wi-Fi-Multi library
#include <ArduinoMqttClient.h>
#include <PubSubClient.h>
//#include <ESP8266mDNS.h>        // Include the mDNS library
//#if defined(ARDUINO_SAMD_MKRWIFI1010) || defined(ARDUINO_SAMD_NANO_33_IOT) || defined(ARDUINO_AVR_UNO_WIFI_REV2)
//  #include <WiFiNINA.h>
//#elif defined(ARDUINO_SAMD_MKR1000)
//  #include <WiFi101.h>
//#elif defined(ARDUINO_ESP8266_ESP12)
#include <ESP8266WiFi.h>
//#endif

// test globals
int LED_SONOFF = 0;
int BLINK_DURATION = 3000;
int cool = 1;
void setupPins();
void testPins();

// wifi globals
ESP8266WiFiMulti wifiMulti;     // Create an instance of the ESP8266WiFiMulti class, called 'wifiMulti'

// mqtt globals
const char* mqtt_server = "192.168.1.123";
PubSubClient client(espClient);


void setup() {
  Serial.begin(115200);         // Start the Serial communication to send messages to the computer
  delay(10);
  //while (!Serial) {
  //  ; // wait for serial port to connect. Needed for Leonardo only  
  //}
  Serial.println("enter setup");

  //delay(10000); // delay 10 seconds to find wifi
  Serial.println("enter wifi setup");
  wifiSetup();
  Serial.println("end wifi setup");

  Serial.println("enter mqtt setup");
  //mqttSetup();
  Serial.println("end mqtt setup");

  Serial.println("enter pin setup");
  setupPins(); 
  Serial.println("end pin setup");

}
  
void loop() {
  Serial.println("start loop");
  testGPIO(12);
  //mqttLoop();
}

// the loop function runs over and over again forever
void testGPIO(int gpio) {
  Serial.println(gpio);
  Serial.println("start relay");
  digitalWrite(gpio, HIGH);
  digitalWrite(13,HIGH);
  delay(BLINK_DURATION);  
  Serial.println("pin low");
  digitalWrite(gpio, LOW);
  digitalWrite(13,LOW);
  delay(BLINK_DURATION); 
}

void setupPins() {
  for(int i = 12; i < 15; i++)
      {
          Serial.println("setting up: ");
          Serial.println(i);
          pinMode(i, OUTPUT);

      }
}

void testPins() {
  for(int i = 12; i < 15; i++)
      {
          Serial.println("testing: ");
          Serial.println(i);
          testGPIO(i);

      }
  }




void mqttSetup() {
  mqttClient.setId("clientId");

  // You can provide a username and password for authentication
  // mqttClient.setUsernamePassword("username", "password");

  Serial.println("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  if (!mqttClient.connect(broker, port)) {
    Serial.println("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());

    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();

  Serial.print("Subscribing to topic: ");
  Serial.println(topic);
  Serial.println();

  // subscribe to a topic
  mqttClient.subscribe(topic);

  // topics can be unsubscribed using:
  // mqttClient.unsubscribe(topic);

  Serial.print("Waiting for messages on topic: ");
  Serial.println(topic);
  Serial.println();
}


void wifiSetup() {
  
  wifiMulti.addAP("twistedfields", "alwaysbekind");   // add Wi-Fi networks you want to connect to
  //wifiMulti.addAP("ssid_from_AP_2", "your_password_for_AP_2");
  //wifiMulti.addAP("ssid_from_AP_3", "your_password_for_AP_3");

  Serial.println("Connecting ...");
  int i = 0;
  while (wifiMulti.run() != WL_CONNECTED) { // Wait for the Wi-Fi to connect: scan for Wi-Fi networks, and connect to the strongest of the networks above
    delay(1000);
    Serial.print('.');
  }
  Serial.println('\n');
  Serial.print("Connected to ");
  delay(10);
  Serial.println(WiFi.SSID());              // Tell us what network we're connected to
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());           // Send the IP address of the ESP8266 to the computer
}

//void mDnsSetup() {
//  if (!MDNS.begin("valve1")) {             // Start the mDNS responder for esp8266.local
//    Serial.println("Error setting up MDNS responder!");
//  }
//  Serial.println("mDNS responder started");
//}


int readPins() {
  // read the analog sensor:
  int sensorReading = analogRead(A0);   
  return sensorReading;
}

void mqttLoop() {
  int messageSize = mqttClient.parseMessage();
  if (messageSize) {
    // we received a message, print out the topic and contents
    Serial.print("Received a message with topic '");
    Serial.print(mqttClient.messageTopic());
    Serial.print("', length ");
    Serial.print(messageSize);
    Serial.println(" bytes:");

    // use the Stream interface to print the contents
    while (mqttClient.available()) {
      Serial.print((char)mqttClient.read());
    }
    Serial.println();

    Serial.println();
    }
}

