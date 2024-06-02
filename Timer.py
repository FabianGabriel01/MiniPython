from tkinter import *
from pyModbusTCP.client import ModbusClient
#import ModbusExtension
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import io
import matplotlib
import random


matplotlib.use("Agg")




# Creating the GUI window.
window = Tk()
window.title("Welcome to PLC Controller Lusi")
window.geometry("1500x1000")
window.resizable(False, False)
window.config(bg='burlywood1')
Timer = 0
IP_Main = ""
UnitID_Main = ""

def plot(): 
   global WindowFloat1
   # the figure that will contain the plot 
   fig = Figure(figsize = (8, 5)) 
  
   # list of squares 
   #y = [i**2 for i in range(101)] 
  
   # adding the subplot 
   plot1 = fig.add_subplot(111) 
  
   # plotting the graph 
   plot1.plot(XList, YList)
   #plot1.draw()
   
  
   # creating the Tkinter canvas 
   # containing the Matplotlib figure 
   canvas = FigureCanvasTkAgg(fig, master = WindowFloat1)   
   canvas.draw() 
  
   # placing the canvas on the Tkinter window 
   canvas.get_tk_widget().pack() 
  
   # creating the Matplotlib toolbar 
   # toolbar = NavigationToolbar2Tk(canvas, window) 
   # toolbar.update() 
  
   # placing the toolbar on the Tkinter window 
   canvas.get_tk_widget().place(x= 350, y=150)
   canvas.get_tk_widget().delete()

def calculate_total_cost(event):
    if IP_Address.get().isdigit():
         total_cost=int(IP_Address.get())

def IP_click(event):
   if IP_Address.get() == "Direccion IP...":
         IP_Address.delete(0, "end")
         IP_Address.configure(foreground="black")

def UnitID_click(event):
   if Unit_ID.get() == "Unit ID...":
      Unit_ID.delete(0, "end")
      Unit_ID.configure(foreground="black")

def IP_Out(event):
   if IP_Address.get() == "":
         IP_Address.insert(0, "Direccion IP...")
         IP_Address.configure(foreground="gray")

def UnitID_Out(event):
   if Unit_ID.get() == "":
      Unit_ID.insert(0, "Unit ID...")
      Unit_ID.configure(foreground="gray")

def IsConnected():
   print("LSAD")
   #return ModbusExtension.GetConnection()
   
def Connection():
   #ModbusExtension.StartConnection(IP_Main, UnitID_Main)
   countdown()
   #if IsConnected():


def GetIpMain(event):
   global IP_Main 
   if IP_Address.get():
      try:
         IP_Main = IP_Address.get()
      except:
         IP_Main = "0" 

def GetUnitIDMain(event):
   global UnitID_Main
   if Unit_ID.get():
      try:
         UnitID_Main = int(Unit_ID.get())
      except:
         UnitID_Main = 1

def set_text_by_button(Text): 
   # Insert method inserts the text at
   # specified position, Here it is the
   # beginning
   IP_Address.delete(0,"end")
   IP_Address.insert(0, Text)


XList = []
YList = []

def countdown():
   global Timer 
   Num =+ 1  
   if Num != 0:
      Timer += 1
      XList.append(Timer)
      #set_text_by_button(str(Timer))
      YList.append(random.randint(0, 5))
      #YList.append(AllRegisters())
      plot()
      #5window.update()
      window.after(1000, countdown)

   if Timer >= 10:
      XList.pop(0)
      YList.pop(0)


#region UIMain
ConnectarMain = Button(window, height=1, width=10, text="Set", command=Connection)
ConnectarMain.place(x=125, y=90)
IP_Address = Entry(window, foreground="gray")
IP_Address.insert(0, "Direccion IP...")
IP_Address.bind("<KeyRelease>", GetIpMain)
IP_Address.bind("<FocusIn>", IP_click)
IP_Address.bind("<FocusOut>", IP_Out)
IP_Address.place(x=50, y=50, width= 100, height= 25)

