from tkinter import Frame, IntVar, Checkbutton, Button
from gui.autoscrollbar import AutoScrollbar
from tkinter import simpledialog, messagebox
from sqlite3 import IntegrityError

ERREUR_WIDTH = 520

class ErreursFrame(Frame):
    """
        Classe pour créer une frame permettant de gérer les erreurs
        faites par un élève à une question.
    """
    def __init__(self, master, width=ERREUR_WIDTH):
        super().__init__(master, width=width, highlightbackground="black", highlightthickness=1)
        
        self.grid_propagate(True)
        self.configure(width=ERREUR_WIDTH)
                        
        #----- initialisation des attributs -----
        self.eleve = master.eleve
        self.evaluation = master.evaluation
        self.question = master.question
        self.correction = master.correction        
        self.checkbuttons = []
        
        #----- affichage des checkbuttons -----
        for erreur in self.question.lister_erreurs():
            self.afficher_checkbutton(erreur)
            
        def ajuster_wraplength(event):
            """
                Ajuste la longueur wraplength des étiquettes des
                checkboxes.
            """
            wrap = ERREUR_WIDTH
            # wrap = event.width-20 if event.width < ERREUR_WIDTH else ERREUR_WIDTH
            for widget in self.winfo_children():
                if isinstance(widget, Checkbutton):
                    widget.configure(wraplength=wrap)

        self.bind("<Configure>", ajuster_wraplength)
        self.after_idle(self.update_idletasks)
        
        #----- bouton pour ajouter une erreur -----
        self.bouton_ajouter = Button(self, text="+", command=self.ajouter_erreur)
        self.bouton_ajouter.grid(row=len(self.checkbuttons), column=0, pady=5, sticky="w")
    
    def afficher_checkbutton(self, erreur):
        """
            Crée et affiche un checkbutton correspondant à une erreur.
        """
        var = IntVar()
        var.set(self.correction.chercher_erreur(erreur))
        cbx = Checkbutton(
            self,
            text=self.wrap_strict(erreur, ERREUR_WIDTH), variable=var,
            onvalue=1, offvalue=0,
            anchor="w", justify="left", wraplength=560,
            command=lambda err=erreur, var=var: self.change_checkbutton(err, var)
        )
        self.checkbuttons.append((erreur, var))
        cbx.grid(row=len(self.checkbuttons)-1, pady=2, column=0, sticky="w")
    
    def wrap_strict(self, texte, max_pixels, avg_char_width=7):
        """
            Coupe les lignes avant le mot qui ferait dépasser la largeur max_pixels.
            Ne coupe jamais les mots.
        """
        mots = texte.split()
        lignes = []
        ligne_actuelle = ""

        for mot in mots:
            # Calcule la longueur approximative si on ajoute ce mot
            longueur_ligne = len(ligne_actuelle + " " + mot) * avg_char_width
            if ligne_actuelle and longueur_ligne > max_pixels:
                lignes.append(ligne_actuelle.strip())
                ligne_actuelle = mot
            else:
                ligne_actuelle += " " + mot

        if ligne_actuelle:
            lignes.append(ligne_actuelle.strip())

        return '\n'.join(lignes)
    
    def change_checkbutton(self, erreur, var):
        """
            Met à jour les erreurs de la correctoin lors d'un changement
            de sélection des checkbuttons.
        """
        if var.get():
            self.correction.ajouter_erreur(erreur)
        else:
            self.correction.supprimer_erreur(erreur)
    
    def ajouter_erreur(self):
        """
            Ajouter une erreur à la question.
        """
        erreur = simpledialog.askstring("Ajouter une erreur", "Ajouter une erreur pour cette question :")
        try:
            self.question.ajouter_erreur(erreur)
            self.afficher_checkbutton(erreur)
            self.bouton_ajouter.grid(row=len(self.checkbuttons), pady=2, column=0, sticky="w")
        except IntegrityError:
            messagebox.showwarning("Erreur", "L'erreur n'a pas pu être ajoutée à la question.")