import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import gc
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mesBox
from tkinter import simpledialog as dialog
from PIL import Image, ImageTk


#Globais
Carregado = [False]
Processada = [False]
Img_Original = []
Img_Processada = []
Filtro = np.zeros((3,3), np.uint8)
Fsize = 3
Log = ""
Editing = False

#setup window
def initWindow():
    global window
    global Log
    global LogFrame
    window = Tk()
    #window.resizable(False, False)
    window.geometry('450x600')
    icone = PhotoImage(file="res/icone.png")
    window.iconphoto(True, icone)
    window.title("processamento de images")
    window.config(background="#22c995")



#funcoes de abrir, salvar e mostrar imagem

def abrirImg():
    global Img_Original
    global Img_Processada
    global Carregado
    global Processada
    Img_Original =   []
    Img_Processada = []
    filetypes = (('image files', ('*.png', '*.bmp', '*.dib' , '*.jpeg', '*.jpg', '*.jpe', '*.jp2', '*.webp', '*.avif', '*.pbm', '*.pgm', '*.ppm', '*.pxm', '*.pnm', '*.pfm', '*.sr', '*.ras' , '*.tiff', '*.tif', '*.exr', '*.hdr', '*.pic')),
                 ("all files", '*.*'))
    #selecione o arquivo
    filepath = filedialog.askopenfilename(title="Abrir Imagem", initialdir="/", filetypes=filetypes)
    if(cv2.haveImageReader(filepath) == True):
        Img_Original = cv2.imread(filepath, 0)
        Carregado[0] = True
    else:
        mesBox.showerror(title="Arquivo nao suportado", message="Arquivo nao suportado. \nPorfavor escolha um válido")

def salvarImg():
    global Carregado
    global Processada
    global Img_Original
    global Img_Processada
    #formatos suportados pelo opencv
    filetypes = ['.png', '.bmp', '.dib' , '.jpeg', '.jpg', '.jpe', '.jp2', '.webp', '.avif', '.pbm', '.pgm', '.ppm', '.pxm', '.pnm', '.pfm', '.sr', '.ras' , '.tiff', '.tif', '.exr', '.hdr', '.pic']
    #faz algo se tiver uma imagem carregada
    if(Carregado[0] == True):
        #seleciona o formato
        formato = dialog.askstring("Input", "Selecione o formato que deseja salvar a Imagem:\n(ex: .png)")
        if(formato.lower() in filetypes):
            #selecione o arquivo
            filepath = filedialog.filepath = filedialog.askdirectory(title='Selecione onde o arquivo sera salvo')
            nome = dialog.askstring("Input", "Digite como deseja salvar o nome do arquivo")
            nome = nome + (formato.lower())
            os.chdir(filepath)
            if Processada[0] == False:
                cv2.imwrite(nome, Img_Original)
            else:
                cv2.imwrite(nome, Img_Processada)
        else:
            mesBox.showerror(title="erro de tipo", message="Formato nao suportado. \nPorfavor escolha um válido")     
    else:
        mesBox.showinfo(title="", message="nenhuma imagem carregada")

def visualizarImgOriginal():
    global Img_Original
    if Carregado[0]: 
        try:
            cv2.imshow('ImageWindow', Img_Original)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao mostrar imagem")
    else:
        mesBox.showinfo(title="", message="nenhuma imagem carregada")

def visualizarLadoALado():
    global Img_Original
    global Img_Processada
    if Processada[0]: 
        try:
            image = np.concatenate((Img_Original, Img_Processada), axis=1)
            cv2.imshow('ImageWindow', image)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao mostrar imagem")
    else:
        mesBox.showinfo(title="", message="nenhuma imagem processada")

#primitivas

def getPixel(Img, x, y):
    l, c = Img_Original.shape
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return 0
    else:
        return Img[y][x]

def setPixel(Img, x, y, intensidade):
    l, c = Img_Original.shape
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return
    else:
        Img[y][x] = intensidade

#processos basicos

def negativo():
    global Carregado
    global Processada
    global Img_Original
    global Img_Processada
    if Carregado[0]:
        Processada[0] = True
        w, h = Img_Original.shape
        Img_Processada = np.zeros((w, h), np.uint8)
        for i in range(w):
            for j in range(h):
                Img_Processada[i][j] = (255 - Img_Original[i][j])
        cv2.imshow('ImageWindow', Img_Processada)
        cv2.waitKey(0)
    else:
        Processada[0] = False
        mesBox.showerror(title="erro de tipo", message="Imagem vazia.") 

