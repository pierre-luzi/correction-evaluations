from tkinter import Frame, Scrollbar, Canvas, IntVar, Checkbutton
from tkinter import BOTH, LEFT, RIGHT, END, X, Y, DISABLED, NORMAL
from gui.autoscrollbar import AutoScrollbar
from logic.competences_manager import CompetencesManager

class CompetencesFrame(Frame):
    """
        Classe pour créer une frame qui affiche la liste des compétences
        d'une catégorie donnée.
    """
    def __init__(self, master, categorie):
        super().__init__(master)
        
        self.evaluation = self.master.evaluation
        self.categorie = categorie
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        #----- Canvas permettant le défilement vertical -----
        self.canvas = Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = AutoScrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.frame_competences = Frame(self.canvas)
        self.frame_competences_id = self.canvas.create_window((0, 0), window=self.frame_competences, anchor="nw")
        self.frame_competences.grid_columnconfigure(0, weight=1)
        
        def update_scrollregion(event):
            self.canvas.after_idle(
                lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            )
        
        self.frame_competences.bind("<Configure>", update_scrollregion)
        
        def resize_frame(event):
            width = event.width
            if self.canvas.cget("yscrollcommand"):
                width -= 15  # marge pour la scrollbar
            self.canvas.itemconfig(self.frame_competences_id, width=width)       
        
        self.canvas.bind("<Configure>", resize_frame)
        
        #----- liste des compétences -----
        i = 0
        self.checkbuttons = []
        
        for competence in CompetencesManager.lister_competences(self.categorie):
            var = IntVar()
            var.set(self.evaluation.chercher_competence(competence))
            cbx = Checkbutton(
                self.frame_competences,
                text=competence, variable=var,
                onvalue=1, offvalue=0,
                anchor="w", justify="left", wraplength=200,
                command=lambda comp=competence, var=var: change(comp, var)
            )
            cbx.grid(row=i, column=0, sticky="w")
            self.checkbuttons.append((competence, var))
            i += 1
        
        def change(competence, var):
            if var.get():
                self.evaluation.ajouter_competence(competence)
            else:
                self.evaluation.supprimer_competence(competence)
            
        def ajuster_wraplength(event):
            """
                Ajuste la longueur wraplength des étiquettes des
                checkboxes.
            """
            for widget in self.frame_competences.winfo_children():
                if isinstance(widget, Checkbutton):
                    widget.configure(wraplength=event.width - 20)
                    
        self.frame_competences.bind("<Configure>", ajuster_wraplength)
        
        self.after_idle(self.update_idletasks)
    
    def update(self):
        for competence, var in self.checkbuttons:
            var.set(self.evaluation.chercher_competence(competence))            