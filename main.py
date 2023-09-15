import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mesBox
from tkinter import simpledialog as dialog
from PIL import Image, ImageTk

#setup window
def initWindow():
    global window
    global Log
    global LogFrame
    window = Tk()
    window.resizable(False, False)
    window.geometry('450x600')
    icone = PhotoImage(file="res/icone.png")
    window.iconphoto(True, icone)
    window.title("processamento de images")
    window.config(background="#22c995")
    LogFrame = Frame(window)
    LogFrame.place(x=10, y=190, width=430, heigh=400)
    LogFrame.grid_columnconfigure(0, weight=1)
    LogFrame.grid_rowconfigure(0,weight=1)
    #log
    Log = Text(LogFrame, font=("Arial", "10"),width=430, heigh=580, bg="#ffffff")
    Log.pack()
    Log.insert(INSERT,"Log:")
    Log.insert(INSERT, "\n"+("_"*58))
    Log.config(state=DISABLED)
    Log.grid(sticky=N + E + S + W)
    scroll = Scrollbar(Log)
    scroll.config(width=10)
    scroll.pack(side=RIGHT,fill=Y)
    Log.config(yscrollcommand=scroll.set)

def attLog(msg):
    Log.config(state=NORMAL)
    Log.insert(INSERT,"\n"+msg)
    Log.config(state=DISABLED)


#funcoes de processar img
def abrirImg():
    global Carregado
    global Processada
    global Img_Original
    global Img_Processada
    global imgMostrar
    global imglabel
    filetypes = (('image files', ('*.png', '*.bmp', '*.dib' , '*.jpeg', '*.jpg', '*.jpe', '*.jp2', '*.webp', '*.avif', '*.pbm', '*.pgm', '*.ppm', '*.pxm', '*.pnm', '*.pfm', '*.sr', '*.ras' , '*.tiff', '*.tif', '*.exr', '*.hdr', '*.pic')),
                 ("all files", '*.*'))
    #selecione o arquivo
    filepath = filedialog.askopenfilename(title="Abrir Imagem",
                                          initialdir="/",
                                          filetypes=filetypes)
    if(cv2.haveImageReader(filepath) == True):
        attLog("Imagem Carregada!")
        Img_Original = cv2.imread(filepath, 0)
        Carregado = True
    else:
        attLog("Falha ao abrir a Imagem")
        mesBox.showerror(title="Arquivo nao suportado", message="Arquivo nao suportado. \nPorfavor escolha um válido")


def salvarImg():
    #formatos suportados pelo opencv
    filetypes = ['.png', '.bmp', '.dib' , '.jpeg', '.jpg', '.jpe', '.jp2', '.webp', '.avif', '.pbm', '.pgm', '.ppm', '.pxm', '.pnm', '.pfm', '.sr', '.ras' , '.tiff', '.tif', '.exr', '.hdr', '.pic']
    #faz algo se tiver uma imagem carregada
    if(Carregado == True):
        #seleciona o formato
        formato = dialog.askstring("Input", "Selecione o formato que deseja salvar a Imagem:\n(ex: .png)")
        if(formato.lower() in filetypes):
            #selecione o arquivo
            filepath = filedialog.filepath = filedialog.askdirectory(title='Selecione onde o arquivo sera salvo')
            nome = dialog.askstring("Input", "Digite como deseja salvar o nome do arquivo")
            nome = nome + (formato.lower())
            os.chdir(filepath)
            if Processada == False:
                cv2.imwrite(nome, Img_Original)
                attLog("Imagem Original Salva em escala de cinza")
            else:
                cv2.imwrite(nome, Img_Processada)
                attLog("Imagem Processada Salva em escala de cinza")
        else:
            mesBox.showerror(title="erro de tipo", message="Formato nao suportado. \nPorfavor escolha um válido")     
    else:
        attLog("nenhuma imagem carregada")

def visualizarImgOriginal():
    if Carregado: 
        cv2.imshow('ImageWindow', Img_Original)
        cv2.waitKey(0)
    else:
        attLog("nenhuma imagem carregada")

def visualizarImgProcessada():
    if Processada: 
        cv2.imshow('ImageWindow', Img_Processada)
        cv2.waitKey(0)
    else:
        attLog("nenhuma imagem Processada")


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
    



if __name__ == "__main__":
    Carregado = False
    Processada = False
    Img_Original = []
    Img_Processada = []
    initWindow()
    initContent()
    window.mainloop()
    if(Carregado == True):
        print(Img_Original[0][0])