from tkinter import Frame, StringVar, Button
from tkinter import NORMAL, DISABLED
from tkinter.ttk import Combobox
from logic.classes_manager import ClassesManager

class SelectionFrame(Frame):
    """
        Classe pour créer une frame permettant de sélectionner
        l'évaluation corrigée et l'élève.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.classe = master.classe
        self.evaluation = master.evaluation
        self.eleve = master.eleve
        
        #----- sélection de la classe -----
        self.classe_var = StringVar()
        self.classe_var.set("Choisir une classe")
        self.combobox_classe = Combobox(self, textvariable=self.classe_var, state="readonly")
        self.combobox_classe.grid(row=0, column=0, padx=10, sticky="w")
        self.combobox_classe['values'] = tuple(ClassesManager.lister())
        self.combobox_classe.bind("<<ComboboxSelected>>", self.select_classe)
        
        #----- sélection de l'évaluation -----
        self.evaluation_var = StringVar()
        self.evaluation_var.set("Sélectionner une évaluation")
        self.combobox_evaluation = Combobox(self, textvariable=self.evaluation_var, state="readonly")
        self.combobox_evaluation.grid(row=0, column=1, padx=10, sticky="w")
        self.combobox_evaluation.config(state=DISABLED)
        self.combobox_evaluation.bind("<<ComboboxSelected>>", self.select_evaluation)
        
        #----- sélection de l'élève ------
        self.eleve_var = StringVar()
        self.eleve_var.set("Sélectionner un élève")
        self.combobox_eleve = Combobox(self, textvariable=self.eleve_var, state="readonly")
        self.combobox_eleve.grid(row=0, column=2, padx=10, sticky="w")
        self.combobox_eleve.config(state=DISABLED)
        self.combobox_eleve.bind("<<ComboboxSelected>>", self.select_eleve)
        
        #----- enregistrer -----
        self.bouton_enregistrer = Button(self, text="Enregistrer", command=self.enregistrer)
        self.bouton_enregistrer.grid(row=0, column=3, sticky="e")
        self.bouton_enregistrer.config(state=DISABLED)
    
    def select_classe(self, event):
        """
            Action lors de la sélection d'une classe.
        """
        self.classe.set(self.classe_var.get())
        
        self.evaluation_var.set("Sélectionner une évaluation")
        self.combobox_evaluation['values'] = tuple(self.classe.lister_evaluations())
        self.combobox_evaluation.config(state=NORMAL)
        
        self.eleve_var.set("Sélectionner un élève")
        self.combobox_eleve['values'] = tuple(self.classe.lister_eleves())
        self.combobox_eleve.config(state=NORMAL)
        
        self.event_generate("<<HideCorrection>>")
        self.bouton_enregistrer.config(state=DISABLED)
    
    def select_evaluation(self, event):
        """
            Action lors de la sélection d'une évluation.
        """
        self.evaluation.set(self.classe.id, self.evaluation_var.get())
        if not self.eleve.id == None:
            self.afficher_correction()
    
    def select_eleve(self, event):
        """
            Action lors de la sélection d'un élève.
        """
        self.eleve.set(self.classe.id, self.eleve_var.get())
        if not self.evaluation.id == None:
            self.afficher_correction()
    
    def afficher_correction(self):
        """
            Affichage de la correction.
        """
        self.event_generate("<<DisplayCorrection>>")
        self.bouton_enregistrer.config(state=NORMAL)
    
    def enregistrer(self):
        """
            Enregistre la correction.
        """
        self.event_generate("<<Save>>")