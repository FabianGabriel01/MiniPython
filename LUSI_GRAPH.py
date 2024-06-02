import pygame_gui
import pygame
import os
from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
from datetime import datetime
import pandas as Pnds
from fpdf import FPDF
import numpy as np
import matplotlib.ticker as tkr

#region INITIALIZATION

pygame.init()
size = (1920, 1080)  # Width, Height
#screen = pygame.display.set_mode(size)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen.fill("black")
pygame.display.set_caption("LUSI GRAPH")
#endregion

#region ReadKeyActivation
KeyText = "ASKKFGY2347592"
ReadKey = open("LogUser.txt", 'r+')
StrKeyActivacion = ""
bFirstTime = True
#endregion


#IMPORTACION DE IMAGENES/GUARDADO DE ARCHIVOS .PDF
#region import IMAGE
LOGOPdf = ''
def openFile():
    filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                          title="Selecciona tu LOGO correspondiente!",
                                          filetypes= (("images","*.png"),
                                          ("all files","*.*")))
    
    if filepath != '':
        print(filepath)
        with open("ConfigFILE.txt", 'a') as R:
            R.seek(0,1)
            R.write('\n' + filepath)
        return filepath
    else:
        print("Archivo NO Abierto")


            
# Create a list to store the values 
C0 = []
C1 = []

C0Energ = []
C1Energ = []

#PARA TEMPERATURA
FechaDesplegableTemp = ["Fecha"]
FechaDesplegableEnerg = ["Fecha"]
returnedFileTemp = ""
returnedFileEnerg = ""
DLocFinTemp = []
DLocFinEnerg = []

# def OpenExample():
#     filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
#                                           title="Select excel file?",
#                                           filetypes= (("files","*.csv"),
#                                           ("all files","*.*")))
    
#     File1 = Pnds.read_csv(filepath, sep="\t")   
#     print(File1)


def OpenCSVTemp():
    filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                          title="Select excel file?",
                                          filetypes= (("files","*.csv"),
                                          ("all files","*.*")))

    File_Excel = Pnds.read_csv(filepath, sep="\t", encoding="utf-16")

    File_Excel.fillna(0, inplace= True)

    File_Excel.iloc[:,1] = Pnds.to_datetime(File_Excel.iloc[:,1]).dt.date
            #File_Excel.iloc[:,1] = File_Excel.iloc[:,1].dt.date
    D = ""
    Dloc = 0
    FechaDesplegableTemp.clear()
    for Z in File_Excel.iloc[:,1]:
        Dloc+=1
        if Z != D:
            FechaDesplegableTemp.append(str(Z))
            DLocFinTemp.append(Dloc)
        D = Z
    DLocFinTemp.append(Dloc)

    List_FechasTemp.options_list = FechaDesplegableTemp
    List_FechasTemp.selected_option = FechaDesplegableTemp[0]

    ShowDatePlotTemp(File_Excel, DLocFinTemp, 1, 0, TypeGraphTemp)

    return File_Excel


def OpenCSVEnerg():
    filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                          title="Select excel file?",
                                          filetypes= (("files","*.csv"),
                                          ("all files","*.*")))
    
    if filepath == "":
        return
    else:
        try:

            File_Excel = Pnds.read_csv(filepath, encoding="utf-16", sep="\t")

            File_Excel.fillna(0, inplace= True)

            File_Excel.iloc[:,1] = Pnds.to_datetime(File_Excel.iloc[:,1]).dt.date
            #File_Excel.iloc[:,1] = File_Excel.iloc[:,1].dt.date
            D = ""
            Dloc = 0
            FechaDesplegableEnerg.clear()
            for Z in File_Excel.iloc[:,1]:
                Dloc+=1
                if Z != D:
                    FechaDesplegableEnerg.append(str(Z))
                    DLocFinEnerg.append(Dloc)
                D = Z
            DLocFinEnerg.append(Dloc)

            List_FechasEnerg.options_list = FechaDesplegableEnerg
            List_FechasEnerg.selected_option = FechaDesplegableEnerg[0]

            ShowDatePlotEnerg(File_Excel, DLocFinEnerg, 1, 0, TypeGraphEnerg)

            return File_Excel
        except:
            print("Formato NO COMPATIBLE")
            


MaxTempTxt1 = 0
MinTempTxt1 = 0
ScatterSizeTxt = 1

MaxEnergTxt1 = 0
MinEnergTxt1 = 0
ScatterSizeEnergTxt = 1

ListHorasTemp = ["Hora"]
ListHorasValuesTemp = ["0"]
UpdateC0Temp = []
UpdateC1Temp = []
NListHoursTemp = []

ListHorasEnerg = ["Hora"]
ListHorasValuesEnerg = ["0"]
UpdateC0Energ = []
UpdateC1Energ = []
NListHoursEnerg = []

C2Temp = []
C3Temp = []

C4Temp = []
C5Temp = []

C2Energ = []
C3Energ = []

C4Energ = []
C5Energ = []

GraphUpTemp = "GraphUpdateTemp.png"
GraphUpEnerg = "GraphUpdateEnerg.png"


ResAvrg = []

