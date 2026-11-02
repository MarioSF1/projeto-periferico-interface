import tkinter
from PIL import ImageTk, Image
import time
import serial
import os

portaArduino = "com5"

respostaArduino = ""
resultadoNaTela = False
aguardandoResposta = False


def mostrarResultado():
    global resultadoNaTela
    resultadoNaTela = True
    if respostaArduino == "OK":
        textoResultado.config(text = "ACESSO LIBERADO!", fg = "green")
    else:
        textoResultado.config(text = "SENHA ERRADA!", fg = "red")


def verificarLeituraSerial():
    global respostaArduino, aguardandoResposta
    if ser.in_waiting > 0:
        recebido = ser.readline().decode('UTF-8').strip()
        if aguardandoResposta:
            respostaArduino = recebido
            aguardandoResposta = False
            print("Recebendo sinal do Arduino: " + respostaArduino)
            mostrarResultado()
    janela.after(100, verificarLeituraSerial)


def limitarDigito(campoAtual, proximoCampo):
    texto = campoAtual.get()
    if len(texto) > 1:
        texto = texto[-1]
    campoAtual.delete(0, "end")
    if texto == "0" or texto == "1":
        campoAtual.insert(0, texto)
        proximoCampo.focus()


def limparTela():
    global resultadoNaTela, aguardandoResposta
    digito1.delete(0, "end")
    digito2.delete(0, "end")
    digito3.delete(0, "end")
    digito4.delete(0, "end")
    textoResultado.config(text = "")
    digito1.focus()
    resultadoNaTela = False
    aguardandoResposta = False
    ser.write(bytes("R\n", 'UTF-8'))
    print("Pedido de limpeza enviado para o Arduino")


def enviarSenha():
    global resultadoNaTela, aguardandoResposta
    if resultadoNaTela:
        limparTela()
        return
    digitos = [digito1.get(), digito2.get(), digito3.get(), digito4.get()]

    for d in digitos:
        if d != "0" and d != "1":
            textoResultado.config(text = "Digite 0 ou 1 em cada campo", fg = "black")
            return

    senha = digitos[0] + digitos[1] + digitos[2] + digitos[3]
    resultadoNaTela = True
    aguardandoResposta = True
    ser.write(bytes(senha + "\n", 'UTF-8'))
    print("Senha enviada para o Arduino: " + senha)
    textoResultado.config(text = "Verificando...", fg = "black")


ser = serial.Serial(port = portaArduino, baudrate = 9600)
print("Conexao serial foi estabelecida!")
time.sleep(2.5)

corFundo = "#8f8f8f"

janela = tkinter.Tk()
janela.geometry('700x400')
janela.resizable(False, False)
janela.title("SuperSenha - Guilherme, Maicon, Mario, Matheus e Vinicius")
janela.config(bg = corFundo)

pastaDoArquivo = os.path.dirname(os.path.abspath(__file__))
figuraUniara = Image.open(os.path.join(pastaDoArquivo, "logoUniara.png"))
figuraUniara = figuraUniara.resize((200, 200))
figuraUniara = ImageTk.PhotoImage(figuraUniara)
janela.iconphoto(False, figuraUniara)
labelUniara = tkinter.Label(
    image = figuraUniara,
    bg = corFundo
)
labelUniara.image = figuraUniara
labelUniara.place(x = 440, y = 55)

textoSenha = tkinter.Label(
    text = "Senha:",
    font = ("Times New Roman", 20, 'bold'),
    bg = corFundo
)
textoSenha.place(x = 60, y = 140)

digito1 = tkinter.Entry(width = 2, font = ("Times New Roman", 20), justify = "center")
digito1.place(x = 180, y = 140)

digito2 = tkinter.Entry(width = 2, font = ("Times New Roman", 20), justify = "center")
digito2.place(x = 240, y = 140)

digito3 = tkinter.Entry(width = 2, font = ("Times New Roman", 20), justify = "center")
digito3.place(x = 300, y = 140)

digito4 = tkinter.Entry(width = 2, font = ("Times New Roman", 20), justify = "center")
digito4.place(x = 360, y = 140)

botaoTentar = tkinter.Button(
    text = "Tentar",
    font = ("Times New Roman", 16, 'bold'),
    fg = "black",
    height = 1,
    width = 12,
    bd = 3,
    activebackground = "gray",
    command = enviarSenha
)
botaoTentar.place(x = 60, y = 290, width = 580)

digito1.bind("<KeyRelease>", lambda e: limitarDigito(digito1, digito2))
digito2.bind("<KeyRelease>", lambda e: limitarDigito(digito2, digito3))
digito3.bind("<KeyRelease>", lambda e: limitarDigito(digito3, digito4))
digito4.bind("<KeyRelease>", lambda e: limitarDigito(digito4, botaoTentar))
digito1.focus()

textoResultado = tkinter.Label(
    text = "",
    font = ("Times New Roman", 16, 'bold'),
    bg = corFundo
)
textoResultado.place(x = 60, y = 220)


def fecharJanela():
    if ser.is_open:
        ser.close()
    janela.destroy()


janela.protocol("WM_DELETE_WINDOW", fecharJanela)

janela.after(100, verificarLeituraSerial)
janela.mainloop()