def logaritmo():
    global Carregado
    global Processada
    global Img_Original
    global Img_Processada
    if Carregado[0]:
        Processada[0] = True
        #pede a base do logaritimo
        base = dialog.askstring("Input", "Selecione a base logaritmica a ser utilizada. \nou ln para logaritmo natural(base e)")
        if(base.lower() == "ln"):
            try:
                w, h = Img_Original.shape
                Img_Processada = np.float32(Img_Original)
                for i in range(w):
                    for j in range(h):
                        if(Img_Original[i][j] != 0):
                            Img_Processada[i][j] = math.log(Img_Processada[i][j])

                cv2.normalize(Img_Processada, Img_Processada,0,255,cv2.NORM_MINMAX)
                Img_Processada = np.int8(Img_Processada)
                cv2.imshow('ImageWindow', Img_Processada)
                cv2.waitKey(0)
            except:
                mesBox.showinfo(title="", message="erro ao processar imagem")
        else:
            try:
                base = int(base)
                w, h = Img_Original.shape
                Img_Processada = np.float32(Img_Original)
                for i in range(w):
                    for j in range(h):
                        if(Img_Original[i][j] != 0):
                            Img_Processada[i][j] = math.log(Img_Processada[i][j], base)

                cv2.normalize(Img_Processada, Img_Processada,0,255,cv2.NORM_MINMAX)
                Img_Processada = np.int8(Img_Processada)
                cv2.imshow('ImageWindow', Img_Processada)
                cv2.waitKey(0)
            except:
                mesBox.showinfo(title="", message="erro ao processar imagem")
    else:
       Processada[0] = False
       mesBox.showerror(title="erro de tipo", message="Imagem vazia.") 
       mesBox.showinfo(title="", message="sem imagem carregada")

def correcaoGama():
    global Carregado
    global Processada
    global Img_Original
    global Img_Processada
    if Carregado[0]:
        try:
            Processada[0] = True
            w, h = Img_Original.shape
        
            #cria uma imagem normalizada de floats de [0,1]
            Img_Processada = np.float32(Img_Original/255.0)
            gamma = dialog.askfloat("Input", "Selecione o gama a ser utilizado")
            for i in range(w):
                for j in range(h):
                    Img_Processada[i][j] = math.pow(Img_Processada[i][j], gamma)

            #coloca a imagem de [0,255]
            Img_Processada = Img_Processada * 255
            #transfoma a imagem em um array de floats novamente
            Img_Processada = np.int8(Img_Processada)
            print(getPixel(Img_Processada, h-1, w-1))
            print(Img_Processada[w-1,h-1])
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao processar imagem")
    else:
        Processada[0] = False
        mesBox.showerror(title="erro de tipo", message="Imagem vazia.") 

def limiarizacao():
    global Processada
    global Img_Original
    global Img_Processada
    if Carregado[0]:
        try:
            Processada[0] = True
            limiar = dialog.askinteger("Input", "Selecione o Limiar a ser utilizado")
            l, c = Img_Original.shape
            Img_Processada = np.zeros((l, c), np.uint8)
            for i in range(l):
                for j in range(c):
                        if(Img_Original[i][j] >= limiar):
                            Img_Processada[i][j] = 255
                        else:
                            Img_Processada[i][j] = 0 
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao processar imagem")
    else:
        mesBox.showerror(title="erro de conteudo", message="Imagem vazia.") 

#Criacao de Filtro

def criaFiltro3():
    global Fsize
    global Filtro
    Fsize = 3
    Filtro = np.zeros((Fsize, Fsize), np.float16)
    #pede os valores para o Filtro
    for i in range(Fsize):
        for j in range(Fsize):
            try:
                num = dialog.askfloat("Input", f"valor para a posicao: {i} x {j}")
                Filtro[i][j] = num
            except:
                mesBox.showerror(title="", message="Valor Invalido")


def criaFiltro5():
    global Fsize
    global Filtro
    Fsize = 5
    Filtro = np.zeros((Fsize, Fsize), np.float16)
    #pede os valores para o Filtro
    for i in range(Fsize):
        for j in range(Fsize):
            try:
                num = dialog.askfloat("Input", f"valor para a posicao: {i} x {j}")
                Filtro[i][j] = num
            except:
                mesBox.showerror(title="", message="Valor Invalido")

def criaFiltro9():
    global Fsize
    global Filtro
    Fsize = 9
    Filtro = np.zeros((Fsize, Fsize), np.float16)
    #pede os valores para o Filtro
    for i in range(Fsize):
        for j in range(Fsize):
            try:
                num = dialog.askfloat("Input", f"valor para a posicao: {i} x {j}")
                Filtro[i][j] = num
            except:
                mesBox.showerror(title="", message="Valor Invalido")

#Aplicacao de Filtros

