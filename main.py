import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import gc
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mesBox
from tkinter import simpledialog as dialog
from PIL import Image, ImageTk


Carregado = [False]
Processada = [False]
Img_Original = []
Img_Processada = []
Filtro = []
Log = ""

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



#funcoes de processar img
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

def visualizarImgProcessada():
    global Img_Processada
    
    if Processada[0]: 
        try:
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao mostrar imagem")
    else:
        mesBox.showinfo(title="", message="nenhuma imagem processada")

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
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao processar imagem")
    else:
        Processada[0] = False
        mesBox.showerror(title="erro de tipo", message="Imagem vazia.") 

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
    viewMenu.add_command(label="process  img", command=visualizarImgProcessada)
    
    editMenu = Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Edit",menu=editMenu)
    editMenu.add_command(label="Negativo", command=negativo)
    editMenu.add_command(label="Logaritmo", command=logaritmo)
    editMenu.add_command(label="Gamma", command=correcaoGama)
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