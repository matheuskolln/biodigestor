#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_BMP280.h>
#include <WiFi.h>
#include <PubSubClient.h>

// DEFINIÇÕES
#define DS18B20        4 
#define pinSensorGas  34 
#define pinBuzzer     27
#define ledVerde      26
#define ledVermelho   14
#define BMP_SCK      (13)
#define BMP_MISO     (12)
#define BMP_MOSI     (11)
#define BMP_CS       (10)
#define VAZAMENTO   1240

// DECLARAÇÃO DE FUNÇÕES
void disparaSirene(byte pin, int intervalo);
void desligaSirene(byte pin);

//Instancia o Objeto oneWire e Seta o pino do Sensor para iniciar as leituras
OneWire oneWire(DS18B20);

//Repassa as referencias do oneWire para o Sensor Dallas (DS18B20)
DallasTemperature Sensor(&oneWire);

Adafruit_BMP280 bmp; // I2C

// Variavel para Armazenar os dados de Leitura
float leitura_DS1820;
float leitura_BMP280;
float pressao_BMP280;

// Variáveis dos tanques
int p_tanque1 = 0;
int p_tanque2 = 10;

//MQTT / Node-Red cfg
const char* ssid = "lab120";
const char* password = "labredes120";
const char* mqtt_server = "broker.mqtt-dashboard.com";

WiFiClient ESP_Monitor;
PubSubClient client(ESP_Monitor);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
  delay(2000);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP_Monitor")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(pinSensorGas, INPUT);
  pinMode(pinBuzzer, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledVermelho, OUTPUT);
  Serial.println("Esperando o Sensor MQ-2 aquecer um pouco");
  delay(5000);

  // Teste de leitura do sensor de gás antes da conexão Wi-Fi
  int nivelGas = analogRead(pinSensorGas);
  Serial.print("Leitura do sensor de gás antes do Wi-Fi: ");
  Serial.println(nivelGas);

  setup_wifi();
  client.setServer(mqtt_server, 1883);

  Sensor.begin();
  
  unsigned status;
  status = bmp.begin(0x76);
  if (!status) {
    Serial.println(F("Could not find a valid BMP280 sensor, check wiring or try a different address!"));
    while (1) delay(10);
  }

  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                  Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                  Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                  Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                  Adafruit_BMP280::STANDBY_MS_500); /* Standby time. */

 Serial.println("Fim do setup()"); 
}

void loop() {
  reconnect();

  int nivelGas = analogRead(pinSensorGas);
  Serial.println(nivelGas);
  client.publish("Nivel_gas", String(nivelGas).c_str());

  if (nivelGas >= VAZAMENTO) {
    Serial.println("Aqui");
    disparaSirene(pinBuzzer, 1000);
  } else {
    desligaSirene(pinBuzzer);
  }

  Sensor.requestTemperatures();
  leitura_DS1820 = Sensor.getTempCByIndex(0);
  leitura_BMP280 = bmp.readTemperature();
  pressao_BMP280 = bmp.readPressure();
  
  client.publish("Temperatura_DS1820", String(leitura_DS1820).c_str());
  client.publish("Temperatura_BMP280", String(leitura_BMP280).c_str());
  client.publish("Pressao_BMP280", String(pressao_BMP280).c_str());

  Serial.print(leitura_DS1820);
  Serial.println("ºC by DS18B20"); 
  Serial.println("--------------------------------------"); 
  Serial.print(F("Temperature = "));
  Serial.print(leitura_BMP280);
  Serial.println(" ºC by BMP280");
  Serial.print(F("Pressure = "));
  Serial.print(pressao_BMP280);
  Serial.println(" Pa");
  Serial.println("--------------------------------------");
  Serial.println();



  // Lógica de controle dos tanques
  if (p_tanque1 < 20) {
    p_tanque1++;
    client.publish("SimPress", String(p_tanque1).c_str());
    Serial.print("p_tanque1: ");
    Serial.println(p_tanque1);
    delay(1000);
  } else {
    ligaLed(ledVermelho);
    while (p_tanque1 > p_tanque2) {
      p_tanque1--;
      client.publish("SimPress", String(p_tanque1).c_str());
      Serial.print("p_tanque1: ");
      Serial.println(p_tanque1);
      delay(1000); // Simula o tempo para esvaziar o tanque
    }
    desligaLed(ledVermelho);
    delay(20);
    ligaLed(ledVerde);
    delay(2000); // LED Verde acende por 2 segundos
    desligaLed(ledVerde);
  }
 
  delay(2000);
}

void disparaSirene(byte pin, int intervalo) {
  static bool nivel = HIGH;
  static unsigned long ultimaTroca = 0;

  if (millis() - ultimaTroca > intervalo) {
    nivel = !nivel;
    ultimaTroca = millis();
    Serial.println("DISPARO");
  }
  
  digitalWrite(pin, nivel);  
}

void desligaSirene(byte pin) {
  digitalWrite(pin, LOW);
}



void ligaLed(byte pin) {
  digitalWrite(pin, HIGH);
}

void desligaLed(byte pin) {
  digitalWrite(pin, LOW);
}
