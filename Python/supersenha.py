import tkinter                      #biblioteca nativa do python
from PIL import ImageTk, Image      #instalar utilizando o comando "py -m pip install pillow"
import time                         #biblioteca nativa do python
import serial                       #instalar utilizando o comando "py -m pip install pyserial"
import os                           #biblioteca nativa do python (usada para achar a pasta do arquivo)

#=================== CONFIGURACAO ===================
usarArduino = True      #False = modo de teste (sem Arduino) | True = conecta no Arduino
portaArduino = "com5"   #Conferir a porta em Ferramentas -> Porta no Arduino IDE
senhaTeste = "1010"     #Senha usada so no modo de teste (simula as chaves DIP)
#====================================================

respostaArduino = ""                #Definicao de uma variavel global
resultadoNaTela = False             #True quando ja tem um resultado (liberado/errado) na tela
aguardandoResposta = False          #True apenas quando enviou uma senha de 4 digitos e espera OK/ERRO


def mostrarResultado():             #Atualiza a tela de acordo com a resposta
    global resultadoNaTela
    resultadoNaTela = True                                  #O proximo clique em "Tentar" vai limpar a tela
    if respostaArduino == "OK":
        textoResultado.config(text = "ACESSO LIBERADO!", fg = "green")
    else:
        textoResultado.config(text = "SENHA ERRADA!", fg = "red")


def verificarLeituraSerial():       #Funcao chamada de 100 em 100 ms
    global respostaArduino, aguardandoResposta              #Considera o uso das variaveis globais
    if ser.in_waiting > 0:                                  #So le se o Arduino mandou alguma coisa
        recebido = ser.readline().decode('UTF-8').strip()   #Le a linha e transforma em texto
        if aguardandoResposta:                              #So mostra resultado se realmente enviou uma senha
            respostaArduino = recebido
            aguardandoResposta = False
            print("Recebendo sinal do Arduino: " + respostaArduino)
            mostrarResultado()
    janela.after(100, verificarLeituraSerial)               #Chama a funcao denovo daqui 100 ms


def limitarDigito(campoAtual, proximoCampo):    #Limita o campo a 1 caractere (0 ou 1) e pula para o proximo
    texto = campoAtual.get()                    #Coleta o que foi digitado no campo
    if len(texto) > 1:                          #Se tiver mais de 1 caractere (ex: "00"), pega so o ultimo
        texto = texto[-1]
    campoAtual.delete(0, "end")                 #Limpa o campo para nao acumular caracteres
    if texto == "0" or texto == "1":            #So aceita se for 0 ou 1
        campoAtual.insert(0, texto)             #Mantem o 0 ou 1 no campo
        proximoCampo.focus()                    #Pula o cursor automaticamente para o proximo campo


def limparTela():                   #Limpa os campos, o resultado e volta o LCD para a tela inicial
    global resultadoNaTela, aguardandoResposta
    digito1.delete(0, "end")                                #Apaga o que estava nos 4 campos
    digito2.delete(0, "end")
    digito3.delete(0, "end")
    digito4.delete(0, "end")
    textoResultado.config(text = "")                        #Apaga o "ACESSO LIBERADO!" / "SENHA ERRADA!"
    digito1.focus()                                         #Volta o cursor para o primeiro campo
    resultadoNaTela = False
    aguardandoResposta = False                              #Ignora qualquer retorno do comando R
    if usarArduino:
        ser.write(bytes("R\n", 'UTF-8'))                   #Pede para o Arduino voltar o LCD para "SuperSenha"
        print("Pedido de limpeza enviado para o Arduino")


def enviarSenha():                  #Funcao chamada quando o botao "Tentar" e pressionado
    global respostaArduino, resultadoNaTela, aguardandoResposta
    if resultadoNaTela:                                     #Se ja tem resultado na tela, este clique so limpa
        limparTela()
        return
    digitos = [digito1.get(), digito2.get(), digito3.get(), digito4.get()]   #Coleta o que foi digitado

    for d in digitos:                                       #Confere se cada campo tem 0 ou 1
        if d != "0" and d != "1":
            textoResultado.config(text = "Digite 0 ou 1 em cada campo", fg = "black")
            return

    senha = digitos[0] + digitos[1] + digitos[2] + digitos[3]   #Junta os 4 digitos, ex: "1010"
    resultadoNaTela = True                                  #Garante que o 2o clique em "Tentar" limpe a tela

    if usarArduino:
        aguardandoResposta = True                           #Aguarda o OK ou ERRO desta tentativa
        ser.write(bytes(senha + "\n", 'UTF-8'))             #Envia a senha para o Arduino
        print("Senha enviada para o Arduino: " + senha)
        textoResultado.config(text = "Verificando...", fg = "black")
    else:
        print("Modo de teste - senha digitada: " + senha)   #Simula a resposta do Arduino
        if senha == senhaTeste:
            respostaArduino = "OK"
        else:
            respostaArduino = "ERRO"
        mostrarResultado()


