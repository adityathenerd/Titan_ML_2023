#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Firebase_ESP_Client.h>

#include <WiFi.h>
#include "time.h"

#include "MAX30105.h"
#include "heartRate.h"
#include "spo2_algorithm.h"

#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

#define WIFI_SSID "RedmiB"
#define WIFI_PASSWORD "9556408049"
#define API_KEY "AIzaSyCR76F4ny2b_V-GPlA7XmZQzpZfRj_lyT4"
#define DATABASE_URL "https://hacksmiths---02-default-rtdb.asia-southeast1.firebasedatabase.app/"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

int pulseSensor = 0;
String uid;
String databasePath;
String parentPath;
String PulsePath = "/Pulse";
String AXPath = "/MPU/acc_x";
String AYPath = "/MPU/acc_y";
String AZPath = "/MPU/acc_z";
String GXPath = "/MPU/gyro_x";
String GYPath = "/MPU/gyro_y";
String GZPath = "/MPU/gyro_z";
String TempPath = "/MPU/Temp";
String spO2Path = "/SpO2";
String timePath = "Sensor/timestamp";

int timestamp;
FirebaseJson json;

const char* ntpServer = "pool.ntp.org";

unsigned long sendDataPrevMillis = 0;
bool signupOK = false;

MAX30105 particleSensor;
double avered    = 0; 
double aveir     = 0;
double sumirrms  = 0;
double sumredrms = 0;
int    i         = 0;
int    Num       = 100;  // For calculating SpO2 by this sampling interval
int    Temperature;
int    temp;
float  ESpO2;            // initial value of estimated SpO2
double FSpO2     = 0.7;  // filter factor for estimated SpO2
double frate     = 0.95; // low pass filter for IR/red LED value to eliminate AC component
#define TIMETOBOOT 3000  // wait for this time(msec) to output SpO2
#define SCALE      88.0  // adjust to display heart beat and SpO2 in the same scale
#define SAMPLING   100 //25 //5  // if user wants to see heart beat more precisely, he/she can set SAMPLING to 1.
#define FINGER_ON  30000 // if red signal is lower than this, it indicates user's finger is not on the sensor.
#define USEFIFO

#define MAX_BRIGHTNESS 255

const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]; //Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; //Time at which the last beat occurred

#if defined(__AVR_ATmega328P__) || defined(__AVR_ATmega168__)
uint16_t irBuffer[100]; //infrared LED sensor data
uint16_t redBuffer[100];  //red LED sensor data
#else
uint32_t irBuffer[100]; //infrared LED sensor data
uint32_t redBuffer[100];  //red LED sensor data
#endif
int32_t bufferLength;
int32_t spo2; 
int8_t validSPO2;
int32_t heartRate;
int8_t validHeartRate;

float beatsPerMinute;
int beatAvg;

int PulseSensorPin = 36;
// int MPUDataPin = 21;
int LED =2;

int Signal;
int Threshold = 2000;

float acc_x;
float acc_y; 
float acc_z;
float gyro_x;
float gyro_y;
float gyro_z;
float tempc;
int spo2_data;

Adafruit_MPU6050 mpu;

byte pulseLED = 11;
byte readLED = 13; 

// Function that gets current epoch time
unsigned long getTime() {
  time_t now;
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    //Serial.println("Failed to obtain time");
    return(0);
  }
  time(&now);
  return now;
}

void setup()
{
  Serial.begin(115200);
  Serial.println("Initializing...");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  configTime(0, 0, ntpServer);
  /* For assigning the api key (required) */
  config.api_key = API_KEY;

  /* For assigning the RTDB URL (required) */
  config.database_url = DATABASE_URL;

  /* Sign up */
  if (Firebase.signUp(&config, &auth, "", "")){
    Serial.println("ok");
    signupOK = true;
  }
  else{
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }
  /* For assigning the callback function for the long running token generation task */
  config.token_status_callback = tokenStatusCallback; //see addons/TokenHelper.h
  config.max_token_generation_retry = 5;

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
  fbdo.setResponseSize(4096);
  
  // Getting the user UID might take a few seconds
  Serial.println("Getting User UID");
  while ((auth.token.uid) == "") {
    Serial.print('.');
    delay(1000);
  }
  // For Printing user UID
  uid = auth.token.uid.c_str();
  Serial.print("User UID: ");
  Serial.println(uid);

  // For updating database path
  databasePath = "/UsersData/" + uid + "/readings";

 // For initializing pulse
 pinMode(LED,OUTPUT); 

  // For initializing MAX30102 sensor
  while (!particleSensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30102 was not found. Please check wiring/power/solder jumper at MH-ET LIVE MAX30102 board. ");
    //while (1);
  }
  byte ledBrightness = 0x7F; //Options: 0=Off to 255=50mA
  byte sampleAverage = 4; //Options: 1, 2, 4, 8, 16, 32
  byte ledMode       = 2; //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green
  //Options: 1 = IR only, 2 = Red + IR on MH-ET LIVE MAX30102 board
  int sampleRate     = 200; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth     = 411; //Options: 69, 118, 215, 411
  int adcRange       = 16384; //Options: 2048, 4096, 8192, 16384

    // For setting up the wanted parameters
  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); //Configure sensor with these settings

  particleSensor.enableDIETEMPRDY();

  //MPU6050 TEST
  Serial.println("Adafruit MPU6050 test!");

  // For trying to initialize.
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");
  mpu.setAccelerometerRange(MPU6050_RANGE_16_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
   Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }

  Serial.println("");
  delay(100);
}

