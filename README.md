# Sistema de Gerenciamento de um biodigestor

## Introdução

Esse projeto foi desenvolvido na disciplina de Projeto de Sistemas Ubíquos e Embarcados. O objetivo do Sistema de Gerenciamento de um Biodigestor é criar uma solução prática e eficiente para monitorar e otimizar o processo de biodigestão. Com esse sistema, é possível acompanhar em tempo real parâmetros como temperatura (lidos por dois sensores), pressão atmosférica e níveis de gases inflamáveis, proporcionando uma visão completa do desempenho do biodigestor. Além disso, o sistema conta com funcionalidades de alertas, guardar o históricos dos dados, integração com sensores avançados e acesso remoto, ajudando na gestão eficaz e sustentável do biodigestor. Esse biodigestor é um projeto da associação "Técnicas sem Fronteiras" da faculdade, e foi proposto pelo professor como um protótipo que precisamos desenvolver para eles.

### Objetivos

Os objetivos do projeto são:

- Realizar a leitura e o armazenamento dos dados coletados pelos sensores.
- Disponibilizar um monitoramento em tempo real através de um dashboard.
- Enviar alertas sobre níveis críticos de gás, indicando possíveis vazamentos.
- Controlar a pressão interna do biodigestor, abrindo uma válvula para regular dois reservatórios de gás e evitar sobrecarga.

Abaixo apresentaremos uma visão detalhada da implementação do projeto, incluindo instruções de montagem de hardware, configuração de software, e operação do sistema.

## Hardware

### Visão Geral

O cerne do sistema de gerenciamento do biodigestor é um conjunto de componentes estrategicamente escolhidos para garantir o monitoramento e controle eficaz do processo. O projeto utiliza um ESP32 como unidade central, responsável pela coordenação das operações de leitura e comunicação com o dashboard. O sensor de temperatura DS18B20 monitora a temperatura interna, enquanto o BMP280 registra tanto temperatura quanto pressão do biodigestor. O sensor de gás MQ-2 detecta gases inflamáveis, acionando o buzzer para alertas audíveis. Dois LEDs simulam visualmente o estado dos reservatórios de gás, oferecendo uma representação intuitiva do nível de preenchimento. Essa configuração assegura um funcionamento seguro e eficiente do biodigestor, adaptado às exigências de monitoramento contínuo e intervenção preventiva.

### Detalhes do Hardware

O sistema de gerenciamento do biodigestor utiliza os seguintes componentes de hardware:

- ESP32: Microcontrolador utilizado para processar dados dos sensores e comunicar-se com o sistema de monitoramento.
- Sensor de Temperatura DS18B20: Sensor digital utilizado para medir a temperatura interna do biodigestor.
- Sensor BMP280: Utilizado para medir a temperatura e a pressão do biodigestor.
- Sensor de Gás MQ-2: Sensor utilizado para detectar a presença de gases inflamáveis no biodigestor.
- Buzzer: Dispositivo sonoro que serve como alerta em caso de níveis críticos de gás ou outros eventos importantes.
- LEDs: Dois LEDs utilizados para simular visualmente os reservatórios sendo completados de gás.

## Imagem e descrição do circuito

### PCB