if usarArduino:
    ser = serial.Serial(port = portaArduino, baudrate = 9600)   #Estabelece a comunicacao serial com o Arduino
    print("Conexao serial foi estabelecida!")
    time.sleep(2.5)                                         #Espera 2,5 segundos (o Arduino reinicia ao conectar)
else:
    print("Modo de teste: rodando sem Arduino")

corFundo = "#8f8f8f"                                        #Cor de fundo cinza mais escuro

janela = tkinter.Tk()                                       #Criacao do objeto
janela.geometry('700x400')                                  #Tamanho da janela
janela.resizable(False, False)                              #Janela nao pode ser redimensionada
janela.title("SuperSenha - Guilherme, Maicon, Mario, Matheus e Vinicius")   #Nome da janela e integrantes
janela.config(bg = corFundo)

#Logo da UNIARA (o arquivo logoUniara.png deve estar na mesma pasta do .py)
pastaDoArquivo = os.path.dirname(os.path.abspath(__file__))        #Pasta onde esta o supersenha.py
figuraUniara = Image.open(os.path.join(pastaDoArquivo, "logoUniara.png"))   #Abre a logo dessa pasta
figuraUniara = figuraUniara.resize((200, 200))              #Tamanho maior alinhado com a senha
figuraUniara = ImageTk.PhotoImage(figuraUniara)
janela.iconphoto(False, figuraUniara)                       #Coloca a logo da UNIARA como icone da janela (no lugar da pena)
labelUniara = tkinter.Label(
    image = figuraUniara,
    bg = corFundo
)
labelUniara.image = figuraUniara                            #Mantem a referencia da figura
labelUniara.place(x = 440, y = 55)                          #Alinhado com a linha da senha (vai de x=440 ate x=640)

#Texto "Senha:"
textoSenha = tkinter.Label(
    text = "Senha:",
    font = ("Times New Roman", 20, 'bold'),
    bg = corFundo
)
textoSenha.place(x = 60, y = 140)

#Os 4 campos da senha (um para cada chave do DIP switch)
digito1 = tkinter.Entry(width = 2, font = ("Times New Roman", 20), justify = "center")
digito1.place(x = 180, y = 140)

digito2 = tkinter.Entry(width = 2, font = ("Times New Roman", 20), justify = "center")
digito2.place(x = 240, y = 140)

digito3 = tkinter.Entry(width = 2, font = ("Times New Roman", 20), justify = "center")
digito3.place(x = 300, y = 140)

digito4 = tkinter.Entry(width = 2, font = ("Times New Roman", 20), justify = "center")
digito4.place(x = 360, y = 140)

#Botao "Tentar"
botaoTentar = tkinter.Button(
    text = "Tentar",
    font = ("Times New Roman", 16, 'bold'),
    fg = "black",
    height = 1,
    width = 12,
    bd = 3,
    activebackground = "gray",
    command = enviarSenha                                   #Funcao chamada ao pressionar o botao
)
botaoTentar.place(x = 60, y = 290, width = 580)             #Ocupa desde o S de Senha (x=60) ate o fim da logo (x=640)

#Configura cada campo para aceitar so 0 ou 1 e pular para o proximo ao digitar
digito1.bind("<KeyRelease>", lambda e: limitarDigito(digito1, digito2))
digito2.bind("<KeyRelease>", lambda e: limitarDigito(digito2, digito3))
digito3.bind("<KeyRelease>", lambda e: limitarDigito(digito3, digito4))
digito4.bind("<KeyRelease>", lambda e: limitarDigito(digito4, botaoTentar))
digito1.focus()                                             #Ja inicia com o cursor no primeiro campo

#Label que mostra o resultado
textoResultado = tkinter.Label(
    text = "",
    font = ("Times New Roman", 16, 'bold'),
    bg = corFundo
)
textoResultado.place(x = 60, y = 220)


def fecharJanela():                 #Libera a porta COM5 ao fechar a janela no X
    if usarArduino and ser.is_open:
        ser.close()
    janela.destroy()


janela.protocol("WM_DELETE_WINDOW", fecharJanela)

if usarArduino:
    janela.after(100, verificarLeituraSerial)               #Comeca a verificar o serial de 100 em 100 ms

janela.mainloop()                                           #Comando do loop que deve estar no final do codigo
