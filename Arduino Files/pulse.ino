void setup()
{
  Serial.begin(115200);
  Serial.println("Started!");  
}
void loop()
{
Serial.println(analogRead(A0)); 
delay(1000);
}
