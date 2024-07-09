// DEFINIÇÕES DE PINOS
#define pinSensorFogo 4
#define pinSensorGas 25

#define pinBuzzer 27

// DEFINIÇÕES
#define VAZAMENTO 1240
#define FOGO LOW

// DECLARAÇÃO DE FUNÇÕES
void disparaSirene(byte pin, int intervalo);
void desligaSirene(byte pin);

void setup() {
  Serial.begin(9600);
  pinMode(pinSensorGas, INPUT);
  pinMode(pinSensorFogo, INPUT);
  pinMode(pinBuzzer, OUTPUT);

  Serial.println("Esperando o Sensor Aquecer um pouco");
  delay(5000);

  Serial.println("Fim do setup()");
}

void loop() {
  int nivelGas = analogRead(pinSensorGas);
  bool leituraSensor = digitalRead(pinSensorFogo);
  
  if ( nivelGas >= VAZAMENTO ) {
    disparaSirene(pinBuzzer, 1000);
  } else if ( leituraSensor == FOGO) {
    disparaSirene(pinBuzzer, 500);
  } else {
    desligaSirene(pinBuzzer);
  }
  
}

// IMPLEMENTO DE FUNÇÕES
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
