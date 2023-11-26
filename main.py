import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import gc
import colorsys
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
    global icone
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

def addImgHSV(Img, h, s, v):
    try:
        l, c, cha = Img.shape[:3]
        for i in range(l):
            for j in range(c):
                (b, g, r) = Img[i][j]
                ho, so, vo = getHSV(r, g, b)
                ho = ho + h
                so = so + s 
                vo = vo + v
                nr, ng, nb = getRGB(ho, so, vo)
                Img[i][j] = (nb, ng, nr)
    except:
        mesBox.showinfo(title="", message="Erro ao somar imagem")

#coloca imagem de 0 a 255
def convertImg(ImgS):
    if(ImgS.max() <= 1 or ImgS.max() >= 255):
        if(ImgS.min() < 0): 
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
    else:
        return ImgS


def visualizarImgOriginal():
    global Img_Original
    if Carregado: 
        try:
            cv2.imshow('ImageWindow', Img_Original)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao mostrar imagem")
    else:
        mesBox.showinfo(title="", message="nenhuma imagem carregada")

def visualizarImgProcess():
    global Img_Processada
    if Processada: 
        try:
            cv2.imshow('ImageWindow', Img_Processada)
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
            image = np.concatenate((Img_Original, convertImg(Img_Processada)), axis=1)
            cv2.imshow('ImageWindow', image)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao mostrar imagem")
    else:
        mesBox.showinfo(title="", message="nenhuma imagem processada")

#primitivas
def getR(Img, x, y):
    l, c = Img.shape[:2]
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return 0
    else:
        b, g, r = Img[y][x]
        return r

def getG(Img, x, y):
    l, c = Img.shape[:2]
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return 0
    else:
        b, g, r = Img[y][x]
        return g

def getB(Img, x, y):
    l, c = Img.shape[:2]
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return 0
    else:
        b, g, r = Img[y][x]
        return b

#retorna o formato B G R
def getPixel(Img, x, y):
    l, c = Img.shape[:2]
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return 0, 0, 0
    else:
        b, g, r = Img[y][x]
        return b, g, r

def setPixel(Img, x, y, intensidade):
    l, c = Img_Original.shape
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return
    else:
        Img[y][x] = intensidade

def getHSV(r, g, b):
    if(r > 255):
        r = 255
    elif(r < 0):
        r = 0

    if(g > 255):
        g = 255
    elif g < 0:
        g = 0

    if(b > 255):
        b = 255
    elif b < 0:
        b = 0

    rl = r/255 
    gl = g/255
    bl = b/255
    Cmax = max(rl, gl, bl)
    Cmin = min(rl, gl, bl)
    deltaC = Cmax - Cmin
    H = 0
    S = 0
    V = Cmax
    if(deltaC != 0):
        if(Cmax == rl):
            H = 60 * (((gl-bl)/deltaC) % 6)
        elif(Cmax == gl):
            H = 60 * (((bl-rl)/deltaC) + 2)
        elif(Cmax == bl):
            H = 60 * (((rl-gl)/deltaC) + 4)
    
    if(Cmax != 0):
        S = deltaC / Cmax
    
    H = round(H)
    return H, S, V

def getRGB(h, s, v):
    if(s > 1):
        s = 1
    elif s < 0:
        s = 0

    if(v > 1):
        v = 1
    elif v < 0:
        v = 0

    if(h > 360):
        h = 360
    elif h < 0:
        h = 0
    
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

    return round((r1+m)*255), round((g1+m)*255), round((b1+m)*255)

def getRGB_CMY(c, m, y, k):
    r = 255 * (1-c) * (1-k)
    g = 255 * (1-m) * (1-k)
    b = 255 * (1-y) * (1-k)
    return r, g, b

#processos basicos

def inverter(Img):
    try:
        w, h, c = Img.shape[:3]
        imgRetorno = np.zeros((w, h, c), np.uint8)
        for i in range(w):
            for j in range(h):
                    b, g, r = Img[i][j]
                    if(b == 0): 
                        b = 255 
                    else: 
                        b = 0
                    if(g == 0): 
                        g = 255 
                    else: 
                        g = 0
                    if(r == 0): 
                        r = 255 
                    else: 
                        r = 0
                    imgRetorno[i][j] = (b, g, r)
        return imgRetorno
    except:
        mesBox.showerror(title="erro na negativa", message="erro na negativa.") 

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
                cv2.imshow('ImageWindow', Img_Processada)
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
                cv2.imshow('ImageWindow', Img_Processada)
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
           
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
        except:
            mesBox.showinfo(title="", message="erro ao processar imagem")
    else:
        Processada = False
        mesBox.showerror(title="erro de tipo", message="Imagem vazia.") 

def limiarizarK(img, k):
    try:
        limiar = k
        l, c, cha = img.shape[:3]
        imgRetorno = np.zeros((l, c, cha), np.uint8)
        for i in range(l):
            for j in range(c):
                    b, g, r = img[i][j]
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
                    imgRetorno[i][j] = (b, g, r)

        return imgRetorno
    except:
            mesBox.showinfo(title="", message="erro ao processar imagem")

def limiarizar(img):
    try:
        limiar = dialog.askinteger("Input", "Selecione o Limiar a ser utilizado")
        l, c, cha = img.shape[:3]
        imgRetorno = np.zeros((l, c, cha), np.uint8)
        for i in range(l):
            for j in range(c):
                    b, g, r = img[i][j]
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
                    imgRetorno[i][j] = (b, g, r)

        return imgRetorno
    except:
            mesBox.showinfo(title="", message="erro ao processar imagem")

def limiarizacaoRGB():
    global Processada
    global Img_Original
    global Img_Processada
    try:
       Img_Processada = limiarizar(Img_Original)
       cv2.imshow('ImageWindow', Img_Processada)
       cv2.waitKey(0)
       Processada = True
    except:
        mesBox.showerror(title="erro de conteudo", message="Imagem vazia.") 


def GrayScaleK(Img):
    try:
            l, c, cha = Img.shape[:3]
            Img = np.float32(Img)
            ImagemRetorno = np.zeros((l, c, cha), np.uint8)
            for i in range(l):
                for j in range(c):
                        (b, g, r) = Img[i][j]
                        valor = r+g+b 
                        valor = valor / 3
                        ImagemRetorno[i][j] = (valor, valor, valor)
            Img = np.uint8(Img)
            return ImagemRetorno
    except:
            mesBox.showinfo(title="", message="erro ao processar imagem")

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

def criaFiltro7():
    global Fsize
    global Filtro
    Fsize = 7
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

