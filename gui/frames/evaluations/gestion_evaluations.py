from tkinter import Frame, Button
from tkinter import messagebox, simpledialog
from tkinter import END, DISABLED, NORMAL
from gui.autoscrollbar import AutoScrollbar
from logic.classe import classe
from logic.classes_manager import ClassesManager
from logic.corrige_evaluation import CorrigeEvaluation
from logic.resultats import Resultats

class GestionEvaluationsFrame(Frame):
    """
        Classe pour créer une frame permettant de gérer les évaluations.
        Argument :
            - classes_manager : objet de la classe ClassesManager ;
            - evaluation : objet de la classe EvaluationsManager.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.classe = self.master.classe
        self.evaluation = self.master.evaluation
        self.resultats = Resultats()
        
        self.bouton_creer = Button(self, text="Créer une évaluation", command=self.creer)
        self.bouton_creer.grid(row=0, column=0, sticky="ew")
        self.bouton_creer.config(state=DISABLED)
        
        self.bouton_supprimer = Button(self, text="Supprimer l'évaluation", command=self.supprimer)
        self.bouton_supprimer.grid(row=1, column=0, sticky="ew")
        self.bouton_supprimer.config(state=DISABLED)
        
        self.bouton_enregistrer = Button(self, text="Enregistrer l'évaluation", command=self.enregistrer)
        self.bouton_enregistrer.grid(row=2, column=0, sticky="ew")
        self.bouton_enregistrer.config(state=DISABLED)
        
        self.bouton_correction = Button(self, text="Générer le corrigé", command=self.correction)
        self.bouton_correction.grid(row=3, column=0, sticky="ew")
        self.bouton_correction.config(state=DISABLED)
        
        self.bouton_auto_correction = Button(self, text="Évaluer l'auto-correction", command=self.evaluer_auto_correction)
        self.bouton_auto_correction.grid(row=4, column=0, sticky="ew")
        self.bouton_auto_correction.config(state=DISABLED)
                               
    def creer(self):
        """
            Crée une nouvelle évaluation.
        """
        if self.classe.id == None:
            messagebox.showwarning("Erreur", "Aucune classe sélectionnée")
            return
        titre = simpledialog.askstring("Créer une évaluation", "Titre de l'évaluation :")
        try:
            self.classe.creer_evaluation(titre)
            self.event_generate("<<CreateEvaluation>>")
        except ValueError as error:
            messagebox.showwarning("Erreur", str(error))
    
    def supprimer(self):
        """
            Supprime l'évaluation sélectionnée.
        """
        if self.evaluation.id == None:
            messagebox.showwarning("Erreur", "Aucune évaluation sélectionnée")
            return
        confirm = messagebox.askyesno("Supprimer l'évaluation", f"Êtes-vous sûr de vouloir supprimer l'évaluation {self.evaluation.titre} ?")
        if confirm:
            self.evaluation.supprimer()
            self.bouton_supprimer.config(state=DISABLED)
            self.event_generate("<<DeleteEvaluation>>")
    
    def enregistrer(self):
        self.event_generate("<<SaveEvaluation>>")
    
    def correction(self):
        corrige = CorrigeEvaluation(self.evaluation, self.classe)
        corrige.generer_corrige()
    
    def evaluer_auto_correction(self):
        self.resultats.set_evaluation(self.evaluation, self.classe)
        self.resultats.generer()
    
    def activer_creation(self):
        self.bouton_creer.config(state=NORMAL)
    
    def desactiver_creation(self):
        self.bouton_creer.config(state=DISABLED)
    
    def activer_suppression(self):
        self.bouton_supprimer.config(state=NORMAL)
    
    def desactiver_suppression(self):
        self.bouton_supprimer.config(state=DISABLED)
    
    def activer_enregistrer(self):
        self.bouton_enregistrer.config(state=NORMAL)
    
    def desactiver_enregistrer(self):
        self.bouton_enregistrer.config(state=DISABLED)
    
    def activer_correction(self):
        self.bouton_correction.config(state=NORMAL)
    
    def desactiver_correction(self):
        self.bouton_correction.config(state=DISABLED)
    
    def activer_auto_correction(self):
        self.bouton_auto_correction.config(state=NORMAL)
    
    def desactiver_auto_correction(self):
        self.bouton_auto_correction.config(state=DISABLED)