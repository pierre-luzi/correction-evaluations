from tkinter import Frame, Label, Button, StringVar, Entry, Listbox, Scrollbar, Text, Canvas
from tkinter import messagebox, simpledialog
from tkinter import BOTH, LEFT, RIGHT, END, X, Y, DISABLED, NORMAL
from tkinter.ttk import Combobox, Spinbox
from gui.autoscrollbar import AutoScrollbar
from gui.frames.exercices.liste_exercices import ListeExercicesFrame
from gui.frames.exercices.gestion_exercices import GestionExercicesFrame
from gui.frames.exercices.creation_exercice import CreationExerciceFrame
from logic.exercice import exercice
from logic.exercices_manager import ExercicesManager

class ExercicesView(Frame):
    """
        Classe pour créer une frame permettant la création
        et la gestion des exercices et des questions.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.exercice = exercice
        self.exercice.__init__()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=5)
                
        #----- frame pour la gestion des exercices -----
        self.frame_liste = ListeExercicesFrame(self)
        self.frame_liste.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.frame_liste.bind("<<SelectExercice>>", self.select_exercice)
        
        #----- création et suppression des exercices -----
        self.frame_gestion = GestionExercicesFrame(self.frame_liste)
        self.frame_gestion.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.frame_gestion.bind("<<CreateExercice>>", self.creer_exercice)
        self.frame_gestion.bind("<<DeleteExercice>>", self.supprimer_exercice)
        
        #----- conception de l'exercice -----
        self.frame_exercice = None
    
    def select_exercice(self, event):
        """
            Sélectionne un exercice dans la liste.
        """
        if self.frame_exercice == None:
            self.afficher_gestion_exercices()
        self.frame_exercice.charger_questions()
        self.frame_gestion.bouton_supprimer.config(state=NORMAL)
    
    def afficher_gestion_exercices(self):
        """
            Affiche la frame de gestion de l'exercice.
        """
        self.frame_exercice = CreationExerciceFrame(self)
        self.frame_exercice.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
    
    def cacher_gestion_exercices(self):
        """
            Cache la frame de gestion de l'exercice.
        """
        self.frame_exercice.destroy()
        self.frame_exercice = None
    
    def creer_exercice(self, event):
        """
            Crée un nouvel exercice.
        """
        self.frame_liste.charger_exercices()
    
    def supprimer_exercice(self, event):
        """
            Supprime l'exercice sélectionné.
        """
        self.frame_liste.charger_exercices()
        self.cacher_gestion_exercices()