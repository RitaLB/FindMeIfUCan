import os
import platform
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

def get_image_path(*path_parts):
    return os.path.join(os.path.dirname(__file__), "imagens", *path_parts)

def set_icon(window):
    os_name = platform.system()
    if os_name == "Windows":
        window.iconbitmap(get_image_path("logo.ico"))
    else:
        # No Linux, use `iconphoto` com PNG
        logo_path = get_image_path("logo.png")
        
        try:
            logo_img = PhotoImage(file=logo_path)
            window.iconphoto(True, logo_img)
        except Exception as e:
            print(f"Erro ao carregar o ícone: {e}")
            


# Inicialização da janela principal
root = Tk()
root.title("Find me if you can")

# Definir o ícone
set_icon(root)

# Imagens principais
img_inicial = ImageTk.PhotoImage(Image.open(get_image_path("tela_inicial.jpg")))
mapa_img = ImageTk.PhotoImage(Image.open(get_image_path("mapa.jpg")))


# Fases:
fases = []
for i in range(9):
    fases.append(ImageTk.PhotoImage(Image.open(get_image_path("fases", f"fase_{i}.jpg"))))
fases.append(ImageTk.PhotoImage(Image.open(get_image_path("fases", "the_end.jpg"))))

# Lista das respostas:
respostas = [
    "il viaggio inizia qui",
    "leminski",
    "que me quiten lo bailado",
    "quanto tempo o tempo tem?",
    "estrelas cantam vida",
    "don't waste my time",
    "living room",
    "vazio",
    "Carpe Diem!"
]

# Lista das coordenadas:
coordenadas = [
    "00000",
    "51° 30' 26'' N, 0° 07' 39'' O",
    "51° 31' 39'' N, 0° 11' 24'' O",
    "47° 28' 19'' N 19° 03' 01'' E",
    "40° 39' 51'' N, 73° 56' 19'' O",
    "42° 21' 29'' N 71° 03' 49'' O",
    "29° 57' 53'' N 90° 4' 14'' O",
    "41° 52' 55'' N 87° 37' 40'' O",
    "51° 30' 26'' N, 0° 07' 35'' O"
]

# label janela principal
jan1_label = Label(image = img_inicial)
jan1_label.grid(row = 0, column=0 , rowspan = 3, columnspan = 3)

# criando variável x para o valor da fase:
x = 0

# criando variável para o valor da fase
leitura  = open("fase.txt", "r")
faseatual = leitura.read()

# criando uma função para o texto teporário da entrada da resposta:
def fin_resp_temp_text(e):
   resposta_entry.delete(0,"end")


# criando uma função para o texto teporário da entrada da coordenada:
def coord_temp_text(e):
    coordenada_entry.delete(0,"end")

#start button função:
def start():
    global jan1_label
    global start_button
    global mapa_button
    global resposta_entry
    global x
    global faseatual
    #deletando a imagem inicial:
    jan1_label.grid_forget()
    #jan1_label recebe a próxima imagem (Fase 1):
    jan1_label = Label(root, image= fases[int(faseatual)])
    jan1_label.grid( row = 1, column=0,  columnspan=3, )

    # x recebe o valor da fase atual:
    x = int(faseatual)
    # start button é deletado da tela: 
    start_button.destroy()
    
    #colocando botões da tela principal das fases:
    mapa_button.grid( row = 2, column =2)
    resposta_entry.grid(row = 0, column=1)
    resposta_button.grid(row = 0, column = 2 )

   
# open map função:
def open_map():
    global mapa_img
    global coordenada_entry
    global coordenada_button
    global mapa_wind
    #creating a new window:
    mapa_wind = Toplevel()

    # label pro mapa:
    mapa_label = Label(mapa_wind,image= mapa_img )

    mapa_wind.title("Mapinha")
    
    #mapa_wind.iconphoto(True, os.path.join("imagens","logo.png"))

    #criando widgets da tela do mapa:
    #botão testar coordenada:
    coordenada_button = Button(mapa_wind, text = "Give it a try", command = tentar_coordenada)
    #coordenada entry:
    coordenada_entry = Entry(mapa_wind, width = 50)
    # texto temporário da entrada:
    coordenada_entry.insert(0, "Write the coordenate here :)")
    coordenada_entry.bind("<FocusIn>", coord_temp_text)
    #putting things inside the mapa_wind:
    mapa_label.grid(row =0, column =0, columnspan = 3)
    coordenada_button.grid(row=1, column = 2)
    coordenada_entry.grid(row=1, column = 1)

# botão de resposta função:
def tentar_resposta():
    global resposta_entry
    global respostas
    global x
    global coordenadas
    global prox_fase
    
    if x == 8:
        prox_fase()
    elif resposta_entry.get() == respostas[x]:
        messagebox.showinfo("Right answer :)", "Congrats! the coordenate is: " + str(coordenadas[x+1]))
        # texto da entry é removido:
        resposta_entry.delete(0,END)

    elif resposta_entry.get() != respostas[x]:
        messagebox.showerror("Ooops", "Nop, that's not the answer")
        # texto da entry é removido:
        resposta_entry.delete(0,END)

# botão de coordenada função:
def tentar_coordenada():
    global coordenada_entry
    global respostas
    global x
    global coordenadas
    global correspondencia
    global prox_fase
    global mapa_wind

    correspondencia = False
    for a in range (len(coordenadas)):
        if coordenada_entry.get() == coordenadas[a]:
            x = a
            messagebox.showinfo("Congrats!", "right way!")
            correspondencia = True
            #função próxima fase é ativada 
            prox_fase()
            mapa_wind.destroy()
            break
            
    
    if correspondencia == False:
        messagebox.showerror("Ooops", "Wrong coodenate")
    
# função prox fase:
def prox_fase():
    global x
    global faseatual
    global jan1_label
    global resposta_entry

    #salvando a nova fase atual na variável fase:
    novafase  = open("fase.txt", "w")
    novafase.write(str(x))
    novafase.close()
    leitura  = open("fase.txt", "r")
    faseatual = leitura.read()
    
    if x == 8:
        #deletando a imagem da fase anterior:
        jan1_label.grid_forget()
        #jan1_label recebe a próxima imagem (ultima fase):
        jan1_label = Label(root, image= fases[x+1])
        jan1_label.grid( row = 1, column=0,  columnspan=3, )
        resposta_entry.destroy()
        resposta_button.destroy()

    else:
        #deletando a imagem da fase anterior:
        jan1_label.grid_forget()
        #jan1_label recebe a próxima imagem (Fase 1):
        jan1_label = Label(root, image= fases[x])
        jan1_label.grid( row = 1, column=0,  columnspan=3, )

        #reinicia a resposta entry:
        resposta_entry.destroy()
        resposta_entry = Entry(root, width = 50)
        resposta_entry.grid(row = 0, column=1)
        resposta_entry.insert(0, "Write the answer here :)")
        resposta_entry.bind("<FocusIn>", fin_resp_temp_text)


    


# coisinhas da tela inicial:   
#start button:
start_button = Button(root, text= "RU readdy? Start Here", command = start)
start_button.grid(row = 2, column = 1)


# coisinhas da tela de fases:
# botão abrir mapa
mapa_button = Button(root, text= "Open Map", command = open_map )

#botão testar resposta:
resposta_button = Button(root, text = "Give it a try", command= tentar_resposta )

# resposta entry:
resposta_entry = Entry(root, width = 50)

# texto temporário da entrada:
resposta_entry.insert(0, "Write the answer here :)")
resposta_entry.bind("<FocusIn>", fin_resp_temp_text)


#criate a loop that keeps the screen showing
root.mainloop()