Para o hardware do sistema foi desenvolvido uma PCB como protótipo, abaixo imagens do circuito:
![PCB](https://github.com/matheuskolln/biodigestor/blob/main/hardware/pcb.png)

### Observações Técnicas Importantes

- A presença de uma resistência de 4k7 à 10k entre DATA-DADOS e VCC (3,3v ou 5v) do sensor DS18B20 é extremamente importante visto que ela tem a função de garantir a precisão e referencia para o sensor captar a temperatura corretamente.

### Pinagem

| Pino (Nome no Código) | Número do Pino | Observações                                                                    |
| --------------------- | -------------- | ------------------------------------------------------------------------------ |
| `DS18B20`             | 4              | Utilizado para sensor de temperatura                                           |
| `BMP_CS `             | 10             | Utilizado para sensor de temperatura e pressão                                 |
| `BMP_MOSI`            | 11             | Utilizado para sensor de temperatura e pressão                                 |
| `BMP_MISO`            | 12             | Utilizado para sensor de temperatura e pressão                                 |
| `BMP_SCK`             | 13             | Utilizado para sensor de temperatura e pressão                                 |
| `ledVermelho`         | 14             | Utilizado para led indicar que o reservatorio principal está cheio             |
| `ledVerde`            | 26             | Utilizado para led indicar que a pressão de ambos reservatorios estão estáveis |
| `pinBuzzer`           | 27             | Utilizado para o buzzer                                                        |
| `pinSensorGas`        | 34             | Utilizado para receber as leituras do MQ-2                                     |

Observação Geral:

- Os pinos de leitura analógica devem estar no ADC1 devido ao uso do Wi-Fi, que interfere com o ADC2.
### Referências das Pinagens
![Pinagem](https://github.com/matheuskolln/biodigestor/blob/main/hardware/38_Pinos.png)

## Configuração de Software

### Ambiente de Desenvolvimento

O código-fonte foi desenvolvido na Arduino IDE, uma plataforma de desenvolvimento que permite a escrita, compilação e upload de programas para placas compatíveis com Arduino, como o ESP32 utilizado neste projeto.

### Instalação

1. Instale a última versão da Arduino IDE a partir do [site oficial](https://www.arduino.cc/en/software).
2. Configure a Arduino IDE para suportar o ESP32 seguindo as instruções disponíveis na [documentação do ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).
3. Após a configuração é preciso instalar duas bibliotecas que estão disponíveis em `hardware/bibliotecas`.

# Documentação do Código

O software do projeto que comanda o hardware foi desenvolvido em apenas um arquivo que está na pasta `hardware`. Porém durante o desenvolvimento foram testados todos os sensores separadamente e os códigos de testes também estão disponiveis em `hardware/testes`.

### Observação importante

Devido à necessidade de medir a pressão interna durante a digestão de matéria orgânica e a liberação de gases, realizar testes com o sensor de pressão torna-se desafiador. Para contornar essa dificuldade, estamos utilizando um contador para simular a atuação do sensor de pressão. Este contador simula a leitura da pressão e a liberação de uma válvula para igualar a pressão entre o reservatório de gás e o ambiente de produção.

Abaixo vamos a uma explicação do código:

<details>
  <summary><b>Bibliotecas Importadas</b></summary>
    
    #include <OneWire.h>
    #include <DallasTemperature.h>
    #include <Wire.h>
    #include <SPI.h>
    #include <Adafruit_BMP280.h>
    #include <WiFi.h>
    #include <PubSubClient.h>

- **OneWire**: Protocolo de comunicação para o sensor de temperatura DS18B20.
- **DallasTemperature**: Biblioteca específica para sensores de temperatura Dallas (como DS18B20).
- **Wire e SPI**: Protocolos de comunicação I2C e SPI, respectivamente.
- **Adafruit_BMP280**: Biblioteca para o sensor de temperatura e pressão BMP280.
- **WiFi e PubSubClient**: Bibliotecas para conexão Wi-Fi e comunicação via MQTT.
</details>

<details>
  <summary><b>Definições de Pinos e Constantes</b></summary>
    
    #define DS18B20        4 
    #define pinSensorGas  34 
    #define pinBuzzer     27
    #define ledVerde      26
    #define ledVermelho   14
    #define BMP_SCK      (13)
    #define BMP_MISO     (12)
    #define BMP_MOSI     (11)
    #define BMP_CS       (10)
    #define VAZAMENTO    1240

- Definem os pinos do ESP32 usados para os sensores e atuadores.
- **VAZAMENTO**: é o valor de referência para detecção de vazamento de gás.
</details>

<details>
  <summary><b>Declaração de Funções</b></summary>
    
    void disparaSirene(byte pin, int intervalo);
    void desligaSirene(byte pin);
    void ligaLed(byte pin);
    void desligaLed(byte pin);

- Funções para controlar a sirene e os LEDs.
</details>

<details>
  <summary><b>Instanciação de Objetos</b></summary>
    
    OneWire oneWire(DS18B20);
    DallasTemperature Sensor(&oneWire);
    Adafruit_BMP280 bmp;

- **oneWire** : Configura o pino do sensor DS18B20.
- **Sensor**: Configura o sensor de temperatura DS18B20.
- **bmp**: Configura o sensor de temperatura e pressão BMP280.
</details>

<details>
  <summary><b>Variáveis Globais</b></summary>
    
    float leitura_DS1820;
    float leitura_BMP280;
    float pressao_BMP280;
    int p_tanque1 = 0;
    int p_tanque2 = 10;
    const char* ssid = "lab120";
    const char* password = "labredes120";
    const char* mqtt_server = "broker.mqtt-dashboard.com";
    WiFiClient ESP_Monitor;
    PubSubClient client(ESP_Monitor);
    unsigned long lastMsg = 0;
    #define MSG_BUFFER_SIZE  (50)
    char msg[MSG_BUFFER_SIZE];
    int value = 0;

- Variáveis para armazenar leituras dos sensores.
- Configurações de Wi-Fi e MQTT.
- Variáveis para simular os níveis dos tanques de gás.
</details>

<details>
  <summary><b>Função 'setup_wifi'</b></summary>
    
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

- Conecta o ESP32 à rede Wi-Fi.
</details>

<details>
  <summary><b>Função 'reconnect'</b></summary>
    
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

- Reconecta ao broker MQTT se a conexão for perdida.
</details>

<details>
  <summary><b>Função 'setup'</b></summary>
    
    void setup() {
     Serial.begin(9600);
     pinMode(pinSensorGas, INPUT);
     pinMode(pinBuzzer, OUTPUT);
     pinMode(ledVerde, OUTPUT);
     pinMode(ledVermelho, OUTPUT);
     Serial.println("Esperando o Sensor MQ-2 aquecer um pouco");
     delay(5000);
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
      bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                  Adafruit_BMP280::SAMPLING_X2,
                  Adafruit_BMP280::SAMPLING_X16,
                  Adafruit_BMP280::FILTER_X16,
                  Adafruit_BMP280::STANDBY_MS_500);
      Serial.println("Fim do setup()"); 
    }

- Configura os pinos, inicializa sensores e conecta ao Wi-Fi e MQTT.
- Realiza uma leitura inicial do sensor de gás.
</details>

<details>
  <summary><b>Função 'loop'</b></summary>
    
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
        delay(1000);
      }
      desligaLed(ledVermelho);
      delay(20);
      ligaLed(ledVerde);
      delay(2000);
      desligaLed(ledVerde);
    }
    delay(2000);
    }

