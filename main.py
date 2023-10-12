import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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
Carregado = False
Processada = False
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
        Img_Original = cv2.imread(filepath, 1)
        Carregado = True
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
                if(CheckDouble(Img_Original)):
                    Img_Original = Img_Original * 255
                cv2.imwrite(nome, Img_Original)
            else:
                if(CheckDouble(Img_Processada)):
                    Img_Processada = Img_Processada * 255
                cv2.imwrite(nome, Img_Processada)
        else:
            mesBox.showerror(title="erro de tipo", message="Formato nao suportado. \nPorfavor escolha um válido")     
    else:
        mesBox.showinfo(title="", message="nenhuma imagem carregada")

def CheckDouble(Img):
    try:
        l, c, cha = Img.shape[:3]
        for i in range(l):
            for j in range(c):
                (b, g, r) = Img[i][j]
                if(r > 0.0 and r < 1.0) or (g > 0.0 and g < 1.0) or (b > 0.0 and b < 1.0):
                    return True
        return False
    except:
        mesBox.showinfo(title="", message="erro ao checkar double")
        return False

def CheckNegative(Img):
    try:
        l, c, cha = Img.shape[:3]
        for i in range(l):
            for j in range(c):
                (b, g, r) = Img[i][j]
                if(r < 0.0):
                    return 1 
                elif(g < 0.0): 
                    return 2
                elif (b < 0.0):
                    return 3
        return 0
    except:
        mesBox.showinfo(title="", message="erro ao achar o negativo")
        return 0

def getMin(Img, channel):
    try:
        (minb, ming, minr) = Img[0][0]
        l, c, cha = Img.shape[:3]
        for i in range(l):
            for j in range(c):
                (b, g, r) = Img[i][j]
                if(minr > r):
                    minr = r
                if(ming > g): 
                    ming = g
                if (minb > b):
                    minb = b
        if(channel == 1):
            return minr
        elif(channel == 2): 
            return ming  
        elif (channel == 3):
            return minb
        else:
            return 0
    except:
        mesBox.showinfo(title="", message="erro ao pegar o minimo")
        return 0

    
def addImg(Img, valR, valG, valB):
    try:
        l, c, cha = Img.shape[:3]
        for i in range(l):
            for j in range(c):
                (b, g, r) = Img[i][j]
                Img[i][j] = (b+valB, g+valG, r+valR)
    except:
        mesBox.showinfo(title="", message="Erro ao somar imagem")

def addImgRGB(Img, val):
    try:
        l, c, cha = Img.shape[:3]
        for i in range(l):
            for j in range(c):
                (b, g, r) = Img[i][j]
                Img[i][j] = (b+val, g+val, r+val)
    except:
        mesBox.showinfo(title="", message="Erro ao somar imagem")

#coloca imagem de 0 a 255
def convertImg(ImgS):
    Img = ImgS * 1
    if(CheckNegative(Img) == 1):
        addImgRGB(Img, -1*getMin(Img, CheckNegative(Img)))
    if(CheckNegative(Img) == 2):
        addImgRGB(Img, -1*getMin(Img, CheckNegative(Img)))
    if(CheckNegative(Img) == 3):
        addImgRGB(Img, -1*getMin(Img, CheckNegative(Img)))

    if(Img.max() > 255):
        Img = Img / Img.max()
        Img = Img * 255
        
    elif(CheckDouble(Img) and Img.max() <= 1):
        Img = Img * 255

    return np.uint8(Img)


def visualizarImgOriginal():
    global Img_Original
    if Carregado: 
        try:
            cv2.imshow('ImageWindow', convertImg(Img_Original))
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao mostrar imagem")
    else:
        mesBox.showinfo(title="", message="nenhuma imagem carregada")


def visualizarLadoALado():
    global Img_Original
    global Img_Processada
    if Processada: 
        try:
            image = np.concatenate((convertImg(Img_Original), convertImg(Img_Processada)), axis=1)
            cv2.imshow('ImageWindow', image)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao mostrar imagem")
    else:
        mesBox.showinfo(title="", message="nenhuma imagem processada")

#primitivas
def getR(Img, x, y):
    l, c = Img_Original.shape[:2]
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return 0
    else:
        b, g, r = Img[y][x]
        return r

def getG(Img, x, y):
    l, c = Img_Original.shape[:2]
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return 0
    else:
        b, g, r = Img[y][x]
        return g

