from tkinter import Frame, Button
from tkinter import messagebox, simpledialog
from tkinter import END, DISABLED, NORMAL
from gui.autoscrollbar import AutoScrollbar
from logic.exercices_manager import ExercicesManager

class GestionExercicesFrame(Frame):
    """
        Classe pour créer une frame permettant de gérer les exercices.
        Argument :

    """
    def __init__(self, master):
        super().__init__(master)
        
        self.exercice = self.master.exercice
        
        self.bouton_creer = Button(self, text="Créer un exercice", command=self.creer)
        self.bouton_creer.grid(row=0, column=0, sticky="w")
        
        self.bouton_supprimer = Button(self, text="Supprimer l'exercice", command=self.supprimer)
        self.bouton_supprimer.grid(row=0, column=1, sticky="w")
        self.bouton_supprimer.config(state=DISABLED)
                               
    def creer(self):
        """
            Crée un nouvel exercice.
        """
        titre = simpledialog.askstring("Créer un exercice", "Titre de l'exercice :")
        try:
            ExercicesManager.creer(titre, self.exercice.niveau)
            self.event_generate("<<CreateExercice>>")
        except ValueError as error:
            messagebox.showwarning("Erreur", str(error))
    
    def supprimer(self):
        """
            Supprime l'exercice sélectionné.
        """
        if self.exercice.id == None:
            messagebox.showwarning("Erreur", "Aucun exercice sélectionné")
            return
        confirm = messagebox.askyesno("Supprimer l'exercice", f"Êtes-vous sûr de vouloir supprimer l'exercice {self.exercice.titre} ?")
        if confirm:
            self.exercice.supprimer()
            self.bouton_supprimer.config(state=DISABLED)
            self.event_generate("<<DeleteExercice>>")