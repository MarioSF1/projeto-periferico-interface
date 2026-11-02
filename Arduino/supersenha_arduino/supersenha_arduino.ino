#include <Wire.h>                   //Biblioteca nativa para comunicacao I2C (pinos A4 e A5)
#include <LiquidCrystal_I2C.h>      //Biblioteca do display LCD I2C (instalar "LiquidCrystal I2C" de Frank de Brabander)

#define pinoChave1 2                //Chave 1 do DIP switch ligada no pino digital 2
#define pinoChave2 3                //Chave 2 do DIP switch ligada no pino digital 3
#define pinoChave3 4                //Chave 3 do DIP switch ligada no pino digital 4
#define pinoChave4 5                //Chave 4 do DIP switch ligada no pino digital 5

// Cria o objeto do LCD no endereco 0x27 com 16 colunas e 2 linhas (se nao aparecer texto, testar 0x3F)
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Mostra a tela inicial no LCD (usada no inicio e quando o Python manda "R")
void telaInicial() {
  lcd.clear();                      //Limpa a tela
  lcd.setCursor(0, 0);              //Posiciona na coluna 0, linha 0
  lcd.print("   SuperSenha   ");
  lcd.setCursor(0, 1);              //Posiciona na coluna 0, linha 1
  lcd.print("Aguardando...   ");
}

void setup() {
  Serial.begin(9600);               //Inicia a comunicacao serial na mesma velocidade do Python (9600 b/s)

  // Configura os pinos do DIP switch como entrada com resistor pull-up interno
  // Com INPUT_PULLUP: chave em ON (ligada no GND) le LOW | chave em OFF le HIGH
  pinMode(pinoChave1, INPUT_PULLUP);
  pinMode(pinoChave2, INPUT_PULLUP);
  pinMode(pinoChave3, INPUT_PULLUP);
  pinMode(pinoChave4, INPUT_PULLUP);

  // Inicializa o display LCD I2C
  lcd.init();                       //Inicia o display LCD
  lcd.backlight();                  //Liga a luz de fundo do LCD
  telaInicial();                    //Mostra a tela inicial "SuperSenha / Aguardando..."
}

void loop() {
  if (Serial.available() > 0) {                             //Verifica se chegou alguma senha enviada pelo Python
    String senhaDigitada = Serial.readStringUntil('\n');    //Le a senha ate a quebra de linha (ex: "1010")
    senhaDigitada.trim();                                   //Remove quebras de linha ou espacos extras

    if (senhaDigitada.length() == 0) {                      //Ignora leituras vazias
      return;
    }

    if (senhaDigitada == "R") {                             //"R" = pedido do Python para limpar (reset)
      telaInicial();                                        //Volta o LCD para "SuperSenha / Aguardando..."
      return;                                               //Nao compara senha nem responde nada
    }

    // Monta a senha atual definida nas 4 chaves do DIP switch
    // Como usamos INPUT_PULLUP, quando a chave esta em ON (conectada ao GND), a leitura e LOW ("1")
    String senhaDIP = "";

    if (digitalRead(pinoChave1) == LOW) { senhaDIP = senhaDIP + "1"; } else { senhaDIP = senhaDIP + "0"; }
    if (digitalRead(pinoChave2) == LOW) { senhaDIP = senhaDIP + "1"; } else { senhaDIP = senhaDIP + "0"; }
    if (digitalRead(pinoChave3) == LOW) { senhaDIP = senhaDIP + "1"; } else { senhaDIP = senhaDIP + "0"; }
    if (digitalRead(pinoChave4) == LOW) { senhaDIP = senhaDIP + "1"; } else { senhaDIP = senhaDIP + "0"; }

    lcd.clear();                                            //Limpa o display LCD antes de escrever o resultado

    if (senhaDigitada == senhaDIP) {                        //Se a senha enviada pelo Python for igual a do DIP switch
      lcd.setCursor(0, 0);
      lcd.print("ACESSO LIBERADO!");
      Serial.println("OK");                                 //Envia "OK" para o Python mostrar ACESSO LIBERADO!
    } else {                                                //Caso contrario, senha incorreta
      lcd.setCursor(0, 0);
      lcd.print(" SENHA ERRADA!  ");
      Serial.println("ERRO");                               //Envia "ERRO" para o Python mostrar SENHA ERRADA!
    }
  }
}