def ShowDatePlotTemp(DataFrame_File, List0, N, S, TypeG):
    
    C1.clear()
    C0.clear()

    i1 = List0[S]
    i2 = List0[S]

    Sum = 0
    Avrg = 0

    ListHorasTemp.clear()
    ListHorasValuesTemp.clear()
    ListHorasValuesTemp.append("0")
    NListHoursTemp.clear()
    ResAvrg.clear()

    for A in range(i1, List0[N]):
        C0.append(DataFrame_File.iloc[A,0])
        
    
    for B in range(i2, List0[N]):
        C1.append(DataFrame_File.iloc[B,2])
        Sum = Sum + int(DataFrame_File.iloc[B,2])

    print(Sum)
    Avrg = len(C1)
    print(Avrg)
    ResAvrg.append((Sum/Avrg)/10)

    C1[:] = [x / 10 for x in C1]
    A = ""
    Ab = 0
    for K in C0:
        timer = datetime.strptime(K, '%H:%M:%S')
        Ab+=1
        if A != timer.hour and A != '':
            ListHorasTemp.append(str(A))
            ListHorasValuesTemp.append(str(Ab))
        A = timer.hour


    C3Temp.clear()
    C3Temp.append(int(MaxTempTxt1))
    C3Temp.append(int(MaxTempTxt1))

    C2Temp.clear()
    C2Temp.append(int(0))
    C2Temp.append(int(ListHorasValuesTemp[-1]))

    C5Temp.clear()
    C5Temp.append(int(MinTempTxt1))
    C5Temp.append(int(MinTempTxt1))

    C4Temp.clear()
    C4Temp.append(int(0))
    C4Temp.append(int(ListHorasValuesTemp[-1]))
    
    for L in range(0, len(ListHorasTemp)):
        NListHoursTemp.append(L)

    ListaHorasDiponiblesStartTemp.options_list = ListHorasTemp
    ListaHorasDiponiblesEndTemp.options_list = ListHorasTemp

    ListaHorasDiponiblesStartTemp.selected_option = str(ListHorasTemp[0])
    ListaHorasDiponiblesEndTemp.selected_option = str(ListHorasTemp[len(ListHorasTemp) - 1])

    
    if TypeG == "Linear":
        plt.figure(figsize=(15,9))
        plt.xlabel('Hora')
        plt.grid(True)
        plt.ylabel('Temperatura')
        plt.plot(C0, C1, label = "Temperatura", color = LineColorTemp1Text)
        plt.plot(C2Temp, C3Temp, label="Temperatura Maxima", color = 'r')
        plt.plot(C4Temp, C5Temp, label="Temperatura Minima", color = 'g')
        plt.legend()
        

        locator = mdates.AutoDateLocator(minticks=12, maxticks=24)
        plt.gcf().axes[0].xaxis.set_major_locator(locator)
        #plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
        #plt.gcf().axes[0].set_xlim(str(FechaDesplegableTemp[0]) + ' 00:00', str(FechaDesplegableTemp[0]) +' 23:59')

        #plt.gcf().axes[0].set_xlim(0, 24*3600)
        #plt.gcf().axes[0].xaxis.set_major_locator(tkr.MultipleLocator(3600))

        plt.gcf().autofmt_xdate()
        plot_stream = io.BytesIO()
        plt.savefig(GraphUpTemp)
        plt.savefig(plot_stream)
        plot_stream.seek(0)
        plot_surface = pygame.image.load(plot_stream, 'PNG')
        Panel_Temp.set_image(plot_surface)


    if TypeG == "Puntos":
        plt.figure(figsize=(15,9))
        plt.xlabel('Hora')
        plt.ylabel('Temperatura')
        plt.scatter(C0, C1, color = PointColor1TempText, s=ScatterSizeTxt)
        plt.plot(C2Temp, C3Temp, label="Temperatura Maxima", color = 'r')
        plt.plot(C4Temp, C5Temp, label="Temperatura Minima", color = 'g')
        plt.legend()
        plot_stream = io.BytesIO()
        plt.savefig(GraphUpTemp)
        plt.savefig(plot_stream)
        plot_stream.seek(0)
        plot_surface = pygame.image.load(plot_stream, 'PNG')
        Panel_Temp.set_image(plot_surface)
    
    if TypeG == "Combinado":
        plt.figure(figsize=(15,9))
        plt.xlabel('Hora')
        plt.ylabel('Temperatura')
        plt.plot(C0, C1, label = "Temperatura", color = LineColorTemp1Text)
        plt.plot(C2Temp, C3Temp, label="Temperatura Maxima", color = 'r')
        plt.plot(C4Temp, C5Temp, label="Temperatura Minima", color = 'g')
        plt.legend()
        plt.scatter(C0, C1, color = PointColor1TempText, s=ScatterSizeTxt)
        plot_stream = io.BytesIO()
        plt.savefig(GraphUpTemp)
        plt.savefig(plot_stream)
        plot_stream.seek(0)
        plot_surface = pygame.image.load(plot_stream, 'PNG')
        Panel_Temp.set_image(plot_surface)

    plt.show()
    WND_Temp.show()

def ShowDatePlotEnerg(DataFrame_File, List0, N, S, TypeG):
    
    C1Energ.clear()
    C0Energ.clear()

    i1 = List0[S]
    i2 = List0[S]

    Sum = 0
    Avrg = 0

    ListHorasEnerg.clear()
    ListHorasValuesEnerg.clear()
    ListHorasValuesEnerg.append("0")
    NListHoursEnerg.clear()
    ResAvrg.clear()

    for A in range(i1, List0[N]):
        C0Energ.append(DataFrame_File.iloc[A,0])
        
    
    for B in range(i2, List0[N]):
        C1Energ.append(DataFrame_File.iloc[B,2])
        Sum = Sum + int(DataFrame_File.iloc[B,2])

    print(Sum)
    Avrg = len(C1Energ)
    print(Avrg)
    ResAvrg.append((Sum/Avrg)/10)

    C1Energ[:] = [x / 10 for x in C1Energ]
    A = ""
    Ab = 0
    for K in C0Energ:
        timer = datetime.strptime(K, '%H:%M:%S')
        Ab+=1
        if A != timer.hour and A != '':
            ListHorasEnerg.append(str(A))
            ListHorasValuesEnerg.append(str(Ab))
        A = timer.hour

    C3Energ.clear()
    C3Energ.append(int(MaxEnergTxt1))
    C3Energ.append(int(MaxEnergTxt1))

    C2Energ.clear()
    C2Energ.append(int(0))
    C2Energ.append(int(ListHorasValuesEnerg[-1]))

    C5Energ.clear()
    C5Energ.append(int(MinEnergTxt1))
    C5Energ.append(int(MinEnergTxt1))

    C4Energ.clear()
    C4Energ.append(int(0))
    C4Energ.append(int(ListHorasValuesEnerg[-1]))
    
    for L in range(0, len(ListHorasTemp)):
        NListHoursEnerg.append(L)

    ListaHorasDiponiblesStartEnerg.options_list = ListHorasEnerg
    ListaHorasDiponiblesEndEnerg.options_list = ListHorasEnerg

    ListaHorasDiponiblesStartEnerg.selected_option = str(ListHorasEnerg[0])
    ListaHorasDiponiblesEndEnerg.selected_option = str(ListHorasEnerg[len(ListHorasEnerg) - 1])

    
    if TypeG == "Linear":
        plt.figure(figsize=(15,9))
        plt.xlabel('Hora')
        plt.ylabel('Conductividad')
        plt.plot(C0Energ, C1Energ, label = "Conductividad", color = LineColorEnerg1Text, markevery = 100)
        plt.plot(C2Energ, C3Energ, label="Conductividad Maxima", color = 'r')
        plt.plot(C4Energ, C5Energ, label="Conductividad Minima", color = 'g')
        plt.legend()
        plot_stream = io.BytesIO()
        plt.savefig(GraphUpEnerg)
        plt.savefig(plot_stream)
        plot_stream.seek(0)
        plot_surface = pygame.image.load(plot_stream, 'PNG')
        Panel_Energ.set_image(plot_surface)


    if TypeG == "Puntos":
        plt.figure(figsize=(15,9))
        plt.xlabel('Hora')
        plt.ylabel('Conductividad')
        plt.scatter(C0Energ, C1Energ, color = PointColor1TempText, s=ScatterSizeTxt)
        plt.plot(C2Energ, C3Energ, label="Conductividad Maxima", color = 'r')
        plt.plot(C4Energ, C5Energ, label="Conductividad Minima", color = 'g')
        plt.legend()
        plot_stream = io.BytesIO()
        plt.savefig(GraphUpEnerg)
        plt.savefig(plot_stream)
        plot_stream.seek(0)
        plot_surface = pygame.image.load(plot_stream, 'PNG')
        Panel_Energ.set_image(plot_surface)
    
    if TypeG == "Combinado":
        plt.figure(figsize=(15,9))
        plt.xlabel('Hora')
        plt.ylabel('Conductividad')
        plt.plot(C0Energ, C1Energ, label = "Conductividad", color = LineColorTemp1Text)
        plt.plot(C2Energ, C3Energ, label="Conductividad Maxima", color = 'r')
        plt.plot(C4Energ, C5Energ, label="Conductividad Minima", color = 'g')
        plt.legend()
        plt.scatter(C0Energ, C1Energ, color = PointColor1EnergText, s=ScatterSizeEnergTxt)
        plot_stream = io.BytesIO()
        plt.savefig(GraphUpEnerg)
        plt.savefig(plot_stream)
        plot_stream.seek(0)
        plot_surface = pygame.image.load(plot_stream, 'PNG')
        Panel_Energ.set_image(plot_surface)

    plt.show()
    WND_Energ.show()

    