def getB(Img, x, y):
    l, c = Img_Original.shape[:2]
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return 0
    else:
        b, g, r = Img[y][x]
        return b

def getPixel(Img, x, y):
    l, c = Img_Original.shape[:2]
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return (0, 0, 0)
    else:
        b, g, r = Img[y][x]
        return (r, g, b)

def setPixel(Img, x, y, intensidade):
    l, c = Img_Original.shape
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return
    else:
        Img[y][x] = intensidade

def getHSV(r, g, b):
    rl = r/255 
    gl = g/255
    bl = b/255
    Cmax = max(rl, gl, bl)
    Cmin = min(rl, gl, bl)
    deltaC = Cmax - Cmin
    H = 0
    S = 0
    V = Cmax
    if(Cmax == rl):
        H = 60 * (((gl-bl)/deltaC) % 6)
    elif(Cmax == gl):
        H = 60 * (((bl-rl)/deltaC) + 2)
    else:
        H = 60 * (((rl-gl)/deltaC) + 4)
    
    if(Cmax != 0):
        S = deltaC / Cmax
    
    H = round(H)
    return H, S, V

def getRGB(h, s, v):
    Cc  = v * s 
    Hl = h/60
    Xx = Cc * (1 - abs((Hl % 2) - 1))
    r1, g1, b1 = 0, 0, 0
    if(0 <= Hl and Hl < 1):
        r1, g1, b1 = Cc, Xx, 0
    elif(1 <= Hl and Hl < 2):
        r1, g1, b1 = Xx, Cc, 0
    elif(2 <= Hl and Hl < 3):
        r1, g1, b1 = 0, Cc, Xx
    elif(3 <= Hl and Hl < 4):
        r1, g1, b1 = 0, Xx, Cc
    elif(4 <= Hl and Hl < 5):
        r1, g1, b1 = Xx, 0, Cc
    elif(5 <= Hl and Hl < 6):
        r1, g1, b1 = Cc, 0, Xx

    m = v - Cc

    return (round((r1+m)*255), round((g1+m)*255), round((b1+m)*255))


#processos basicos

def negativo():
    global Carregado
    global Processada
    global Img_Original
    global Img_Processada
    if Carregado:
        Processada = True
        w, h, c = Img_Original.shape[:3]
        Img_Processada = np.zeros((w, h, c), np.uint8)
        for i in range(w):
            for j in range(h):
                (b, g, r) = Img_Original[i][j]
                Img_Processada[i][j] = (255 - b, 255 - g, 255 - r)
        cv2.imshow('ImageWindow', Img_Processada)
        cv2.waitKey(0)
    else:
        Processada = False
        mesBox.showerror(title="erro de tipo", message="Imagem vazia.") 

def logaritmoRGB():
    global Carregado
    global Processada
    global Img_Original
    global Img_Processada
    if Carregado:
        Processada = True
        #pede a base do logaritimo
        base = dialog.askstring("Input", "Selecione a base logaritmica a ser utilizada. \nou ln para logaritmo natural(base e)")
        if(base.lower() == "ln"):
            try:
                w, h, c = Img_Original.shape[:3]
                Img_Processada = np.zeros((w, h, c), np.float32)
                for i in range(w):
                    for j in range(h):
                        b, g, r = Img_Original[i][j]
                        if(b != 0):
                            b = math.log(b)
                        if(g != 0):
                            g = math.log(g)
                        if(r != 0):
                            r = math.log(r)

                        Img_Processada[i][j] = (b, g, r)

                cv2.normalize(Img_Processada, Img_Processada,0,255,cv2.NORM_MINMAX)
                Img_Processada = np.uint8(Img_Processada)
                cv2.imshow('ImageWindow', convertImg(Img_Processada))
                cv2.waitKey(0)
            except:
                mesBox.showinfo(title="", message="erro ao processar imagem")
        else:
            try:
                base = int(base)
                w, h, c = Img_Original.shape[:3]
                Img_Processada = np.zeros((w, h, c), np.float32)
                for i in range(w):
                    for j in range(h):
                        b, g, r = Img_Original[i][j]
                        if(b != 0):
                            b = math.log(b, base)
                        if(g != 0):
                            g = math.log(g, base)
                        if(r != 0):
                            r = math.log(r, base)

                        Img_Processada[i][j] = (b, g, r)

                cv2.normalize(Img_Processada, Img_Processada,0,255,cv2.NORM_MINMAX)
                Img_Processada = np.uint8(Img_Processada)
                cv2.imshow('ImageWindow', convertImg(Img_Processada))
                cv2.waitKey(0)
            except:
                mesBox.showinfo(title="", message="erro ao processar imagem")
    else:
       Processada = False
       mesBox.showerror(title="erro de tipo", message="Imagem vazia.") 
       mesBox.showinfo(title="", message="sem imagem carregada")