Unit_ID = Entry(window, foreground="gray")
Unit_ID.insert(0, "Unit ID...")
Unit_ID.bind("<KeyRelease>", GetUnitIDMain)
Unit_ID.bind("<FocusIn>", UnitID_click)
Unit_ID.bind("<FocusOut>", UnitID_Out)
Unit_ID.place(x=175, y=50, width= 100, height= 25)
#endregion

#region Panel Lecturas
PanelMain = PanedWindow(window)
PanelMain.place(x= 300 , y=50, width=350, height=600)

def AllRegisters():
   print("ALIHD")

   # PanelLecturaHR1.config(text=str(ModbusExtension.HoldingRegistersLecture(LectTxt1)))
   # PanelLecturaHR2.config(text=str(ModbusExtension.HoldingRegistersLecture(LectTxt2)))
   # PanelLecturaHR3.config(text=str(ModbusExtension.HoldingRegistersLecture(LectTxt3)))
   # PanelLecturaHR4.config(text=str(ModbusExtension.HoldingRegistersLecture(LectTxt4)))
   # PanelLecturaHR5.config(text=str(ModbusExtension.HoldingRegistersLecture(LectTxt5)))
   # return ModbusExtension.HoldingRegistersLecture(LectTxt1)
      

def Lectura1(event):
   global LectTxt1
   if LecturaHR1.get():
      try:
         LectTxt1 = int(LecturaHR1.get())
      except:
         LecturaHR1.insert(0, "0")
         LectTxt1 = 0
LectTxt1 = 0
LecturaHR1 = Entry(PanelMain)
LecturaHR1.bind("<KeyRelease>", Lectura1)
LecturaHR1.place(x= 10 , y=10, width=100, height=25)
PanelLecturaHR1 = Label(PanelMain, text="Valor")
PanelLecturaHR1.place(x=120, y=10 , width=100, height=25)


def Lectura2(event):
   global LectTxt2
   if LecturaHR2.get():
      try:
         LectTxt2 = int(LecturaHR2.get())
      except:
         LecturaHR2.insert(0, "0")
         LectTxt2 = 0
LectTxt2 = 0
LecturaHR2 = Entry(PanelMain)
LecturaHR2.bind("<KeyRelease>", Lectura2)
LecturaHR2.place(x= 10 , y=40, width=100, height=25)
PanelLecturaHR2 = Label(PanelMain, text="Valor")
PanelLecturaHR2.place(x=120, y=40 , width=100, height=25)

def Lectura3(event):
   global LectTxt3
   if LecturaHR3.get():
      try:
         LectTxt3 = int(LecturaHR3.get())
      except:
         LecturaHR3.insert(0, "0")
         LectTxt3 = 0
LectTxt3 = 0
LecturaHR3 = Entry(PanelMain)
LecturaHR3.bind("<KeyRelease>", Lectura3)
LecturaHR3.place(x= 10 , y=70, width=100, height=25)
PanelLecturaHR3 = Label(PanelMain, text="Valor")
PanelLecturaHR3.place(x=120, y=70 , width=100, height=25)


def Lectura4(event):
   global LectTxt4
   if LecturaHR4.get():
      try:
         LectTxt4 = int(LecturaHR4.get())
      except:
         LecturaHR4.insert(0, "0")
         LectTxt4 = 0
LectTxt4 = 0
LecturaHR4 = Entry(PanelMain)
LecturaHR4.bind("<KeyRelease>", Lectura4)
LecturaHR4.place(x= 10 , y=100, width=100, height=25)
PanelLecturaHR4 = Label(PanelMain, text="Valor")
PanelLecturaHR4.place(x=120, y=100 , width=100, height=25)


def Lectura5(event):
   global LectTxt5
   if LecturaHR5.get():
      try:
         LectTxt5 = int(LecturaHR5.get())
      except:
         LecturaHR5.insert(0, "0")
         LectTxt5 = 0
LectTxt5 = 0
LecturaHR5 = Entry(PanelMain)
LecturaHR5.bind("<KeyRelease>", Lectura5)
LecturaHR5.place(x= 10 , y=130, width=100, height=25)
PanelLecturaHR5 = Label(PanelMain, text="Valor")
PanelLecturaHR5.place(x=120, y=130 , width=100, height=25)

