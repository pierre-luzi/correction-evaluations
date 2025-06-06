from tkinter import Frame, Button
from tkinter import messagebox, simpledialog, filedialog
from tkinter import END, DISABLED, NORMAL
from gui.autoscrollbar import AutoScrollbar

class GestionElevesFrame(Frame):
    """
        Classe pour créer une frame permettant de gérer les élèves
        d'une classe.
        Argument :
            - classes_manager : objet de la classe ClassesManager ;
            - eleves_manager : objet de la classe ElevesManager.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.classe = self.master.classe
        self.eleve = self.master.eleve
        
        self.bouton_ajouter = Button(self, text="Ajouter un élève", command=self.ajouter)
        self.bouton_ajouter.grid(row=0, column=0, sticky="w")
        self.bouton_ajouter.config(state=DISABLED)
        
        self.bouton_importer = Button(self, text="Importer une liste", command=self.importer)
        self.bouton_importer.grid(row=0, column=1, sticky="w")
        self.bouton_importer.config(state=DISABLED)
        
        self.bouton_supprimer = Button(self, text="Supprimer l'élève", command=self.supprimer)
        self.bouton_supprimer.grid(row=0, column=2, sticky="w")
        self.bouton_supprimer.config(state=DISABLED)
    
    def ajouter(self):
        """
            Ajoute un élève à la classe sélectionnée.
        """
        nom = simpledialog.askstring("Ajouter un élève", "Nom de l'élève :")
        try:
            self.classe.ajouter_eleve(nom)
            self.event_generate("<<AddEleve>>")
        except ValueError as error:
            messagebox.showwarning("Erreur", str(error))
    
    def importer(self):
        """
            Importe une liste d'élèves.
        """
        if self.classe.id == None:
            messagebox.showwarning("Erreur", "Aucune classe sélectionnée !")
            return
            
        chemin = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        try:
            self.classe.importer_liste(chemin)
            self.event_generate("<<AddEleve>>")
        except Exception as exception:
            messagebox.showwarning("Erreur", f"Erreur lors de la lecture du fichier : {exception}")
            return
    
    def supprimer(self):
        """
            Supprime l'élève sélectionné.
        """
        confirm = messagebox.askyesno("Supprimer l'élève", f"Êtes-vous sûr de vouloir supprimer l'élève {self.eleve.nom} ?")
        if confirm:
            self.eleve.supprimer(self.classe.id)
            self.event_generate("<<DeleteEleve>>")