def correcaoGamaRGB():
    global Carregado
    global Processada
    global Img_Original
    global Img_Processada
    if Carregado:
        try:
            Processada = True
            w, h, c = Img_Original.shape[:3]
        
            #cria uma imagem normalizada de floats de [0,1]
            Img_Processada = np.zeros((w, h, c), np.float32)
            gamma = dialog.askfloat("Input", "Selecione o gama a ser utilizado")
            for i in range(w):
                for j in range(h):
                    b, g, r = Img_Original[i][j]
                    b = b/255.0
                    g = g/255.0
                    r = r/255.0
                    Img_Processada[i][j] = (math.pow(b, gamma), math.pow(g, gamma), math.pow(r, gamma))

            #coloca a imagem de [0,255]
            for i in range(w):
                for j in range(h):
                    b, g, r = Img_Processada[i][j]
                    b = b*255.0
                    g = g*255.0
                    r = r*255.0
                    Img_Processada[i][j] = (b, g, r)
            
            #transfoma a imagem em um array de floats novamente
            Img_Processada = np.int8(Img_Processada)
           
            cv2.imshow('ImageWindow', convertImg(Img_Processada))
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao processar imagem")
    else:
        Processada = False
        mesBox.showerror(title="erro de tipo", message="Imagem vazia.") 

def limiarizacaoRGB():
    global Processada
    global Img_Original
    global Img_Processada
    if Carregado:
        try:
            Processada = True
            limiar = dialog.askinteger("Input", "Selecione o Limiar a ser utilizado")
            l, c, cha = Img_Original.shape[:3]
            Img_Processada = np.zeros((l, c, cha), np.uint8)
            for i in range(l):
                for j in range(c):
                        b, g, r = Img_Original[i][j]
                        if(b >= limiar): 
                            b = 255 
                        else: 
                            b = 0
                        if(g >= limiar): 
                            g = 255 
                        else: 
                            g = 0
                        if(r >= limiar): 
                            r = 255 
                        else: 
                            r = 0
                        Img_Processada[i][j] = (b, g, r)
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao processar imagem")
    else:
        mesBox.showerror(title="erro de conteudo", message="Imagem vazia.") 

def GrayScale():
    global Processada
    global Img_Original
    global Img_Processada
    if Carregado:
        try:
            Processada = True
            l, c, cha = Img_Original.shape[:3]
            Img_Original = np.float32(Img_Original)
            Img_Processada = np.zeros((l, c, cha), np.uint8)
            for i in range(l):
                for j in range(c):
                        (b, g, r) = Img_Original[i][j]
                        valor = r+g+b 
                        valor = valor / 3
                        Img_Processada[i][j] = (valor, valor, valor)
            Img_Original = np.uint8(Img_Original)
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao processar imagem")
    else:
        mesBox.showerror(title="erro de conteudo", message="Imagem vazia.") 

def GrayScaleAprim():
    global Processada
    global Img_Original
    global Img_Processada
    if Carregado:
        try:  #RED*0,3 + GREEN*0,59 + BLUE*0,11
            Processada = True
            l, c, cha = Img_Original.shape[:3]
            Img_Original = np.float32(Img_Original)
            Img_Processada = np.zeros((l, c, cha), np.uint8)
            for i in range(l):
                for j in range(c):
                        (b, g, r) = Img_Original[i][j]
                        valor = r*0.3 + g*0.59 + b*0.11
                        valor = valor / 3
                        Img_Processada[i][j] = (valor, valor, valor)
            Img_Original = np.uint8(Img_Original)
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao processar imagem")
    else:
        mesBox.showerror(title="erro de conteudo", message="Imagem vazia.") 

