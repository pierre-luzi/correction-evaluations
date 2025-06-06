from tkinter import Frame, Label, Listbox
from tkinter import messagebox, simpledialog
from tkinter import END, DISABLED, NORMAL
from gui.autoscrollbar import AutoScrollbar
from logic.classes_manager import ClassesManager

class ListeClassesFrame(Frame):
    """
        Classe pour créer une frame affichant la liste des classes.
        Argument :
            - classes_manager : objet de la classe ClassesManager.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.classe = self.master.classe
        self.grid_columnconfigure(0, weight=1)
                
        label_classes = Label(self, text="Liste des classes")
        label_classes.grid(row=0, column=0, padx=10, pady=0, sticky="w")

        #----- conteneur pour la liste des classes -----
        frame_liste = Frame(self)
        frame_liste.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")
        frame_liste.grid_columnconfigure(0, weight=1)
        
        self.listbox = Listbox(frame_liste, height=5, exportselection=0)
        self.listbox.grid(row=0, column=0, sticky="nsew")

        scrollbar = AutoScrollbar(frame_liste, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind("<<ListboxSelect>>", self.select)
        
        self.charger()
    
    def charger(self):
        """
            Affiche la liste des classes.
        """
        self.listbox.delete(0, END)
        noms = ClassesManager.lister()
        for nom in noms:
            self.listbox.insert(END, nom)
    
    def select(self, event):
        """
            Sélectionne une classe.
        """
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            nom = event.widget.get(index)
            self.classe.set(nom)
            self.event_generate("<<SelectClasse>>")