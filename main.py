from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as msb
from ctypes import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from glob import glob
import os


window = Tk()
window.title("iLOGGER Mangue Baja")
window.geometry('450x140')
photo = PhotoImage(file = 'icone_window.png')
window.wm_iconphoto(False, photo)


def grafico():

    if txt5.get() and ":/" in txt5.get():
        df = pd.read_csv(txt5.get())
        tabela1 = df.set_index('f1')
        tabela2 = df.set_index('f2')
        f1 = tabela1.index.values
        f2 = tabela2.index.values

        vel_bruto = []
        rot_bruto = []
        rel = []
        cont = 0
        for i in range(int(len(f1) / 10)):
            rot_bruto.append(sum(f2[i * 10:i * 10 + 10]))
            vel_bruto.append(sum(f1[i * 10:i * 10 + 10]))

        raio = 0.29  # em milímetros
        if txt4.get().isnumeric():
            furos_do_disco_de_freio = int(txt4.get())
            msb.showinfo("Disco de Freio","Usando quantidade de furos no disco = {}".format(furos_do_disco_de_freio))
            txt4.delete(0, "end")
        else:
            furos_do_disco_de_freio = 24
            msb.showerror("ERRO", "Quantidade inválida, configurando para padrão de 24 furos!")
            txt4.delete(0, "end")


        rot = [j * 20 * 60 for j in rot_bruto]
        vel = [i * 2 * raio * 3.1415 * 20 * 3.6 / furos_do_disco_de_freio for i in vel_bruto]
        # vel = [i * 0.584 * 3.1415 * 20 * 3.6 / 24 for i in vel_bruto]

        t = np.linspace(0, 0.05 * len(f1) / 10, int(len(f1) / 10))
        data = {
            'RPM': rot,
            'vel': vel}
        csv = pd.DataFrame(data, columns=['RPM', 'vel'])
        csv.to_csv('AV_data.csv')

        b, a = signal.butter(4, 0.10, analog=False)
        impulse = np.zeros(1000)
        impulse[500] = 1
        imp_ff = signal.filtfilt(b, a, impulse)
        imp_lf = signal.lfilter(b, a, signal.lfilter(b, a, impulse))

        # PLOT_ROTAÇÃO
        sig_rot = signal.filtfilt(b, a, rot)
        plt.plot(t, rot, color='silver', label='Original')
        plt.plot(t, sig_rot, color='#3465a4', label='Filtrado')
        plt.grid(True, which='both')
        plt.legend(loc="best")
        plt.xlabel('tempo (s)')
        plt.ylabel('RPM')
        plt.title("Rotação do Motor")
        plt.show()

        c, d = signal.butter(4, 0.15, analog=False)
        impulse = np.zeros(1000)
        impulse[500] = 1
        imp_ff = signal.filtfilt(c, d, impulse)
        imp_lf = signal.lfilter(c, d, signal.lfilter(c, d, impulse))

        # PLOT_VELOCIDADE
        sig_vel = signal.filtfilt(c, d, vel)
        plt.plot(t[50:340], vel[50:340], color='silver', label='Original')
        plt.plot(t[50:340], sig_vel[50:340], color='#3465a4', label='Filtrado')
        plt.grid(True, which='both')
        plt.legend(loc="best")
        plt.xlabel('tempo (s)')
        plt.ylabel('Km/h')
        plt.title("Velocidade")
        plt.show()

        # PLOT_RPM_VELOCIDADE
        plt.plot(sig_vel[5:350], sig_rot[5:350], marker='o', linestyle='--', color='b')
        plt.xlabel('Km/h')
        plt.ylabel('RPM')
        plt.minorticks_on()
        plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
        plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        plt.title("Rotação por Velocidade")
        # plt.savefig('Vel x Rot.jpeg')
        plt.show()

        data = {
            'RPM': sig_rot,
            'vel': sig_vel}
        csv = pd.DataFrame(data, columns=['RPM', 'vel'])
        csv.to_csv('AV_filt.csv')

        tabela3 = df.set_index('lsmaccx')
        tabela4 = df.set_index('lsmaccy')
        tabela5 = df.set_index('lsmaccz')

        accx = tabela3.index.values * 0.00036
        accy = tabela4.index.values * 0.00036
        accz = tabela5.index.values * 0.00036
        t1 = np.linspace(0, 0.005 * len(f1), len(f1))
        e, f = signal.butter(4, 0.007, analog=False)

        sig_accx = signal.filtfilt(e, f, accx)
        sig_accy = signal.filtfilt(e, f, accy)
        sig_accz = signal.filtfilt(e, f, accz)
    else:
        msb.showerror("ERRO", "O Caminho acima é inválido")