def Sepia():
    global Processada
    global Img_Original
    global Img_Processada
    if Carregado:
        try:
            Processada = True
            l, c, cha = Img_Original.shape[:3]
            Img_Original = np.float32(Img_Original)
            Img_Processada = np.zeros((l, c, cha), np.uint8)
            for i in range(l):
                for j in range(c):
                        (b, g, r) = Img_Original[i][j]
                        valr = int(r*0.393 +g*0.769 +b*0.189)
                        valg = int(r*0.349 +g*0.686 +b*0.168) 
                        valb = int(r*0.272 +g*0.534 +b*0.131) 
                        if valr > 255:
                            valr = 255
                        if valg > 255:
                            valg = 255
                        if valb > 255:
                            valb = 255
                        Img_Processada[i][j] = (valb, valg, valr)
            Img_Original = np.uint8(Img_Original)
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao processar imagem")
    else:
        mesBox.showerror(title="erro de conteudo", message="Imagem vazia.") 

#Criacao de Filtros

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

#aplicacao de filtros
def aplicaFiltro3(x, y, c):
    global Img_Original
    global Filtro
    valoresR = [Filtro[c-1][c-1]*getR(Img_Original, x-1, y-1), Filtro[c-1][c]*getR(Img_Original, x, y-1), Filtro[c-1][c+1]*getR(Img_Original, x+1, y-1),
               Filtro[c][c-1]*getR(Img_Original, x-1, y),     Filtro[c][c]*getR(Img_Original, x, y),     Filtro[c][c+1]*getR(Img_Original, x+1, y),
               Filtro[c+1][c-1]*getR(Img_Original, x-1, y+1), Filtro[c+1][c]*getR(Img_Original, x, y+1), Filtro[c+1][c+1]*getR(Img_Original, x+1, y+1)]
    
    valoresG = [Filtro[c-1][c-1]*getG(Img_Original, x-1, y-1), Filtro[c-1][c]*getG(Img_Original, x, y-1), Filtro[c-1][c+1]*getG(Img_Original, x+1, y-1),
               Filtro[c][c-1]*getG(Img_Original, x-1, y),     Filtro[c][c]*getG(Img_Original, x, y),     Filtro[c][c+1]*getG(Img_Original, x+1, y),
               Filtro[c+1][c-1]*getG(Img_Original, x-1, y+1), Filtro[c+1][c]*getG(Img_Original, x, y+1), Filtro[c+1][c+1]*getG(Img_Original, x+1, y+1)]
    
    valoresB = [Filtro[c-1][c-1]*getB(Img_Original, x-1, y-1), Filtro[c-1][c]*getB(Img_Original, x, y-1), Filtro[c-1][c+1]*getB(Img_Original, x+1, y-1),
               Filtro[c][c-1]*getB(Img_Original, x-1, y),     Filtro[c][c]*getB(Img_Original, x, y),     Filtro[c][c+1]*getB(Img_Original, x+1, y),
               Filtro[c+1][c-1]*getB(Img_Original, x-1, y+1), Filtro[c+1][c]*getB(Img_Original, x, y+1), Filtro[c+1][c+1]*getB(Img_Original, x+1, y+1)]
    
    valR = 0
    valG = 0
    valB = 0
    for i in range(9):
        valR = valR + valoresR[i]
        valG = valG + valoresG[i]
        valB = valB + valoresB[i]

    return valB, valG, valR

