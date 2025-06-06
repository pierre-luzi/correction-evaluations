from tkinter import Frame, Label, IntVar, Radiobutton

class CorrectionCompetencesFrame(Frame):
    """
        Classe permettant de créer la frame dans laquelle les compétences
        de l'élève sont évaluées.
    """
    def __init__(self, master, parent):
        super().__init__(master, highlightbackground="black", highlightthickness=1)
        
        #----- initialisation des attributs -----
        self.classe = parent.classe
        self.eleve = parent.eleve
        self.evaluation = parent.evaluation
        
        Label(self, text="A").grid(row=0, column=1)
        Label(self, text="B").grid(row=0, column=2)
        Label(self, text="C").grid(row=0, column=3)
        Label(self, text="D").grid(row=0, column=4)
        
        self.competences = self.evaluation.lister_competences()
        self.vars = []
        i = 1
        for competence in self.competences:
            label = Label(self, text=competence, justify="left", wraplength=500)
            label.grid(row=i, column=0, sticky="w")
            
            var = IntVar()
            var.set(3)
            self.vars.append(var)
            
            R1 = Radiobutton(self, variable=var, value=3)
            R2 = Radiobutton(self, variable=var, value=2)
            R3 = Radiobutton(self, variable=var, value=1)
            R4 = Radiobutton(self, variable=var, value=0)
            
            R1.grid(row=i, column=1)
            R2.grid(row=i, column=2)
            R3.grid(row=i, column=3)
            R4.grid(row=i, column=4)            
            
            i += 1
    
    def enregistrer(self):
        pass