from tkinter import Frame, Label, Listbox
from tkinter import END
from gui.autoscrollbar import AutoScrollbar
from logic.classes_manager import ClassesManager

class ListeElevesFrame(Frame):
    """
        Classe pour créer une frame affichant la liste des élèves.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.classe = self.master.classe
        self.eleve = self.master.eleve

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        label = Label(self, text="Liste des élèves")
        label.grid(row=0, column=0, padx=10, pady=0, sticky="w")
        
        frame_liste = Frame(self)
        frame_liste.grid(row=1, column=0, padx=10, sticky="nsew")
        frame_liste.grid_columnconfigure(0, weight=1)        

        self.listbox = Listbox(frame_liste, height=25, exportselection=False)
        self.listbox.grid(row=1, column=0, sticky="nsew")

        eleves_scrollbar = AutoScrollbar(frame_liste, orient="vertical", command=self.listbox.yview)
        eleves_scrollbar.grid(row=1, column=1, sticky="ns")
        
        self.listbox.config(yscrollcommand=eleves_scrollbar.set)
        self.listbox.bind("<<ListboxSelect>>", self.select)
    
    def select(self, event):
        """
            Sélectionne un élève dans la liste de la classe.
        """
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            nom = event.widget.get(index)
            self.eleve.set(self.classe.id, nom)
            self.event_generate("<<SelectEleve>>")
    
    def charger(self):
        """
            Affiche la liste des élèves de la classe sélectionnée.
        """
        self.listbox.delete(0, END)
        if not self.classe.id == None:
            noms = self.classe.lister_eleves()
            for nom in noms:
                self.listbox.insert(END, nom)