def aplicaFiltro5(x, y, c):
    global Img_Original
    global Filtro
    valoresR = [Filtro[c-2][c-2]*getR(Img_Original, x-2, y-2), Filtro[c-2][c-1]*getR(Img_Original, x-1, y-2), Filtro[c-2][c]*getR(Img_Original, x, y-2), Filtro[c-2][c+1]*getR(Img_Original, x+1, y-2), Filtro[c-2][c+2]*getR(Img_Original, x+2, y-2), #linha 1
               Filtro[c-1][c-2]*getR(Img_Original, x-2, y-1), Filtro[c-1][c-1]*getR(Img_Original, x-1, y-1), Filtro[c-1][c]*getR(Img_Original, x, y-1), Filtro[c-1][c+1]*getR(Img_Original, x+1, y-1), Filtro[c-1][c+2]*getR(Img_Original, x+2, y-1), #linha 2
               Filtro[c][c-2]*getR(Img_Original, x-2, y),     Filtro[c][c-1]*getR(Img_Original, x-1, y),     Filtro[c][c]*getR(Img_Original, x, y),     Filtro[c][c+1]*getR(Img_Original, x+1, y),     Filtro[c][c+2]*getR(Img_Original, x+2, y), #linha 3
               Filtro[c+1][c-2]*getR(Img_Original, x-2, y+1), Filtro[c+1][c-1]*getR(Img_Original, x-1, y+1), Filtro[c+1][c]*getR(Img_Original, x, y+1), Filtro[c+1][c+1]*getR(Img_Original, x+1, y+1), Filtro[c+1][c+2]*getR(Img_Original, x+2, y+1), #linha 4
               Filtro[c+2][c-2]*getR(Img_Original, x-2, y+2), Filtro[c+2][c-1]*getR(Img_Original, x-1, y+2), Filtro[c+2][c]*getR(Img_Original, x, y+2), Filtro[c+2][c+1]*getR(Img_Original, x+1, y+2), Filtro[c+2][c+2]*getR(Img_Original, x+2, y+2), #linha 5
              ]
    
    valoresG = [Filtro[c-2][c-2]*getG(Img_Original, x-2, y-2), Filtro[c-2][c-1]*getG(Img_Original, x-1, y-2), Filtro[c-2][c]*getG(Img_Original, x, y-2), Filtro[c-2][c+1]*getG(Img_Original, x+1, y-2), Filtro[c-2][c+2]*getG(Img_Original, x+2, y-2), #linha 1
               Filtro[c-1][c-2]*getG(Img_Original, x-2, y-1), Filtro[c-1][c-1]*getG(Img_Original, x-1, y-1), Filtro[c-1][c]*getG(Img_Original, x, y-1), Filtro[c-1][c+1]*getG(Img_Original, x+1, y-1), Filtro[c-1][c+2]*getG(Img_Original, x+2, y-1), #linha 2
               Filtro[c][c-2]*getG(Img_Original, x-2, y),     Filtro[c][c-1]*getG(Img_Original, x-1, y),     Filtro[c][c]*getG(Img_Original, x, y),     Filtro[c][c+1]*getG(Img_Original, x+1, y),     Filtro[c][c+2]*getG(Img_Original, x+2, y), #linha 3
               Filtro[c+1][c-2]*getG(Img_Original, x-2, y+1), Filtro[c+1][c-1]*getG(Img_Original, x-1, y+1), Filtro[c+1][c]*getG(Img_Original, x, y+1), Filtro[c+1][c+1]*getG(Img_Original, x+1, y+1), Filtro[c+1][c+2]*getG(Img_Original, x+2, y+1), #linha 4
               Filtro[c+2][c-2]*getG(Img_Original, x-2, y+2), Filtro[c+2][c-1]*getG(Img_Original, x-1, y+2), Filtro[c+2][c]*getG(Img_Original, x, y+2), Filtro[c+2][c+1]*getG(Img_Original, x+1, y+2), Filtro[c+2][c+2]*getG(Img_Original, x+2, y+2), #linha 5
              ]
    
    valoresB = [Filtro[c-2][c-2]*getB(Img_Original, x-2, y-2), Filtro[c-2][c-1]*getB(Img_Original, x-1, y-2), Filtro[c-2][c]*getB(Img_Original, x, y-2), Filtro[c-2][c+1]*getB(Img_Original, x+1, y-2), Filtro[c-2][c+2]*getB(Img_Original, x+2, y-2), #linha 1
               Filtro[c-1][c-2]*getB(Img_Original, x-2, y-1), Filtro[c-1][c-1]*getB(Img_Original, x-1, y-1), Filtro[c-1][c]*getB(Img_Original, x, y-1), Filtro[c-1][c+1]*getB(Img_Original, x+1, y-1), Filtro[c-1][c+2]*getB(Img_Original, x+2, y-1), #linha 2
               Filtro[c][c-2]*getB(Img_Original, x-2, y),     Filtro[c][c-1]*getB(Img_Original, x-1, y),     Filtro[c][c]*getB(Img_Original, x, y),     Filtro[c][c+1]*getB(Img_Original, x+1, y),     Filtro[c][c+2]*getB(Img_Original, x+2, y), #linha 3
               Filtro[c+1][c-2]*getB(Img_Original, x-2, y+1), Filtro[c+1][c-1]*getB(Img_Original, x-1, y+1), Filtro[c+1][c]*getB(Img_Original, x, y+1), Filtro[c+1][c+1]*getB(Img_Original, x+1, y+1), Filtro[c+1][c+2]*getB(Img_Original, x+2, y+1), #linha 4
               Filtro[c+2][c-2]*getB(Img_Original, x-2, y+2), Filtro[c+2][c-1]*getB(Img_Original, x-1, y+2), Filtro[c+2][c]*getB(Img_Original, x, y+2), Filtro[c+2][c+1]*getB(Img_Original, x+1, y+2), Filtro[c+2][c+2]*getB(Img_Original, x+2, y+2), #linha 5
              ]
    valR = 0
    valG = 0
    valB = 0
    for i in range(25):
        valR = valR + valoresR[i]
        valG = valG + valoresG[i]
        valB = valB + valoresB[i]
    return valB, valG, valR