def file_select():
    filename = fd.askopenfilename()
    if ".csv" in filename:
        txt5.delete(0, "end")
        txt5.insert(0, filename)
    else:
        msb.showerror("ERRO", "Arquivo Inválido!")
        txt5.delete(0, "end")


def path_select():
    pathname = fd.askdirectory()
    txt2.delete(0, "end")
    txt2.insert(0, pathname)


def runs_select():
    pathname = fd.askdirectory()
    files = glob(os.path.join(pathname, "RUN*"))
    if files:
        txt1.delete(0, "end")
        txt1.insert(0, pathname)
    else:
        msb.showerror("ERRO", "O diretório selecionado não possui nenhuma RUN!")
        txt1.delete(0, "end")


def generate_csv():
    cfunctions = CDLL("./libshared_read_object.dll")
    if txt1.get() and txt2.get() and (":/" in txt2.get()) and txt3.get().isnumeric():
        cfunctions.read_struct(txt1.get().encode("utf8"), txt2.get().encode("utf8"), int(txt3.get()))
    elif not(txt3.get().isnumeric()):
        msb.showerror("ERRO", "Você digitou algo inválido para ser lido!")
        txt3.delete(0, "end")
    else:
        msb.showerror("ERRO", "Algum dos caminhos acima está inválido!")


# ------------------- FIRST LINE -------------------
lbl1 = Label(window, text="Selecione o diretório das RUNs:")
lbl1.grid(column=0, row=0)
txt1 = Entry(window, width=30)
txt1.grid(column=1, row=0)
txt1.focus()
btn1 = Button(window, text="Procurar", command=runs_select)
btn1.grid(column=2, row=0)
# ------------------- FIRST LINE -------------------

# ------------------- SECOND LINE -------------------
lbl2 = Label(window, text="Selecione um diretório para salvar:")
lbl2.grid(column=0, row=1)
txt2 = Entry(window, width=30)
txt2.grid(column=1, row=1)
txt2.focus()
btn2 = Button(window, text="Procurar", command=path_select)
btn2.grid(column=2, row=1)
# ------------------- SECOND LINE -------------------

# ------------------- THIRD LINE -------------------
lbl3 = Label(window, text="Digite o número da RUN:")
lbl3.grid(column=0, row=2)
txt3 = Entry(window, width=30)
txt3.grid(column=1, row=2)
txt3.focus()
btn3 = Button(window, text="Gerar CSV", command=generate_csv)
btn3.grid(column=2, row=2)
# ------------------- THIRD LINE -------------------

# ------------------- FOURTH LINE -------------------
lbl4 = Label(window, text="Número de furos no disco de freio:")
lbl4.grid(column=0, row=3)
txt4 = Entry(window, width=30)
txt4.grid(column=1, row=3)
txt4.focus()
# ------------------- FOURTH LINE -------------------

# ------------------- FIFTH LINE -------------------
lbl5 = Label(window, text="Selecione o arquivo para plot:")
lbl5.grid(column=0, row=4)
txt5 = Entry(window, width=30)
txt5.grid(column=1, row=4)
txt5.focus()
btn5 = Button(window, text="Procurar", command=file_select)
btn5.grid(column=2, row=4)
btn6 = Button(window, text="Plotar Gráficos", command=grafico)
btn6.grid(column=1, row=5)
# ------------------- FIFTH LINE -------------------

window.mainloop()
