import tkinter as tk
import os
from tkinter import ttk, filedialog
from pytube import YouTube
import subprocess
import threading

# Função para salvar a pasta de vídeos em um arquivo
def salvar_pasta_videos(pasta_videos):
    with open("pasta_videos.txt", "w") as file:
        file.write(pasta_videos)

# Função para carregar a pasta de vídeos do arquivo, se existir
def carregar_pasta_videos():
    if os.path.exists("pasta_videos.txt"):
        with open("pasta_videos.txt", "r") as file:
            return file.read().strip()
    else:
        return ""

def baixar_video(url, caminho_salvar, resolution):
    try:
        # Criar um objeto YouTube com a URL do vídeo
        yt = YouTube(url)
        
        # Baixar o vídeo na melhor qualidade disponível
        video = yt.streams.filter(res=resolution, progressive=True).first()

        # Concatenar o texto adicional ao nome do arquivo
        nome_arquivo = video.default_filename.replace(".mp4", f" - {resolution}.mp4")
        
        
        # Fazer o download do vídeo para o caminho especificado
        video.download(output_path=caminho_salvar, filename=nome_arquivo)
        print("Download concluído!")
    except Exception as e:
        print("Ocorreu um erro:", str(e))

# Exemplo de uso
url_do_video = "https://www.youtube.com/watch?v=XidQQr2Q7Bo&ab_channel=ge"
caminho_para_salvar = "C:/Users/guilh/Videos"

def selecionar_pasta():
    pasta = filedialog.askdirectory()
    pasta_videos_entry.delete(0, tk.END)
    pasta_videos_entry.insert(0, pasta)
    habilitar_botao_baixar()
    salvar_pasta_videos(pasta)

def abrir_pasta_videos():
    pasta_videos = pasta_videos_entry.get()
    subprocess.Popen('explorer "' + os.path.abspath(pasta_videos) + '"')

def baixar_video_callback():
    url = url_entry.get()
    pasta_videos = pasta_videos_entry.get()

    if not url or not pasta_videos:
        tk.messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
        return

    # Calcula as coordenadas para centralizar a janela
    largura_janela = 300
    altura_janela = 50
    x = (largura_tela - largura_janela) // 2
    y = (altura_tela - altura_janela) // 2

    # Cria e mostra a janela de carregamento
    loading_window = tk.Toplevel(root)
    loading_window.title("Aguarde...")
    loading_window.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")  # Centraliza a janela
    loading_window.grab_set()  # Torna a janela modal
    loading_window.resizable(False, False)

    loading_label = ttk.Label(loading_window, text="Baixando vídeo, por favor, aguarde...")
    loading_label.pack(padx=20, pady=10)

    # Inicia uma nova thread para executar o download do vídeo
    download_thread = threading.Thread(target=baixar_video, args=(url, pasta_videos, opcao_selecionada.get()))
    download_thread.start()

    # Monitora o término do download e fecha a janela de carregamento
    root.after(100, check_download_finished, download_thread, loading_window)

def check_download_finished(download_thread, loading_window):
    if download_thread.is_alive():
        # Se o download ainda estiver em andamento, verifica novamente após 100ms
        root.after(100, check_download_finished, download_thread, loading_window)
    else:
        # Se o download estiver concluído, fecha a janela de carregamento
        loading_window.destroy()
        


# Cria a janela principal
root = tk.Tk()
root.title("Filó Video Downloader")

# Definindo que a janela não é redimensionável
root.resizable(False, False)

# Obtém as dimensões da tela
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()

# Calcula as coordenadas para centralizar a janela principal
largura_janela_principal = 580
altura_janela_principal = 110
x_principal = (largura_tela - largura_janela_principal) // 2
y_principal = (altura_tela - altura_janela_principal) // 2

# Define a posição da janela principal
root.geometry(f"{largura_janela_principal}x{altura_janela_principal}+{x_principal}+{y_principal}")
root.iconbitmap("filo.ico")
root.deiconify() 

pasta_videos_salva = carregar_pasta_videos()

opcoes = ["360p", "720p"]
opcao_selecionada = tk.StringVar(root)
opcao_selecionada.set(opcoes[1])

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, padx=10, pady=10)

# Cria os widgets
url_label = ttk.Label(root, text="URL:")
url_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5)

pasta_videos_label = ttk.Label(root, text="Pasta de Vídeos:")
pasta_videos_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

pasta_videos_entry = ttk.Entry(root, width=50)
pasta_videos_entry.grid(row=1, column=1, padx=10, pady=5)
pasta_videos_entry.insert(0, pasta_videos_salva) 

selecionar_pasta_button = ttk.Button(root, text="Selecionar Pasta", command=selecionar_pasta)
selecionar_pasta_button.grid(row=1, column=2, padx=10, pady=5)

dropdown = ttk.OptionMenu(root, opcao_selecionada, opcoes[1], *opcoes)
dropdown.grid(row=2, column=0, padx=10, pady=5)

baixar_video_button = ttk.Button(root, text="Baixar Vídeo", command=baixar_video_callback, state=tk.DISABLED)
baixar_video_button.grid(row=2, column=1, padx=10, pady=5)

abrir_pasta_button = ttk.Button(root, text="Abrir Pasta de Vídeos", command=abrir_pasta_videos)
abrir_pasta_button.grid(row=2, column=2, padx=10, pady=5)

def habilitar_botao_baixar(*args):
    if url_entry.get() and pasta_videos_entry.get():
        baixar_video_button.config(state=tk.NORMAL)
    else:
        baixar_video_button.config(state=tk.DISABLED)

url_entry.bind("<KeyRelease>", habilitar_botao_baixar)
pasta_videos_entry.bind("<KeyRelease>", habilitar_botao_baixar)

# Inicia o loop principal
root.mainloop()