def aplicaFiltro7(x, y, c):
    global Img_Original
    global Filtro
    valoresR = [Filtro[c-3][c-3]*getR(Img_Original, x-3, y-3),Filtro[c-3][c-2]*getR(Img_Original, x-2, y-3), Filtro[c-3][c-1]*getR(Img_Original, x-1, y-3), Filtro[c-3][c]*getR(Img_Original, x, y-3), Filtro[c-3][c+1]*getR(Img_Original, x+1, y-3), Filtro[c-3][c+2]*getR(Img_Original, x+2, y-3),Filtro[c-3][c+3]*getR(Img_Original, x+3, y-3),
               Filtro[c-2][c-3]*getR(Img_Original, x-3, y-2),Filtro[c-2][c-2]*getR(Img_Original, x-2, y-2), Filtro[c-2][c-1]*getR(Img_Original, x-1, y-2), Filtro[c-2][c]*getR(Img_Original, x, y-2), Filtro[c-2][c+1]*getR(Img_Original, x+1, y-2), Filtro[c-2][c+2]*getR(Img_Original, x+2, y-2),Filtro[c-2][c+3]*getR(Img_Original, x+3, y-2), #linha 1
               Filtro[c-1][c-3]*getR(Img_Original, x-3, y-1),Filtro[c-1][c-2]*getR(Img_Original, x-2, y-1), Filtro[c-1][c-1]*getR(Img_Original, x-1, y-1), Filtro[c-1][c]*getR(Img_Original, x, y-1), Filtro[c-1][c+1]*getR(Img_Original, x+1, y-1), Filtro[c-1][c+2]*getR(Img_Original, x+2, y-1),Filtro[c-2][c+3]*getR(Img_Original, x+3, y-1), #linha 2
               Filtro[c][c-3]*getR(Img_Original, x-3, y),Filtro[c][c-2]*getR(Img_Original, x-2, y),     Filtro[c][c-1]*getR(Img_Original, x-1, y),     Filtro[c][c]*getR(Img_Original, x, y),     Filtro[c][c+1]*getR(Img_Original, x+1, y),     Filtro[c][c+2]*getR(Img_Original, x+2, y),Filtro[c][c+3]*getR(Img_Original, x+3, y), #linha 3
               Filtro[c+1][c-3]*getR(Img_Original, x-3, y+1),Filtro[c+1][c-2]*getR(Img_Original, x-2, y+1), Filtro[c+1][c-1]*getR(Img_Original, x-1, y+1), Filtro[c+1][c]*getR(Img_Original, x, y+1), Filtro[c+1][c+1]*getR(Img_Original, x+1, y+1), Filtro[c+1][c+2]*getR(Img_Original, x+2, y+1),Filtro[c+1][c+3]*getR(Img_Original, x+3, y+1), #linha 4
               Filtro[c+2][c-3]*getR(Img_Original, x-3, y+2),Filtro[c+2][c-2]*getR(Img_Original, x-2, y+2), Filtro[c+2][c-1]*getR(Img_Original, x-1, y+2), Filtro[c+2][c]*getR(Img_Original, x, y+2), Filtro[c+2][c+1]*getR(Img_Original, x+1, y+2), Filtro[c+2][c+2]*getR(Img_Original, x+2, y+2),Filtro[c+2][c+3]*getR(Img_Original, x+3, y+2),
               Filtro[c+3][c-3]*getR(Img_Original, x-3, y+3),Filtro[c+3][c-2]*getR(Img_Original, x-2, y+3), Filtro[c+3][c-1]*getR(Img_Original, x-1, y+3), Filtro[c+3][c]*getR(Img_Original, x, y+3), Filtro[c+3][c+1]*getR(Img_Original, x+1, y+3), Filtro[c+3][c+2]*getR(Img_Original, x+2, y+3),Filtro[c+3][c+3]*getR(Img_Original, x+3, y+3)#linha 5
              ]
    
    valoresG = [Filtro[c-3][c-3]*getG(Img_Original, x-3, y-3),Filtro[c-3][c-2]*getG(Img_Original, x-2, y-3), Filtro[c-3][c-1]*getG(Img_Original, x-1, y-3), Filtro[c-3][c]*getG(Img_Original, x, y-3), Filtro[c-3][c+1]*getG(Img_Original, x+1, y-3), Filtro[c-3][c+2]*getG(Img_Original, x+2, y-3),Filtro[c-3][c+3]*getG(Img_Original, x+3, y-3),
               Filtro[c-2][c-3]*getG(Img_Original, x-3, y-2),Filtro[c-2][c-2]*getG(Img_Original, x-2, y-2), Filtro[c-2][c-1]*getG(Img_Original, x-1, y-2), Filtro[c-2][c]*getG(Img_Original, x, y-2), Filtro[c-2][c+1]*getG(Img_Original, x+1, y-2), Filtro[c-2][c+2]*getG(Img_Original, x+2, y-2),Filtro[c-2][c+3]*getG(Img_Original, x+3, y-2), #linha 1
               Filtro[c-1][c-3]*getG(Img_Original, x-3, y-1),Filtro[c-1][c-2]*getG(Img_Original, x-2, y-1), Filtro[c-1][c-1]*getG(Img_Original, x-1, y-1), Filtro[c-1][c]*getG(Img_Original, x, y-1), Filtro[c-1][c+1]*getG(Img_Original, x+1, y-1), Filtro[c-1][c+2]*getG(Img_Original, x+2, y-1),Filtro[c-2][c+3]*getG(Img_Original, x+3, y-1), #linha 2
               Filtro[c][c-3]*getG(Img_Original, x-3, y),Filtro[c][c-2]*getG(Img_Original, x-2, y),     Filtro[c][c-1]*getG(Img_Original, x-1, y),     Filtro[c][c]*getG(Img_Original, x, y),     Filtro[c][c+1]*getG(Img_Original, x+1, y),     Filtro[c][c+2]*getG(Img_Original, x+2, y),Filtro[c][c+3]*getG(Img_Original, x+3, y), #linha 3
               Filtro[c+1][c-3]*getG(Img_Original, x-3, y+1),Filtro[c+1][c-2]*getG(Img_Original, x-2, y+1), Filtro[c+1][c-1]*getG(Img_Original, x-1, y+1), Filtro[c+1][c]*getG(Img_Original, x, y+1), Filtro[c+1][c+1]*getG(Img_Original, x+1, y+1), Filtro[c+1][c+2]*getG(Img_Original, x+2, y+1),Filtro[c+1][c+3]*getG(Img_Original, x+3, y+1), #linha 4
               Filtro[c+2][c-3]*getG(Img_Original, x-3, y+2),Filtro[c+2][c-2]*getG(Img_Original, x-2, y+2), Filtro[c+2][c-1]*getG(Img_Original, x-1, y+2), Filtro[c+2][c]*getG(Img_Original, x, y+2), Filtro[c+2][c+1]*getG(Img_Original, x+1, y+2), Filtro[c+2][c+2]*getG(Img_Original, x+2, y+2),Filtro[c+2][c+3]*getG(Img_Original, x+3, y+2),
               Filtro[c+3][c-3]*getG(Img_Original, x-3, y+3),Filtro[c+3][c-2]*getG(Img_Original, x-2, y+3), Filtro[c+3][c-1]*getG(Img_Original, x-1, y+3), Filtro[c+3][c]*getG(Img_Original, x, y+3), Filtro[c+3][c+1]*getG(Img_Original, x+1, y+3), Filtro[c+3][c+2]*getG(Img_Original, x+2, y+3),Filtro[c+3][c+3]*getG(Img_Original, x+3, y+3)#linha 5
              ]
    
    valoresB = [Filtro[c-3][c-3]*getB(Img_Original, x-3, y-3),Filtro[c-3][c-2]*getB(Img_Original, x-2, y-3), Filtro[c-3][c-1]*getB(Img_Original, x-1, y-3), Filtro[c-3][c]*getB(Img_Original, x, y-3), Filtro[c-3][c+1]*getB(Img_Original, x+1, y-3), Filtro[c-3][c+2]*getB(Img_Original, x+2, y-3),Filtro[c-3][c+3]*getB(Img_Original, x+3, y-3),
               Filtro[c-2][c-3]*getB(Img_Original, x-3, y-2),Filtro[c-2][c-2]*getB(Img_Original, x-2, y-2), Filtro[c-2][c-1]*getB(Img_Original, x-1, y-2), Filtro[c-2][c]*getB(Img_Original, x, y-2), Filtro[c-2][c+1]*getB(Img_Original, x+1, y-2), Filtro[c-2][c+2]*getB(Img_Original, x+2, y-2),Filtro[c-2][c+3]*getB(Img_Original, x+3, y-2), #linha 1
               Filtro[c-1][c-3]*getB(Img_Original, x-3, y-1),Filtro[c-1][c-2]*getB(Img_Original, x-2, y-1), Filtro[c-1][c-1]*getB(Img_Original, x-1, y-1), Filtro[c-1][c]*getB(Img_Original, x, y-1), Filtro[c-1][c+1]*getB(Img_Original, x+1, y-1), Filtro[c-1][c+2]*getB(Img_Original, x+2, y-1),Filtro[c-2][c+3]*getB(Img_Original, x+3, y-1), #linha 2
               Filtro[c][c-3]*getB(Img_Original, x-3, y),Filtro[c][c-2]*getB(Img_Original, x-2, y),     Filtro[c][c-1]*getB(Img_Original, x-1, y),     Filtro[c][c]*getB(Img_Original, x, y),     Filtro[c][c+1]*getB(Img_Original, x+1, y),     Filtro[c][c+2]*getB(Img_Original, x+2, y),Filtro[c][c+3]*getB(Img_Original, x+3, y), #linha 3
               Filtro[c+1][c-3]*getB(Img_Original, x-3, y+1),Filtro[c+1][c-2]*getB(Img_Original, x-2, y+1), Filtro[c+1][c-1]*getB(Img_Original, x-1, y+1), Filtro[c+1][c]*getB(Img_Original, x, y+1), Filtro[c+1][c+1]*getB(Img_Original, x+1, y+1), Filtro[c+1][c+2]*getB(Img_Original, x+2, y+1),Filtro[c+1][c+3]*getB(Img_Original, x+3, y+1), #linha 4
               Filtro[c+2][c-3]*getB(Img_Original, x-3, y+2),Filtro[c+2][c-2]*getB(Img_Original, x-2, y+2), Filtro[c+2][c-1]*getB(Img_Original, x-1, y+2), Filtro[c+2][c]*getB(Img_Original, x, y+2), Filtro[c+2][c+1]*getB(Img_Original, x+1, y+2), Filtro[c+2][c+2]*getB(Img_Original, x+2, y+2),Filtro[c+2][c+3]*getB(Img_Original, x+3, y+2),
               Filtro[c+3][c-3]*getB(Img_Original, x-3, y+3),Filtro[c+3][c-2]*getB(Img_Original, x-2, y+3), Filtro[c+3][c-1]*getB(Img_Original, x-1, y+3), Filtro[c+3][c]*getB(Img_Original, x, y+3), Filtro[c+3][c+1]*getB(Img_Original, x+1, y+3), Filtro[c+3][c+2]*getB(Img_Original, x+2, y+3),Filtro[c+3][c+3]*getB(Img_Original, x+3, y+3)#linha 5
              ]
    valR = 0
    valG = 0
    valB = 0
    for i in range(25):
        valR = valR + valoresR[i]
        valG = valG + valoresG[i]
        valB = valB + valoresB[i]
    return valB, valG, valR

