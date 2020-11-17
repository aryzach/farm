int LED_SONOFF = 13;
int BLINK_DURATION = 2000;

int cool = 1;


// the setup function runs once when you press reset or power the board
void osetup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_SONOFF, OUTPUT);
}

// the loop function runs over and over again forever
void oloop() {
  digitalWrite(LED_SONOFF, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(BLINK_DURATION);                       // wait for a second
  digitalWrite(LED_SONOFF, LOW);    // turn the LED off by making the voltage LOW
  delay(BLINK_DURATION);                       // wait for a second
  Serial.print(cool);
  cool += 1;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  osetup();
}

void loop() {
  // put your main code here, to run repeatedly:
  oloop();

}
