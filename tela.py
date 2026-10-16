import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import time
import serial
import os

PORTA_SERIAL = "COM3"  # Altere para a porta do seu Arduino (ex: COM3, COM4, etc.)
BAUD_RATE = 9600

COR_FUNDO = "#B6AEB1"      # Tom cinza da tela exibida no monitor
COR_TEXTO = "#111111"
FONTE_LABEL = ("Times New Roman", 18, "bold")
FONTE_BOTAO = ("Times New Roman", 15, "bold")
FONTE_ENTRADA = ("Times New Roman", 20, "bold")

# Tentativa de conexão segura com a porta serial
conexao_serial = None
try:
    conexao_serial = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
    print(f"[SERIAL] Conectado na porta {PORTA_SERIAL}!")
except Exception as e:
    print(f"[SERIAL] Dispositivo não conectado em {PORTA_SERIAL}. Executando em modo de teste.")

# ==============================================================================
# INICIALIZAÇÃO DA JANELA TKINTER
# ==============================================================================
tela = tk.Tk()
tela.title("Sistema de Acesso - Uniara")
tela.configure(bg=COR_FUNDO)

# Centralização da janela no monitor
LARGURA = 640
ALTURA = 400
largura_monitor = tela.winfo_screenwidth()
altura_monitor = tela.winfo_screenheight()
pos_x = (largura_monitor - LARGURA) // 2
pos_y = (altura_monitor - ALTURA) // 2
tela.geometry(f"{LARGURA}x{ALTURA}+{pos_x}+{pos_y}")
tela.resizable(False, False)

# ==============================================================================
# LOGO UNIARA (CANTO SUPERIOR DIREITO)
# ==============================================================================
caminho_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_uniara.png")
logo_img = None

if os.path.exists(caminho_logo):
    try:
        pil_img = Image.open(caminho_logo)
        pil_img = pil_img.resize((115, 105), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(pil_img)
    except Exception as e:
        print(f"[AVISO] Não foi possível carregar a imagem do logo: {e}")

logo_frame = tk.Frame(tela, bg="white", relief="solid", bd=1, padx=6, pady=6)
logo_frame.place(x=480, y=35)

if logo_img:
    logo_label = tk.Label(logo_frame, image=logo_img, bg="white")
    logo_label.pack()
else:
    logo_label = tk.Label(
        logo_frame,
        text="UNIARA",
        font=("Arial", 16, "bold"),
        fg="#0066B3",
        bg="white",
        width=10,
        height=4
    )
    logo_label.pack()

# ==============================================================================
# CAMPOS DE SENHA (CENTRO-ESQUERDA)
# ==============================================================================
frame_senha = tk.Frame(tela, bg=COR_FUNDO)
frame_senha.place(x=70, y=140)

label_senha = tk.Label(
    frame_senha,
    text="Senha:",
    font=FONTE_LABEL,
    bg=COR_FUNDO,
    fg=COR_TEXTO
)
label_senha.pack(side="left", padx=(0, 15))

# 4 caixas individuais para os dígitos da senha
entradas = []

def ao_digitar(event, indice):
    # Teclas de navegação que não devem acionar o avanço
    if event.keysym in ("Tab", "BackSpace", "Return", "Left", "Right", "Shift_L", "Shift_R"):
        return
    tela.after(10, lambda: avancar_foco(indice))

def avancar_foco(indice):
    conteudo = entradas[indice].get()
    # Limita a 1 único caractere por caixa
    if len(conteudo) > 1:
        entradas[indice].delete(0, tk.END)
        entradas[indice].insert(0, conteudo[-1])
        conteudo = conteudo[-1]
    
    # Pula para a próxima caixa automaticamente ao digitar
    if len(conteudo) == 1 and indice < 3:
        entradas[indice + 1].focus_set()
        entradas[indice + 1].select_range(0, tk.END)

def ao_apagar(event, indice):
    conteudo = entradas[indice].get()
    if event.keysym == "BackSpace":
        if len(conteudo) == 0 and indice > 0:
            entradas[indice - 1].focus_set()
            entradas[indice - 1].delete(0, tk.END)

for i in range(4):
    entry = tk.Entry(
        frame_senha,
        width=3,
        font=FONTE_ENTRADA,
        justify="center",
        relief="solid",
        bd=1,
        bg="white",
        fg="black",
        show="*"  # Use show="*" para esconder a senha como na imagem, ou remova se preferir ver os números
    )
    entry.pack(side="left", padx=6)
    
    # Eventos para avanço e retorno automático
    entry.bind("<KeyRelease>", lambda ev, idx=i: ao_digitar(ev, idx))
    entry.bind("<KeyPress>", lambda ev, idx=i: ao_apagar(ev, idx))
    entradas.append(entry)

# Inicia com o cursor focado na primeira caixa
entradas[0].focus_set()

# ==============================================================================
# BOTÃO "TENTAR" E STATUS
# ==============================================================================
def tentar(event=None):
    senha_digitada = "".join(e.get() for e in entradas)
    
    if len(senha_digitada) < 4:
        label_status.config(text="Por favor, digite os 4 dígitos!", fg="#8B0000")
        return
    
    print(f"[SISTEMA] Tentativa de acesso com a senha: {senha_digitada}")
    
    # Envio pela Serial se disponível
    if conexao_serial and conexao_serial.is_open:
        try:
            conexao_serial.write(f"{senha_digitada}\n".encode("utf-8"))
            label_status.config(text=f"Senha {senha_digitada} enviada via Serial!", fg="#005500")
        except Exception as erro:
            label_status.config(text=f"Erro na Serial: {erro}", fg="#8B0000")
    else:
        label_status.config(text=f"Senha digitada: {senha_digitada} (Modo Teste)", fg="#111111")

btn_tentar = tk.Button(
    tela,
    text="Tentar",
    font=FONTE_BOTAO,
    bg="#ECECEC",
    activebackground="#DCDCDC",
    fg=COR_TEXTO,
    relief="raised",
    bd=2,
    padx=28,
    pady=4,
    cursor="hand2",
    command=tentar
)
btn_tentar.place(x=250, y=245)

# Label de feedback
label_status = tk.Label(
    tela,
    text="",
    font=("Arial", 11, "italic"),
    bg=COR_FUNDO,
    fg="#111111"
)
label_status.place(x=320, y=315, anchor="center")

# Pressionar Enter em qualquer lugar também dispara o botão
tela.bind("<Return>", tentar)

# ==============================================================================
# LOOP DA APLICAÇÃO
# ==============================================================================
tela.mainloop()