from tkinter import Frame, Listbox, Scrollbar, Label, StringVar
from tkinter import messagebox, simpledialog
from tkinter import END
from tkinter.ttk import Combobox
from gui.autoscrollbar import AutoScrollbar
from logic.exercices_manager import ExercicesManager

class ListeExercicesFrame(Frame):
    """
        Classe pour créer une frame affichant la liste des exercices.
        Argument :
            - exercices_manager : objet de la classe ExercicesManager
            permettant la gestion des exercices.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.exercice = self.master.exercice
        self.niveau = None
        
        self.grid_columnconfigure(0, weight=1)
                
        label_exercices = Label(self, text="Choisir un niveau:")
        label_exercices.grid(row=0, column=0, padx=10, pady=0, sticky="w")
        
        #----- sélection du niveau -----
        self.niveau = StringVar()
        self.combobox_niveau = Combobox(self, textvariable=self.niveau, state="readonly")
        self.combobox_niveau.grid(row=0, column=1, padx=10, sticky="w")
        self.combobox_niveau['values'] = ('2e', '1re', 'TSTL')
        self.combobox_niveau.bind("<<ComboboxSelected>>", self.select_niveau)
        
        #----- liste des exercices -----
        self.frame_liste_exercices = Frame(self)
        self.frame_liste_exercices.grid(row=1, column=0, columnspan=2, padx=10, sticky="nsew")
        self.frame_liste_exercices.grid_columnconfigure(0, weight=1, minsize=300)
        
        self.listbox_exercices = Listbox(self.frame_liste_exercices, height=30, exportselection=0)
        self.listbox_exercices.grid(row=0, column=0, sticky="nsew")

        scrollbar_exercices = AutoScrollbar(self.frame_liste_exercices, orient="vertical", command=self.listbox_exercices.yview)
        scrollbar_exercices.grid(row=0, column=1, sticky="ns")

        self.listbox_exercices.config(yscrollcommand=scrollbar_exercices.set)
        self.listbox_exercices.bind("<<ListboxSelect>>", self.select_exercice)
        
        self.combobox_niveau.set("1re")
        self.exercice.set_niveau(self.niveau.get())
        self.charger_exercices()
    
    def select_niveau(self, event):
        """
            Sélectionne le niveau de l'exercice.
        """
        self.exercice.__init__()
        self.exercice.set_niveau(self.niveau.get())
        self.charger_exercices()
        self.event_generate("<<SelectNiveau>>")
        
    def charger_exercices(self):
        """
            Affiche la liste des exercices.
        """
        self.listbox_exercices.delete(0, END)
        titres = ExercicesManager.lister_exercices(self.exercice.niveau)
        for titre in titres:
            self.listbox_exercices.insert(END, titre)
            
    def select_exercice(self, event):
        """
            Sélectionne un exercice dans la liste.
        """
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            titre = event.widget.get(index)
            self.exercice.set_exercice(titre)
            self.event_generate("<<SelectExercice>>")
    
    def set_listbox_height(self, height):
        self.listbox_exercices.config(height=height)