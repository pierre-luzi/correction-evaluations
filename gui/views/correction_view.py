from tkinter import Frame, Label, Button
from tkinter import END, NORMAL, DISABLED
from tkinter import messagebox
from tkinter.ttk import Combobox
from logic.classe import Classe
from logic.evaluation import Evaluation
from logic.eleve import Eleve
from gui.frames.correction.selection_frame import SelectionFrame
from gui.frames.correction.correction_frame import CorrectionFrame


class CorrectionView(Frame):
    """
        Vue permettant la correction d'une évaluation.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.classe = Classe()
        self.eleve = Eleve()
        self.evaluation = Evaluation()
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        #----- frame pour la sélection de l'évaluation et de l'élève -----
        self.frame_selection = SelectionFrame(self)
        self.frame_selection.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.frame_selection.bind("<<DisplayCorrection>>", self.afficher_correction)
        self.frame_selection.bind("<<HideCorrection>>", self.cacher_correction)
        self.frame_selection.bind("<<Save>>", self.enregistrer)
        
        #----- frame pour la correction -----
        self.correction_frame = None
        
    def afficher_correction(self, event):
        if not self.correction_frame == None:
            self.correction_frame.destroy()
        self.correction_frame = CorrectionFrame(self)
        self.correction_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.correction_frame.charger()
    
    def cacher_correction(self, event):
        if not self.correction_frame == None:
            self.correction_frame.destroy()
    
    def enregistrer(self, event):
        self.correction_frame.enregistrer()