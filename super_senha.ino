/*
 * SuperSenha - Projeto 8 (Periféricos e Interfaces - UNIARA)
 * 4 chaves DIP definem a senha; a interface Python envia um código de 4 dígitos (0/1)
 * pela serial; o LCD I2C informa se o acesso foi liberado ou não.
 *
 * Ligações (Arduino UNO):
 *   DIP chave 1..4 -> pinos 2, 3, 4, 5  (o outro lado de cada chave vai no GND)
 *   LCD I2C: VCC -> 5V | GND -> GND | SDA -> A4 | SCL -> A5
 *
 * Biblioteca: "LiquidCrystal I2C" (Frank de Brabander) - instalar pelo Gerenciador de Bibliotecas
 */

#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// No módulo físico o endereço costuma ser 0x27 ou 0x3F.
// Se o LCD não mostrar nada, rode o scanner I2C e troque aqui.
#define ENDERECO_LCD 0x27

LiquidCrystal_I2C lcd(ENDERECO_LCD, 16, 2);

const int pinDIP[4] = {2, 3, 4, 5};
const unsigned long TEMPO_RESULTADO = 3000;  // ms que o resultado fica na tela

void telaEspera() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Insira a senha:");
  lcd.setCursor(0, 1);
  lcd.print("no computador...");
}

// Chave ON (fechada para GND) lê LOW por causa do PULL-UP -> vira '1'
String lerSenhaDIP() {
  String senha = "";
  for (int i = 0; i < 4; i++) {
    senha += (digitalRead(pinDIP[i]) == LOW) ? '1' : '0';
  }
  return senha;
}

// Aceita apenas exatamente 4 caracteres '0' ou '1'
bool codigoValido(const String &s) {
  if (s.length() != 4) return false;
  for (int i = 0; i < 4; i++) {
    if (s[i] != '0' && s[i] != '1') return false;
  }
  return true;
}

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);  // evita travar 1s esperando o '\n'

  for (int i = 0; i < 4; i++) {
    pinMode(pinDIP[i], INPUT_PULLUP);
  }

  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("  SUPER SENHA");
  lcd.setCursor(0, 1);
  lcd.print("Sistema Pronto");
  delay(1500);
  telaEspera();

  Serial.println("PRONTO");  // avisa o Python que o Arduino terminou de iniciar
}

void loop() {
  if (Serial.available() > 0) {
    String recebido = Serial.readStringUntil('\n');
    recebido.trim();
    if (recebido.length() == 0) return;

    lcd.clear();

    if (!codigoValido(recebido)) {
      lcd.setCursor(0, 0);
      lcd.print("CODIGO INVALIDO");
      lcd.setCursor(0, 1);
      lcd.print("Use 4 digitos 0/1");
      Serial.println("ERRO: CODIGO INVALIDO");
    } else if (recebido == lerSenhaDIP()) {
      lcd.setCursor(0, 0);
      lcd.print("ACESSO LIBERADO!");
      lcd.setCursor(0, 1);
      lcd.print("Senha: " + recebido);
      Serial.println("OK: ACESSO LIBERADO");
    } else {
      lcd.setCursor(0, 0);
      lcd.print("SENHA ERRADA!");
      lcd.setCursor(0, 1);
      lcd.print("Tentou: " + recebido);
      Serial.println("ERRO: SENHA INCORRETA");
    }

    delay(TEMPO_RESULTADO);

    // Descarta cliques feitos enquanto o resultado estava na tela
    while (Serial.available() > 0) Serial.read();

    telaEspera();
  }
}