def aplicaFiltro9(x, y, c):
    global Img_Original
    global Filtro
    valoresR = [Filtro[c-4][c-3]*getR(Img_Original, x-3, y-3),Filtro[c-3][c-2]*getR(Img_Original, x-2, y-3), Filtro[c-3][c-1]*getR(Img_Original, x-1, y-3), Filtro[c-3][c]*getR(Img_Original, x, y-3), Filtro[c-3][c+1]*getR(Img_Original, x+1, y-3), Filtro[c-3][c+2]*getR(Img_Original, x+2, y-3),Filtro[c-3][c+3]*getR(Img_Original, x+3, y-3),
               Filtro[c-3][c-3]*getR(Img_Original, x-3, y-3),Filtro[c-3][c-2]*getR(Img_Original, x-2, y-3), Filtro[c-3][c-1]*getR(Img_Original, x-1, y-3), Filtro[c-3][c]*getR(Img_Original, x, y-3), Filtro[c-3][c+1]*getR(Img_Original, x+1, y-3), Filtro[c-3][c+2]*getR(Img_Original, x+2, y-3),Filtro[c-3][c+3]*getR(Img_Original, x+3, y-3),
               Filtro[c-2][c-3]*getR(Img_Original, x-2, y-2),Filtro[c-2][c-2]*getR(Img_Original, x-2, y-2), Filtro[c-2][c-1]*getR(Img_Original, x-1, y-2), Filtro[c-2][c]*getR(Img_Original, x, y-2), Filtro[c-2][c+1]*getR(Img_Original, x+1, y-2), Filtro[c-2][c+2]*getR(Img_Original, x+2, y-2),Filtro[c-2][c+3]*getR(Img_Original, x+3, y-2), #linha 1
               Filtro[c-1][c-3]*getR(Img_Original, x-1, y-1),Filtro[c-1][c-2]*getR(Img_Original, x-2, y-1), Filtro[c-1][c-1]*getR(Img_Original, x-1, y-1), Filtro[c-1][c]*getR(Img_Original, x, y-1), Filtro[c-1][c+1]*getR(Img_Original, x+1, y-1), Filtro[c-1][c+2]*getR(Img_Original, x+2, y-1),Filtro[c-2][c+3]*getR(Img_Original, x+3, y-1), #linha 2
               Filtro[c][c-3]*getR(Img_Original, x, y-3),Filtro[c][c-2]*getR(Img_Original, x-2, y),     Filtro[c][c-1]*getR(Img_Original, x-1, y),     Filtro[c][c]*getR(Img_Original, x, y),     Filtro[c][c+1]*getR(Img_Original, x+1, y),     Filtro[c][c+2]*getR(Img_Original, x+2, y),Filtro[c][c+3]*getR(Img_Original, x+3, y), #linha 3
               Filtro[c+1][c-3]*getR(Img_Original, x+1, y-3),Filtro[c+1][c-2]*getR(Img_Original, x-2, y+1), Filtro[c+1][c-1]*getR(Img_Original, x-1, y+1), Filtro[c+1][c]*getR(Img_Original, x, y+1), Filtro[c+1][c+1]*getR(Img_Original, x+1, y+1), Filtro[c+1][c+2]*getR(Img_Original, x+2, y+1),Filtro[c+1][c+3]*getR(Img_Original, x+3, y+1), #linha 4
               Filtro[c+2][c-3]*getR(Img_Original, x+2, y-3),Filtro[c+2][c-2]*getR(Img_Original, x-2, y+2), Filtro[c+2][c-1]*getR(Img_Original, x-1, y+2), Filtro[c+2][c]*getR(Img_Original, x, y+2), Filtro[c+2][c+1]*getR(Img_Original, x+1, y+2), Filtro[c+2][c+2]*getR(Img_Original, x+2, y+2),Filtro[c+2][c+3]*getR(Img_Original, x+3, y+2),
               Filtro[c+3][c-3]*getR(Img_Original, x+3, y-3),Filtro[c+3][c-2]*getR(Img_Original, x-2, y+3), Filtro[c+3][c-1]*getR(Img_Original, x-1, y+3), Filtro[c+3][c]*getR(Img_Original, x, y+3), Filtro[c+3][c+1]*getR(Img_Original, x+1, y+3), Filtro[c+3][c+2]*getR(Img_Original, x+2, y+3),Filtro[c+3][c+3]*getR(Img_Original, x+3, y+3)#linha 5
              ]
    
    valoresG = [Filtro[c-3][c-3]*getG(Img_Original, x-3, y-3),Filtro[c-3][c-2]*getG(Img_Original, x-2, y-3), Filtro[c-3][c-1]*getG(Img_Original, x-1, y-3), Filtro[c-3][c]*getG(Img_Original, x, y-3), Filtro[c-3][c+1]*getG(Img_Original, x+1, y-3), Filtro[c-3][c+2]*getG(Img_Original, x+2, y-3),Filtro[c-3][c+3]*getG(Img_Original, x+3, y-3),
               Filtro[c-2][c-3]*getG(Img_Original, x-2, y-3),Filtro[c-2][c-2]*getG(Img_Original, x-2, y-2), Filtro[c-2][c-1]*getG(Img_Original, x-1, y-2), Filtro[c-2][c]*getG(Img_Original, x, y-2), Filtro[c-2][c+1]*getG(Img_Original, x+1, y-2), Filtro[c-2][c+2]*getG(Img_Original, x+2, y-2),Filtro[c-2][c+3]*getG(Img_Original, x+3, y-2), #linha 1
               Filtro[c-1][c-3]*getG(Img_Original, x-1, y-3),Filtro[c-1][c-2]*getG(Img_Original, x-2, y-1), Filtro[c-1][c-1]*getG(Img_Original, x-1, y-1), Filtro[c-1][c]*getG(Img_Original, x, y-1), Filtro[c-1][c+1]*getG(Img_Original, x+1, y-1), Filtro[c-1][c+2]*getG(Img_Original, x+2, y-1),Filtro[c-2][c+3]*getG(Img_Original, x+3, y-1), #linha 2
               Filtro[c][c-3]*getG(Img_Original, x, y-3),Filtro[c][c-2]*getG(Img_Original, x-2, y),     Filtro[c][c-1]*getG(Img_Original, x-1, y),     Filtro[c][c]*getG(Img_Original, x, y),     Filtro[c][c+1]*getG(Img_Original, x+1, y),     Filtro[c][c+2]*getG(Img_Original, x+2, y),Filtro[c][c+3]*getG(Img_Original, x+3, y), #linha 3
               Filtro[c+1][c-3]*getG(Img_Original, x+1, y-3),Filtro[c+1][c-2]*getG(Img_Original, x-2, y+1), Filtro[c+1][c-1]*getG(Img_Original, x-1, y+1), Filtro[c+1][c]*getG(Img_Original, x, y+1), Filtro[c+1][c+1]*getG(Img_Original, x+1, y+1), Filtro[c+1][c+2]*getG(Img_Original, x+2, y+1),Filtro[c+1][c+3]*getG(Img_Original, x+3, y+1), #linha 4
               Filtro[c+2][c-3]*getG(Img_Original, x+2, y-3),Filtro[c+2][c-2]*getG(Img_Original, x-2, y+2), Filtro[c+2][c-1]*getG(Img_Original, x-1, y+2), Filtro[c+2][c]*getG(Img_Original, x, y+2), Filtro[c+2][c+1]*getG(Img_Original, x+1, y+2), Filtro[c+2][c+2]*getG(Img_Original, x+2, y+2),Filtro[c+2][c+3]*getG(Img_Original, x+3, y+2),
               Filtro[c+3][c-3]*getG(Img_Original, x+3, y-3),Filtro[c+3][c-2]*getG(Img_Original, x-2, y+3), Filtro[c+3][c-1]*getG(Img_Original, x-1, y+3), Filtro[c+3][c]*getG(Img_Original, x, y+3), Filtro[c+3][c+1]*getG(Img_Original, x+1, y+3), Filtro[c+3][c+2]*getG(Img_Original, x+2, y+3),Filtro[c+3][c+3]*getG(Img_Original, x+3, y+3)#linha 5
              ]
    
    valoresB = [Filtro[c-3][c-3]*getB(Img_Original, x-3, y-3),Filtro[c-3][c-2]*getB(Img_Original, x-2, y-3), Filtro[c-3][c-1]*getB(Img_Original, x-1, y-3), Filtro[c-3][c]*getB(Img_Original, x, y-3), Filtro[c-3][c+1]*getB(Img_Original, x+1, y-3), Filtro[c-3][c+2]*getB(Img_Original, x+2, y-3),Filtro[c-3][c+3]*getB(Img_Original, x+3, y-3),
               Filtro[c-2][c-3]*getB(Img_Original, x-2, y-3),Filtro[c-2][c-2]*getB(Img_Original, x-2, y-2), Filtro[c-2][c-1]*getB(Img_Original, x-1, y-2), Filtro[c-2][c]*getB(Img_Original, x, y-2), Filtro[c-2][c+1]*getB(Img_Original, x+1, y-2), Filtro[c-2][c+2]*getB(Img_Original, x+2, y-2),Filtro[c-2][c+3]*getB(Img_Original, x+3, y-2), #linha 1
               Filtro[c-1][c-3]*getB(Img_Original, x-1, y-3),Filtro[c-1][c-2]*getB(Img_Original, x-2, y-1), Filtro[c-1][c-1]*getB(Img_Original, x-1, y-1), Filtro[c-1][c]*getB(Img_Original, x, y-1), Filtro[c-1][c+1]*getB(Img_Original, x+1, y-1), Filtro[c-1][c+2]*getB(Img_Original, x+2, y-1),Filtro[c-2][c+3]*getB(Img_Original, x+3, y-1), #linha 2
               Filtro[c][c-3]*getB(Img_Original, x, y-3),Filtro[c][c-2]*getB(Img_Original, x-2, y),     Filtro[c][c-1]*getB(Img_Original, x-1, y),     Filtro[c][c]*getB(Img_Original, x, y),     Filtro[c][c+1]*getB(Img_Original, x+1, y),     Filtro[c][c+2]*getB(Img_Original, x+2, y),Filtro[c][c+3]*getB(Img_Original, x+3, y), #linha 3
               Filtro[c+1][c-3]*getB(Img_Original, x+1, y-3),Filtro[c+1][c-2]*getB(Img_Original, x-2, y+1), Filtro[c+1][c-1]*getB(Img_Original, x-1, y+1), Filtro[c+1][c]*getB(Img_Original, x, y+1), Filtro[c+1][c+1]*getB(Img_Original, x+1, y+1), Filtro[c+1][c+2]*getB(Img_Original, x+2, y+1),Filtro[c+1][c+3]*getB(Img_Original, x+3, y+1), #linha 4
               Filtro[c+2][c-3]*getB(Img_Original, x+2, y-3),Filtro[c+2][c-2]*getB(Img_Original, x-2, y+2), Filtro[c+2][c-1]*getB(Img_Original, x-1, y+2), Filtro[c+2][c]*getB(Img_Original, x, y+2), Filtro[c+2][c+1]*getB(Img_Original, x+1, y+2), Filtro[c+2][c+2]*getB(Img_Original, x+2, y+2),Filtro[c+2][c+3]*getB(Img_Original, x+3, y+2),
               Filtro[c+3][c-3]*getB(Img_Original, x+3, y-3),Filtro[c+3][c-2]*getB(Img_Original, x-2, y+3), Filtro[c+3][c-1]*getB(Img_Original, x-1, y+3), Filtro[c+3][c]*getB(Img_Original, x, y+3), Filtro[c+3][c+1]*getB(Img_Original, x+1, y+3), Filtro[c+3][c+2]*getB(Img_Original, x+2, y+3),Filtro[c+3][c+3]*getB(Img_Original, x+3, y+3)#linha 5
              ]
    valR = 0
    valG = 0
    valB = 0
    for i in range(25):
        valR = valR + valoresR[i]
        valG = valG + valoresG[i]
        valB = valB + valoresB[i]
    return valB, valG, valR