def UpdatePlotTemp(C0, C1, Min, Max, TypeG):
    UpdateC0Temp.clear()
    UpdateC1Temp.clear()

    for C in range(Min, Max):
        UpdateC0Temp.append(C0[C])
        UpdateC1Temp.append(C1[C])

    Result = Max - Min
    

    C3Temp.clear()
    C3Temp.append(int(MaxTempTxt1))
    C3Temp.append(int(MaxTempTxt1))

    C2Temp.clear()
    C2Temp.append(int(0))
    C2Temp.append(int(Result))

    C5Temp.clear()
    C5Temp.append(int(MinTempTxt1))
    C5Temp.append(int(MinTempTxt1))

    C4Temp.clear()
    C4Temp.append(int(0))
    C4Temp.append(int(Result))


    if TypeG == "Linear":
        plt.figure(figsize=(15,9))
        plt.xlabel('Hora')
        plt.ylabel('Temperatura')
        plt.plot(UpdateC0Temp, UpdateC1Temp, label = "Temperatura", color = LineColorTemp1Text)
        plt.plot(C2Temp, C3Temp, label="Temperatura Maxima", color = 'r')
        plt.plot(C4Temp, C5Temp, label="Temperatura Minima", color = 'black')
        plt.legend()
        plot_stream = io.BytesIO()
        plt.savefig(GraphUpTemp)
        plt.savefig(plot_stream)
        plot_stream.seek(0)
        plot_surface = pygame.image.load(plot_stream, 'PNG')
        Panel_Temp.set_image(plot_surface)

    if TypeG == "Puntos":
        plt.figure(figsize=(15,9))
        plt.xlabel('Hora')
        plt.ylabel('Temperatura')
        plt.scatter(UpdateC0Temp, UpdateC1Temp, color = PointColor1TempText, s=ScatterSizeTxt)
        plt.plot(C2Temp, C3Temp, label="Temperatura Maxima", color = 'r')
        plt.plot(C4Temp, C5Temp, label="Temperatura Minima", color = 'black')
        plt.legend()
        plot_stream = io.BytesIO()
        plt.savefig(GraphUpTemp)
        plt.savefig(plot_stream)
        plot_stream.seek(0)
        plot_surface = pygame.image.load(plot_stream, 'PNG')
        Panel_Temp.set_image(plot_surface)

    if TypeG == "Combinado":
        plt.figure(figsize=(15,9))
        plt.xlabel('Hora')
        plt.ylabel('Temperatura')
        plt.plot(UpdateC0Temp, UpdateC1Temp, label = "Temperatura", color = LineColorTemp1Text)
        plt.plot(C2Temp, C3Temp, label="Temperatura Maxima", color = 'r')
        plt.plot(C4Temp, C5Temp, label="Temperatura Minima", color = 'black')
        plt.legend()
        plt.scatter(UpdateC0Temp, UpdateC1Temp, color = PointColor1TempText, s=ScatterSizeTxt)
        plot_stream = io.BytesIO()
        plt.savefig(GraphUpTemp)
        plt.savefig(plot_stream)
        plot_stream.seek(0)
        plot_surface = pygame.image.load(plot_stream, 'PNG')
        Panel_Temp.set_image(plot_surface)

    plt.show()
    
    

