from random import randint
import tkinter as tk
from tkinter import messagebox as mess
from datetime import *

nomeFile = "domande.txt"
nomeFileHistory = "history.txt"
colori = {
    "null":"#f9dbbd",
    "bgLabel":"#fca17d",
    "bgMain":"#da627d",
    "bgPuls":"#9a348e",
    "fgMain":"#0d0628",
    "Red": "#FF0000",
    "White":"#FFFFFF",
    "Green":"#00FF00"
}

totalWidth = 1000
totalHeigth = 700
belFont = ("Times",14)
#https://coolors.co/f9dbbd-fca17d-da627d-9a348e-0d0628

class Simulatore(tk.Frame):
    i : int
    risposteGiuste : list
    risposteSbagliate : list
    risposte : dict

    def __init__(self):
        super().__init__(bg=colori["bgMain"])
        self.master.geometry(f"{totalWidth}x{totalHeigth}")
        self.master.title("Simulatore patente")
        self.master.config(bg=colori["bgMain"])
        self.master.resizable(0,0)
        self.grid()
        self.creaHome()
        self.caricaDomande()
        self.quizInCorso = False
        self.nStandard = 30
        self.tStandard = 20*60
    
    def creaHome(self):
        self.titolo = tk.Label(self,text="Simulatore patente 2026",font=belFont,height=2,bg=colori["bgLabel"],fg=colori["fgMain"],border=10)
        self.titolo.grid(row=0,column=0,columnspan=4,padx=totalWidth/2-100,pady=20)
        self.start = tk.Button(self,text="Inizia il quiz",command=lambda : self.startQuiz(self.nStandard,self.tStandard),width=10,height=2,bg=colori["bgPuls"],fg=colori["White"],border=0,font=belFont)
        self.start.grid(row=1,column=0,pady=10)
        self.startInf = tk.Button(self,text="Mega quiz",command=lambda : self.startQuiz(len(self.everyDomande),30*60),fg=colori["White"],width=10,border=0,height=2,bg=colori["bgPuls"],font=belFont)
        self.startInf.grid(row=1,column=3,pady=10)
        self.esci = tk.Button(self,text="Esci",command=self.master.destroy,fg=colori["Red"],width=10,font=belFont,border=5)
        self.esci.grid(row=6,column=0,columnspan=4)
        self.master.bind("cl",self.clear)
        self.master.bind("s",lambda x:self.startQuiz(self.nStandard,self.tStandard))
        self.master.bind("<Escape>",lambda x:self.master.destroy())

    def creaQuiz(self):
        self.domanda = tk.Label(self,text=self.domande[self.i].get("domanda"),font=belFont,bg=colori["bgMain"])
        self.domanda.grid(row=3,column=0,pady=50,columnspan=4)
        self.vero = tk.Button(self,text="V",command=lambda : self.verifica(True),bg=colori["Green"],font=belFont)
        self.vero.grid(row=4,column=1)
        self.falso = tk.Button(self,text="F",command=lambda : self.verifica(False),bg=colori["Red"],font=belFont)
        self.falso.grid(row=4,column=2)
        self.numero = tk.Label(self,text=f"1/{self.numeroDomande}",font=belFont,bg=colori["bgLabel"],height=2,width=5)
        self.numero.grid(row=1,column=1)
        self.sinistra = tk.Button(self,text="<-",command=lambda: self.vaiSinistra(None),font=belFont)
        self.sinistra.grid(row=5,column=1,pady=10)
        self.destra = tk.Button(self,text="->",command=lambda: self.vaiDestra(None),font=belFont)
        self.destra.grid(row=5,column=2,pady=10)
        self.tempoL = tk.Label(self,text=f"{self.tStandard//60:02}:{00}",font=belFont,bg=colori["bgLabel"],height=2,width=5)
        self.tempoL.grid(row=1,column=2)
        self.esci.config(command=self.stopQuiz)

        

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

    def aggiornaQuiz(self):     #Per passare alla prossima domanda
        self.domanda.config(text=self.domande[self.i].get("domanda"))
        self.numero.config(text=f"{self.i+1}/{self.numeroDomande}")

    def verifica(self,ris):     #Verifica la risposta
        self.risposte.update({self.i:ris})
        self.vaiDestra(None)
    
    def stopQuiz(self):     # Ferma l'esame facendo la correzione,salvataggio e ritorno alla home page
        risp = True
        if len(self.risposte) != self.numeroDomande:
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
            self.master.bind("<Escape>",lambda x: self.master.destroy())
            self.salvaHistory()
    
    def spiegazione(self):  #Spiega le risposte sbagliate
        if self.i == len(self.risposteSbagliate):
            return
        mess.askokcancel(f"Risposte errate",f"Domanda {self.i+1} / {len(self.risposteSbagliate)}\n{self.risposteSbagliate[self.i].get("domanda")}\n\nInvece è {self.traduzioneVF(self.risposteSbagliate[self.i].get("risposta"))}")
        self.i+=1
        self.spiegazione()

    def startQuiz(self,k,tem):        
        if self.quizInCorso:
            return
        self.numeroDomande = k
        self.getDomande(self.numeroDomande)
        self.i = 0
        self.risposteSbagliate = []
        self.risposteGiuste = []
        self.risposte = {}
        self.creaQuiz()
        self.quizInCorso = True
        self.master.bind("<Escape>",lambda x: self.stopQuiz())
        self.master.bind("v",lambda x: self.verifica(True))
        self.master.bind("f",lambda x: self.verifica(False))
        self.master.bind("<Left>",self.vaiSinistra)
        self.master.bind("<Right>",self.vaiDestra)
        self.tempoR = tem
        self.after(100,self.timer)
        
    
    def clear(self,e):  #Pulisce il file di history
        with open(nomeFileHistory,"w") as fl:
            fl.write("")

    def caricaDomande(self):    #Carica le domande in una lista di dicts
        domande = []
        with open(nomeFile,"r") as fl:
            co = fl.readlines()
            for i in co:
                cont = i.split(":")
                dom = cont[0].strip()
                ris = cont[1].strip() == "True"
                domande.append({"domanda":dom,"risposta":ris})
        self.everyDomande = domande
    
    def salvaHistory(self):     #Salva l'esame fatto nella history
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
            minuti = self.tempoR // 60
            secondi = self.tempoR % 60
            self.tempoL.config(text=f"{minuti:02}:{secondi:02}")
            self.tempoR -= 1
            self.after(1000,self.timer)
    