#pega os valores

def getValores3(x, y):
    global Img_Original
    global Filtro
    valoresR = np.array([getR(Img_Original, x-1, y-1), getR(Img_Original, x, y-1), getR(Img_Original, x+1, y-1), getR(Img_Original, x-1, y), getR(Img_Original, x, y), getR(Img_Original, x+1, y), getR(Img_Original, x-1, y+1), getR(Img_Original, x, y+1), getR(Img_Original, x+1, y+1)])
    
    valoresG = np.array([getG(Img_Original, x-1, y-1), getG(Img_Original, x, y-1), getG(Img_Original, x+1, y-1), getG(Img_Original, x-1, y), getG(Img_Original, x, y), getG(Img_Original, x+1, y), getG(Img_Original, x-1, y+1), getG(Img_Original, x, y+1), getG(Img_Original, x+1, y+1)])
    
    valoresB = np.array([getB(Img_Original, x-1, y-1), getB(Img_Original, x, y-1), getB(Img_Original, x+1, y-1), getB(Img_Original, x-1, y),    getB(Img_Original, x, y), getB(Img_Original, x+1, y), getB(Img_Original, x-1, y+1), getB(Img_Original, x, y+1),  getB(Img_Original, x+1, y+1)])
    
    valR = np.median(valoresR)
    valG = np.median(valoresG)
    valB = np.median(valoresB)

    return valB, valG, valR

