from tkinter import Frame, Label, StringVar
from tkinter.ttk import Spinbox

class BaremeFrame(Frame):
    """
        Classe pour créer une frame qui gère le barême de l'évaluation pour
        la rédaction et affiche le barême total.
        Argument :
            - evaluation : objet de la classe EvaluationsManager
            permettant la gestion des évaluations.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.evaluation = self.master.evaluation
        
        label_redaction = Label(self, text="Barême pour la rédaction :")
        label_redaction.grid(row=0, column=0, sticky="w")
        
        self.valeur_redaction = StringVar()
        self.valeur_redaction.set(self.evaluation.bareme_redaction)
        bareme_redaction = Spinbox(
            self,
            from_=0.0, to=5.0, increment=0.5,
            textvariable=self.valeur_redaction,
            width=5,
            format="%.1f",
            command=self.set_bareme_redaction
        )
        bareme_redaction.grid(row=0, column=1, sticky="w")
        
        self.label_bareme = Label(self)
        self.label_bareme.grid(row=1, column=0, sticky="w")
        self.calculer_bareme()
    
    def set_bareme_redaction(self, *args):
        self.evaluation.set_bareme_redaction(self.valeur_redaction.get())
        self.calculer_bareme()
        
    def calculer_bareme(self):
        bareme = self.evaluation.calculer_bareme()
        self.label_bareme.config(text=f"Barème de l'évaluation : {bareme}")
    
    def update(self):
        self.valeur_redaction.set(self.evaluation.bareme_redaction)
        self.calculer_bareme()