- Lê o sensor de gás e publica o valor via MQTT.
- Dispara ou desliga a sirene com base no valor do gás.
- Lê e publica as temperaturas e pressão dos sensores.
- Simula a lógica de controle dos tanques e aciona os LEDs conforme a condição dos tanques.
</details>

<details>
  <summary><b>Funções Auxiliares</b></summary>
    
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

- **disparaSirene**: Alterna o estado do pino do buzzer para simular uma sirene.
- **desligaSirene**: Desliga o buzzer.
- **ligaLed** e **desligaLed**: Controlam o estado dos LEDs.
</details>

### Observação sobre BMP280

Durante os testes de uso dos sensores, precisamos identificar qual é o endereço do sensor BMP280. Para isso é preciso rodar o código `for_ic2.ino` em `hardware/testes`. Apos ter o endreço do sensor na função stup do código é nescessário passar o valor correto em `status = bmp.begin(0x76);`. No nosso caso o endereço era `0x76`.

## Ultilização do Node-Red

Node-RED é uma ferramenta de programação visual que permite conectar dispositivos, APIs e serviços online de maneira intuitiva. Com uma interface baseada em fluxos, o Node-RED facilita a criação e a implementação de lógica de controle e automação.

Utilizamos o Node-RED para montar um dashboard interativo, que nos permite monitorar em tempo real os dados coletados pelos sensores do nosso Sistema de Gerenciamento de Biodigestor. Esta plataforma nos possibilita visualizar informações como temperatura, pressão e níveis de gás, proporcionando uma maneira eficiente de 
acompanhar e gerenciar o desempenho do biodigestor.

O flow do projeto está disponivel em `hardware/flows.json`.

![node_red](https://github.com/matheuskolln/biodigestor/blob/main/hardware/node-red/Captura%20de%20tela%20de%202024-07-09%2017-29-55.png)


# Biodigestor Server

This is the server for the biodigestor project. It is a REST API that allows the client to interact with the biodigestor and perform actions such as reading the data and posting into the database.

# Prerequisites

- Python 3.x
- Django 3.x or higher
- A database (PostgreSQL is recommended)

# Installation

1. Clone the repository

```bash
git clone https://github.com/matheuskolln/biodigestor
cd biodigestor
```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

4. Apply the migrations

```bash
python manage.py migrate
```

5. Run the server

```bash
python manage.py runserver
```

# Models

The server has three models: `User`, `Biodigestor` and `Measurement`.

## User

The `User` model is used to authenticate the client. It has the following fields:

- `name`: The user's name
- `email`: The user's email
- `password`: The user's password
- `created_at`: The date and time the user was created
- `updated_at`: The date and time the user was last updated

## Biodigestor

The `Biodigestor` model represents the biodigestor. It has the following fields:

- `name`: The biodigestor's name
- `description`: A description of the biodigestor
- `created_at`: The date and time the biodigestor was created
- `updated_at`: The date and time the biodigestor was last updated

## Measurement

The `Measurement` model represents a measurement taken from the biodigestor. It has the following fields:

- `internal_temperature`: The internal temperature of the biodigestor
- `external_temperature`: The external temperature of the biodigestor
- `main_pressure`: The main pressure of the biodigestor
- `gas_level`: The gas level of the biodigestor
- `created_at`: The date and time the measurement was taken
- `updated_at`: The date and time the measurement was last updated

# Views

The server has three views: `UserView`, `BiodigestorView` and `MeasurementView`.

## UserView

The `UserView` is used to create, read, update and delete users. It has the following endpoints:

- `GET /users/`: Get a list of all users
- `POST /users/`: Create a new user: `name`, `email` and `password` are required

## BiodigestorView

The `BiodigestorView` is used to create, read, update and delete biodigestors. It has the following endpoints:

- `GET /biodigestors/`: Get a list of all biodigestors
- `POST /biodigestors/`: Create a new biodigestor: `name` and `description` are required

## MeasurementView

The `MeasurementView` is used to create, read, update and delete measurements. It has the following endpoints:

- `GET /measurements/`: Get a list of all measurements
- `POST /measurements/`: Create a new measurement: `internal_temperature`, `external_temperature`, `main_pressure` and `gas_level` are required
