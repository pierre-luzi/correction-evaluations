from tkinter import Frame, Label, Button, Scrollbar, Canvas
from tkinter import BOTH, LEFT, RIGHT, END, X, Y, DISABLED, NORMAL
from gui.autoscrollbar import AutoScrollbar
from logic.exercices_manager import ExercicesManager
from gui.frames.exercices.question_frame import QuestionFrame

class CreationExerciceFrame(Frame):
    """
        Classe pour créer une frame qui contient les questions de l'exercice.
        Argument :
            - exercices_manager : objet de la classe ExercicesManager
            permettant la gestion des exercices.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.exercice = self.master.exercice
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.canvas = Canvas(self)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        
        scrollbar = AutoScrollbar(self, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.frame_questions = Frame(self.canvas)
        self.frame_questions_id = self.canvas.create_window((0, 0), window=self.frame_questions, anchor="nw")
        self.frame_questions.grid_columnconfigure(0, weight=1)
        
        def update_scrollregion(event):
            self.canvas.after_idle(
                lambda: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            )
        
        self.frame_questions.bind("<Configure>", update_scrollregion)
        
        def resize_frame(event):
            width = event.width
            if self.canvas.cget("yscrollcommand"):
                width -= 15  # marge pour la scrollbar
            self.canvas.itemconfig(self.frame_questions_id, width=width)       
        
        self.canvas.bind("<Configure>", resize_frame)
        
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())  # Pour que le canvas capte les scrolls
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        self.frame_gerer_questions = Frame(self)
        self.frame_gerer_questions.grid(row=0, column=0, sticky="we")
        
        bouton_enregistrer_question = Button(self.frame_gerer_questions, text="Enregistrer l'exercice", command=self.enregistrer)
        bouton_enregistrer_question.grid(row=0, column=0, sticky="w")
        
        bouton_ajouter_question = Button(self.frame_gerer_questions, text="Ajouter une question", command=self.ajouter_question)
        bouton_ajouter_question.grid(row=0, column=1, sticky="w")
        
        self.bouton_supprimer_question = Button(self.frame_gerer_questions, text="Supprimer une question", command=self.supprimer_question)
        self.bouton_supprimer_question.grid(row=0, column=2, sticky="w")
        
        self.liste_frames_questions = []
    
    def _on_mousewheel(self, event):
        """
            Permet le défilement du canvas au trackpad.
        """
        direction = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(direction, "units")
    
    def charger_questions(self):
        """
            Affiche les questions de l'exercice sélectionné.
        """
        for frame in self.liste_frames_questions:
            frame.destroy()
            self.liste_frames_questions = []

        questions = self.exercice.get_questions()

        if len(questions) == 0:
            self.afficher_question([1, "", "", 1.00])
        else:
            for question in questions:
                self.afficher_question(question)
        
        if len(self.liste_frames_questions) == 1:
            self.bouton_supprimer_question.config(state=DISABLED)
        else:
            self.bouton_supprimer_question.config(state=NORMAL)
    
    def afficher_question(self, question):
        """
            Affiche une question.
            Argument :
                - question : tuple contenant le numéro, la réponse et
                le barème de la question.
        """
        frame = QuestionFrame(self.frame_questions, question)
        frame.grid(row=question[0]+2, column=0, sticky="ew", pady=5)        
        self.liste_frames_questions.append(frame)        
    
    def ajouter_question(self):
        """
            Ajoute une question dans l'interface.
            Cette fonction ne modifie pas les données :
            aucune nouvelle question n'est créée dans la base
            de données !
        """
        numero = len(self.liste_frames_questions)+1
        question = (numero, "", "", 1.00)
        self.afficher_question(question)
        self.bouton_supprimer_question.config(state=NORMAL)
    
    def supprimer_question(self):
        """
            Supprime une question de l'interface.
            Cette fonction ne modifie pas les données :
            aucune question n'est supprimée dans la base de données !
        """        
        self.liste_frames_questions.pop().destroy()
        if len(self.liste_frames_questions) == 1:
            self.bouton_supprimer_question.config(state=DISABLED)
    
    def enregistrer(self):
        questions = []
        for frame in self.liste_frames_questions:
            reponseA = frame.reponseA.get("1.0", "end-1c")
            reponseB = frame.reponseB.get("1.0", "end-1c")
            bareme = frame.valeur_bareme.get()
            questions.append((reponseA, reponseB, bareme))
        self.exercice.enregistrer_exercice(questions)