def getValores5(x, y):
    global Img_Original
    global Filtro
    valoresR = np.array([getR(Img_Original, x-2, y-2), getR(Img_Original, x-1, y-2), getR(Img_Original, x, y-2), getR(Img_Original, x+1, y-2), getR(Img_Original, x+2, y-2), #linha 1
               getR(Img_Original, x-2, y-1), getR(Img_Original, x-1, y-1), getR(Img_Original, x, y-1), getR(Img_Original, x+1, y-1), getR(Img_Original, x+2, y-1), #linha 2
               getR(Img_Original, x-2, y),     getR(Img_Original, x-1, y),     getR(Img_Original, x, y),     getR(Img_Original, x+1, y),  getR(Img_Original, x+2, y), #linha 3
               getR(Img_Original, x-2, y+1), getR(Img_Original, x-1, y+1), getR(Img_Original, x, y+1), getR(Img_Original, x+1, y+1), getR(Img_Original, x+2, y+1), #linha 4
               getR(Img_Original, x-2, y+2), getR(Img_Original, x-1, y+2), getR(Img_Original, x, y+2), getR(Img_Original, x+1, y+2), getR(Img_Original, x+2, y+2), #linha 5
              ])
    
    valoresG = np.array([getG(Img_Original, x-2, y-2), getG(Img_Original, x-1, y-2), getG(Img_Original, x, y-2), getG(Img_Original, x+1, y-2), getG(Img_Original, x+2, y-2), #linha 1
               getG(Img_Original, x-2, y-1), getG(Img_Original, x-1, y-1), getG(Img_Original, x, y-1), getG(Img_Original, x+1, y-1), getG(Img_Original, x+2, y-1), #linha 2
               getG(Img_Original, x-2, y),     getG(Img_Original, x-1, y),     getG(Img_Original, x, y),     getG(Img_Original, x+1, y),  getG(Img_Original, x+2, y), #linha 3
               getG(Img_Original, x-2, y+1), getG(Img_Original, x-1, y+1), getG(Img_Original, x, y+1), getG(Img_Original, x+1, y+1), getG(Img_Original, x+2, y+1), #linha 4
               getG(Img_Original, x-2, y+2), getG(Img_Original, x-1, y+2), getG(Img_Original, x, y+2), getG(Img_Original, x+1, y+2), getG(Img_Original, x+2, y+2), #linha 5
              ])
    
    valoresB = np.array([getB(Img_Original, x-2, y-2), getB(Img_Original, x-1, y-2), getB(Img_Original, x, y-2), getB(Img_Original, x+1, y-2), getB(Img_Original, x+2, y-2), #linha 1
               getB(Img_Original, x-2, y-1), getB(Img_Original, x-1, y-1), getB(Img_Original, x, y-1), getB(Img_Original, x+1, y-1), getB(Img_Original, x+2, y-1), #linha 2
               getB(Img_Original, x-2, y),     getB(Img_Original, x-1, y),     getB(Img_Original, x, y),     getB(Img_Original, x+1, y),  getB(Img_Original, x+2, y), #linha 3
               getB(Img_Original, x-2, y+1), getB(Img_Original, x-1, y+1), getB(Img_Original, x, y+1), getB(Img_Original, x+1, y+1), getB(Img_Original, x+2, y+1), #linha 4
               getB(Img_Original, x-2, y+2), getB(Img_Original, x-1, y+2), getB(Img_Original, x, y+2), getB(Img_Original, x+1, y+2), getB(Img_Original, x+2, y+2), #linha 5
              ])
    
    valR = np.median(valoresR)
    valG = np.median(valoresG)
    valB = np.median(valoresB)

    return valB, valG, valR
   

#convolucao

def MedianaS(size):
    global Processada
    global Img_Processada
    global Img_Original
    try:
        l, c, cha = Img_Original.shape[:3]
        Img_Processada = np.zeros((l, c, cha), np.float32)
        if(size == 3):
            for i in range(l-1): #y
                for j in range(c-1): #x
                    (b, g, r) = getValores3(j, i)
                    Img_Processada[i][j] = (b, g, r)
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
            Processada = True
        elif(size == 5):
            for i in range(l-1): #y
                for j in range(c-1): #x
                    (b, g, r) = getValores5(j, i)
                    Img_Processada[i][j] =  (b, g, r)
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
            Processada = True
    except:
        mesBox.showerror(title="", message="erro ao aplicar filtro")


def convRet():
    global Fsize
    global Processada
    global Img_Processada
    global Img_Original
    global Filtro
    try:
        l, c, cha = Img_Original.shape[:3]
        Imagem_convol = np.zeros((l, c, cha), np.float32)
        center = math.floor(Fsize/2)
        if(Fsize == 3):
            for i in range(l-1): #y
                for j in range(c-1): #x
                    (b, g, r) = aplicaFiltro3(j, i, center)
                    Imagem_convol[i][j] = (b, g, r)
        elif(Fsize == 5):
            for i in range(l-1): #y
                for j in range(c-1): #x
                    (b, g, r) = aplicaFiltro5(j, i, center)
                    Imagem_convol[i][j] =  (b, g, r)
        elif(Fsize == 7):
            for i in range(l-1): #y
                for j in range(c-1): #x
                    (b, g, r) = aplicaFiltro7(j, i, center)
                    Imagem_convol[i][j] =  (b, g, r)
        elif(Fsize == 9):
            for i in range(l-1): #y
                for j in range(c-1): #x
                    (b, g, r) = aplicaFiltro9(j, i, center)
                    Imagem_convol[i][j] =  (b, g, r)
        
        return Imagem_convol
    except:
        mesBox.showerror(title="", message="erro ao aplicar filtro")

def Convolucao():
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
        elif(Fsize == 7):
            for i in range(l-1): #y
                for j in range(c-1): #x
                    (b, g, r) = aplicaFiltro7(j, i, center)
                    Img_Processada[i][j] =  (b, g, r)
            cv2.imshow('ImageWindow', convertImg(Img_Processada))
            cv2.waitKey(0)
            Processada = True
        elif(Fsize == 9):
            for i in range(l-1): #y
                for j in range(c-1): #x
                    (b, g, r) = aplicaFiltro9(j, i, center)
                    Img_Processada[i][j] =  (b, g, r)
            cv2.imshow('ImageWindow', convertImg(Img_Processada))
            cv2.waitKey(0)
            Processada = True
    except:
        mesBox.showerror(title="", message="erro ao aplicar filtro")


#callback

def Sobel():
    global Fsize
    global Processada
    global Img_Processada
    global Img_Original
    global Filtro
    #setup filtro
    try:
        Filtro = np.zeros((3,3), np.float16)
        Fsize = 3
        Filtro[0][0], Filtro[0][1], Filtro[0][2] =  -1, 0,  1
        Filtro[1][0], Filtro[1][1], Filtro[1][2] =  -2, 0,  2 
        Filtro[2][0], Filtro[2][1], Filtro[2][2] =  -1, 0,  1
        xAplicado = convRet()

        Filtro[0][0], Filtro[0][1], Filtro[0][2] =  1,  2,   1
        Filtro[1][0], Filtro[1][1], Filtro[1][2] =  0,  0,   0 
        Filtro[2][0], Filtro[2][1], Filtro[2][2] = -1, -2,  -1
        yAplicado = convRet()

        G = np.sqrt(np.square(xAplicado) + np.square(yAplicado))
        
        Img_Processada = G*1
        cv2.imshow('ImageWindow', convertImg(Img_Processada))
        cv2.waitKey(0)
        Processada = True
    except:
      mesBox.showerror(title="", message="erro o Laplaciano")


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
        Convolucao()
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
        Convolucao()
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
        Convolucao()
    except:
       mesBox.showerror(title="", message="erro o Laplaciano")

def HighBoost():
    global Fsize
    global Processada
    global Img_Processada
    global Img_Original
    global Filtro
    #setup filtro
    try:
        Filtro = np.zeros((3,3), np.float16)
        Fsize = 3
        Filtro[0][0], Filtro[0][1], Filtro[0][2] =  -1, -1, -1
        Filtro[1][0], Filtro[1][1], Filtro[1][2] =  -1,  9, -1 
        Filtro[2][0], Filtro[2][1], Filtro[2][2] =  -1, -1, -1
        Convolucao()
    except:
       mesBox.showerror(title="", message="erro o Laplaciano")