LecturaHR6 = Entry(PanelMain)
LecturaHR6.place(x= 10 , y=160, width=100, height=25)

PanelLecturaHR6 = Label(PanelMain, text="Valor")
PanelLecturaHR6.place(x=120, y=160 , width=100, height=25)

LecturaHR7 = Entry(PanelMain)
LecturaHR7.place(x= 10 , y=190, width=100, height=25)

PanelLecturaHR7 = Label(PanelMain, text="Valor")
PanelLecturaHR7.place(x=120, y=190 , width=100, height=25)

LecturaHR8 = Entry(PanelMain)
LecturaHR8.place(x= 10 , y=220, width=100, height=25)

PanelLecturaHR8 = Label(PanelMain, text="Valor")
PanelLecturaHR8.place(x=120, y=220 , width=100, height=25)

LecturaHR9 = Entry(PanelMain)
LecturaHR9.place(x= 10 , y=250, width=100, height=25)

PanelLecturaHR9 = Label(PanelMain, text="Valor")
PanelLecturaHR9.place(x=120, y=250 , width=100, height=25)

LecturaHR10 = Entry(PanelMain)
LecturaHR10.place(x= 10 , y=280, width=100, height=25)

PanelLecturaHR10 = Label(PanelMain, text="Valor")
PanelLecturaHR10.place(x=120, y=280 , width=100, height=25)

LecturaHR11 = Entry(PanelMain)
LecturaHR11.place(x= 10 , y=310, width=100, height=25)

PanelLecturaHR11 = Label(PanelMain, text="Valor")
PanelLecturaHR11.place(x=120, y=310 , width=100, height=25)

LecturaHR12 = Entry(PanelMain)
LecturaHR12.place(x= 10 , y=340, width=100, height=25)

PanelLecturaHR12 = Label(PanelMain, text="Valor")
PanelLecturaHR12.place(x=120, y=340 , width=100, height=25)

LecturaHR13 = Entry(PanelMain)
LecturaHR13.place(x= 10 , y=370, width=100, height=25)

PanelLecturaHR13 = Label(PanelMain, text="Valor")
PanelLecturaHR13.place(x=120, y=370 , width=100, height=25)

LecturaHR14 = Entry(PanelMain)
LecturaHR14.place(x= 10 , y=400, width=100, height=25)

PanelLecturaHR14 = Label(PanelMain, text="Valor")
PanelLecturaHR14.place(x=120, y=400 , width=100, height=25)

LecturaHR15 = Entry(PanelMain)
LecturaHR15.place(x= 10 , y=430, width=100, height=25)

PanelLecturaHR15 = Label(PanelMain, text="Valor")
PanelLecturaHR15.place(x=120, y=430 , width=100, height=25)

LecturaHR16 = Entry(PanelMain)
LecturaHR16.place(x= 10 , y=460, width=100, height=25)

PanelLecturaHR16 = Label(PanelMain, text="Valor")
PanelLecturaHR16.place(x=120, y=460 , width=100, height=25)

LecturaHR17 = Entry(PanelMain)
LecturaHR17.place(x= 10 , y=490, width=100, height=25)

PanelLecturaHR17 = Label(PanelMain, text="Valor")
PanelLecturaHR17.place(x=120, y=490 , width=100, height=25)




#endregion

#region EnergiaElectrica
OpenWindowEE = 0
def DoOnce(Num):
   global OpenWindowEE
   if Num >= 1:
      print("Ya existente")
      return False
   else:
      return True

def CloseEE(self):
   self.destroy()

def ClosingEEWindow():
   global WindowFloat1
   global OpenWindowEE
   print("Closed")
   OpenWindowEE = 0
   CloseEE(WindowFloat1)
   