def UpdatePlotEnerg(C0, C1, Min, Max, TypeG):
    UpdateC0Energ.clear()
    UpdateC1Energ.clear()

    for C in range(Min, Max):
        UpdateC0Energ.append(C0[C])
        UpdateC1Energ.append(C1[C])

    Result = Max - Min
    ReturnEnergAvgr(Max, Min)

    C3Energ.clear()
    C3Energ.append(int(MaxEnergTxt1))
    C3Energ.append(int(MaxEnergTxt1))

    C2Energ.clear()
    C2Energ.append(int(0))
    C2Energ.append(int(Result))

    C5Energ.clear()
    C5Energ.append(int(MinEnergTxt1))
    C5Energ.append(int(MinEnergTxt1))

    C4Energ.clear()
    C4Energ.append(int(0))
    C4Energ.append(int(Result))


    if TypeG == "Linear":
        plt.figure(figsize=(15,9))
        plt.xlabel('Hora')
        plt.ylabel('Conductividad')
        plt.plot(UpdateC0Energ, UpdateC1Energ, label = "Conductividad", color = LineColorEnerg1Text)
        plt.plot(C2Energ, C3Energ, label="Conductividad Maxima", color = 'r')
        plt.plot(C4Energ, C5Energ, label="Conductividad Minima", color = 'black')
        plt.legend()
        plot_stream = io.BytesIO()
        plt.savefig(GraphUpEnerg)
        plt.savefig(plot_stream)
        plot_stream.seek(0)
        plot_surface = pygame.image.load(plot_stream, 'PNG')
        Panel_Energ.set_image(plot_surface)

    if TypeG == "Puntos":
        plt.figure(figsize=(15,9))
        plt.xlabel('Hora')
        plt.ylabel('Conductividad')
        plt.scatter(UpdateC0Energ, UpdateC1Energ, color = PointColor1EnergText, s=ScatterSizeEnergTxt)
        plt.plot(C2Energ, C3Energ, label="Conductividad Maxima", color = 'r')
        plt.plot(C4Energ, C5Energ, label="Conductividad Minima", color = 'black')
        plt.legend()
        plot_stream = io.BytesIO()
        plt.savefig(GraphUpEnerg)
        plt.savefig(plot_stream)
        plot_stream.seek(0)
        plot_surface = pygame.image.load(plot_stream, 'PNG')
        Panel_Energ.set_image(plot_surface)

    if TypeG == "Combinado":
        plt.figure(figsize=(15,9))
        plt.xlabel('Hora')
        plt.ylabel('Conductividad')
        plt.plot(UpdateC0Energ, UpdateC1Energ, label = "Conductividad", color = LineColorTemp1Text)
        plt.plot(C2Energ, C3Energ, label="Conductividad Maxima", color = 'r')
        plt.plot(C4Energ, C5Energ, label="Conductividad Minima", color = 'black')
        plt.legend()
        plt.scatter(UpdateC0Energ, UpdateC1Energ, color = PointColor1EnergText, s=ScatterSizeEnergTxt)
        plot_stream = io.BytesIO()
        plt.savefig(GraphUpEnerg)
        plt.savefig(plot_stream)
        plot_stream.seek(0)
        plot_surface = pygame.image.load(plot_stream, 'PNG')
        Panel_Energ.set_image(plot_surface)

    plt.show()
    
def ReturnTempAvgr(Min, Max):
    Res = Max - Min
    return Res

def ReturnEnergAvgr(Min , Max):
    Res = Max - Min
    return Res
    
    



#region FPS CONTROLLER and RUN TIME CLOCK
#Set FRAME RATE INDEPENDENCY
Clock = pygame.time.Clock()
#endregion


#region UIController
# UI CLASS FOR JUST HIDING WINDOWS
class MyHidingWindow(pygame_gui.elements.UIWindow):
    def on_close_window_button_pressed(self):
        self.hide()

#PANEL PRINCIPAL    
Manager = pygame_gui.UIManager(size)


PasswordPanel = pygame_gui.elements.UIPanel(pygame.Rect(600,200, 600,500), manager=Manager)
PassText1 = pygame_gui.elements.UILabel(pygame.Rect(150,10 ,300,50), manager=Manager, text="Activacion De Producto DCA", container=PasswordPanel, parent_element=PasswordPanel)
PassText2 = pygame_gui.elements.UITextEntryLine(pygame.Rect(150,100 ,300,50), manager=Manager, container=PasswordPanel, parent_element=PasswordPanel)
BTNPass1 = pygame_gui.elements.UIButton(pygame.Rect(150, 190, 100,50), manager=Manager, container=PasswordPanel, parent_element=PasswordPanel, text="Activar")
BTNPass2 = pygame_gui.elements.UIButton(pygame.Rect(350, 190, 100,50), manager=Manager, container=PasswordPanel, parent_element=PasswordPanel, text="Cerrar")
#PanelIntro = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,75), (1800,1000)), manager=Manager)
SliderUI = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((10,10),(135,140)), manager=Manager)
SliderUI.hide()

LOGO = pygame.image.load('logo.png')
OnlineIMG = pygame_gui.elements.UIImage(relative_rect= pygame.Rect((450,150), (1000,800)), manager=Manager, image_surface=LOGO)

FTempo = 1.0
BTN_Temp =  pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 10), (130,30)),
                                        manager=Manager, object_id="BTN_Temp", text="Temperatura", container=SliderUI, parent_element=SliderUI)

BTN_Energ =  pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 40), (130,30)),
                                        manager=Manager, object_id="BTN_Energ", text="Conductividad", container=SliderUI, parent_element=SliderUI)

BTN_ConfigGlobal = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 70), (130,50)),
                                        manager=Manager, object_id="BTN_ConfigGlobal", text="Config Global", container=SliderUI, parent_element=SliderUI)


BTN_Info = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 10), (120,30)), manager=Manager, object_id="BTN_Info", text="Ayuda")

Wnd_Info = MyHidingWindow(pygame.Rect((100,100,650,700)), manager=Manager, window_display_title="Informacion")
TxtInfo1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(-250,5,1000,50),
                                    text="Este software fue creado dentro de las instalaciones de DCA",
    manager=Manager, container= Wnd_Info, parent_element=Wnd_Info)
TxtInfo2 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(-305,20,1000,50),
                                    text="por el departamento de Desarrollo de Software",
    manager=Manager, container= Wnd_Info, parent_element=Wnd_Info)

TxtInfo3 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(-305,50,1000,50),
                                    text="LUSI_GRAPH V1.0.1", manager=Manager, container= Wnd_Info, parent_element=Wnd_Info)

Wnd_Info.hide()
TxtInfo1.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
TxtInfo2.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)

Verde = (0, 255, 0)
AZUL = (0, 0, 255)

WND_Temp = pygame_gui.elements.UIPanel(pygame.Rect(10,150,1900,900), manager=Manager)
WND_Temp.hide()

Wnd_ConfigGlobal = MyHidingWindow(pygame.Rect(0,0,500,500), manager=Manager, window_display_title="Configuracion Global")
Wnd_ConfigGlobal.hide()

Wnd_ConfigTemp = MyHidingWindow(pygame.Rect(0,0,500,500), manager=Manager, window_display_title="Configuracion Temperatura")
Wnd_ConfigTemp.hide()

Wnd_ConfigEnerg = MyHidingWindow(pygame.Rect(0,0,500,500), manager=Manager, window_display_title="Configuracion Conductividad")
Wnd_ConfigEnerg.hide()