#convolucao

def convRGB():
    global Fsize
    global Processada
    global Img_Processada
    global Img_Original
    global Filtro
    try:
        l, c, cha = Img_Original.shape[:3]
        Img_Processada = np.zeros((l, c, cha), np.float32)
        center = math.floor(Fsize/2)
        if(Fsize == 3):
            for i in range(l-1): #y
                for j in range(c-1): #x
                    (b, g, r) = aplicaFiltro3(j, i, center)
                    Img_Processada[i][j] = (b, g, r)
            cv2.imshow('ImageWindow', convertImg(Img_Processada))
            cv2.waitKey(0)
            Processada = True
        elif(Fsize == 5):
            for i in range(l-1): #y
                for j in range(c-1): #x
                    (b, g, r) = aplicaFiltro5(j, i, center)
                    Img_Processada[i][j] =  (b, g, r)
            cv2.imshow('ImageWindow', convertImg(Img_Processada))
            cv2.waitKey(0)
            Processada = True
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
        convRGB()
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
        convRGB()
    except:
        mesBox.showerror(title="", message="erro ao aplicar filtro ponderada")

def Laplaciano():
    global Fsize
    global Processada
    global Img_Processada
    global Img_Original
    global Filtro
    #setup filtro
    try:
        Filtro = np.zeros((3,3), np.float16)
        Fsize = 3
        Filtro[0][0], Filtro[0][1], Filtro[0][2] =  0, -1,  0
        Filtro[1][0], Filtro[1][1], Filtro[1][2] = -1,  4, -1 
        Filtro[2][0], Filtro[2][1], Filtro[2][2] =  0, -1,  0
        convRGB()
    except:
       mesBox.showerror(title="", message="erro o Laplaciano")
################ Histograma #####################

#faz os arrays de cor 

def MakeRed(img):
    arr = convertImg(img)
    l, c = img.shape[:2]
    redArray = np.zeros((l*c), np.uint8)
    for i in range(l):
        for j in range(c):
            (b, g, r) = arr[i][j]
            redArray[i*c + j] = r

    return redArray

def MakeGreen(img):
    arr = convertImg(img)
    l, c = img.shape[:2]
    greenArray = np.zeros((l*c), np.uint8)
    for i in range(l):
        for j in range(c):
            (b, g, r) = arr[i][j]
            greenArray[i*c + j] = g

    return greenArray

def MakeBlue(img):
    arr = convertImg(img)
    l, c = img.shape[:2]
    blueArray = np.zeros((l*c), np.uint8)
    for i in range(l):
        for j in range(c):
            (b, g, r) = arr[i][j]
            blueArray[i*c + j] = b

    return blueArray

#cria histograma
def Histograma(img, cor):
    corA = []
    if cor.lower() == "r":
        corA = MakeRed(img)
        plt.hist(corA, bins=256, range=(0,255), color='red')
        plt.show()

    elif cor.lower() == "g":
        corA = MakeGreen(img)
        plt.hist(corA, bins=256, range=(0,255), color='green')
        plt.show()

    elif cor.lower() == "b":
        corA = MakeBlue(img)
        plt.hist(corA, bins=256, range=(0,255), color='blue')
        plt.show()
    
    else:
        redData   = pd.DataFrame(dict(Red=np.array(MakeRed(img))))
        greenData = pd.DataFrame(dict(Green=np.array(MakeGreen(img))))
        blueData  = pd.DataFrame(dict(Blue=np.array(MakeBlue(img))))

        fig, axes = plt.subplots(1, 3)

        redData.hist('Red',     bins=256,  range=(0,255), color='red',   ax=axes[0])
        greenData.hist('Green', bins=256,  range=(0,255), color='green', ax=axes[1])
        blueData.hist('Blue',   bins=256,  range=(0,255), color='blue',  ax=axes[2])

        plt.show()

