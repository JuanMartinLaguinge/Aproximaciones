#TP4 Teoria de Cirucitos.

#La GUI de este programa funciona a través de pasos. Es decir, a medida que el usuario va haciendo los pasos que se
#le indica, el siguiente paso aparece.

import math
import matplotlib
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk as toolbar
from matplotlib.figure import Figure
import matplotlib.patches as patches #para plotear la plantilla en el plot.
from scipy import signal
from singularidades import singularidades as sing
from Aproximador import AproximadorFiltro

class Gui:
    def reset_button_color(self): #pone todos los botones en el color que simboliza como NO precionado.
        if(self.step <= 1):
            self.b_LP.configure(bg="light gray")
            self.b_HP.configure(bg="light gray")
            self.b_BP.configure(bg="light gray")
            self.b_BS.configure(bg="light gray")
        if(self.step <= 2):
            self.b_butter.configure(bg="light gray")
            self.b_cheby_I.configure(bg="light gray")
            self.b_cheby_II.configure(bg="light gray")
            self.b_bess.configure(bg="light gray")
            self.b_graph.configure(bg="light gray")
            self.b_graph.configure(bg="light gray")
        if(self.step <= 3):
            self.b_attenuation.configure(bg="light gray")
            self.b_phase.configure(bg="light gray")
            self.b_zp.configure(bg="light gray")
            self.b_step.configure(bg="light gray")
            self.b_impulse.configure(bg="light gray")
            if(self.screen != 0):
                self.b_screen1.configure(bg="light gray")
            if(self.screen != 1):
                self.b_screen2.configure(bg="light gray")
            self.b_c_stage.configure(bg="light gray")
            self.b_s_stages.configure(bg="light gray")

    def forget_buttons(self): #deja de mostrar todos los botones en pantalla.
        self.text1.place_forget()
        self.b_LP.place_forget()
        self.b_HP.place_forget()
        self.b_BP.place_forget()
        self.b_BS.place_forget()
        self.text2.place_forget()
        self.b_butter.place_forget()
        self.b_cheby_I.place_forget()
        self.b_cheby_II.place_forget()
        self.b_bess.place_forget()
        self.text3.place_forget()
        self.Ap.place_forget()
        self.Ap_val.place_forget()
        self.fp.place_forget()
        self.fp_val.place_forget()
        self.As.place_forget()
        self.As_val.place_forget()
        self.fs.place_forget()
        self.fs_val.place_forget()
        self.fp1.place_forget()
        self.fp1_val.place_forget()
        self.fs1.place_forget()
        self.fs1_val.place_forget()
        self.b_graph.place_forget()
        self.b_attenuation.place_forget()
        self.b_phase.place_forget()
        self.b_zp.place_forget()
        self.b_step.place_forget()
        self.b_impulse.place_forget()
        self.b_screen1.place_forget()
        self.b_screen2.place_forget()
        self.zp.place_forget()
        self.zlist.place_forget()
        self.plist.place_forget()
        self.b_c_stage.place_forget()
        self.b_s_stages.place_forget()

    def update_listboxes(self):
        self.zlist.delete(0,tk.END)
        self.plist.delete(0,tk.END)
        k = 1
        for i in range(len(self.zlist_val)):
            if(self.zlist_val[i].imag != 0):
                if(self.zlist_val[i].sel == 0):
                    self.zlist.insert(i,"z"+str(2*i+k)+",z"+str(2*i+k+1))
                else:
                    self.zlist.insert(i,"z"+str(2*i+k)+",z"+str(2*i+k+1)+" (used)")
            else:
                if(self.zlist_val[i].sel == 0):
                    self.zlist.insert(i,"z"+str(2*i+1))
                else:
                    self.zlist.insert(i,"z"+str(2*i+1)+" (used)")
                k = 0
        self.zlist.insert(tk.END,"none")
        self.zlist.place(x=700,y=50)
        k = 1
        for i in range(len(self.plist_val)):
            if(self.plist_val[i].imag != 0):
                if(self.plist_val[i].sel == 0):
                    self.plist.insert(i,"p"+str(2*i+k)+",p"+str(2*i+k+1))
                else:
                    self.plist.insert(i,"p"+str(2*i+k)+",p"+str(2*i+k+1)+" (used)")
            else:
                if(self.plist_val[i].sel == 0):
                    self.plist.insert(i,"p"+str(2*i+1))
                else:
                    self.plist.insert(i,"p"+str(2*i+1)+" (used)")
                k = 0
        self.plist.insert(tk.END,"none")
        self.plist.place(x=870,y=50)

    def update_screen(self): #coloca los botones, esta función se usa para actualizar la presencia de los botones de acurdo al paso y la página en el que el usuario esta. 
        self.forget_buttons()
        self.warning.place_forget()
        if(self.screen == 0):
            if(self.step < 3):
                self.plt.clear()
                self.fig.suptitle("")
                self.data_plt.draw()
            self.text1.place(x=700,y=15)
            self.b_LP.place(x=700,y=45)
            self.b_HP.place(x=762,y=45)
            self.b_BP.place(x=828,y=45)
            self.b_BS.place(x=895,y=45)
            if(self.step > 0):
                self.text2.place(x=700,y=90)
                self.b_butter.place(x=700,y=120)
                self.b_cheby_I.place(x=777,y=120)
                self.b_cheby_II.place(x=855,y=120)
                self.b_bess.place(x=936,y=120)
            if(self.step > 1):
                self.text3.place(x=700,y=165)
                self.Ap.place(x=700,y=195)
                self.Ap_val.place(x=735,y=195)
                self.As.place(x=700,y=225)
                self.As_val.place(x=735,y=225)
                self.b_graph.place(x=700,y=300)
                if(self.filter_type == "low pass" or self.filter_type == "high pass"):
                    self.fp.configure(text = "fp = ")
                    self.fp.place(x=850,y=195)
                    self.fp_val.place(x=885,y=195)
                    self.fs.configure(text = "fs = ")
                    self.fs.place(x=850,y=225)
                    self.fs_val.place(x=885,y=225)
                if(self.filter_type == "band pass" or self.filter_type == "band stop"):
                    self.fp.configure(text = "fp- = ")
                    self.fp.place(x=850,y=195)
                    self.fp_val.place(x=889,y=195)
                    self.fs.configure(text = "fs- = ")
                    self.fs.place(x=850,y=225)
                    self.fs_val.place(x=889,y=225)
                    self.fp1.place(x=1003,y=195)
                    self.fp1_val.place(x=1046,y=195)
                    self.fs1.place(x=1003,y=225)
                    self.fs1_val.place(x=1046,y=225)
            if(self.step > 2):
                self.b_attenuation.place(x=10, y=15)
                self.b_phase.place(x=125, y=15)
                self.b_zp.place(x=208, y=15)
                self.b_step.place(x=295, y=15)
                self.b_impulse.place(x=385, y=15)
                self.b_screen1.place(x=10, y=545)
                self.b_screen2.place(x=125, y=545)
        if(self.screen == 1 and self.step > 2):
            self.b_screen1.place(x=10, y=545)
            self.b_screen2.place(x=125, y=545)
            self.zp.place(x=700,y=15)
            self.b_zp.place(x=10, y=15)
            self.zlist_val = sing(self.H.zeros)
            self.plist_val = sing(self.H.poles)
            self.update_listboxes()
            self.b_c_stage.place(x=1050,y=50)
            self.b_s_stages.place(x=1050,y=108)
            

    def plot_attenuation(self): #se plotea la atenuación en bode de la función transferencia junto con la plantilla.
        self.reset_button_color()
        self.b_attenuation.configure(bg="olive drab")
        self.plt.clear()
        self.plt.semilogx(self.f,(-1)*self.mag)
        self.fig.suptitle("Attenuation (Bode)")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Frequency (Hz)") #"$Frequency (Hz)$" -> con los '$' se cambia la letra a cursiva.
        self.plt.set_ylabel("Attenuation (dB)") #_{out} -> pone out en letra chica y abajo.

        #se plotea la plantilla.
        if(self.filter_type == "low pass"):
            self.plt.add_patch(patches.Rectangle((self.axes.get_xlim()[0], float(self.Ap_val.get())), float(self.fp_val.get())-self.axes.get_xlim()[0], self.axes.get_ylim()[1]-float(self.Ap_val.get()),fill=None, hatch='////'))
            self.plt.add_patch(patches.Rectangle((float(self.fs_val.get()), self.axes.get_ylim()[0]), self.axes.get_xlim()[1]-float(self.fs_val.get()), float(self.As_val.get())-self.axes.get_ylim()[0],fill=None, hatch='////'))
        if(self.filter_type == "high pass"):
            self.plt.add_patch(patches.Rectangle((self.axes.get_xlim()[0], self.axes.get_ylim()[0]), float(self.fs_val.get())-self.axes.get_xlim()[0], float(self.As_val.get())-self.axes.get_ylim()[0],fill=None, hatch='////'))
            self.plt.add_patch(patches.Rectangle((float(self.fp_val.get()), float(self.Ap_val.get())), self.axes.get_xlim()[1]-float(self.fp_val.get()), self.axes.get_ylim()[1]-float(self.Ap_val.get()),fill=None, hatch='////'))  
        if(self.filter_type == "band pass"):
            self.plt.add_patch(patches.Rectangle((self.axes.get_xlim()[0], self.axes.get_ylim()[0]), float(self.fs_val.get())-self.axes.get_xlim()[0], float(self.As_val.get())-self.axes.get_ylim()[0],fill=None, hatch='////'))
            self.plt.add_patch(patches.Rectangle((float(self.fp_val.get()), float(self.Ap_val.get())), float(self.fp1_val.get())-float(self.fp_val.get()), self.axes.get_ylim()[1]-float(self.Ap_val.get()),fill=None, hatch='////'))      
            self.plt.add_patch(patches.Rectangle((float(self.fs1_val.get()), self.axes.get_ylim()[0]), self.axes.get_xlim()[1]-float(self.fs1_val.get()), float(self.As_val.get())-self.axes.get_ylim()[0],fill=None, hatch='////'))
        if(self.filter_type == "band stop"):
            self.plt.add_patch(patches.Rectangle((self.axes.get_xlim()[0], float(self.Ap_val.get())), float(self.fp_val.get())-self.axes.get_xlim()[0], self.axes.get_ylim()[1]-float(self.Ap_val.get()),fill=None, hatch='////'))
            self.plt.add_patch(patches.Rectangle((float(self.fs_val.get()), self.axes.get_ylim()[0]), float(self.fs1_val.get())-float(self.fs_val.get()), float(self.As_val.get())-self.axes.get_ylim()[0],fill=None, hatch='////'))            
            self.plt.add_patch(patches.Rectangle((float(self.fp1_val.get()), float(self.Ap_val.get())), self.axes.get_xlim()[1]-float(self.fp1_val.get()), self.axes.get_ylim()[1]-float(self.Ap_val.get()),fill=None, hatch='////'))            
        self.data_plt.draw()

    def plot_phase(self): #plotea la fase en bode de la función transferencia.
        self.reset_button_color()
        self.b_phase.configure(bg="olive drab")
        self.plt.clear()
        self.plt.semilogx(self.f,self.phase)
        self.fig.suptitle("Phase (Bode)")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Frequency (Hz)")
        self.plt.set_ylabel("Phase (Deg)")
        self.data_plt.draw()

    def plot_zp(self): #plotea los polos y ceros de la función transferencia y nombra cada uno de ellos.
        self.reset_button_color()
        self.b_zp.configure(bg="olive drab")
        self.plt.clear()
        self.plt.scatter(self.H.zeros.real,self.H.zeros.imag, marker = 'o', color = "red")
        for i in range(len(self.H.zeros)):
            self.plt.annotate("z"+str(i+1),xy=(self.H.zeros[i].real,self.H.zeros[i].imag))
        self.plt.scatter(self.H.poles.real,self.H.poles.imag, marker = 'x', color = "blue")
        for i in range(len(self.H.poles)):
            self.plt.annotate("p"+str(i+1),xy=(self.H.poles[i].real,self.H.poles[i].imag))
            
        self.fig.suptitle("Zeros & Poles")    
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Real Part")
        self.plt.set_ylabel("Imaginary Part")
        self.data_plt.draw()

    def plot_step(self): #plotea la respuesta al escalon u(t) de la señal.
        self.reset_button_color()
        self.b_step.configure(bg="olive drab")
        self.plt.clear() #simpre limpiar antes de plotear.
        self.plt.plot(self.stepT,self.stepMag) #stepT -> tiempo. stepMag -> tension de la respuesta al escalón.
        self.fig.suptitle("Step Response")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Time (sec)")
        self.plt.set_ylabel("Voltage (V)")
        self.data_plt.draw()

    def plot_impulse(self): #plotea la respuesta al impulso (delta de dirac) de la señal.
        self.reset_button_color()
        self.b_impulse.configure(bg="olive drab")
        self.plt.clear()
        self.plt.plot(self.impT,self.impMag) #impT -> tiempo. impMag -> tension de la respuesta al impulso
        self.fig.suptitle("Impulse Response")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Time (sec)")
        self.plt.set_ylabel("Voltage (V)")
        self.data_plt.draw() 

    def set_low_pass(self): #se selecciona el filtro pasa bajos y se completa el primer paso.
        self.step = 1
        self.reset_button_color()
        self.b_LP.configure(bg="olive drab")
        self.filter_type = "low pass"  
        self.update_screen()

    def set_high_pass(self): #se selecciona el filtro pasa altos y se completa el primer paso.
        self.step = 1
        self.reset_button_color()
        self.b_HP.configure(bg="olive drab")
        self.filter_type = "high pass"
        self.update_screen()

    def set_band_pass(self): #se selecciona el filtro pasa banda y se completa el primer paso.
        self.step = 1
        self.reset_button_color()
        self.b_BP.configure(bg="olive drab")
        self.filter_type = "band pass"
        self.update_screen()

    def set_band_stop(self): #se selecciona el filtro rechaza banda y se completa el primer paso.
        self.step = 1
        self.reset_button_color()
        self.b_BS.configure(bg="olive drab")
        self.filter_type = "band stop"
        self.update_screen()

    def set_butter(self): #se selecciona la aproximación de butterworth y se completa el segundo paso.
        self.step = 2
        self.reset_button_color()
        self.b_butter.configure(bg="olive drab")
        self.approx_type = "butterworth"  
        self.update_screen()

    def set_cheby_I(self): #se selecciona la aproximación de chebyshev y se completa el segundo paso.
        self.step = 2
        self.reset_button_color()
        self.b_cheby_I.configure(bg="olive drab")
        self.approx_type = "chebyshev I"
        self.update_screen()

    def set_cheby_II(self): #se selecciona la aproximación de chebychev inverso y se completa el segundo paso.
        self.step = 2
        self.approx_type = "chebyshev II"
        self.reset_button_color()
        self.b_cheby_II.configure(bg="olive drab")
        self.update_screen()

    def set_bess(self): #se selecciona la aproximación de bessel y se completa el segundo paso.
        self.step = 2
        self.reset_button_color()
        self.b_bess.configure(bg="olive drab")
        self.approx_type = "bessel"
        self.update_screen()

    def start_graph(self): #se verifica que las especificaciones ingresas son validas y plotea la aproximación en atenuación junto con la plantilla.
        try: #se fija si alguna de las especificaciones está vacio o no es un número.
            float(self.Ap_val.get())
            float(self.As_val.get())
            float(self.fp_val.get())
            float(self.fs_val.get())
            if(self.filter_type == "band pass" or self.filter_type == "band stop"):
                float(self.fp1_val.get())
                float(self.fs1_val.get())
        except ValueError:
            self.warning.configure(text="WARNING: Fill all the specifications with valid numbers.")
            self.warning.place(x=700,y=520)
            return
        if(float(self.Ap_val.get()) >= float(self.As_val.get())): #se fija si Ap >= AS.
            self.warning.configure(text="WARNING: Be sure that... Ap < As.")
            self.warning.place(x=700,y=520)
            return
        if(float(self.fp_val.get()) == 0 or float(self.fs_val.get()) == 0): #se fija si alguna frecuencia es nula.
            self.warning.configure(text="WARNING: Frequency must not be zero.")
            self.warning.place(x=700,y=520)
            return
        if(self.filter_type == "band pass" or self.filter_type == "band stop"):
            if(float(self.fp_val.get()) == 0 or float(self.fs_val.get()) == 0): #se fija si alguna frecuencia es nula. 
                self.warning.configure(text="WARNING: Frecuency must not be zero.")
                self.warning.place(x=700,y=520)
                return
        if(self.filter_type == "low pass"):
            if(float(self.fp_val.get()) >= float(self.fs_val.get())): #se fija si en pasa bajos fp >= fs.
                self.warning.configure(text="WARNING: Low Pass Filter: Be sure that... fp < fs.")
                self.warning.place(x=700,y=520)
                return
        if(self.filter_type == "high pass"): 
            if(float(self.fp_val.get()) <= float(self.fs_val.get())): #se fija si en pasa altos fs >= fp.
                self.warning.configure(text="WARNING: High Pass Filter: Be sure that... fs < fp.")
                self.warning.place(x=700,y=520)
                return
        if(self.filter_type == "band pass"):
            if(not (float(self.fs_val.get()) < float(self.fp_val.get()) and float(self.fp_val.get()) < float(self.fp1_val.get()) and float(self.fp1_val.get()) < float(self.fs1_val.get()))):
                self.warning.configure(text="WARNING: Band Pass Filter: Be sure that... fs- < fp- < fp+ < fs+.")
                self.warning.place(x=700,y=520)
                return
        if(self.filter_type == "band stop"):
            if(not (float(self.fp_val.get()) < float(self.fs_val.get()) and float(self.fs_val.get()) < float(self.fs1_val.get()) and float(self.fs1_val.get()) < float(self.fp1_val.get()))):
                self.warning.configure(text="WARNING: Band Stop Filter: Be sure that... fp- < fs- < fs+ < fp+.")
                self.warning.place(x=700,y=520)
                return

        #si todo esta bien en las especificaciones, se borra el mensaje de error y se completa el tercer paso.
        self.warning.place_forget()
        self.step = 3
        self.reset_button_color()
        self.b_graph.configure(bg="olive drab")
        self.b_screen1.configure(bg="olive drab")

        if(self.filter_type == "low pass" or self.filter_type == "high pass"):
            self.approx_F.Datos(self.approx_type, float(self.Ap_val.get()), float(self.As_val.get()), float(self.fp_val.get())*2*math.pi, float(self.fs_val.get())*2*math.pi)
        
        num, den = self.approx_F.Aproximacion()
        print("\n\n\n",num,"\n\n\n",den,"\n\n\n")
        print(type(num),type(den),"\n\n\n")
        print(type([1,2,3]))
        num = 1.002377
        den = [4.0314418*10**-9, 5.0700715*10**-6, 0.00318814, 1.002377]
        self.H = signal.TransferFunction(num, den)
        w, self.mag, self.phase = signal.bode(self.H) #el w está en rad/seg.
        self.f = w/(2*math.pi) #convierto a Hz.
        self.stepT, self.stepMag = signal.step(self.H)
        self.impT, self.impMag = signal.impulse(self.H)

        self.plot_attenuation()
        self.update_screen() #refrezca los botones para que aparezcan los botones para elegir la página y el plot que se desee.
        
    def set_screen1(self): #actualiza la página para setear la página uno (donde estan las especificaciones y plots)
        if(self.screen != 0):
            self.screen = 0
            self.update_screen()
            self.reset_button_color()
            self.b_screen1.configure(bg="olive drab")    
            self.plot_attenuation()
            
    def set_screen2(self): #actualiza la página para setear la página dos (donde estan las etapas)
        if(self.screen != 1):
            self.screen = 1
            self.update_screen()
            self.reset_button_color()
            self.b_screen2.configure(bg="olive drab")
            self.plot_zp()

    def create_stage(self):
        if(self.zlist.curselection() == () or self.plist.curselection() == ()):
            self.warning.configure(text="WARNING: Select a valid item from the listboxes.")
            self.warning.place(x=700,y=520)
            return
        if(self.zlist.curselection()[0] == len(self.zlist_val) and self.plist.curselection()[0] == len(self.plist_val)):
            self.warning.configure(text="WARNING: Select a valid item from the listboxes.")
            self.warning.place(x=700,y=520)
            return
        if(self.zlist_val[self.zlist.curselection()[0]].sel == 1 or self.plist_val[self.plist.curselection()[0]].sel == 1):
            self.warning.configure(text="WARNING: An used item was selected.")
            self.warning.place(x=700,y=520)
            return
        self.warning.place_forget()
        self.zlist_val[self.zlist.curselection()[0]].sel = 1
        self.plist_val[self.plist.curselection()[0]].sel = 1
        self.update_listboxes()

    def set_stages(self):
        print("hi")
            
    def __init__(self): #función de inicialización. (constructor)
        #se inicializan varibles, botones, textos, labels, etc.
        self.step = 0
        self.filter_type = "none"
        self.approx_type = "none"
        self.screen = 0

        window = tk.Tk()
        window.title("CIRCUITS THEORY")
        window.geometry("1200x600+50+50")
        window.configure(bg="gray64")

        graph = tk.Canvas(window)
        graph.place(x=10, y=50) #plotea el plot.

        self.fig = Figure()
        self.plt = self.fig.add_subplot(1,1,1) #los dos primeros parámetros le da una escala a la figura (mientras más grandes son los parámetros, mas chico será la figura). El tercero le da la posición en el window.
        self.axes = self.fig.gca()
        self.data_plt = FigureCanvasTkAgg(self.fig, master=graph)
        self.data_plt._tkcanvas.pack(padx = 2, pady = 2) #plotea el plot.

        self.approx_F = AproximadorFiltro()

        self.text1 = tk.Label(window, font=("arial",10,"bold"), text="Choose a Filter:",bg="gray64")
        self.text2 = tk.Label(window, font=("arial",10,"bold"), text="Choose an Approximation:",bg="gray64")
        self.text3 = tk.Label(window, font=("arial",10,"bold"), text="Set the Specifications:",bg="gray64")

        self.Ap = tk.Label(window, font=("arial",10), text="Ap = ",bg="gray64")
        self.fp = tk.Label(window, font=("arial",10), bg="gray64")
        self.As = tk.Label(window, font=("arial",10), text="As = ",bg="gray64")
        self.fs = tk.Label(window, font=("arial",10), bg="gray64")
        self.fp1 = tk.Label(window, font=("arial",10), text="fp+ = ",bg="gray64")
        self.fs1 = tk.Label(window, font=("arial",10), text="fs+ = ",bg="gray64")
        self.Ap_val = tk.Entry(window, width = 10)
        self.fp_val = tk.Entry(window, width = 10)
        self.fp1_val = tk.Entry(window, width = 10)
        self.As_val = tk.Entry(window, width = 10)
        self.fs_val = tk.Entry(window, width = 10)
        self.fs1_val = tk.Entry(window, width = 10)
        
        self.warning = tk.Label(window, font=("arial",10,"bold"),bg="gray64",fg="red")        
        
        self.b_attenuation = tk.Button(window,text="Attenuation (Bode)",command=self.plot_attenuation)
        self.b_phase = tk.Button(window,text="Phase (Bode)",command=self.plot_phase)
        self.b_zp = tk.Button(window,text="Zeros & Poles",command=self.plot_zp)
        self.b_step = tk.Button(window,text="Step Response",command=self.plot_step)
        self.b_impulse = tk.Button(window,text="Impulse Response",command=self.plot_impulse)

        self.b_LP = tk.Button(window,text="Low Pass",command=self.set_low_pass)
        self.b_HP = tk.Button(window,text="High Pass",command=self.set_high_pass)
        self.b_BP = tk.Button(window,text="Band Pass",command=self.set_band_pass)
        self.b_BS = tk.Button(window,text="Band Stop",command=self.set_band_stop)

        self.b_butter = tk.Button(window,text="Butterworth",command=self.set_butter)
        self.b_cheby_I = tk.Button(window,text="Chebyshev I",command=self.set_cheby_I)
        self.b_cheby_II = tk.Button(window,text="Chebyshev II",command=self.set_cheby_II)
        self.b_bess = tk.Button(window,text="Bessel",command=self.set_bess)

        self.b_graph = tk.Button(window,text="GRAPH!",command=self.start_graph)
        self.b_screen1 = tk.Button(window,text="View Filter",command=self.set_screen1)
        self.b_screen2 = tk.Button(window,text="View Stages",command=self.set_screen2)

        self.zp = tk.Label(window, font=("arial",10,"bold"), text="Zeros\t\t\tpoles",bg="gray64")
        self.zlist = tk.Listbox(window, selectbackground="olive drab",width = 20,height=5,exportselection=0)
        self.plist = tk.Listbox(window, selectbackground="olive drab",width = 20,height=5,exportselection=0)

        self.b_c_stage = tk.Button(window,text="Set Up Stage",command=self.create_stage)
        self.b_s_stages = tk.Button(window,text="Automatic Set Up",command=self.set_stages)

        self.reset_button_color()
        self.update_screen()
        
        window.mainloop() #sigue corriendo el programa hasta que se cierra la ventana.

if __name__ == "__main__":
    ex = Gui() #aca se llama la clase y se la ejecuta.