ListColorsLineTemp = ['green', 'red', 'blue']
ListColorsPointTemp = ['green', 'red', 'blue']
ListTypeGrapghTemp = ['Linear', 'Puntos', 'Combinado']
TypeGraphTemp = "Linear"

BTN_LeerCSVTemp = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1650, 50), (120,30)), manager=Manager, object_id="BTN_LeerCSVTemp", text="Leer CSV", container=WND_Temp, parent_element=WND_Temp)
BTN_ConfigTemp = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1650, 90), (120,30)), manager=Manager, object_id="BTN_ConfigTemp", text="Config", container=WND_Temp, parent_element=WND_Temp)

LineColorTemp1Text = 0
LabelTextConfigTemp1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5,10, 200, 30), text="Color Linea Grafica", manager=Manager, container=Wnd_ConfigTemp, parent_element=Wnd_ConfigTemp)
ListColorGraphTemp1 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(250, 10, 120, 30), options_list=ListColorsLineTemp, starting_option=ListColorsLineTemp[0], manager=Manager, container=Wnd_ConfigTemp, parent_element=Wnd_ConfigTemp)

PointColor1TempText = 0
LabelTextConfigTemp2 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5,50, 200, 30), text="Color Puntos Grafica", manager=Manager, container=Wnd_ConfigTemp, parent_element=Wnd_ConfigTemp)
ListColorGraphTemp2 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(250, 50, 120, 30), options_list=ListColorsPointTemp, starting_option=ListColorsPointTemp[0], manager=Manager, container=Wnd_ConfigTemp, parent_element=Wnd_ConfigTemp)

SizeScatterTemp = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(25,90, 230,30), manager=Manager, container=Wnd_ConfigTemp, parent_element=Wnd_ConfigTemp, placeholder_text="Tamaño de los Puntos 1-20")

LabelTextConfigTemp3 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5,210, 200, 30), text="Tipo de Grafica", manager=Manager, container=Wnd_ConfigTemp, parent_element=Wnd_ConfigTemp)
ListGraphTypeTemp = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(250, 210, 120, 30), options_list=ListTypeGrapghTemp, starting_option=ListTypeGrapghTemp[0], manager=Manager, container=Wnd_ConfigTemp, parent_element=Wnd_ConfigTemp)


MaxTemp = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(25,130, 230,30), manager=Manager, container=Wnd_ConfigTemp, parent_element=Wnd_ConfigTemp, placeholder_text="Temperatura Máxima")
MinTemp = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(25,170, 230,30), manager=Manager, container=Wnd_ConfigTemp, parent_element=Wnd_ConfigTemp, placeholder_text="Temperatura Minima")

BTN_Logo = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(25, 250, 120, 30), manager=Manager, object_id="BTN_Logo", text="Insertar Logo", container=Wnd_ConfigGlobal, parent_element=Wnd_ConfigGlobal)

Panel_Temp = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(0,0,1600,900), manager=Manager, container=WND_Temp, parent_element=WND_Temp)

BTN_UpdateTemp = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(1650,500,120,30), manager=Manager, object_id="BTN_UpdateTemp", text="Actualizar", container=WND_Temp, parent_element=WND_Temp)

BTN_PLAYTemp = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(1650,800,120,30), manager=Manager, object_id="BTN_PLAYTemp", text="Jugar", container=WND_Temp, parent_element=WND_Temp)

BTN_PDFTemp = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(1650,850,120,30), manager=Manager, object_id="BTN_PDFTemp", text="Reporte PDF", container=WND_Temp, parent_element=WND_Temp)


LabelText1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(1480,350, 200, 30), text="Dias disponibles:", manager=Manager, container=WND_Temp, parent_element=WND_Temp)
List_FechasTemp = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(1650, 350, 120, 30), options_list=FechaDesplegableTemp, starting_option=FechaDesplegableTemp[0], manager=Manager, container=WND_Temp, parent_element=WND_Temp)

LabelText1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(1500, 400, 200, 30), text="Hora Inicial:", manager=Manager, container=WND_Temp, parent_element=WND_Temp)
ListaHorasDiponiblesStartTemp = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(1650, 400, 120, 30), options_list=ListHorasTemp, starting_option=ListHorasTemp[0], manager=Manager, container=WND_Temp, parent_element=WND_Temp)

LabelText1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(1505,450, 200, 30), text="Hora Final:", manager=Manager, container=WND_Temp, parent_element=WND_Temp)
ListaHorasDiponiblesEndTemp = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(1650, 450, 120, 30), options_list=ListHorasTemp, starting_option=ListHorasTemp[0], manager=Manager, container=WND_Temp, parent_element=WND_Temp)



CommentsTxtTemp = ""
LabelText3 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(1600, 550, 200, 30), text="Comentarios:", manager=Manager, container=WND_Temp, parent_element=WND_Temp)
BocCommentsTemp = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect(1550, 590, 300, 200), manager=Manager, container=WND_Temp, parent_element=WND_Temp)
#########################################################################################################
HoraMinTemp = 0
HoraMaxTemp = 0
#####################################################ENEERGIA CORRIENTE

WND_Energ = pygame_gui.elements.UIPanel(pygame.Rect(10,150,1900,900), manager=Manager)
WND_Energ.hide()

BTN_LeerCSVEnerg = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1650, 50), (120,30)), manager=Manager, object_id="BTN_LeerCSVEnerg", text="Leer CSV", container=WND_Energ, parent_element=WND_Energ)
BTN_ConfigEnerg = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((1650, 90), (120,30)), manager=Manager, object_id="BTN_ConfigEnerg", text="Config", container=WND_Energ, parent_element=WND_Energ)

ListColorsLineEnerg = ['green', 'red', 'blue']
ListColorsPointEnerg= ['green', 'red', 'blue']
ListTypeGrapghEnerg = ['Linear', 'Puntos', 'Combinado']
TypeGraphEnerg = "Linear"

Panel_Energ = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(0,0,1600,900), manager=Manager, container=WND_Energ, parent_element=WND_Energ)

BTN_UpdateEnerg = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(1650,500,120,30), manager=Manager, object_id="BTN_UpdateTemp", text="Actualizar", container=WND_Energ, parent_element=WND_Temp)

BTN_PLAYEnerg = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(1650,800,120,30), manager=Manager, object_id="BTN_PLAYEnerg", text="Jugar", container=WND_Energ, parent_element=WND_Energ)

