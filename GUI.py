#TP4 Teoria de Cirucitos.

import math
import matplotlib
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk as toolbar
from matplotlib.figure import Figure
from scipy import signal #para realizar plots.

class View:
    def plot_attenuation(self):
        self.plt.clear()
        self.plt.semilogx(self.w,(-1)*self.mag)
        self.fig.suptitle("Attenuation (Bode)")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Frequency (Hz)") #"$Frequency (Hz)$" -> con los '$' se cambia la letra a cursiva.
        self.plt.set_ylabel("Attenuation (dB)") #_{out} -> pone out en letra chica y abajo.
        self.dataPlot.draw()

    def plot_phase(self): #define función, la cual recibe self.
        self.plt.clear()
        self.plt.semilogx(self.w,self.phase)
        self.fig.suptitle("Phase (Bode)")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Frequency (Hz)")
        self.plt.set_ylabel("Phase (Deg)")
        self.dataPlot.draw()

    def plot_zp(self):
        self.plt.clear()
        self.plt.scatter(self.H.zeros.real,self.H.zeros.imag, marker = 'o', color = "red")
        self.plt.scatter(self.H.poles.real,self.H.poles.imag, marker = 'x', color = "blue")   
        self.fig.suptitle("Zeros & Poles")    
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Real Part")
        self.plt.set_ylabel("Imaginary Part")
        self.dataPlot.draw()

    def plot_step(self): #respuesta al escalon u(t).
        self.plt.clear() #simpre limpiar antes de dibujar.
        self.plt.plot(self.stepT,self.stepMag) #stepT -> tiempo. stepMag -> tension de la respuesta al escalon
        self.fig.suptitle("Step Response")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Time (sec)")
        self.plt.set_ylabel("Voltage (V)")
        self.dataPlot.draw()

    def plot_impulse(self): #respuesta al impulso (delta de dirac)
        self.plt.clear()
        self.plt.plot(self.impT,self.impMag) #impT -> tiempo. impMag -> tension de la respuesta al impulso
        self.fig.suptitle("Impulse Response")
        self.plt.grid(color="black",linestyle='-',linewidth=0.1)
        self.plt.set_xlabel("Time (sec)")
        self.plt.set_ylabel("Voltage (V)")
        self.dataPlot.draw()        

    def __init__(self): #función de inicialización. (constructor)
        self.step = 0
        self.filter_type = "none"

        window = tk.Tk()
        window.title("CIRCUITS THEORY")
        window.geometry("1200x600+0+0")
        window.configure(bg="gray64")

        view = tk.Frame(window, width=700, heigh=600,bg="gray64")
        view.pack(side=tk.LEFT, padx = 2, pady = 2) #dibuja el view donde iran los botones. si esto no se dibuja, tampoco los botones.

        menu = tk.Frame(window, width=500, heigh=600,bg="gray64")
        menu.pack(padx = 2, pady = 2)

        b_view = tk.Frame(view, width=700, heigh=100,bg="gray64")

        b_view.pack(padx = 2, pady = 2)

        filter_ = tk.Frame(menu, width=500, heigh=100,bg="gray64")
        filter_.pack(padx = 2, pady = 2)

        approximation = tk.Frame(menu, width=500, heigh=100,bg="gray64")
        approximation.pack(padx = 2, pady = 2)

        specification1 = tk.Frame(menu, width=500, heigh=100,bg="gray64")
        specification1.pack(padx = 2, pady = 2)

        specification2 = tk.Frame(menu, width=500, heigh=100,bg="gray64")
        specification2.pack(padx = 2, pady = 2)

        ##################################################

        graph = tk.Canvas(view)
        graph.pack(padx = 2, pady = 2) #dibuja el plot.

        b_attenuation = tk.Button(b_view,text="Attenuation (Bode)",command=self.plot_attenuation)
        b_attenuation.pack(side = tk.LEFT, padx = 2, pady = 2)
        b_phase = tk.Button(b_view,text="Phase (Bode)",command=self.plot_phase)
        b_phase.pack(side = tk.LEFT, padx = 2, pady = 2)
        b_zp = tk.Button(b_view,text="Zeros & Poles",command=self.plot_zp)
        b_zp.pack(side = tk.LEFT, padx = 2, pady = 2)
        b_step = tk.Button(b_view,text="Step Response",command=self.plot_step)
        b_step.pack(side = tk.LEFT, padx=2, pady=2)
        b_impulse = tk.Button(b_view,text="Impulse Response",command=self.plot_impulse)
        b_impulse.pack(side = tk.LEFT, padx=2, pady=2)

        self.fig = Figure()
        self.plt = self.fig.add_subplot(1,1,1) #los dos primeros parámetros le da una escala a la figura (mientras más grandes son los parámetros, mas chico sera la figura). El tercero le da la posición en el window.
        self.H = signal.TransferFunction([1,7,4],[1,2,7,9])
        self.w, self.mag, self.phase = signal.bode(self.H) #el w está en rad/seg.
        self.w = self.w/(2*math.pi) #convierto a Hz.
        self.stepT, self.stepMag = signal.step(self.H)
        self.impT, self.impMag = signal.impulse(self.H)
        self.dataPlot = FigureCanvasTkAgg(self.fig, master=graph)
        self.dataPlot._tkcanvas.pack(padx = 2, pady = 2) #dibuja el plot.

        ##################################################

        text1 = tk.Label(filter_, font=("arial",10,"bold"), text="Choose a Filter:",bg="gray64")
        text1.pack(padx = 2, pady = 2)

        b_LP = tk.Button(filter_,text="Low Pass",command=self.plot_attenuation)
        b_LP.pack(side = tk.LEFT, padx = 2, pady = 2)
        b_HP = tk.Button(filter_,text="High Pass",command=self.plot_phase)
        b_HP.pack(side = tk.LEFT, padx = 2, pady = 2)
        b_BP = tk.Button(filter_,text="Band Pass",command=self.plot_zp)
        b_BP.pack(side = tk.LEFT, padx = 2, pady = 2)
        b_BS = tk.Button(filter_,text="Band Stop",command=self.plot_step)
        b_BS.pack(side = tk.LEFT, padx = 2, pady = 2)

        text2 = tk.Label(approximation, font=("arial",10,"bold"), text="Choose an Approximation:",bg="gray64")
        text2.pack(padx = 2, pady = 2)

        b_butter = tk.Button(approximation,text="Butterworth",command=self.plot_attenuation,)
        b_butter.pack(side = tk.LEFT, padx = 2, pady = 2)
        b_cheby_1 = tk.Button(approximation,text="Chebyshev I",command=self.plot_phase)
        b_cheby_1.pack(side = tk.LEFT, padx = 2, pady = 2)
        b_cheby_2 = tk.Button(approximation,text="chebyshev II",command=self.plot_zp)
        b_cheby_2.pack(side = tk.LEFT, padx = 2, pady = 2)
        b_bessel = tk.Button(approximation,text="Bessel",command=self.plot_step)
        b_bessel.pack(side = tk.LEFT, padx = 2, pady = 2)

        text3 = tk.Label(specification1, font=("arial",10,"bold"), text="Set the Specifications:",bg="gray64")
        text3.pack(padx = 2, pady = 2)

        Ap = tk.Label(specification1, font=("arial",10), text="Ap = ",bg="gray64")
        Ap.pack(side=tk.LEFT, padx = 2, pady = 2)
        Ap_v = tk.Entry(specification1)
        Ap_v.pack(side=tk.LEFT, padx = 2, pady = 2)
        wp = tk.Label(specification1, font=("arial",10), text="wp = ",bg="gray64")
        wp.pack(side=tk.LEFT, padx = 2, pady = 2)
        wp_v = tk.Entry(specification1)
        wp_v.pack(side=tk.LEFT, padx = 2, pady = 2)

        As = tk.Label(specification2, font=("arial",10), text="As = ",bg="gray64")
        As.pack(side=tk.LEFT, padx = 2, pady = 2)
        As_v = tk.Entry(specification2)
        As_v.pack(side=tk.LEFT, padx = 2, pady = 2)
        ws = tk.Label(specification2, font=("arial",10), text="ws = ",bg="gray64")
        ws.pack(side=tk.LEFT, padx = 2, pady = 2)
        ws_v = tk.Entry(specification2)
        ws_v.pack(side=tk.LEFT, padx = 2, pady = 2)

        window.mainloop() #sigue corriendo el programa hasta que se cierra la ventana.

if __name__ == "__main__":
    ex = View() #aca se llama la clase y se la ejecuta.