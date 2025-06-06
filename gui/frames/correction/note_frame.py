from tkinter import Frame, IntVar, Label, Radiobutton

NOTE_WIDTH = 130

class NoteFrame(Frame):
    """
        Classe pour créer une frame permettant d'indiquer la note
        de l'élève à une question.
    """
    def __init__(self, master, width=NOTE_WIDTH):
        super().__init__(master, width=width)
        
        self.grid_propagate(True)
        self.configure(width=NOTE_WIDTH)
                        
        #----- initialisation des attributs -----
        self.eleve = master.eleve
        self.evaluation = master.evaluation
        self.question = master.question
        self.correction = master.correction
        
        label = Label(self, text="Note")
        label.grid(row=0, column=0)
        
        #----- création des radio buttons -----
        self.var = IntVar()
        self.var.set(int(self.correction.note*100))
        
        R1 = Radiobutton(self, text="0 %", variable=self.var, value=0, command=self.change_radiobutton)
        R2 = Radiobutton(self, text="25 %", variable=self.var, value=25, command=self.change_radiobutton)
        R3 = Radiobutton(self, text="50 %", variable=self.var, value=50, command=self.change_radiobutton)
        R4 = Radiobutton(self, text="75 %", variable=self.var, value=75, command=self.change_radiobutton)
        R5 = Radiobutton(self, text="100 %", variable=self.var, value=100, command=self.change_radiobutton)
        
        R1.grid(row=1, column=0, padx=5, sticky="w")
        R2.grid(row=2, column=0, padx=5, sticky="w")
        R3.grid(row=3, column=0, padx=5, sticky="w")
        R4.grid(row=4, column=0, padx=5, sticky="w")
        R5.grid(row=5, column=0, padx=5, sticky="w")
    
    def change_radiobutton(self):
        """
            Lors d'une modification des radio buttons, modifie la note.
        """
        self.correction.note = self.var.get()/100.