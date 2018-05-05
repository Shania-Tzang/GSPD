// Temperature/humidity library
#include <DHT.h>

// Light sensor libraries
#include <Wire.h>
#include "Adafruit_SI1145.h"

Adafruit_SI1145 uv = Adafruit_SI1145();

#define DHTPIN 7 // Pin #7
#define DHTTYPE DHT22 // DHT 22  (AM2302)
#define BTSerial Serial1 // Bluetooth serial communication

DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor

int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value


void setup() {
  // Temperature/humidity
  Serial.begin(9600);
  //Serial.println("Enter AT commands:");
  //dht.begin();

  // Light sensor  
  if (!uv.begin()) {
    //Serial.println("Didn't find light sensor.");
    while (1);
  }

  //Serial.println("Setting up...");
  //Serial.println("Light sensor OK!\n\n");

  // Bluetooth
  BTSerial.begin(9600);
}

void loop() {
  
  // Temperature/humidity
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  /*
  BTSerial.println("\n=== TEMPERATURE / HUMIDITY ======");
  BTSerial.print("Humidity (%): ");
  BTSerial.println(hum);
  BTSerial.print("Temperature (°C): ");
  BTSerial.println(temp);

  // Light sensor
  BTSerial.println("=== LIGHT SENSOR ================");
  BTSerial.print("Vis: "); 
  BTSerial.println(uv.readVisible());
  BTSerial.print("IR: "); 
  BTSerial.println(uv.readIR());
  */
  BTSerial.print("Humidity (%): ");
  BTSerial.print(hum);
  BTSerial.print(" | Temperature (°C): ");
  BTSerial.print(temp);
  BTSerial.print(" | Vis: "); 
  BTSerial.print(uv.readVisible());
  BTSerial.print(" | IR: "); 
  BTSerial.println(uv.readIR());

  // Print the information also on the serial channel, to be sure.
  Serial.println("\n=== TEMPERATURE / HUMIDITY ======");
  Serial.print("Humidity (%): ");
  Serial.println(hum);
  Serial.print("Temperature (°C): ");
  Serial.println(temp);
  Serial.println("=== LIGHT SENSOR ================");
  Serial.print("Vis: "); 
  Serial.println(uv.readVisible());
  Serial.print("IR: "); 
  Serial.println(uv.readIR());

  // Does not output any data, not using this atm
  /*float UVindex = uv.readUV();
  UVindex /= 100.0;  
  BTSerial.print("UV: ");  Serial.println(UVindex);*/

  int delay_seconds = 5;
  delay(delay_seconds * 1000);
}
