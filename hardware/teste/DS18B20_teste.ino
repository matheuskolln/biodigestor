/*** INCLUSÃO DE BIBLIOTECAS DO SISTEMA********************************************************************************************************************/

// Biblioteca DS18B20 Dallas Temperatura
#include <OneWire.h>
#include <DallasTemperature.h>





// Pinos de acesso ao Esp32 ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#define DS18B20      4 // OK 





/***INSTANCIANDO OBJETOS***********************************************************************************************************************************/
// Sensor de Temperatura DS18B20

//Instacia o Objeto oneWire e Seta o pino do Sensor para iniciar as leituras
OneWire oneWire(DS18B20);

//Repassa as referencias do oneWire para o Sensor Dallas (DS18B20)
DallasTemperature Sensor(&oneWire);

// Variavel para Armazenar os dados de Leitura
float leitura;




void setup() {
  // Inicia a Serial
  Serial.begin(115200);

  // Inicia o Sensor
  Sensor.begin();

}

void loop() {

  // Leitura do Sensor  DS18B20  //////////////
  Sensor.requestTemperatures();

  // Armazerna na variavel o valor da Leitura
  leitura          = Sensor.getTempCByIndex(0);


 // Imprime na Tela a Leitura
  Serial.print(leitura);
  Serial.println("ºC"); 
  Serial.println("--------------------------------------"); 
  

}