def WindowEnergiaElectrica():
   global OpenWindowEE
   global WindowFloat1
   if DoOnce(OpenWindowEE):
      OpenWindowEE +=1
      print(OpenWindowEE)
      WindowFloat1 = Toplevel(window)
      WindowFloat1.title("Energia Electrica")
      WindowFloat1.geometry("1400x1000")
      WindowFloat1.resizable(False, False)
      WindowFloat1.protocol("WM_DELETE_WINDOW", ClosingEEWindow)
      UIEnergiaElectrica(WindowFloat1)

EnergiaBTN = Button(window, height=5, width=25, text="Energia electrica", command=WindowEnergiaElectrica)
EnergiaBTN.place(x=125, y=120)

def Menu1Value(event):
   global ClickMenu1
   print(ClickMenu1.get())

def Menu2Value(event):
   global ClickMenu2
   print(ClickMenu2.get())

def UIEnergiaElectrica(Parent):
   print("Generando")
   global ClickMenu1
   global ClickMenu2
   #region Panel1
   Panel1EE = PanedWindow(Parent, bg="gray")
   Panel1EE.place(x=0, y=95, width=195, height=900)

   LecturaMedidoresBTN = Button(Parent, height=5, width=25, text="Lectura Medidores")
   LecturaMedidoresBTN.place(x=5, y=100)

   RecivosVirtualesBTN = Button(Parent, height=5, width=25, text="Recivos Virtuales")
   RecivosVirtualesBTN.place(x=5, y=200)

   ProyeccionesCostoBTN = Button(Parent, height=5, width=25, text="Proyecciones de Costo")
   ProyeccionesCostoBTN.place(x=5, y=300)

   AnalisisCBBTN = Button(Parent, height=5, width=25, text="Analisis de Costo beneficio")
   AnalisisCBBTN.place(x=5, y=400)

   HistoricosBTN = Button(Parent, height=5, width=25, text="Historicos")
   HistoricosBTN.place(x=5, y=500)

   RegistroManualBTN = Button(Parent, height=5, width=25, text="Registro Manual")
   RegistroManualBTN.place(x=5, y=600)

   ReconectarASerBTN = Button(Parent, height=5, width=25, text="Reconectar a Servidor")
   ReconectarASerBTN.place(x=5, y=700)

   SincroRelojcRIOBTN = Button(Parent, height=5, width=25, text="Sincronizar reloj cRIO")
   SincroRelojcRIOBTN.place(x=5, y=800)
   #endregion

   #region Panel2
   Panel2EE = PanedWindow(Parent, bg="dark gray")
   Panel2EE.place(x=195, y=95, width=1300, height=900)
   #endregion

   EmpresaLabel = Label(Parent, text="Empresa", fg="white", bg="gray")
   EmpresaLabel.place(x= 50, y=20, width=150, height=30)

   PlantaLabel = Label(Parent, text="Planta", fg="white", bg="gray")
   PlantaLabel.place(x= 205, y=20, width=150, height=30)

   ClickMenu1 = StringVar()
   ClickMenu1.set("Sur")
   OptionsMenu1 = ["Norte", "Sur"]
   Menu1 = OptionMenu(Parent, ClickMenu1, *OptionsMenu1) 
   Menu1.bind("<Configure>", Menu1Value)
   Menu1.place(x= 355, y=20, width=150, height=30)

   ClickMenu2 = StringVar()
   ClickMenu2.set("HS")
   OptionsMenu2 = ["HS", "RS"]
   Menu2 = OptionMenu(Parent, ClickMenu2, *OptionsMenu2) 
   Menu2.bind("<Configure>", Menu2Value)
   Menu2.place(x= 500, y=20, width=150, height=30)

   CargaConLabel = Label(Parent, text="Carga Conectada", fg="White", bg="gray")
   CargaConLabel.place(x=650, y=20, width=150, height=30)

   DemandaContLabel = Label(Parent, text="Demanda Contrada", fg="White", bg="gray")
   DemandaContLabel.place(x=805, y=20, width=150, height=30)


   #region Panel 3


   #endregion

#endregion


# Panel = PanedWindow(window, height=100, width=100, showhandle=True)
# Panel.pack()


if __name__ == "__main__":
   app = window 
   app.mainloop()