#mostrar histograma
def ShowHistogramOR():
    try:
        Histograma(Img_Original, "R")
    except:
        mesBox.showerror("Error", "Erro ao plotar histograma")

def ShowHistogramOG():
    try:
        Histograma(Img_Original, "G")
    except:
        mesBox.showerror("Error", "Erro ao plotar histograma")

def ShowHistogramOB():
    try:
        Histograma(Img_Original, "B")
    except:
        mesBox.showerror("Error", "Erro ao plotar histograma")

def ShowHistogramORGB():
    try:
        Histograma(Img_Original, "RGB")
    except:
        mesBox.showerror("Error", "Erro ao plotar histograma")

def ShowHistogramPR():
    try:
        Histograma(Img_Processada, "R")
    except:
        mesBox.showerror("Error", "Erro ao plotar histograma")

def ShowHistogramPG():
    try:
        Histograma(Img_Processada, "G")
    except:
        mesBox.showerror("Error", "Erro ao plotar histograma")

def ShowHistogramPB():
    try:
        Histograma(Img_Processada, "B")
    except:
        mesBox.showerror("Error", "Erro ao plotar histograma")

def ShowHistogramPRGB():
    try:
        Histograma(Img_Processada, "RGB")
    except:
        mesBox.showerror("Error", "Erro ao plotar histograma")

#equalizar histogramas
def equalizarHistogramaRGB(Img, pros):
    try:
        global Carregado
        global Processada
        global Img_Original
        global Img_Processada
        Processada = True

        corR = MakeRed(Img)
        corG = MakeGreen(Img)
        corB = MakeBlue(Img)
        
        if(pros == False):
            Img_Processada = Img_Original * 1

        histR = np.zeros(256)
        histG = np.zeros(256)
        histB = np.zeros(256)

        for i in range(len(corR)):
            histR[corR[i]] = histR[corR[i]] + 1
            histG[corG[i]] = histG[corG[i]] + 1
            histB[corB[i]] = histB[corB[i]] + 1

        histCulmR = np.zeros(256)
        histCulmG = np.zeros(256)
        histCulmB = np.zeros(256)

        acumuladorR = 0
        acumuladorG = 0
        acumuladorB = 0

        for i in range(len(histR)):
            acumuladorR = acumuladorR + histR[i]
            acumuladorG = acumuladorG + histG[i]
            acumuladorB = acumuladorB + histB[i]

            histCulmR[i] = acumuladorR
            histCulmG[i] = acumuladorG
            histCulmB[i] = acumuladorB

        for i in range(len(histCulmR)):
            histCulmR[i] = int((histCulmR[i]/len(corR))*255)
            histCulmG[i] = int((histCulmG[i]/len(corG))*255)
            histCulmB[i] = int((histCulmB[i]/len(corB))*255)

        w, h, ch = Img_Processada.shape[:3]
        for i in range(w):
            for j in range(h):
                (b, g, r) = Img_Processada[i][j]
                Img_Processada[i][j] = (histCulmB[b], histCulmG[g], histCulmR[r])
        
        cv2.imshow("Equalizada",Img_Processada)
        cv2.waitKey(0)
    except:
        mesBox.showinfo(title="", message="erro ao processar imagem")

def equalizarHistograma(Img, Color, pros):
    try:
        global Carregado
        global Processada
        global Img_Original
        global Img_Processada
        Processada = True

        cor = []
        if(Color == "R"):
            cor = MakeRed(Img)
        elif(Color == "G"):
            cor = MakeGreen(Img)
        elif(Color == "B"):
            cor = MakeBlue(Img)
        
        if(pros == False):
            Img_Processada = Img_Original * 1

        hist = np.zeros(256)

        for i in range(len(cor)):
            hist[cor[i]] = hist[cor[i]] + 1
  
        histCulm = np.zeros(256)

        acumulador = 0

        for i in range(len(hist)):
            acumulador = acumulador + hist[i]

            histCulm[i] = acumulador

        for i in range(len(histCulm)):
            histCulm[i] = int((histCulm[i]/len(cor))*255)
           

        w, h, ch = Img_Processada.shape[:3]
        for i in range(w):
            for j in range(h):
                (b, g, r) = Img_Processada[i][j]

                if(Color == "R"):
                    r = histCulm[r]
                elif(Color == "G"):
                    g = histCulm[g]
                elif(Color == "B"):
                    b = histCulm[b]
                
                Img_Processada[i][j] = (b, g, r)
        
        cv2.imshow("Equalizada",Img_Processada)
        cv2.waitKey(0)
    except:
        mesBox.showinfo(title="", message="erro ao processar imagem")

