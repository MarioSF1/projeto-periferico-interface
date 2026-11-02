# Projeto 8 — SuperSenha

Projeto desenvolvido para a disciplina de **Periféricos e Interfaces** da **UNIARA** (Prof. Augusto Perez de Andrade).

**Integrantes:** Guilherme, Maicon, Mario, Matheus e Vinicius

---

## Sobre o Projeto

O sistema consiste em um validador de senha de 4 dígitos binários (`0` e `1`) que integra uma interface gráfica no computador com um circuito físico no Arduino UNO:

1. Um conjunto de **4 chaves DIP switch** conectadas ao Arduino define a senha física (`ON = 1`, `OFF = 0`).
2. Na interface gráfica desenvolvida em **Python (Tkinter)**, o usuário digita os 4 bits da senha e clica no botão **Tentar**.
3. A senha é enviada pela porta serial (`9600 baud`) para o Arduino UNO, que compara o valor recebido com a leitura atual das chaves DIP.
4. O resultado é exibido tanto no **Display LCD 16x2 I2C** quanto na interface do computador (**ACESSO LIBERADO!** ou **SENHA ERRADA!**).
5. Um segundo clique no botão **Tentar** limpa os campos da interface e envia o comando de reset (`R`) para o Arduino, retornando o LCD para a tela inicial (`SuperSenha / Aguardando...`).

---

## Estrutura de Pastas

```text
├── Arduino/
│   ├── supersenha_arduino/
│   │   └── supersenha_arduino.ino               # Código principal do Arduino UNO (comentado)
│   ├── supersenha_sem_comentarios/
│   │   └── supersenha_sem_comentarios.ino       # Código do Arduino UNO sem comentários (apresentação)
│   ├── scanner_i2c/
│   │   └── scanner_i2c.ino                      # Utilitário para identificar o endereço do LCD I2C
│   └── Guia_Estudo_Arduino_SuperSenha.pdf
├── Python/
│   ├── supersenha.py                            # Interface gráfica comentada (Tkinter + PySerial)
│   ├── supersenha_sem_comentarios.py            # Interface gráfica sem comentários (apresentação)
│   ├── logoUniara.png                           # Logo utilizada na interface
│   └── Guia_Estudo_Python_SuperSenha.pdf
└── requirements.txt                             # Dependências do Python
```

---

## Ligações de Hardware (Arduino UNO)

### DIP Switch (4 chaves)
O código utiliza o resistor interno do Arduino (`INPUT_PULLUP`), dispensando resistores externos na protoboard.

| Chave DIP | Pino no Arduino | Outro lado da chave |
| :---: | :---: | :---: |
| Chave 1 | `D2` | `GND` |
| Chave 2 | `D3` | `GND` |
| Chave 3 | `D4` | `GND` |
| Chave 4 | `D5` | `GND` |

### Display LCD 16x2 (Módulo I2C)

| Pino do Módulo I2C | Pino no Arduino |
| :---: | :---: |
| `GND` | `GND` |
| `VCC` | `5V` |
| `SDA` | `A4` |
| `SCL` | `A5` |

---

## Como Executar

### 1. Gravar o código no Arduino
1. Abra o arquivo `Arduino/supersenha_arduino/supersenha_arduino.ino` (ou `Arduino/supersenha_sem_comentarios/supersenha_sem_comentarios.ino`) no **Arduino IDE**.
2. No Gerenciador de Bibliotecas, instale a biblioteca **LiquidCrystal I2C** (de *Frank de Brabander*).
3. Selecione a placa **Arduino Uno** e a porta **COM** correspondente em *Ferramentas > Porta*.
4. Faça o upload para a placa e **feche o Monitor Serial** (para liberar a porta COM para o Python).

### 2. Executar a interface em Python
1. Instale as bibliotecas necessárias:
   ```bash
   pip install -r requirements.txt
   ```
2. No arquivo `Python/supersenha.py` (ou `Python/supersenha_sem_comentarios.py`), confira a porta serial configurada no topo do código:
   ```python
   portaArduino = "com5"   # Ajustar para a porta COM identificada no Arduino IDE
   ```
3. Execute a interface:
   ```bash
   python Python/supersenha.py
   ```
