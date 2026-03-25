from random import randint
import tkinter as tk
from tkinter import messagebox as mess
from datetime import *
from math import floor

nomeFile = "domande.txt"
nomeFileHistory = "history.txt"
bgMain = "#E0F7FA"
bgPuls = "#29B6F6"
fgPuls = "#81D4FA"
bgIO = "#B3E5FC"
fgIO = "#0D47A1"
totalWidth = 1000
totalHeigth = 700
tempo = 20*60

class Simulatore(tk.Frame):
    i : int
    risposteGiuste : list
    risposteSbagliate : list
    risposte : dict

    def __init__(self):
        super().__init__(bg="light green")
        self.master.geometry(f"{totalWidth}x{totalHeigth}")
        self.master.title("Simulatore patente")
        self.master.config(bg="light green")
        self.master.resizable(0,0)
        self.grid()
        self.crea()
        self.caricaDomande()
        self.quizInCorso = False
    
    def crea(self):
        self.titolo = tk.Label(self,text="Simulatore patente 2026")
        self.titolo.grid(row=0,column=0,columnspan=2,padx=totalWidth/2-50,pady=20)
        self.start = tk.Button(self,text="Inizia il quiz",command=self.start,width=10,height=2,bg=bgPuls)
        self.start.grid(row=1,column=0,columnspan=2,pady=10)
        self.esci = tk.Button(self,text="Esci",command=self.master.destroy,fg="#d1666f",width=10)
        self.esci.grid(row=4,column=0,columnspan=2)
        self.master.bind("6",self.clear)
        self.master.bind("Enter",self.start)

    
    def creaQuiz(self):
        self.domanda = tk.Label(self,text=self.domande[self.i].get("domanda"))
        self.domanda.grid(row=3,column=0,pady=50,columnspan=2)
        self.vero = tk.Button(self,text="V",command=self.veroQuiz,bg="#98c379")
        self.vero.grid(row=4,column=0)
        self.falso = tk.Button(self,text="F",command=self.falsoQuiz,bg="#e06b74")
        self.falso.grid(row=4,column=1)
        self.numero = tk.Label(self,text=f"1/{self.numeroDomande}")
        self.numero.grid(row=2,column=0,columnspan=2)
        self.sinistra = tk.Button(self,text="<-",command=self.vaiSinistra)
        self.sinistra.grid(row=5,column=0)
        self.destra = tk.Button(self,text="->",command=self.vaiDestra)
        self.destra.grid(row=5,column=1)
        self.tempoL = tk.Label(self,text="20:00")
        self.tempoL.grid(row=6,column=0,columnspan=2)
        self.master.bind("v",self.veroQuiz)
        self.master.bind("f",self.falsoQuiz)
        self.master.bind("<Left>",self.vaiSinistra)
        self.master.bind("<Right>",self.vaiDestra)
        self.tempoR = tempo
        self.after(100,self.timer)

    def vaiDestra(self,e):
        if self.i == self.numeroDomande-1:
            return
        self.i += 1
        self.aggiornaQuiz()

    def vaiSinistra(self,e):
        if self.i == 0:
            return
        self.i -= 1
        self.aggiornaQuiz()

    def aggiornaQuiz(self):
        self.domanda.config(text=self.domande[self.i].get("domanda"))
        self.numero.config(text=f"{self.i+1}/{self.numeroDomande}")

    def falsoQuiz(self,e):
        self.verifica(False)

    def veroQuiz(self,e):
        self.verifica(True)
    
    def verifica(self,ris):
        self.risposte.update({self.i:ris})
        self.vaiDestra(None)
    
    def stopQuiz(self):
        risp = True
        if len(self.risposte) != 30:
            risp = mess.askyesno("Fine","Concludere l'esame anche se non si hanno fatto tutte e 30 le domande?")
        if risp:
            for i in range(len(self.risposte)):
                if self.domande[i].get("risposta") == self.risposte.get(i):
                    self.risposteGiuste.append(self.domande[i])
                else:
                    self.risposteSbagliate.append(self.domande[i])
            
            if len(self.risposte) > 0:
                mess.showinfo("Quiz",f"Quiz giusti: {len(self.risposteGiuste)}/{len(self.risposte)}")
                self.i = 0
                self.spiegazione()
            else:
                mess.showinfo("Quiz","Non hai fatto nessuna domanda")

            for i in [self.domanda,self.vero,self.falso,self.numero,self.destra,self.sinistra,self.tempoL]:
                i.destroy()
            
            self.quizInCorso = False
            self.esci.config(command=self.master.destroy)
            self.salvaHistory()
    
    def spiegazione(self):
        if self.i == len(self.risposteSbagliate):
            return
        mess.askokcancel(f"Risposte errate",f"Domanda {self.i+1} / {len(self.risposteSbagliate)}\n{self.risposteSbagliate[self.i].get("domanda")}\n\nInvece è {self.traduzioneVF(self.risposteSbagliate[self.i].get("risposta"))}")
        self.i+=1
        self.spiegazione()

    def start(self):
        if self.quizInCorso:
            return
        self.numeroDomande = 30
        self.getDomande(self.numeroDomande)
        self.i = 0
        self.risposteSbagliate = []
        self.risposteGiuste = []
        self.risposte = {}
        self.creaQuiz()
        self.quizInCorso = True
        self.esci.config(command=self.stopQuiz)
    
    def clear(self,e):
        with open(nomeFileHistory,"w") as fl:
            fl.write("")

    def caricaDomande(self):
        domande = []
        with open(nomeFile,"r") as fl:
            co = fl.readlines()
            for i in co:
                cont = i.split(":")
                dom = cont[0].strip()
                ris = bool(cont[1].strip())
                domande.append({"domanda":dom,"risposta":ris})
        self.everyDomande = domande
    
    def salvaHistory(self):
        if len(self.risposte) == 0:
            return
        data = datetime.now()
        with open(nomeFileHistory,"a") as fl:
            fl.write(f"Quiz in data {data}\nRisposte giuste: {len(self.risposteGiuste)} su {len(self.risposte)}\n")
            fl.write(f"Domande: \n")
            for i in range(len(self.risposte)):
                ris = self.risposte[i]
                dom = self.domande[i].get("domanda")
                fl.write(f"{dom} -> Hai risposto {self.traduzioneVF(ris)} {self.traduzioneEmoji(ris and self.domande[i].get("risposta"))}\n")
            fl.write("\n")
    
    def traduzioneVF(self,inp):
        return "Vero" if inp else "Falso"

    def traduzioneEmoji(self,inp):
        return "✅" if inp else "❌"
    
    def getDomande(self,n = 30):
        nums = []
        ris = []
        for i in range(n):
            while True:
                random = randint(0,len(self.everyDomande)-1)
                if random not in nums:
                    ris.append(self.everyDomande[random])
                    break
            nums.append(random)
        self.domande = ris

    def timer(self):
        if self.tempoR >= 0 and self.quizInCorso:
            minuti = floor(self.tempoR / 60)
            secondi = self.tempoR - minuti * 60
            self.tempoL.config(text=f"{minuti}:{secondi}")
            self.tempoR -= 1
            self.after(1000,self.timer)
    