def aplicaFiltro5(x, y, c):
    global Img_Original
    global Filtro
    valores = [Filtro[c-2][c-2]*getPixel(Img_Original, x-2, y-2), Filtro[c-2][c-1]*getPixel(Img_Original, x-1, y-2), Filtro[c-2][c]*getPixel(Img_Original, x, y-2), Filtro[c-2][c+1]*getPixel(Img_Original, x+1, y-2), Filtro[c-2][c+2]*getPixel(Img_Original, x+2, y-2), #linha 1
               Filtro[c-1][c-2]*getPixel(Img_Original, x-2, y-1), Filtro[c-1][c-1]*getPixel(Img_Original, x-1, y-1), Filtro[c-1][c]*getPixel(Img_Original, x, y-1), Filtro[c-1][c+1]*getPixel(Img_Original, x+1, y-1), Filtro[c-1][c+2]*getPixel(Img_Original, x+2, y-1), #linha 2
               Filtro[c][c-2]*getPixel(Img_Original, x-2, y),     Filtro[c][c-1]*getPixel(Img_Original, x-1, y),     Filtro[c][c]*getPixel(Img_Original, x, y),     Filtro[c][c+1]*getPixel(Img_Original, x+1, y),     Filtro[c][c+2]*getPixel(Img_Original, x+2, y), #linha 3
               Filtro[c+1][c-2]*getPixel(Img_Original, x-2, y+1), Filtro[c+1][c-1]*getPixel(Img_Original, x-1, y+1), Filtro[c+1][c]*getPixel(Img_Original, x, y+1), Filtro[c+1][c+1]*getPixel(Img_Original, x+1, y+1), Filtro[c+1][c+2]*getPixel(Img_Original, x+2, y+1), #linha 4
               Filtro[c+2][c-2]*getPixel(Img_Original, x-2, y+2), Filtro[c+2][c-1]*getPixel(Img_Original, x-1, y+2), Filtro[c+2][c]*getPixel(Img_Original, x, y+2), Filtro[c+2][c+1]*getPixel(Img_Original, x+1, y+2), Filtro[c+2][c+2]*getPixel(Img_Original, x+2, y+2), #linha 5
              ]
    val = 0
    for i in range(25):
        val = val + valores[i]
    return val

def aplicaFiltro3(x, y, c):
    global Img_Original
    global Filtro
    valores = [Filtro[c-1][c-1]*getPixel(Img_Original, x-1, y-1), Filtro[c-1][c]*getPixel(Img_Original, x, y-1), Filtro[c-1][c+1]*getPixel(Img_Original, x+1, y-1),
               Filtro[c][c-1]*getPixel(Img_Original, x-1, y),     Filtro[c][c]*getPixel(Img_Original, x, y),     Filtro[c][c+1]*getPixel(Img_Original, x+1, y),
               Filtro[c+1][c-1]*getPixel(Img_Original, x-1, y+1), Filtro[c+1][c]*getPixel(Img_Original, x, y+1), Filtro[c+1][c+1]*getPixel(Img_Original, x+1, y+1)]
    val = 0
    for i in range(9):
        val = val + valores[i]
    return val

def conv():
    global Fsize
    global Img_Processada
    global Img_Original
    global Filtro
    try:
        l, c = Img_Original.shape
        Img_Processada = np.zeros((l, c), np.uint8)
        center = math.floor(Fsize/2)
        if(Fsize == 3):
            for i in range(l-1): #y
                for j in range(c-1): #x
                    Img_Processada[i][j] = aplicaFiltro3(j, i, center)
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
            Processada[0] = True
        elif(Fsize == 5):
            for i in range(l-1): #y
                for j in range(c-1): #x
                  Img_Processada[i][j] = aplicaFiltro3(j, i, center)
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
            Processada[0] = True
    except:
        mesBox.showerror(title="", message="erro ao aplicar filtro")

def Media():
    global Fsize
    global Processada
    global Img_Processada
    global Img_Original
    global Filtro
    #setup filtro
    try:
        Filtro = np.zeros((3,3), np.float16)
        Fsize = 3
        Filtro[0][0], Filtro[0][1], Filtro[0][2] = 1/9, 1/9, 1/9
        Filtro[1][0], Filtro[1][1], Filtro[1][2] = 1/9, 1/9, 1/9
        Filtro[2][0], Filtro[2][1], Filtro[2][2] = 1/9, 1/9, 1/9
        conv()
    except:
        mesBox.showerror(title="", message="erro ao aplicar filtro media")

def Ponderada():
    global Fsize
    global Processada
    global Img_Processada
    global Img_Original
    global Filtro
    #setup filtro
    try:
        Filtro = np.zeros((3,3), np.float16)
        Fsize = 3
        Filtro[0][0], Filtro[0][1], Filtro[0][2] = 1/16, 2/16, 1/16
        Filtro[1][0], Filtro[1][1], Filtro[1][2] = 2/16, 4/16, 2/16
        Filtro[2][0], Filtro[2][1], Filtro[2][2] = 1/16, 2/16, 1/16
        conv()
    except:
        mesBox.showerror(title="", message="erro ao aplicar filtro ponderada")

