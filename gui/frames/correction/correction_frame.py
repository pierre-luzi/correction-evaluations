from tkinter import Frame, Button, Canvas, Label
from tkinter import BOTH, LEFT, RIGHT, END, X, Y, DISABLED, NORMAL
from gui.autoscrollbar import AutoScrollbar
from gui.frames.correction.correction_exercice import CorrectionExerciceFrame
from gui.frames.correction.correction_competences import CorrectionCompetencesFrame

class CorrectionFrame(Frame):
    """
        Classe permettant de créer la frame dans laquelle l'évaluation
        est corrigée pour un élève.
    """
    def __init__(self, master):
        super().__init__(master, highlightbackground="black", highlightthickness=1)
        
        #----- initialisation des attributs -----
        self.classe = master.classe
        self.eleve = master.eleve
        self.evaluation = master.evaluation
        self.liste_frames_correction = []
        
        #----- configuration de la grille -----
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # canvas
        self.grid_columnconfigure(1, weight=0)  # scrollbar
        
        #----- création d'une frame scrollable -----
        self.canvas = Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = AutoScrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.frame_correction = Frame(self.canvas)
        self.frame_correction_id = self.canvas.create_window((0, 0), window=self.frame_correction, anchor="nw")
        self.frame_correction.grid_columnconfigure(0, weight=1)
        
        def update_scrollregion(event):
            self.canvas.after_idle(
                lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            )
        
        self.frame_correction.bind("<Configure>", update_scrollregion)
        
        def resize_frame(event):
            width = event.width
            if self.canvas.cget("yscrollcommand"):
                width -= 15  # marge pour la scrollbar
            self.canvas.itemconfig(self.frame_correction_id, width=width)       
        
        self.canvas.bind("<Configure>", resize_frame)
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())  # Pour que le canvas capte les scrolls
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
                
    def _on_mousewheel(self, event):
        """
            Permet le défilement du canvas au trackpad.
        """
        direction = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(direction, "units")
        
    def charger(self):
        self.liste_frames_correction = []
        
        # ajout des exercices
        i = 0
        for titre in self.evaluation.lister_exercices():
            frame_exercice = CorrectionExerciceFrame(self.frame_correction, self, titre)
            frame_exercice.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            frame_exercice.charger_questions()
            self.liste_frames_correction.append(frame_exercice)
            i += 1
        
        # compétences et rédaction
        frame_competences = CorrectionCompetencesFrame(self.frame_correction, self)
        frame_competences.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
        self.liste_frames_correction.append(frame_competences)
    
    def enregistrer(self):
        for frame in self.liste_frames_correction:
            frame.enregistrer()