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

O cerne do sistema de gerenciamento do biodigestor é um conjunto de componentes estrategicamente escolhidos para garantir o monitoramento e controle eficaz do processo. O projeto utiliza um ESP32 como unidade central, responsável pela coordenação das operações de leitura e comunicação com o dashboard. O sensor de temperatura DS18B20 monitora a temperatura interna, enquanto o BMP280 registra tanto temperatura quanto pressão do biodigestor. O sensor de gás MQ-2 detecta gases inflamáveis, acionando o buzzer para alertas audíveis. Dois LEDs simulam visualmente o estado dos reservatórios de gás, oferecendo uma representação intuitiva do nível de preenchimento. Essa configuração assegura um funcionamento seguro e eficiente do biodigestor, adaptado às exigências de monitoramento contínuo e intervenção preventiva..

### Detalhes do Hardware

O sistema de gerenciamento do biodigestor utiliza os seguintes componentes de hardware:

- ESP32: Microcontrolador utilizado para processar dados dos sensores e comunicar-se com o sistema de monitoramento.
- Sensor de Temperatura DS18B20: Sensor digital utilizado para medir a temperatura interna do biodigestor.
- Sensor BMP280: Utilizado para medir a temperatura e a pressão do biodigestor.
- Sensor de Gás MQ-2: Sensor utilizado para detectar a presença de gases inflamáveis no biodigestor.
- Buzzer: Dispositivo sonoro que serve como alerta em caso de níveis críticos de gás ou outros eventos importantes.
- LEDs: Dois LEDs utilizados para simular visualmente os reservatórios sendo completados de gás.

## Imagem e descrição do circuito

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

## Configuração de Software

### Ambiente de Desenvolvimento

O código-fonte foi desenvolvido na Arduino IDE, uma plataforma de desenvolvimento que permite a escrita, compilação e upload de programas para placas compatíveis com Arduino, como o ESP32 utilizado neste projeto.

### Instalação

1. Instale a última versão da Arduino IDE a partir do [site oficial](https://www.arduino.cc/en/software).
2. Configure a Arduino IDE para suportar o ESP32 seguindo as instruções disponíveis na [documentação do ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).
