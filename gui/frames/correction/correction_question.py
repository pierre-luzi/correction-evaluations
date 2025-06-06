from tkinter import Frame, Text, Label
from tkinter import font
from gui.frames.correction.erreurs_frame import ErreursFrame
from gui.frames.correction.erreurs_frame import ERREUR_WIDTH
from gui.frames.correction.note_frame import NoteFrame
from gui.frames.correction.note_frame import NOTE_WIDTH
from logic.question import Question
from logic.correction import Correction

class CorrectionQuestionFrame(Frame):
    """
        Frame permettant de corriger une question.
    """
    def __init__(self, master, numero):
        super().__init__(master)
        
        self.eleve = master.eleve
        self.evaluation = master.evaluation
        self.exercice = master.exercice
        
        self.question = Question()
        self.correction = Correction()
        self.question.set(self.exercice.id, numero)
        self.correction.set(self.eleve.id, self.evaluation.id, self.question.id)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=ERREUR_WIDTH)
        self.grid_columnconfigure(2, weight=0, minsize=NOTE_WIDTH)
        
        #----- commentaire sur la réponse de l'élève -----
        label_commentaire = Label(self, text="Commentaire")
        label_commentaire.grid(row=0, column=0, padx=5, sticky="w")
        self.commentaire = Text(self, height=5, font=font.Font(size=14), wrap="word")
        self.commentaire.grid(row=1, column=0, padx=5, pady=0, sticky="nsew")  
        if not self.correction.commentaire == None:              
            self.commentaire.insert(1.0, f"{self.correction.commentaire}")
        
        #----- frame listant les erreurs possibles -----
        label_erreurs = Label(self, text="Erreurs")
        label_erreurs.grid(row=0, column=1, padx=5, sticky="w")
        self.frame_erreurs = ErreursFrame(self)
        self.frame_erreurs.grid(row=1, column=1, padx=5, pady=0, sticky="nsew")
        
        #----- frame pour noter la question -----
        label_note = Label(self, text="Note")
        label_note.grid(row=0, column=2, padx=5, sticky="w")
        self.frame_note = NoteFrame(self, width=80)
        self.frame_note.grid(row=1, column=2, padx=5, pady=0, sticky="ew")
    
    def enregistrer(self):
        """
            Enregistre la correction de la question.
        """
        self.correction.commentaire = self.commentaire.get('1.0', 'end-1c')
        self.correction.enregistrer()