BTN_PDFEnerg = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(1650,850,120,30), manager=Manager, object_id="BTN_PDFEnerg", text="Reporte PDF", container=WND_Energ, parent_element=WND_Energ)


LabelText1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(1480,350, 200, 30), text="Dias disponibles:", manager=Manager, container=WND_Energ, parent_element=WND_Energ)
List_FechasEnerg = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(1650, 350, 120, 30), options_list=FechaDesplegableEnerg, starting_option=FechaDesplegableEnerg[0], manager=Manager, container=WND_Energ, parent_element=WND_Energ)

LabelText1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(1500, 400, 200, 30), text="Hora Inicial:", manager=Manager, container=WND_Energ, parent_element=WND_Energ)
ListaHorasDiponiblesStartEnerg = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(1650, 400, 120, 30), options_list=ListHorasEnerg, starting_option=ListHorasEnerg[0], manager=Manager, container=WND_Energ, parent_element=WND_Energ)

LabelText1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(1505,450, 200, 30), text="Hora Final:", manager=Manager, container=WND_Energ, parent_element=WND_Energ)
ListaHorasDiponiblesEndEnerg = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(1650, 450, 120, 30), options_list=ListHorasEnerg, starting_option=ListHorasEnerg[0], manager=Manager, container=WND_Energ, parent_element=WND_Energ)

CommentsTxtEnerg = ""
LabelText3 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(1600, 550, 200, 30), text="Comentarios:", manager=Manager, container=WND_Energ, parent_element=WND_Energ)
BocCommentsEnerg = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect(1550, 590, 300, 200), manager=Manager, container=WND_Energ, parent_element=WND_Energ)

LineColorEnerg1Text = 0
LabelTextConfigEnerg1 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5,10, 200, 30), text="Color Linea Grafica", manager=Manager, container=Wnd_ConfigEnerg, parent_element=Wnd_ConfigEnerg)
ListColorGraphEnerg1 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(250, 10, 120, 30), options_list=ListColorsLineTemp, starting_option=ListColorsLineTemp[0], manager=Manager, container=Wnd_ConfigEnerg, parent_element=Wnd_ConfigEnerg)

PointColor1EnergText = 0
LabelTextConfigEnerg2 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5,50, 200, 30), text="Color Puntos Grafica", manager=Manager, container=Wnd_ConfigEnerg, parent_element=Wnd_ConfigEnerg)
ListColorGraphEnerg2 = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(250, 50, 120, 30), options_list=ListColorsPointTemp, starting_option=ListColorsPointTemp[0], manager=Manager, container=Wnd_ConfigEnerg, parent_element=Wnd_ConfigEnerg)

SizeScatterEnerg = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(25,90, 230,30), manager=Manager, container=Wnd_ConfigEnerg, parent_element=Wnd_ConfigEnerg, placeholder_text="Tamaño de los Puntos 1-20")

LabelTextConfigEnerg3 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(5,210, 200, 30), text="Tipo de Grafica", manager=Manager, container=Wnd_ConfigEnerg, parent_element=Wnd_ConfigEnerg)
ListGraphTypeEnerg = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(250, 210, 120, 30), options_list=ListTypeGrapghTemp, starting_option=ListTypeGrapghTemp[0], manager=Manager, container=Wnd_ConfigEnerg, parent_element=Wnd_ConfigEnerg)


MaxEnerg = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(25,130, 230,30), manager=Manager, container=Wnd_ConfigEnerg, parent_element=Wnd_ConfigEnerg, placeholder_text="Conductividad Maxima")
MinEnerg = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(25,170, 230,30), manager=Manager, container=Wnd_ConfigEnerg, parent_element=Wnd_ConfigEnerg, placeholder_text="Conductividad Minima")

HoraMinEnerg = 0
HoraMaxEnerg = 0
#endregion


def ShowUI():
    SliderUI.show()
    PasswordPanel.hide()

def ActivacionDCProduct(StrKey):
    if StrKey == KeyText:
        print("Activacion Realizada")
        with open('LogUser.txt', 'w') as f:
            f.write(StrKey)
        #ReadKey.write(StrKey)
        ReadKey.close()
        return False
    else:
        print("Activacion Incorrecta")
        return True

SecondTry = ReadKey.read()
bFirstTime = ActivacionDCProduct(SecondTry)
if bFirstTime == False:
    ShowUI()



class PDF(FPDF):
    def header(self):
        #self.image('Logo2.png', w=20, x=170)
        self.image(ImgLogo, w=20, x=170)
        self.set_font('Arial', 'B', 20)
        self.set_xy(0,0)
        self.cell(100, 40, "Gráfica de Temperatura", 0,0, 'R')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        #self.cell(0,10, 'Page ' + str(self.page_no()), 0,0, 'C')
        self.cell(0,10, "https://dca-mx.com/", 0,0, 'C')

        self.image('logo.png', w=20, x=15, y=270)

class PDF2(FPDF):
    def header(self):
        #self.image('Logo2.png', w=20, x=170)
        self.image(ImgLogo, w=20, x=170)
        self.set_font('Arial', 'B', 20)
        self.set_xy(0,0)
        self.cell(100, 40, "Gráfica de Conductividad", 0,0, 'R')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        #self.cell(0,10, 'Page ' + str(self.page_no()), 0,0, 'C')
        self.cell(0,10, "https://dca-mx.com/", 0,0, 'C')

        self.image('logo.png', w=20, x=15, y=270)

PDFHOraInit = ""
PDFHoraEnd = ""

def GenerateReportPDF():
    PDfReport = PDF()
    PDfReport.add_page()
    PDfReport.set_font('Arial', 'B', 14)
    PDfReport.image("GraphUpdateTemp.png", w=250, x=-20, y=30)
    PDfReport.set_xy(10, 170)
    PDfReport.cell(w=100, h=5,txt="Fecha de Lectura: \n" + FechaPDFTemp, align='L')

    PDfReport.set_xy(10, 180)
    PDfReport.cell(w=100, h=5,txt="Hora de Inicio: \nDesde las: " + HoraPDFInitTemp + ":00", align='L')

    PDfReport.set_xy(10, 190)
    PDfReport.cell(w=100, h=5,txt="Hora Final: \nHasta las: " + HoraPDFEndTemp + ":00", align='L')

    PDfReport.set_xy(10, 200)
    PDfReport.cell(w=100, h=5,txt="Temperatura Promedio: " + str(TempAvrg) + "°C", align='L')

    PDfReport.set_xy(10, 210)
    PDfReport.cell(w=100, h=5,txt="Datos leidos: " + str(DataTemp), align='L')

    PDfReport.set_xy(10, 230)
    PDfReport.multi_cell(w=150, h=5,txt="Observaciones: \n" + CommentsTxtTemp, align='L', border=1)
    DateNow = datetime.now()
    DateUpdate = DateNow.strftime("Fecha" + "%d-%m-%Y" + "Hora" + "%H-%M-%S")
    PDfReport.output(str(DateUpdate)+ ".pdf", 'F')
    os.startfile(DateUpdate + ".pdf")

