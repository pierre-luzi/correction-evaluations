from tkinter import Frame, Label
from tkinter import font
from logic.exercice import Exercice
from gui.frames.correction.correction_question import CorrectionQuestionFrame

class CorrectionExerciceFrame(Frame):
    """
        Classe pour créer une frame permettant de corriger un exercice.
    """
    def __init__(self, container, parent, titre):
        super().__init__(container)
        
        self.eleve = parent.eleve
        self.evaluation = parent.evaluation
        self.exercice = Exercice()
        self.exercice.set_exercice(titre)
        
        self.grid_columnconfigure(0, weight=1)
        
        label = Label(self, text=titre, font=font.Font(size=24),)
        label.grid(row=0, column=0, padx=5, sticky="")
        
        self.liste_frames_question = []
    
    def charger_questions(self):
        """
            Affiche les questions de l'exercice sélectionné.
        """
        for frame in self.liste_frames_question:
            frame.destroy()
            self.liste_frames_question = []

        questions = self.exercice.get_questions()

        for question in questions:
            self.afficher_question(question[0])
    
    def afficher_question(self, numero):
        label = Label(self, text=f"Question {numero}")
        label.grid(row=2*numero-1, column=0, padx=10, pady=2, sticky="w")
        frame = CorrectionQuestionFrame(self, numero)
        frame.grid(row=2*numero, column=0, padx=5, pady=5, sticky="ew")
        self.grid_rowconfigure(2*numero, weight=1)
        self.liste_frames_question.append(frame)
    
    def enregistrer(self):
        for frame in self.liste_frames_question:
            frame.enregistrer()