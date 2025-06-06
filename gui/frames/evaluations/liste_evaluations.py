from tkinter import Frame, Label, Listbox
from tkinter import messagebox, simpledialog
from tkinter import END, DISABLED, NORMAL
from gui.autoscrollbar import AutoScrollbar

class ListeEvaluationsFrame(Frame):
    """
        Classe pour créer une frame affichant la liste des classes.
        Argument :
            - classes_manager : objet de la classe ClassesManager.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.classe = self.master.classe
        self.evaluation = self.master.evaluation
        self.grid_columnconfigure(0, weight=1)
                
        label_evaluations = Label(self, text="Liste des évaluations")
        label_evaluations.grid(row=0, column=0, padx=10, pady=0, sticky="w")

        #----- conteneur pour la liste des évaluations -----
        frame_liste = Frame(self)
        frame_liste.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        frame_liste.grid_columnconfigure(0, weight=1)
        
        self.listbox = Listbox(frame_liste, height=5, exportselection=0)
        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.listbox.focus_set()

        scrollbar = AutoScrollbar(frame_liste, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind("<<ListboxSelect>>", self.select_evaluation)
        
        self.charger_evaluations()
    
    def charger_evaluations(self):
        """
            Affiche la liste des évaluations.
        """
        self.listbox.delete(0, END)
        noms = self.classe.lister_evaluations()
        for nom in noms:
            self.listbox.insert(END, nom)
    
    def select_evaluation(self, event):
        """
            Sélectionne une classe.
        """
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            titre = event.widget.get(index)
            self.evaluation.set(self.classe.id, titre)
            self.event_generate("<<SelectEvaluation>>")