def GenerateReportPDFEnerg():
    PDfReport = PDF2()
    PDfReport.add_page()
    PDfReport.set_font('Arial', 'B', 14)
    PDfReport.image("GraphUpdateEnerg.png", w=250, x=-20, y=30)
    PDfReport.set_xy(10, 170)
    PDfReport.cell(w=100, h=5,txt="Fecha de Lectura: \n" + FechaPDFEnerg, align='L')

    PDfReport.set_xy(10, 180)
    PDfReport.cell(w=100, h=5,txt="Hora de Inicio: \nDesde las: " + HoraPDFInitEnerg + ":00", align='L')

    PDfReport.set_xy(10, 190)
    PDfReport.cell(w=100, h=5,txt="Hora Final: \nHasta las: " + HoraPDFEndEnerg + ":00", align='L')

    PDfReport.set_xy(10, 200)
    PDfReport.cell(w=100, h=5,txt="Conductividad Promedio: " + str(TempAvrgEnerg) + "mS", align='L')

    PDfReport.set_xy(10, 210)
    PDfReport.cell(w=100, h=5,txt="Datos leidos: " + str(DataEnerg), align='L')

    PDfReport.set_xy(10, 230)
    PDfReport.multi_cell(w=150, h=5,txt="Observaciones: \n" + CommentsTxtEnerg, align='L', border=1)
    DateNow = datetime.now()
    DateUpdate = DateNow.strftime("Fecha" + "%d-%m-%Y" + "Hora" + "%H-%M-%S")
    PDfReport.output(str(DateUpdate)+ ".pdf", 'F')
    os.startfile(DateUpdate + ".pdf")


ImgLogo = ""
FechaPDFTemp = FechaDesplegableTemp[0]
HoraPDFInitTemp = ListHorasTemp[0]
HoraPDFEndTemp = ListHorasTemp[-1]
TempAvrg = 0.0
DataTemp = 0

FechaPDFEnerg = FechaDesplegableTemp[0]
HoraPDFInitEnerg = ListHorasTemp[0]
HoraPDFEndEnerg = ListHorasTemp[-1]
TempAvrgEnerg = 0.0
DataEnerg = 0

#region GlobalVariables
GameLoop = True
#endregion


def ReadProperties():
    with open("ConfigFILE.txt", 'r+') as Cfg:
        Props = Cfg.readlines()
        Lines = [s.rstrip() for s in Props]
        return Lines      
ReadProps = ReadProperties()



LineColorTemp1Text = ListColorsLineTemp[int(ReadProps[0])]
PointColor1TempText = ListColorsPointTemp[int(ReadProps[1]) + 1]

LineColorEnerg1Text = ListColorsLineEnerg[int(ReadProps[0])]
PointColor1EnergText = ListColorsPointEnerg[int(ReadProps[1]) + 1]