void loop(){

  int pulseData = analogRead(PulseSensorPin);

  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
   acc_x = a.acceleration.x;
   acc_y = a.acceleration.y;
   acc_z = a.acceleration.z;
   
   gyro_x = g.gyro.x;
   gyro_y = g.gyro.y;
   gyro_z = g.gyro.z;
   tempc = temp.temperature;

  uint32_t ir, red, green;
  double fred, fir;
  double SpO2 = 0; //raw SpO2 before low pass filtered
  
#ifdef USEFIFO
  particleSensor.check(); //To Check the sensor, and read up to 3 samples
  while (particleSensor.available()) { //if we have new data
#ifdef MAX30105
   red = particleSensor.getFIFORed(); //Sparkfun's MAX30105
   ir  = particleSensor.getFIFOIR();  //Sparkfun's MAX30105
#else
   red = particleSensor.getFIFOIR();  
   ir  = particleSensor.getFIFORed(); 
#endif
i++;
    fred = (double)red;
    fir  = (double)ir;
    avered = avered * frate + (double)red * (1.0 - frate); //To compute average red level by low pass filter
    aveir = aveir * frate + (double)ir * (1.0 - frate); //To calculate average IR level by low pass filter
    sumredrms += (fred - avered) * (fred - avered); //To compute square sum of alternate component of red level
    sumirrms += (fir - aveir) * (fir - aveir);//To calculate square sum of alternate component of IR level
    if ((i % SAMPLING) == 0) {// To slow down graph plotting speed for arduino Serial plotter by thin out
      if ( millis() > TIMETOBOOT) {
        float ir_forGraph = (2.0 * fir - aveir) / aveir * SCALE;
        float red_forGraph = (2.0 * fred - avered) / avered * SCALE;
        //truncation for Serial plotter's autoscaling
        if ( ir_forGraph > 100.0) ir_forGraph = 100.0;
        if ( ir_forGraph < 80.0) ir_forGraph = 80.0;
        if ( red_forGraph > 100.0 ) red_forGraph = 100.0;
        if ( red_forGraph < 80.0 ) red_forGraph = 80.0;
        // To print out red and IR sensor reading to serial interface for monitoring...
        Serial.print("Red: "); Serial.print(red); Serial.print(","); Serial.print("Infrared: "); Serial.print(ir); Serial.print(".    ");
        float temperature = particleSensor.readTemperatureF();
        
        if (ir < FINGER_ON){ //if no finger on the sensor is found
           Serial.println("No finger detected");
           break;
        }
        if(ir > FINGER_ON){
           //Temperature = mlx.readObjectTempC();
           Serial.print("Oxygen % = ");
           Serial.print(ESpO2);
           Serial.println("%");
        }
      }
    }
    if ((i % Num) == 0) {
      double R = (sqrt(sumredrms) / avered) / (sqrt(sumirrms) / aveir);
      // Serial.println(R);
      SpO2 = -23.3 * (R - 0.4) + 100; 
      ESpO2 = FSpO2 * ESpO2 + (1.0 - FSpO2) * SpO2;//low pass filter
      //  Serial.print(SpO2);Serial.print(",");Serial.println(ESpO2); //It was done for debugging purposes.
      sumredrms = 0.0; sumirrms = 0.0; i = 0;
      break;
    }
    particleSensor.nextSample(); //We're finished with this sample so move to next sample.
  }
#endif

if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0)){
    sendDataPrevMillis = millis();
    //To get current timestamp
    timestamp = getTime();
    Serial.print ("time: ");
    Serial.println (timestamp);

    parentPath = databasePath + "/" + String(timestamp);
    // Pulse Data
    int pulseData = analogRead(PulseSensorPin);
    
}
    json.set(PulsePath.c_str(),pulseData);
    json.set(TempPath.c_str(), tempc);
    json.set(AXPath.c_str(), acc_x);
    json.set(AYPath.c_str(), acc_y);
    json.set(AZPath.c_str(), acc_z);
    json.set(GXPath.c_str(), gyro_x);
    json.set(GYPath.c_str(), gyro_y);
    json.set(GZPath.c_str(), gyro_z);
    json.set(spO2Path.c_str(),ESpO2);
    json.set(timePath, String(timestamp));

Serial.printf("Set json... %s\n", Firebase.RTDB.setJSON(&fbdo, parentPath.c_str(), &json) ? "ok" : fbdo.errorReason().c_str());

} 

