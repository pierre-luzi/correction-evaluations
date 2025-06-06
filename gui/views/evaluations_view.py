from tkinter import Frame, Label, StringVar, Button
from tkinter import END, NORMAL, DISABLED
from tkinter import messagebox
from tkinter.ttk import Combobox
from gui.frames.classes.liste_classes import ListeClassesFrame
from gui.frames.evaluations.liste_evaluations import ListeEvaluationsFrame
from gui.frames.evaluations.gestion_evaluations import GestionEvaluationsFrame
from gui.frames.evaluations.creation_evaluation import CreationEvaluationFrame
from gui.frames.exercices.liste_exercices import ListeExercicesFrame
from logic.classe import classe
from logic.classes_manager import ClassesManager
from logic.evaluation import evaluation
from logic.exercice import exercice
from logic.exercices_manager import ExercicesManager
from sqlite3 import IntegrityError

class EvaluationsView(Frame):
    """
        Vue pour la gestion et la modification des évaluations.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.classe = classe
        self.evaluation = evaluation
        self.exercice = exercice
        self.classe.__init__()
        self.evaluation.__init__()
        self.exercice.__init__()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        
        #----- frame pour la sélection des classes -----
        liste_classes = ListeClassesFrame(self)
        liste_classes.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        liste_classes.bind("<<SelectClasse>>", self.select_classe)
        
        #----- frame pour la sélection des exercices -----
        liste_exercices = ListeExercicesFrame(self)
        liste_exercices.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        liste_exercices.set_listbox_height(25)
        liste_exercices.bind("<<SelectNiveau>>", self.select_niveau)
        liste_exercices.bind("<<SelectExercice>>", self.select_exercice)
        
        self.ajout_exercice = Button(liste_exercices, text="Ajouter à l'évaluation", command=self.ajouter_exercice)
        self.ajout_exercice.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ajout_exercice.config(state=DISABLED)
        
        #----- frame pour la gestion des évaluations
        self.liste_evaluations = ListeEvaluationsFrame(self)
        self.liste_evaluations.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.liste_evaluations.bind("<<SelectEvaluation>>", self.select_evaluation)
        
        self.gestion_evaluations = GestionEvaluationsFrame(self.liste_evaluations)
        self.gestion_evaluations.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        self.gestion_evaluations.bind("<<CreateEvaluation>>", self.creer_evaluation)
        self.gestion_evaluations.bind("<<DeleteEvaluation>>", self.supprimer_evaluation)
        self.gestion_evaluations.bind("<<SaveEvaluation>>", self.enregistrer_evaluation)
        
        #----- frame pour la création des évaluations -----
        self.creation_evaluation = None
        
    def select_classe(self, event):
        """
            Actions lors de la sélection d'une classe.
        """
        self.cacher_evaluation()
        self.evaluation.__init__()
        self.liste_evaluations.charger_evaluations()
        self.gestion_evaluations.activer_creation()
        self.gestion_evaluations.desactiver_suppression()
        self.gestion_evaluations.desactiver_enregistrer()
        self.ajout_exercice.config(state=DISABLED)
    
    def select_niveau(self, event):
        """
            Actions lors de la sélection d'un niveau.
        """
        self.liste_exercices.charger_exercices()
    
    def select_exercice(self, event):
        """
            Actions lors de la sélection d'un exercice.
        """
        if not self.evaluation.id == None:
            self.ajout_exercice.config(state=NORMAL)
    
    def select_evaluation(self, event):
        """
            Actions lors de la sélection d'une évaluation.
        """
        if self.creation_evaluation == None:
            self.afficher_evaluation()
        else:
            self.creation_evaluation.update()
        self.gestion_evaluations.activer_suppression()
        self.gestion_evaluations.activer_enregistrer()
        if not self.exercice.id == None:
            self.ajout_exercice.config(state=NORMAL)
    
    def creer_evaluation(self, event):
        """
            Actions lors de la création d'une évaluation.
        """
        self.liste_evaluations.charger_evaluations()
    
    def supprimer_evaluation(self, frame):
        """
            Actions lors de la suppression d'une évaluation.
        """
        self.liste_evaluations.charger_evaluations()
        self.gestion_evaluations.desactiver_suppression()
        self.gestion_evauations.desactiver_enregistrer()
        self.ajout_exercice.confif(state=DISABLED)
    
    def enregistrer_evaluation(self, event):
        """
            Enregistrer l'évaluation.
        """
        self.evaluation.enregistrer()
    
    def ajouter_exercice(self):
        """
            Ajouter un exercice à l'évaluation.
        """
        try:
            evaluation.ajouter_exercice(exercice.id)
            self.creation_evaluation.update()
        except IntegrityError:
            messagebox.showwarning("Erreur", "L'exercice est déjà inclus dans l'évaluation.")
    
    def afficher_evaluation(self):
        """
            Afficher le frame permettant la création de l'évaluation.
        """
        self.creation_evaluation = CreationEvaluationFrame(self, self.evaluation)
        self.creation_evaluation.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
    
    def cacher_evaluation(self):
        """
            Cacher le frame permettant la création de l'évaluation.
        """
        if not self.creation_evaluation == None:
            self.creation_evaluation.destroy()
            self.creation_evaluation = None