from tkinter import Tk, Menu, messagebox
from gui.views.classes_view import ClassesView
from gui.views.evaluations_view import EvaluationsView
from gui.views.exercices_view import ExercicesView
from gui.views.correction_view import CorrectionView

class Application(Tk):
    def __init__(self):
        super().__init__()
        
        self.minsize(850, 400)
        self.state('zoomed')
        self.title("Correction des évaluations")
        
        self.creer_menu()
        
        self.current_frame = None
        self.show_frame(CorrectionView)
        
    def creer_menu(self):
        """
            Crée le menu de l'application.
        """
        menu_bar = Menu(self)
        
        # menu Classes
        menu_classes = Menu(menu_bar, tearoff=0)
        menu_classes.add_command(label="Gestion des classes", command=lambda: self.show_frame(ClassesView))
        menu_classes.add_command(label="Résultats")
        menu_bar.add_cascade(label="Classes", menu=menu_classes)
        
        # menu Évaluations
        menu_evaluations = Menu(menu_bar, tearoff=0)
        menu_evaluations.add_command(label="Exercices", command=lambda: self.show_frame(ExercicesView))
        menu_evaluations.add_command(label="Gérer les évaluations", command=lambda: self.show_frame(EvaluationsView))
        menu_evaluations.add_command(label="Corriger", command=lambda: self.show_frame(CorrectionView))
        menu_bar.add_cascade(label="Évaluations", menu=menu_evaluations)

        self.config(menu=menu_bar)
    
    def show_frame(self, FrameClass):
        """
            Affiche la frame indiquée.
            Argument :
                - FrameClass : classe définissant le type de frame.
        """
        if self.current_frame:
            self.current_frame.destroy()

        # Crée un nouveau frame et l'affiche
        self.current_frame = FrameClass(self)
        self.current_frame.pack(fill="both", expand=True)
        self.update_idletasks()