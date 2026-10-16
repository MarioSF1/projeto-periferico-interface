# Projeto Periférico - Interface Gráfica

Interface gráfica desenvolvida em Python (Tkinter + Pillow) para o controle e envio de senhas via comunicação serial com microcontroladores (ex: Arduino).

## 📋 Funcionalidades

- **Campos de Senha com Auto-Avanço**: 4 caixas individuais para digitação de senha, com salto automático para a próxima caixa e retorno ao pressionar Backspace.
- **Comunicação Serial**: Envio automático da senha digitada para o microcontrolador conectado via porta serial (`COM3`, configurável).
- **Modo de Teste / Simulação**: Permite testar a interface mesmo sem o dispositivo serial conectado, evitando erros em tempo de execução.
- **Identidade Visual UNIARA**: Interface estilizada e padronizada com o logotipo institucional da Universidade de Araraquara.

## 🚀 Como Executar

### 1. Pré-requisitos

Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

### 2. Executando a Aplicação

Inicie o script principal:
```bash
python tela.py
```

## ⚙️ Configurações

No topo do arquivo `tela.py`, você pode ajustar a porta serial e a velocidade de comunicação conforme a sua placa:

```python
PORTA_SERIAL = "COM3"  # Altere para a porta do seu dispositivo (ex: COM4, /dev/ttyUSB0)
BAUD_RATE = 9600
```
