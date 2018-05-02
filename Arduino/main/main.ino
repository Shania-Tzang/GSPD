// Temperature/humidity library
#include <DHT.h>

// Light sensor libraries
#include <Wire.h>
#include "Adafruit_SI1145.h"

Adafruit_SI1145 uv = Adafruit_SI1145();

#define DHTPIN 7 // Pin #7
#define DHTTYPE DHT22 // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE); //// Initialize DHT sensor

int chk;
float hum;  //Stores humidity value
float temp; //Stores temperature value


void setup() {
  // Temperature/humidity
  Serial.begin(9600);
  dht.begin();

  // Light sensor  
  if (! uv.begin()) {
    Serial.println("Didn't find light sensor.");
    while (1);
  }

  Serial.println("Setting up...");
  Serial.println("Light sensor OK!\n\n");
}

void loop() {
  // Temperature/humidity
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  Serial.println("\n=== TEMPERATURE / HUMIDITY ======");
  Serial.print("Humidity: ");
  Serial.print(hum);
  Serial.println(" %");
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println(" °C");

  Serial.println("=== LIGHT SENSOR ================");
  Serial.print("Vis: "); 
  Serial.println(uv.readVisible());
  Serial.print("IR: "); 
  Serial.println(uv.readIR());

  float UVindex = uv.readUV();
  UVindex /= 100.0;  
  Serial.print("UV: ");  Serial.println(UVindex);
  
  delay(5000);
}
