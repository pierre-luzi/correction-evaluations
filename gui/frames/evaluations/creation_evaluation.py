from tkinter import Frame, Label, Button, Listbox
from tkinter import BOTH, LEFT, RIGHT, END, X, Y, DISABLED, NORMAL
from gui.autoscrollbar import AutoScrollbar
from gui.frames.evaluations.bareme_frame import BaremeFrame
from gui.frames.evaluations.competences_notebook import CompetencesNotebook

class CreationEvaluationFrame(Frame):
    """
        Classe pour créer une frame qui gère les paramètres d'une évaluation.
    """
    def __init__(self, master, evaluation):
        super().__init__(master, highlightbackground="black", highlightthickness=1)
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)
        
        self.evaluation = evaluation
        
        liste_exercices = Frame(self)
        liste_exercices.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        liste_exercices.grid_columnconfigure(1, weight=1)
        
        label_exercices = Label(liste_exercices, text="Liste des exercices de l'évaluation")
        label_exercices.grid(row=0, column=0, sticky="w")
        
        self.listbox_exercices = Listbox(liste_exercices, height=5, exportselection=0)
        self.listbox_exercices.grid(row=1, column=0, sticky="ew")
                
        scrollbar_exercices = AutoScrollbar(liste_exercices, orient="vertical", command=self.listbox_exercices.yview)
        scrollbar_exercices.grid(row=0, column=1, sticky="ns")

        self.listbox_exercices.config(yscrollcommand=scrollbar_exercices.set)

        self.frame_bareme = BaremeFrame(self)
        self.frame_bareme.grid(row=1, column=1, sticky="nsew")
        
        self.notebook_competences = CompetencesNotebook(self)
        self.notebook_competences.grid(row=2, column=0, columnspan=3, sticky="nsew")
        
        self.charger_exercices()
        self.after_idle(self.update_idletasks)
        
    def charger_exercices(self):
        """
            Affiche la liste des exercices.
        """
        self.listbox_exercices.delete(0, END)
        exercices = self.evaluation.lister_exercices()
        for exercice in exercices:
            self.listbox_exercices.insert(END, exercice)
    
    def update(self):
        """
            Met à jour l'affichage de la frame.
        """
        self.charger_exercices()
        self.frame_bareme.update()
        self.notebook_competences.update()
    
    def enregistrer(self):
        """
            Enregistre l'évaluation.
        """
        self.notebook_competences.enregistrer()