def Mediana3():
    try:
        MedianaS(3)
    except:
        mesBox.showerror(title="", message="erro ao aplicar filtro")

def Mediana5():
    try:
        MedianaS(5)
    except:
        mesBox.showerror(title="", message="erro ao aplicar filtro")
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

##pega os HSV para o histograma
def MakeHue(img):
    arr = convertImg(img)
    l, c = img.shape[:2]
    hueArray = np.zeros((l*c), np.uint16)
    for i in range(l):
        for j in range(c):
            (b, g, r) = arr[i][j]
            h, s, v = getHSV(r, g, b)
            hueArray[i*c + j] = h

    return hueArray

def MakeSaturation(img):
    arr = convertImg(img)
    l, c = img.shape[:2]
    satArray = np.zeros((l*c), np.float32)
    for i in range(l):
        for j in range(c):
            (b, g, r) = arr[i][j]
            h, s, v = getHSV(r, g, b)
            satArray[i*c + j] = s

    return satArray

def MakeBrilho(img):
    arr = convertImg(img)
    l, c = img.shape[:2]
    brilArray = np.zeros((l*c), np.float32)
    for i in range(l):
        for j in range(c):
            (b, g, r) = arr[i][j]
            h, s, v = getHSV(r, g, b)
            brilArray[i*c + j] = v

    return brilArray

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

def HistogramaHSV(img):
    hueData   = pd.DataFrame(dict(Hue=np.array(MakeHue(img))))
    saturaData = pd.DataFrame(dict(Saturation=np.array(MakeSaturation(img))))
    brilhoData  = pd.DataFrame(dict(Value=np.array(MakeBrilho(img))))

    fig, axes = plt.subplots(1, 3)

    hueData.hist('Hue',     bins=256,  range=(0,360), color='red',   ax=axes[0])
    saturaData.hist('Saturation', bins=256,  range=(0,1), color='green', ax=axes[1])
    brilhoData.hist('Value',   bins=256,  range=(0,1), color='blue',  ax=axes[2])

    plt.show()

#mostrar histograma HSV
def ShowHistogramOHSV():
    try:
        HistogramaHSV(Img_Original)
    except:
        mesBox.showerror("Error", "Erro ao plotar histograma")

def ShowHistogramPHSV():
    try:
        HistogramaHSV(Img_Processada)
    except:
        mesBox.showerror("Error", "Erro ao plotar histograma")

#mostra histograma RGB
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

#transfomacoes
def pontoRotacionado(x, y, xc, yc, ang):
    xR = ((x-xc)*math.cos(math.radians(ang))) - ((y-yc)*math.sin(math.radians(ang))) +xc
    yR = ((x-xc)*math.sin(math.radians(ang))) + ((y-yc)*math.cos(math.radians(ang))) +xc
    return int(xR), int(yR)

def interpolar(img, x, y):
    # Obtenha os índices dos quatro cantos
    x1 = x
    y1 = y
    x2 = x1 + 1
    y2 = y1 + 1

    
    # se for a ultima coluna repita os valores
    l, c, cha = img.shape[:3]
    if x2 > c or y2 > l:
        return getPixel(img, x1, y1)

    # Calcule os pesos para cada canto
    q11b, q11g, q11r = getPixel(img, x1, y1)
    q21b, q21g, q21r = getPixel(img, x2, y1)
    q12b, q12g, q12r = getPixel(img, x1, y2)
    q22b, q22g, q22r = getPixel(img, x2, y2)

    # Interpolação bilinear
    valor_interpoladoR = q11r * (x2 - x) * (y2 - y) + \
                        q21r * (x - x1) * (y2 - y) + \
                        q12r * (x2 - x) * (y - y1) + \
                        q22r * (x - x1) * (y - y1)

    valor_interpoladoG = q11g * (x2 - x) * (y2 - y) + \
                        q21g * (x - x1) * (y2 - y) + \
                        q12g * (x2 - x) * (y - y1) + \
                        q22g * (x - x1) * (y - y1)
    
    valor_interpoladoB = q11b * (x2 - x) * (y2 - y) + \
                        q21b * (x - x1) * (y2 - y) + \
                        q12b * (x2 - x) * (y - y1) + \
                        q22b * (x - x1) * (y - y1)
    
    return valor_interpoladoB, valor_interpoladoG, valor_interpoladoR

def RotacionarNear(img, angle):
    l, c, cha = img.shape[:3]
    xcenter, ycenter = int(c/2), int(l/2)
    p1 = pontoRotacionado(0,0,xcenter, ycenter, angle)
    p2 = pontoRotacionado(c,0,xcenter, ycenter, angle)
    p3 = pontoRotacionado(c,l,xcenter, ycenter, angle)
    p4 = pontoRotacionado(0,l,xcenter, ycenter, angle)


    ymin = round(min(p1[1], p2[1], p3[1], p4[1]))
    xmin = round(min(p1[0], p2[0], p3[0], p4[0]))

    ymax = round(max(p1[1], p2[1], p3[1], p4[1]))
    xmax = round(max(p1[0], p2[0], p3[0], p4[0]))

    ln = ymax + abs(ymin)
    cn = xmax + abs(xmin)

    ImagemRotacionada = np.zeros((ln,cn, cha), np.float32)
    for i in range(ln):
        for j in range(cn):
            px, py = pontoRotacionado(j,i,xcenter, ycenter, -angle)
            (b, g, r) = getPixel(img, px, py)
            ImagemRotacionada[i][j] = (b, g, r)
    return ImagemRotacionada

def ScaleNear(scaleSize, img):
    l, c, cha = img.shape[:3]
    ln = l*round(scaleSize)
    cn = c*round(scaleSize)
    ImagemScalada = np.zeros((ln,cn, cha), np.float32)
    for i in range(ln):
        for j in range(cn):
            (b, g, r) = getPixel(img, round(j/round(scaleSize)), round(i/round(scaleSize)))
            ImagemScalada[i][j] = (b, g, r)
    return ImagemScalada

def ScaleLinear(scaleSize, img):
    l, c, cha = img.shape[:3]
    ln = l*round(scaleSize)
    cn = c*round(scaleSize)
    ImagemScalada = np.zeros((ln,cn, cha), np.float32)
    for i in range(ln):
        for j in range(cn):
            (b, g, r) = interpolar(img, round(j/round(scaleSize)), round(i/round(scaleSize)))
            ImagemScalada[i][j] = (b, g, r)
    return ImagemScalada

def Escalar():
    global Img_Original
    global Img_Processada
    global Processada
    global Carregado
    try:
        tipo = dialog.askstring("Input", "digite o tipo de escala a ser usada: L - linear | N - nearest")
        scaSize = dialog.askfloat("Input", "digite a escala:")
        if(tipo.lower() == "l"):
            Img_Processada = ScaleLinear(scaSize, Img_Original)
        elif(tipo.lower() == "n"):
            Img_Processada = ScaleNear(scaSize, Img_Original)
        
        Processada = True
        visualizarImgProcess()
    except:
        mesBox.showerror(title="", message="erro ao escalar")

#Tratamento de Cores
def ChromaKey():
    global Img_Original
    global Img_Processada
    global Processada
    global Carregado
    try:
        Img_Chroma = []
        distancia = dialog.askinteger("Input", "digite a distancia da cor verde:")
        #abri a imagem que substitui
        filetypes = (('image files', ('*.png', '*.bmp', '*.dib' , '*.jpeg', '*.jpg', '*.jpe', '*.jp2', '*.webp', '*.avif', '*.pbm', '*.pgm', '*.ppm', '*.pxm', '*.pnm', '*.pfm', '*.sr', '*.ras' , '*.tiff', '*.tif', '*.exr', '*.hdr', '*.pic')),
                 ("all files", '*.*'))
            #selecione o arquivo
        filepath = filedialog.askopenfilename(title="Abrir Imagem", initialdir="/", filetypes=filetypes)
        if(cv2.haveImageReader(filepath) == True):
            Img_Chroma = cv2.imread(filepath, 1)
        else:
            mesBox.showerror(title="Arquivo nao suportado", message="Arquivo nao suportado. \nPorfavor escolha um válido")
            return
        
        Img_Processada = Img_Original*1
        Img_Processada = np.float32(Img_Processada)
        l, c, cha = Img_Processada.shape[:3]
        for i in range(l):
            for j in range(c):
                bo, go, ro = getPixel(Img_Processada, j, i)
                if(go - ro >= distancia and go - bo >= distancia):
                    bn, gn, rn = getPixel(Img_Chroma, j, i)
                    Img_Processada[i][j] = (bn, gn, rn)
                    
        Processada = True
        visualizarImgProcess()
    except:
        mesBox.showerror(title="", message="erro ao criar Chroma")