def equalizarOriginalRGB():
    equalizarHistogramaRGB(Img_Original, False)

def equalizarOriginalR():
    equalizarHistograma(Img_Original, "R", False)

def equalizarOriginalG():
    equalizarHistograma(Img_Original, "G", False)

def equalizarOriginalB():
    equalizarHistograma(Img_Original, "B", False)

###############################################

def equalizarProcessadaRGB():
    equalizarHistogramaRGB(Img_Processada, True)

def equalizarProcessadaR():
    equalizarHistograma(Img_Processada, "R", True)

def equalizarProcessadaG():
    equalizarHistograma(Img_Processada, "G", True)

def equalizarProcessadaB():
    equalizarHistograma(Img_Processada, "B", True)

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
    #RGB
    editMenu.add_command(label="Logaritmo", command=logaritmoRGB)
    editMenu.add_command(label="Gamma", command=correcaoGamaRGB)
    editMenu.add_command(label="Limiarizacao", command=limiarizacaoRGB)
    editMenu.add_command(label="Gray Simple", command=GrayScale)
    editMenu.add_command(label="Gray Ponderada", command=GrayScaleAprim)
    editMenu.add_command(label="Sepia", command=Sepia)
    #editMenu.add_command(label="Editar", command=editar)

    #filtro
    filtroMenu = Menu(editMenu, tearoff=0)
    barraMenu.add_cascade(label="Filtro", menu=filtroMenu)
    filtroMenu.add_command(label="Media", command=Media)
    filtroMenu.add_command(label="Ponderada", command=Ponderada)
    filtroMenu.add_command(label="Convolucao", command=convRGB)
    filtroMenu.add_command(label="Laplaciano", command=Laplaciano)
    #cria filtros
    criafiltroMenu = Menu(filtroMenu, tearoff=0)
    filtroMenu.add_cascade(label="Cria Filtro", menu=criafiltroMenu)
    #3x3
    criafiltroMenu.add_command(label="Cria Filtro 3", command=criaFiltro3)
    #5x5
    criafiltroMenu.add_command(label="Cria Filtro 5", command=criaFiltro5)
    #9x9
    #criafiltroMenu.add_command(label="Cria Filtro 9", command=criaFiltro9)
    
    #histograma
    histMenu = Menu(editMenu, tearoff=0)
    editMenu.add_cascade(label="Histograma", menu=histMenu)
    histMenu.add_command(label="Histograma Original canal R", command=ShowHistogramOR)
    histMenu.add_command(label="Histograma Original canal G", command=ShowHistogramOG)
    histMenu.add_command(label="Histograma Original canal B", command=ShowHistogramOB)
    histMenu.add_command(label="Histograma Original canal RGB", command=ShowHistogramORGB)
    histMenu.add_separator()
    #HISTOGRAMA IMAGEM PROCESSADA
    histMenu.add_command(label="Histograma Processada canal R", command=ShowHistogramPR)
    histMenu.add_command(label="Histograma Processada canal G", command=ShowHistogramPG)
    histMenu.add_command(label="Histograma Processada canal B", command=ShowHistogramPB)
    histMenu.add_command(label="Histograma Processada canal RGB", command=ShowHistogramPRGB)
    histMenu.add_separator()
    #equalizar
    histMenu.add_command(label="Equalizar Original R", command=equalizarOriginalR)
    histMenu.add_command(label="Equalizar Original G", command=equalizarOriginalG)
    histMenu.add_command(label="Equalizar Original B", command=equalizarOriginalB)
    histMenu.add_command(label="Equalizar Original RGB", command=equalizarOriginalRGB)
    histMenu.add_separator()
    histMenu.add_command(label="Equalizar Processada R", command=equalizarProcessadaR)
    histMenu.add_command(label="Equalizar Processada G", command=equalizarProcessadaG)
    histMenu.add_command(label="Equalizar Processada B", command=equalizarProcessadaB)
    histMenu.add_command(label="Equalizar Processada RGB", command=equalizarProcessadaRGB)


if __name__ == "__main__":
    #initWindow()
    #initContent()
    #window.mainloop()
    print(getRGB(343,0.84,0.49))
   
        
