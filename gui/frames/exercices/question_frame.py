from tkinter import Frame, StringVar, Text, Label
from tkinter import font
from tkinter.ttk import Spinbox

class QuestionFrame(Frame):
    """
        Classe pour créer une frame affichant les informations
        d'une question.
        Argument :
            - question : tuple contenant le numéro, la réponse et
            le barème de la question.
    """
    def __init__(self, master, question):
        super().__init__(master)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        
        label = Label(self, text=f"Question {question[0]}")
        label.grid(row=0, column=0, sticky="w")
        
        #----- réponse à la question -----        
        self.reponseA = Text(self, height=5, font=font.Font(size=14), wrap="word")
        self.reponseA.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")    
        self.reponseA.insert(1.0, question[1])
        
        self.reponseB = Text(self, height=5, font=font.Font(size=14), wrap="word")
        self.reponseB.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")    
        self.reponseB.insert(1.0, question[2])
        
        #----- barème de la question -----
        self.valeur_bareme = StringVar()
        self.valeur_bareme.set(f"{question[3]:.2f}")
        bareme = Spinbox(self, from_=0.0, to=5.0, increment=0.25, textvariable=self.valeur_bareme, width=5, format="%.2f")
        bareme.grid(row=1, column=2, padx=10, pady=5, sticky="e")