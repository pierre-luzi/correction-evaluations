from tkinter import Frame, Label, Button, StringVar, Entry, Listbox, Scrollbar
from tkinter import messagebox, simpledialog, filedialog
from tkinter import BOTH, LEFT, RIGHT, END, X, Y, DISABLED, NORMAL
from tkinter.ttk import Notebook
from gui.frames.classes.liste_classes import ListeClassesFrame
from gui.frames.classes.gestion_classes import GestionClassesFrame
from gui.frames.classes.liste_eleves import ListeElevesFrame
from gui.frames.classes.gestion_eleves import GestionElevesFrame
from logic.classe import classe
from logic.classes_manager import ClassesManager
from logic.eleve import eleve

class ClassesView(Frame):
    """
        Classe pour créer une frame permettant la création
        et la gestion des classes et des élèves.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.classe = classe
        self.eleve = eleve
        self.classe.__init__()
        self.eleve.__init__()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        
        #----- frame pour la gestion des classes -----
        self.liste_classes = ListeClassesFrame(self)
        self.liste_classes.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")        
        
        self.gestion_classes = GestionClassesFrame(self.liste_classes)
        self.gestion_classes.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        #----- frame pour la gestion des élèves -----
        self.liste_eleves = ListeElevesFrame(self)
        self.liste_eleves.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.gestion_eleves = GestionElevesFrame(self.liste_eleves)
        self.gestion_eleves.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        
        #----- événements -----
        self.liste_classes.bind("<<SelectClasse>>", self.select_classe)
        self.gestion_classes.bind("<<DeleteClasse>>", self.supprimer_classe)
        self.gestion_classes.bind("<<CreateClasse>>", self.charger_classes)
        self.liste_eleves.bind("<<SelectEleve>>", self.select_eleve)
        self.gestion_eleves.bind("<<AddEleve>>", self.charger_eleves)
        self.gestion_eleves.bind("<<DeleteEleve>>", self.supprimer_eleve)

    def charger_classes(self, event):
        """
            Actions lors du chargement des classes.
        """
        self.liste_classes.charger()
        self.charger_eleves()
    
    def select_classe(self, event):
        """
            Actions lors de la sélection d'une classe.
        """
        self.charger_eleves()
        self.gestion_classes.bouton_supprimer.config(state=NORMAL)
        self.gestion_eleves.bouton_ajouter.config(state=NORMAL)
        self.gestion_eleves.bouton_importer.config(state=NORMAL)
        self.gestion_eleves.bouton_supprimer.config(state=DISABLED)
    
    def supprimer_classe(self, event):
        """
            Actions lors de la suppression d'une classe.
        """
        self.liste_classes.charger()
        self.charger_eleves()
        self.gestion_classes.bouton_supprimer.config(state=DISABLED)
        self.gestion_eleves.bouton_ajouter.config(state=DISABLED)
        self.gestion_eleves.bouton_importer.config(state=DISABLED)
        self.gestion_eleves.bouton_supprimer.config(state=DISABLED)
    
    def charger_eleves(self, event=None):
        """
            Affiche la liste des élèves de la classe sélectionnée.
        """
        self.liste_eleves.charger()
    
    def select_eleve(self, event):
        """
            Sélectionne un élève dans la liste de la classe.
        """
        self.gestion_eleves.bouton_supprimer.config(state=NORMAL)
    
    def supprimer_eleve(self, event):
        """
            Actions lors de la suppression d'un élève.
        """
        self.charger_eleves()
        self.gestion_eleves.bouton_supprimer.config(state=DISABLED)