#include <Wire.h>

// Scanner I2C: descobre o endereco do modulo LCD I2C (normalmente 0x27 ou 0x3F)
// Abra o Monitor Serial em 9600 baud para ver o endereco encontrado

void setup() {
  Wire.begin();
  Serial.begin(9600);
  Serial.println("Procurando dispositivos I2C...");
}

void loop() {
  byte erro, endereco;
  int encontrados = 0;

  for (endereco = 1; endereco < 127; endereco++) {
    Wire.beginTransmission(endereco);
    erro = Wire.endTransmission();

    if (erro == 0) {
      Serial.print("Dispositivo I2C encontrado no endereco 0x");
      if (endereco < 16) Serial.print("0");
      Serial.println(endereco, HEX);
      encontrados++;
    }
  }

  if (encontrados == 0) {
    Serial.println("Nenhum dispositivo I2C encontrado (verifique SDA=A4, SCL=A5, VCC e GND)");
  }

  delay(3000);
}