def TratarCanalRGB():
    global Img_Original
    global Img_Processada
    global Processada
    global Carregado
    try:
        #abre uma janela com os valores para aumentar ou diminuir de R G B
        valR = dialog.askinteger("Input", "digite o valor para aumentar em R:")
        valG = dialog.askinteger("Input", "digite o valor para aumentar em G:")
        valB = dialog.askinteger("Input", "digite o valor para aumentar em B:")
        #adiciona os valores para a imagem original
        Img_Processada = Img_Original
        addImg(Img_Processada, valR, valG, valB)
        Processada = True
        visualizarImgProcess()
        #mostrar a imagem com os valores alterados
    except:
        mesBox.showerror(title="", message="erro ao Tratar Canal")

def TratarCanalCMY():
    global Img_Original
    global Img_Processada
    global Processada
    global Carregado
    try:
        #abre uma janela com os valores para aumentar ou diminuir de R G B
        valC = dialog.askinteger("Input", "digite o valor para aumentar em C (-100 a 100):")
        valM = dialog.askinteger("Input", "digite o valor para aumentar em M (-100 a 100):")
        valY = dialog.askinteger("Input", "digite o valor para aumentar em Y (-100 a 100):")
        #adiciona os valores para a imagem original
        Img_Processada = convertImg(Img_Original)
        valR, valG, valB = getRGB_CMY((valC/100), (valM/100), (valY/100), 0)
        addImg(Img_Processada, valR, valG, valB)
        Processada = True
        visualizarImgProcess()
        #mostrar a imagem com os valores alterados
    except:
        mesBox.showerror(title="", message="erro ao Tratar Canal")

def TratarMSB():
    global Img_Original
    global Img_Processada
    global Processada
    global Carregado
    try:
        #abre uma janela com os valores para aumentar ou diminuir de R G B
        valM = dialog.askinteger("Input", "digite o valor para alterar na matriz:")
        valS = dialog.askfloat("Input", "digite o valor para alterar na saturacao:")
        valB = dialog.askfloat("Input", "digite o valor para alterar no brilho:")
        #adiciona os valores para a imagem original
        Img_Processada = convertImg(Img_Original)
        addImgHSV(Img_Processada, valM, valS, valB )
        Processada = True
        visualizarImgProcess()
        #mostrar a imagem com os valores alterados
    except:
        mesBox.showerror(title="", message="erro ao Tratar Canal")

def recuperar_imagem(imagem_espectro):
    # Aplicar a Transformada Inversa de Fourier
    imagem_recuperada = np.fft.ifft2(imagem_espectro)

    # A imagem recuperada pode ter componentes complexos devido à transformação inversa
    # Portanto, pegamos apenas a parte real da imagem
    imagem_recuperada = np.real(imagem_recuperada)

    return imagem_recuperada

def rgb_para_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def draw(event):
    global pen_intensity
    global pen_size
    global canvas
    color = rgb_para_hex(pen_intensity, pen_intensity, pen_intensity)
    x1, y1 = (event.x - pen_size), (event.y - pen_size) 
    x2, y2 = (event.x + pen_size), (event.y + pen_size) 
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline='')

def Aplicar():
    global canvas
    global wi
    global hi
    canvas.update()
    canvas.postscript(file='canvas.ps', colormode='color')

    img = Image.open('canvas.ps')
    img = img.resize((wi, hi), Image.Resampling.BILINEAR)

    img = np.fft.ifftshift(img)
    ImagemOr = recuperar_imagem(np.array(img))
    
    cv2.imshow("array", ImagemOr)
    cv2.waitKey(0)
    

#Criacao e edicao de fourier
def Fourrier():
    #abre Janela
    global Img_Original
    global Img_Processada
    global editWidow
    global icone
    global pen_size
    global pen_intensity
    global fourrier_Img
    global Img_edit
    global canvas
    global wi
    global hi
    #variaveis
    fourrier_Img = []
    Img_edit = []
    pen_size = 5
    pen_intensity = 255

    #window config
    editWidow = tk.Toplevel()
    editWidow.resizable(False, False)
    editWidow.geometry('1280x720')
    editWidow.title("Fourrier")
    editWidow.config(background="#22c995")
    #frames
    editFrame = tk.Frame(editWidow, width=280, height=720, bg="white")
    editFrame.pack(side="left", fill="y")
    
    canvas =tk.Canvas(editWidow, width=800, height=700)
    canvas.pack()
    canvas.place(x=780, y=360, anchor=CENTER)
    
    
    #botao aplicar
    Img_edit = cv2.cvtColor(Img_Original, cv2.COLOR_BGR2GRAY)
    
    # Aplique a Transformada de Fourier 2D usando np.fft.fft2
    fft_imagem = np.fft.fft2(Img_edit)

    # Para visualizar o espectro de frequência, você pode fazer o seguinte:
    fft_imagem_shift = np.fft.fftshift(fft_imagem)

    imag = np.abs(fft_imagem_shift)
    imag = (imag / np.max(imag) * 255).astype(np.uint8)

    imagem_pil = Image.fromarray(imag)
    wi, hi = imagem_pil.width, imagem_pil.height
    
    imagem_pil = imagem_pil.resize((800, 700), Image.Resampling.BILINEAR)
    photo = ImageTk.PhotoImage(imagem_pil)
    
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    canvas.bind("<B1-Motion>", draw)
    

    color_button = tk.Button(editFrame, text="Color", command=Aplicar)
    color_button.pack(pady=15, padx=10)

    size_button = tk.Button(editFrame, text="Color", command=Aplicar)
    size_button.pack(pady=15, padx=10)

    salvar_button = tk.Button(editFrame, text="Aplicar", command=Aplicar)
    salvar_button.pack(pady=15, padx=10)

    editWidow.mainloop()

def AplicarFourrier():
    #abre Janela
    global Img_Original
    global Img_Processada
    global fourrier_Img

#conteudo
def getPB(Img, x, y):
    l, c = Img.shape[:2]
    if(x >= c) or (x < 0) or (y < 0) or (y >= l):
        return 255
    else:
        b, g, r = Img[y][x]
        return b
    
def comparar(i, j):
    return int((i == 0 and j == 255))

def A(Img, x, y):
    contador = 0
    p2 = getPB(Img, x, y-1)
    p3 = getPB(Img, x+1, y-1)
    p4 = getPB(Img, x+1, y)
    p5 = getPB(Img, x+1, y+1)
    p6 = getPB(Img, x, y+1)
    p7 = getPB(Img, x-1, y+1)
    p8 = getPB(Img, x-1, y)
    p9 = getPB(Img, x-1, y-1)
    contador += comparar(p2, p3) + comparar(p3, p4) + comparar(p4, p5) + comparar(p5, p6) + comparar(p6, p7) + comparar(p7, p8) + comparar(p8, p9) + comparar(p9, p2) 
    return contador

def B(Img, x, y):
    contador = 0
    pontos = []
    pontos.append(getPB(Img, x, y-1))
    pontos.append(getPB(Img, x+1, y-1))
    pontos.append(getPB(Img, x+1, y))
    pontos.append(getPB(Img, x+1, y+1))
    pontos.append(getPB(Img, x, y+1))
    pontos.append(getPB(Img, x-1, y+1))
    pontos.append(getPB(Img, x-1, y))
    pontos.append(getPB(Img, x-1, y-1))

    for i in pontos:
        if(i == 0):
            contador += 1

    return contador

