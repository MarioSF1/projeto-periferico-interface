#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define pinoChave1 2
#define pinoChave2 3
#define pinoChave3 4
#define pinoChave4 5

LiquidCrystal_I2C lcd(0x27, 16, 2);

void telaInicial() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("   SuperSenha   ");
  lcd.setCursor(0, 1);
  lcd.print("Aguardando...   ");
}

void setup() {
  Serial.begin(9600);

  pinMode(pinoChave1, INPUT_PULLUP);
  pinMode(pinoChave2, INPUT_PULLUP);
  pinMode(pinoChave3, INPUT_PULLUP);
  pinMode(pinoChave4, INPUT_PULLUP);

  lcd.init();
  lcd.backlight();
  telaInicial();
}

void loop() {
  if (Serial.available() > 0) {
    String senhaDigitada = Serial.readStringUntil('\n');
    senhaDigitada.trim();

    if (senhaDigitada.length() == 0) {
      return;
    }

    if (senhaDigitada == "R") {
      telaInicial();
      return;
    }

    String senhaDIP = "";

    if (digitalRead(pinoChave1) == LOW) { senhaDIP = senhaDIP + "1"; } else { senhaDIP = senhaDIP + "0"; }
    if (digitalRead(pinoChave2) == LOW) { senhaDIP = senhaDIP + "1"; } else { senhaDIP = senhaDIP + "0"; }
    if (digitalRead(pinoChave3) == LOW) { senhaDIP = senhaDIP + "1"; } else { senhaDIP = senhaDIP + "0"; }
    if (digitalRead(pinoChave4) == LOW) { senhaDIP = senhaDIP + "1"; } else { senhaDIP = senhaDIP + "0"; }

    lcd.clear();

    if (senhaDigitada == senhaDIP) {
      lcd.setCursor(0, 0);
      lcd.print("ACESSO LIBERADO!");
      Serial.println("OK");
    } else {
      lcd.setCursor(0, 0);
      lcd.print(" SENHA ERRADA!  ");
      Serial.println("ERRO");
    }
  }
}
