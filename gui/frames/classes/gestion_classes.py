from tkinter import Frame, Button
from tkinter import messagebox, simpledialog
from tkinter import END, DISABLED, NORMAL
from gui.autoscrollbar import AutoScrollbar
from logic.classes_manager import ClassesManager

class GestionClassesFrame(Frame):
    """
        Classe pour créer une frame permettant de gérer les classes.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.classe = self.master.classe
                
        bouton_creer = Button(self, text="Créer une classe", command=self.creer)
        bouton_creer.grid(row=0, column=0, sticky="w")
        
        self.bouton_supprimer = Button(self, text="Supprimer la classe", command=self.supprimer)
        self.bouton_supprimer.grid(row=0, column=1, sticky="w")
        self.bouton_supprimer.config(state=DISABLED)
                               
    def creer(self):
        """
            Crée une nouvelle classe.
        """
        nom = simpledialog.askstring("Créer une classe", "Nom de la nouvelle classe :")
        try:
            ClassesManager.creer(nom)
            self.event_generate("<<CreateClasse>>")
        except ValueError as error:
            messagebox.showwarning("Erreur", str(error))
    
    def supprimer(self):
        """
            Supprime la classe sélectionnée.
        """
        if self.classe.id == None:
            messagebox.showwarning("Erreur", "Aucune classe sélectionnée")
            return
        confirm = messagebox.askyesno("Supprimer la classe", f"Êtes-vous sûr de vouloir supprimer la classe {self.classe.nom} ?")
        if confirm:
            self.classe.supprimer()
            self.event_generate("<<DeleteClasse>>")