def p246(Img, x, y):
    p2 = getPB(Img, x, y-1)
    p4 = getPB(Img, x+1, y)
    p6 = getPB(Img, x, y+1)
    return(p2 == 255 or p4 == 255 or p6 == 255)

def p468(Img, x, y):
    p4 = getPB(Img, x+1, y)
    p6 = getPB(Img, x, y+1)
    p8 = getPB(Img, x-1, y)
    return(p4 == 255 or p6 == 255 or p8 == 255)

def p248(Img, x, y):
    p2 = getPB(Img, x, y-1)
    p4 = getPB(Img, x+1, y)
    p8 = getPB(Img, x-1, y)
    return(p2 == 255 or p4 == 255 or p8 == 255)

def p268(Img, x, y):
    p2 = getPB(Img, x, y-1)
    p6 = getPB(Img, x, y+1)
    p8 = getPB(Img, x-1, y)
    return(p2 == 255 or p8 == 255 or p6 == 255)

def passo1(Img):
    modificado = False
    w, h, c = Img.shape[:3]
    Img_Retorno = np.zeros((w, h, c), np.uint8)
    for i in range(w):
        for j in range(h):
         (b, g, r) = Img[i][j]
         if(b == 0 and (A(Img, j, i) == 1) and (B(Img, j, i) >= 2 and B(Img, j, i) <= 6) and p246(Img, j, i) == True and p468(Img, j, i) == True):
            Img_Retorno[i][j] = (255, 255, 255)
            modificado = True
         else:
             Img_Retorno[i][j] = Img[i][j]

    return modificado, Img_Retorno

def passo2(Img):
    modificado = False
    w, h, c = Img.shape[:3]
    Img_Retorno = np.zeros((w, h, c), np.uint8)
    for i in range(w):
        for j in range(h):
         (b, g, r) = Img[i][j]
         if(b == 0 and (A(Img, j, i) == 1) and (B(Img, j, i) >= 2 and B(Img, j, i) <= 6) and p248(Img, j, i) == True and p268(Img, j, i) == True):
            Img_Retorno[i][j] = (255, 255, 255)
            modificado = True
         else:
             Img_Retorno[i][j] = Img[i][j]

    return modificado, Img_Retorno
    

def Zhang_Suen(Img):
    k = 0
    while True:
        print(f"iteracao: {k}")
        #passo 1
        p1, Img = passo1(Img)
        print("passo 1 -> feito")
        #passo 2
        p2, Img = passo2(Img)
        print("passo 2 -> feito")
        k += 1
        if(p1 == False and p2 == False):
            print("Terminado")
            return Img
    


def EsqueletoGray():
    global Processada
    global Img_Processada
    global Img_Original
    try:
        Img_Processada = GrayScaleK(Img_Original)
        Img_Processada = limiarizarK(Img_Processada, 100)
        Img_Processada = inverter(Img_Processada)
        cv2.imshow('ImageWindow', Img_Processada)
        cv2.waitKey(0)
        Img_Processada = Zhang_Suen(Img_Processada)
        cv2.imshow('ImageWindow', Img_Processada)
        cv2.waitKey(0)
    except:
        mesBox.showerror(title="", message="erro")

def EsqueletoBin():
    global Processada
    global Img_Processada
    global Img_Original
    try:
        branco = dialog.askstring("Input", "Os objetos da imagem estao branco ?(s/n)")
        if(branco.lower() == "s"):
            Img_Processada = inverter(Img_Processada)
            Img_Processada = limiarizarK(Img_Processada, 100)
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
        else:
            Img_Processada = limiarizarK(Img_Original, 100)
            cv2.imshow('ImageWindow', Img_Processada)
            cv2.waitKey(0)
        Img_Processada = Zhang_Suen(Img_Processada)
        cv2.imshow('ImageWindow', Img_Processada)
        cv2.waitKey(0)
    except:
        mesBox.showerror(title="", message="erro")

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
    viewMenu.add_command(label="process  img", command=visualizarImgProcess)
    viewMenu.add_command(label="lado a lado", command=visualizarLadoALado)
    
    editMenu = Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label="Edit",menu=editMenu)
    editMenu.add_command(label="Fourier", command=Fourrier)
    editMenu.add_command(label="Negativo", command=negativo)
    editMenu.add_command(label="Logaritmo", command=logaritmoRGB)
    editMenu.add_command(label="Gamma", command=correcaoGamaRGB)
    editMenu.add_command(label="EsqueletoGray", command=EsqueletoGray)
    editMenu.add_command(label="EsqueletoBin", command=EsqueletoBin)

    editMenu.add_separator()
    editMenu.add_command(label="Gray Simple", command=GrayScale)
    editMenu.add_command(label="Gray Ponderada", command=GrayScaleAprim)
    editMenu.add_command(label="Sepia", command=Sepia)
    editMenu.add_separator()

    editMenu.add_command(label="Chroma Key", command=ChromaKey)
    editMenu.add_command(label="Ajuste Canal RGB", command=TratarCanalRGB)
    editMenu.add_command(label="Ajuste Canal CMY", command=TratarCanalCMY)
    editMenu.add_command(label="Ajuste M, S, B", command=TratarMSB)

    #transformacoes
    transformMenu = Menu(editMenu, tearoff=0)
    barraMenu.add_cascade(label="Transformacoes", menu=transformMenu)
    transformMenu.add_command(label="Escala", command=Escalar)


    #filtro
    filtroMenu = Menu(editMenu, tearoff=0)
    barraMenu.add_cascade(label="Filtro", menu=filtroMenu)
    filtroMenu.add_command(label="Media", command=Media)
    filtroMenu.add_command(label="Ponderada", command=Ponderada)
    filtroMenu.add_command(label="Mediana 3x3", command=Mediana3)
    filtroMenu.add_command(label="Mediana 5x5", command=Mediana5)
    filtroMenu.add_command(label="Convolucao", command=Convolucao)
    filtroMenu.add_command(label="Laplaciano", command=Laplaciano)
    filtroMenu.add_command(label="High Boost", command=HighBoost)
    filtroMenu.add_command(label="Sobel", command=Sobel)
    #cria filtros
    criafiltroMenu = Menu(filtroMenu, tearoff=0)
    filtroMenu.add_cascade(label="Cria Filtro", menu=criafiltroMenu)
    #3x3
    criafiltroMenu.add_command(label="Cria Filtro 3", command=criaFiltro3)
    #5x5
    criafiltroMenu.add_command(label="Cria Filtro 5", command=criaFiltro5)
    #7x7
    criafiltroMenu.add_command(label="Cria Filtro 7", command=criaFiltro7)
    #9x9
    criafiltroMenu.add_command(label="Cria Filtro 9", command=criaFiltro9)

    
    #histograma
    editMenu.add_separator()
    histMenu = Menu(editMenu, tearoff=0)
    editMenu.add_cascade(label="Histograma", menu=histMenu)
    histMenu.add_command(label="Histograma Original canal R", command=ShowHistogramOR)
    histMenu.add_command(label="Histograma Original canal G", command=ShowHistogramOG)
    histMenu.add_command(label="Histograma Original canal B", command=ShowHistogramOB)
    histMenu.add_command(label="Histograma Original HSV", command=ShowHistogramOHSV)
    histMenu.add_command(label="Histograma Original canal RGB", command=ShowHistogramORGB)
    histMenu.add_separator()

    #HISTOGRAMA IMAGEM PROCESSADA
    histMenu.add_command(label="Histograma Processada canal R", command=ShowHistogramPR)
    histMenu.add_command(label="Histograma Processada canal G", command=ShowHistogramPG)
    histMenu.add_command(label="Histograma Processada canal B", command=ShowHistogramPB)
    histMenu.add_command(label="Histograma Processada HSV", command=ShowHistogramPHSV)
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
    initWindow()
    initContent()
    window.mainloop()
    #Fourrier()

   
        