while GameLoop:
    DeltaTime = Clock.tick(60)
    UIRate =  Clock.tick(60)/10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameLoop = False

        Manager.process_events(event)

        KEYS = pygame.key.get_pressed()
        MOUSE = event.type

        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == PassText2:
                StrKeyActivacion = event.text

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTNPass1:
                bFirstTime = ActivacionDCProduct(StrKeyActivacion)
                if bFirstTime == False:
                    ShowUI()


        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_LeerCSVTemp:
                if LineColorTemp1Text != 0 and PointColor1TempText !=0 and MaxTemp.text != "" and MinTemp.text != "" and TypeGraphTemp != "":
                    #OpenExample()
                    returnedFileTemp = OpenCSVTemp()
                    try:
                        FechaPDFTemp = FechaDesplegableTemp[0]
                        HoraPDFInitTemp = ListHorasTemp[0]
                        HoraPDFEndTemp = ListHorasTemp[-1]
                        TempAvrg = round(float(ResAvrg[0]), 2)
                        print(TempAvrg)
                    except:
                        print("Archivo No Leido")
                else:
                    Wnd_ConfigTemp.show()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == BTN_ConfigTemp:
                    Wnd_ConfigTemp.show()

        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_LeerCSVEnerg:
                if LineColorEnerg1Text != 0 and PointColor1EnergText !=0 and MaxEnerg.text != "" and MinEnerg.text != "" and TypeGraphEnerg != "":
                    returnedFileEnerg = OpenCSVEnerg()
                    try:
                        FechaPDFEnerg = FechaDesplegableTemp[0]
                        HoraPDFInitEnerg = ListHorasTemp[0]
                        HoraPDFEndEnerg = ListHorasTemp[-1]
                        TempAvrgEnerg = round(float(ResAvrg[0]), 2)
                        print(TempAvrgEnerg)
                    except:
                        print("Archivo No Leido")
                else:
                    Wnd_ConfigEnerg.show()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_ConfigEnerg:
                Wnd_ConfigEnerg.show()

        
        

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_Temp:
                WND_Temp.show()
                WND_Energ.hide()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_Energ:
                WND_Energ.show()
                WND_Temp.hide()

        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == MaxTemp:
                try:
                    float(MaxTemp.text)
                    MaxTempTxt1 = int(MaxTemp.text)

                except:
                    print("No es numero")

        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == MaxEnerg:
                try:
                    float(MaxEnerg.text)
                    MaxEnergTxt1 = int(MaxEnerg.text)
                except:
                    print("No es numero")

        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == SizeScatterTemp:
                try:
                    float(SizeScatterTemp.text)
                    ScatterSizeTxt = int(SizeScatterTemp.text)

                except:
                    print("No es numero")

        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == SizeScatterEnerg:
                try:
                    float(SizeScatterEnerg.text)
                    ScatterSizeEnergTxt = int(SizeScatterEnerg.text)

                except:
                    print("No es numero")



        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == BocCommentsEnerg:
                CommentsTxtEnerg = BocCommentsEnerg.get_text()
                print(CommentsTxtEnerg)

        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == BocCommentsTemp:
                CommentsTxtTemp = BocCommentsTemp.get_text()
                print(CommentsTxtTemp)
        

        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == MinTemp:
                try:
                    float(MinTemp.text)
                    MinTempTxt1 = int(MinTemp.text)
                except:
                    print("No es numero")

        if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
            if event.ui_element == MinEnerg:
                try:
                    float(MinEnerg.text)
                    MinEnergTxt1 = int(MinEnerg.text)
                except:
                    print("No es numero")

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_UpdateTemp:
                UpdatePlotTemp(C0, C1, HoraMinTemp, HoraMaxTemp, TypeGraphTemp)
                DataTemp = ReturnTempAvgr(HoraMinTemp, HoraMaxTemp)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_UpdateEnerg:
                UpdatePlotEnerg(C0Energ, C1Energ, HoraMinEnerg, HoraMaxEnerg, TypeGraphEnerg)
                DataEnerg = ReturnEnergAvgr(HoraMinEnerg, HoraMaxEnerg)
                

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_Info:
                Wnd_Info.show()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_PLAYTemp:
                plt.show()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_PLAYEnerg:
                plt.show()
                

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_Logo:
                ImgLogo = openFile()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_PDFTemp:
                print("Generando PDF")
                if ImgLogo != "" and FechaPDFTemp != "" and HoraPDFInitTemp != "" and HoraPDFEndTemp != "" and CommentsTxtTemp != "":
                    GenerateReportPDF()
                else:
                    print("Asegurarse de LOGO, fechas y horas")

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_PDFEnerg:
                print("Generando PDF")
                if ImgLogo != "" and FechaPDFEnerg != "" and HoraPDFInitEnerg != "" and HoraPDFEndEnerg != "" and CommentsTxtEnerg != "":
                    GenerateReportPDFEnerg()
                else:
                    print("Asegurarse de LOGO, fechas y horas")


        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == BTN_ConfigGlobal:
                Wnd_ConfigGlobal.show()


        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == List_FechasTemp:
                FechaPDFTemp = List_FechasTemp.selected_option
                print(List_FechasTemp.selected_option)
                ShowDatePlotTemp(returnedFileTemp, DLocFinTemp, int(List_FechasTemp.options_list.index(List_FechasTemp.selected_option)) + 1, int(List_FechasTemp.options_list.index(List_FechasTemp.selected_option)), TypeGraphTemp)


        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == List_FechasEnerg:
                FechaPDFEnerg = List_FechasEnerg.selected_option
                print(List_FechasEnerg.selected_option)
                ShowDatePlotEnerg(returnedFileEnerg, DLocFinEnerg, int(List_FechasEnerg.options_list.index(List_FechasEnerg.selected_option)) + 1, int(List_FechasEnerg.options_list.index(List_FechasEnerg.selected_option)), TypeGraphEnerg)


        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == ListaHorasDiponiblesStartTemp:
                HoraPDFInitTemp = ListaHorasDiponiblesStartTemp.selected_option
                #print(ListHorasValues[ListaHorasDiponiblesStart.options_list.index(ListaHorasDiponiblesStart.selected_option)])
                HoraMinTemp = int(ListHorasValuesTemp[ListaHorasDiponiblesStartTemp.options_list.index(ListaHorasDiponiblesStartTemp.selected_option)])

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == ListaHorasDiponiblesStartEnerg:
                HoraPDFInitEnerg = ListaHorasDiponiblesStartEnerg.selected_option
                #print(ListHorasValues[ListaHorasDiponiblesStart.options_list.index(ListaHorasDiponiblesStart.selected_option)])
                HoraMinEnerg = int(ListHorasValuesEnerg[ListaHorasDiponiblesStartEnerg.options_list.index(ListaHorasDiponiblesStartEnerg.selected_option)])

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == ListaHorasDiponiblesEndTemp:
                HoraPDFEndTemp = ListaHorasDiponiblesEndTemp.selected_option
                HoraMaxTemp= int(ListHorasValuesTemp[ListaHorasDiponiblesEndTemp.options_list.index(ListaHorasDiponiblesEndTemp.selected_option)])
                print(ListHorasValuesTemp[ListaHorasDiponiblesEndTemp.options_list.index(ListaHorasDiponiblesEndTemp.selected_option)])

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == ListaHorasDiponiblesEndEnerg:
                HoraPDFEndEnerg = ListaHorasDiponiblesEndEnerg.selected_option
                HoraMaxEnerg= int(ListHorasValuesEnerg[ListaHorasDiponiblesEndEnerg.options_list.index(ListaHorasDiponiblesEndEnerg.selected_option)])
                print(ListHorasValuesEnerg[ListaHorasDiponiblesEndEnerg.options_list.index(ListaHorasDiponiblesEndEnerg.selected_option)])

        
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == ListColorGraphTemp1:
                LineColorTemp1Text = ListColorGraphTemp1.options_list.index(ListColorGraphTemp1.selected_option)
                LineColorTemp1Text = ListColorsLineTemp[int(LineColorTemp1Text)]

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == ListColorGraphEnerg1:
                LineColorEnerg1Text = ListColorGraphEnerg1.options_list.index(ListColorGraphEnerg1.selected_option)
                LineColorEnerg1Text = ListColorsLineEnerg[int(LineColorEnerg1Text)]
                print(LineColorEnerg1Text)

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == ListColorGraphTemp2:
                PointColor1TempText = ListColorGraphTemp2.options_list.index(ListColorGraphTemp2.selected_option)
                PointColor1TempText = ListColorsPointTemp[int(PointColor1TempText)]
                print(PointColor1TempText)

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == ListColorGraphEnerg2:
                PointColor1EnergText = ListColorGraphEnerg2.options_list.index(ListColorGraphEnerg2.selected_option)
                PointColor1EnergText = ListColorsPointTemp[int(PointColor1EnergText)]
                print(PointColor1EnergText)


        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == ListGraphTypeTemp:
                TypeGraphTemp = ListGraphTypeTemp.selected_option
                print(TypeGraphTemp)

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == ListGraphTypeEnerg:
                TypeGraphEnerg = ListGraphTypeEnerg.selected_option
                print(TypeGraphEnerg)
        

    pygame.display.flip()
    screen.fill("gray")
    Manager.update(UIRate)
    Manager.draw_ui(screen)
    

pygame.quit()
