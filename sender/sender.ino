#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>



//khai bao bien
const char* ssid = "KasdaMiFi-FA5B";
const char* password = "6060067729";
#define buttonPin 5
#define LED 4
int tick = 0;
String time_signal = "";
int pressTime = 0;
String post_data;



void setup () {
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(LED, OUTPUT);
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(1000);
    Serial.print("Connecting..");
  }

}


void post_request(String data) {
  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status

    HTTPClient http;    //Declare object of class HTTPClient

    http.begin("http://45.117.169.186:5000/api_1_0/data");      //Specify request destination
    http.addHeader("Content-Type", "text/plain");  //Specify content-type header

    int httpCode = http.POST(data);   //Send the request
    String payload = http.getString();                  //Get the response payload

    Serial.println(httpCode);   //Print HTTP return code
    Serial.println(payload);    //Print request response payload

    http.end();  //Close connection

  } else {

    Serial.println("Error in WiFi connection");

  }
}


void vibrateShort() {
  analogWrite(LED, 600);
  delay(200);
  analogWrite(LED, 0);
}

void vibrateLong() {
  analogWrite(LED, 600);
  delay(700);
  analogWrite(LED, 0);
}

void buttonStore() {
  pressTime = pressTime + 1;
}

void loop() {
  if ((digitalRead(buttonPin) == 0)) { //khi nut duoc nhan
    delay(20); // nghi 20 mili giay de chong nhieu
    while ((digitalRead(buttonPin) == 0)) {
      tick = tick + 1; // dem thoi gian tuong doi
      Serial.println(tick);
    }
  }
  if ((digitalRead(buttonPin) == 1)) { //neu thoi gian nhan qua thap huy tick
    if (tick < 70) {
      tick = 0;
    }
    else if ((70 < tick) and (tick < 1000)) { //danh dau timestamp
      buttonStore();
      vibrateShort();
      tick = 0;
    }

    else {
      Serial.println("Long press");
      post_data = String(pressTime);
      post_request(post_data);//gui tra loi len server
      vibrateLong();
      post_data = "";
      pressTime = 0;
      tick = 0;
    }
  }

}