#histograma

def histograma(Img):
    try:
        cores = np.array(Img)
        cores = cores.flatten()
        # Cria o histograma
        plt.hist(cores, bins=256, range=(0,256), color='black')
        # Mostra o histograma
        plt.show()
    except:
        mesBox.showinfo(title="", message="erro ao montar histograma")

def showHistogramaOrigin():
    global Img_Original
    if Carregado[0]:
        histograma(Img_Original)
       
    else:
        mesBox.showerror(title="erro de tipo", message="Imagem vazia.") 
        

def showHistogramaProcess():
    global Img_Processada
    if Processada[0]:
        histograma(Img_Processada)
    else:
        mesBox.showerror(title="erro de tipo", message="Imagem vazia.") 


def equalizar():
    global Carregado
    global Processada
    global Img_Original
    if Carregado[0]:
        equalizarHistogramaG(Img_Original)
    else:
        mesBox.showerror(title="erro de conteudo", message="Imagem vazia.") 

def equalizarHistogramaG(Img):
    try:
        global Carregado
        global Processada
        global Img_Original
        global Img_Processada
        Processada[0] = True
        cores = np.array(Img)
        cores = cores.flatten()
        Img_Processada = Img_Original * 1
        hist = np.zeros(256)
        for i in range(len(cores)):
            hist[cores[i]] = hist[cores[i]] + 1 
        histCulm = np.zeros(256)
        acumulador = 0
        for i in range(len(hist)):
            acumulador = acumulador + hist[i]
            histCulm[i] = acumulador
        for i in range(len(histCulm)):
            histCulm[i] = int((histCulm[i]/len(cores))*255)

        w, h = Img_Processada.shape
        for i in range(w):
            for j in range(h):
                Img_Processada[i][j] = histCulm[Img_Processada[i][j]]
        
        cv2.imshow("Equalizada",Img_Processada)
        cv2.waitKey(0)
    except:
        mesBox.showinfo(title="", message="erro ao processar imagem")


#editor de imagem

def initEditWindow():
    global editWind
    editWind = Tk()
    editWind.resizable(False, False)
    editWind.geometry('1250x600')
    editWind.title("editor de img")
    editWind.config(background="#ffffff")
    editing_frame = tk.Frame(editWind, width=200, height=600, bg="Black")
    editing_frame.pack(side="left", fill="y")
    
def editar():
    global editWind
    initEditWindow()
    editWind.mainloop()

#conteudo
def initContent():
    #barra do menu
    barraMenu = Menu(window)
    window.config(menu=barraMenu)

    fileMenu = Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="File",menu=fileMenu)

    fileMenu.add_command(label="Open Image", command=abrirImg)
    fileMenu.add_command(label="Save Image", command=salvarImg)
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=window.destroy)

    viewMenu = Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="View",menu=viewMenu)
    viewMenu.add_command(label="original img", command=visualizarImgOriginal)
    viewMenu.add_command(label="lado a lado", command=visualizarLadoALado)
    
    editMenu = Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Edit",menu=editMenu)
    editMenu.add_command(label="Negativo", command=negativo)
    editMenu.add_command(label="Logaritmo", command=logaritmo)
    editMenu.add_command(label="Gamma", command=correcaoGama)
    editMenu.add_command(label="Limiarizacao", command=limiarizacao)
    editMenu.add_command(label="Editar", command=editar)

    #filtro
    filtroMenu = Menu(editMenu, tearoff=0)
    editMenu.add_cascade(label="Filtro", menu=filtroMenu)
    filtroMenu.add_command(label="Media", command=Media)
    filtroMenu.add_command(label="Ponderada", command=Ponderada)
    filtroMenu.add_command(label="Convolucao", command=conv)
    #cria filtros
    criafiltroMenu = Menu(filtroMenu, tearoff=0)
    filtroMenu.add_cascade(label="Cria Filtro", menu=criafiltroMenu)
    #3x3
    criafiltroMenu.add_command(label="Cria Filtro 3", command=criaFiltro3)
    #5x5
    criafiltroMenu.add_command(label="Cria Filtro 5", command=criaFiltro5)
    #9x9
    criafiltroMenu.add_command(label="Cria Filtro 9", command=criaFiltro9)
    
    #histograma
    histMenu = Menu(editMenu, tearoff=0)
    editMenu.add_cascade(label="Histograma", menu=histMenu)
    histMenu.add_command(label="histograma Original", command=showHistogramaOrigin)
    histMenu.add_command(label="histograma Process", command=showHistogramaProcess)
    histMenu.add_command(label="equalizar", command=equalizar)



if __name__ == "__main__":
    initWindow()
    initContent()
    window.mainloop()
        
