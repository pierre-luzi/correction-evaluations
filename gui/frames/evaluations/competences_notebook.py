from tkinter import Frame
from tkinter import BOTH, LEFT, RIGHT, END, X, Y, DISABLED, NORMAL
from tkinter.ttk import Notebook
from gui.autoscrollbar import AutoScrollbar
from gui.frames.evaluations.competences_frame import CompetencesFrame
from logic.competences_manager import CompetencesManager

class CompetencesNotebook(Notebook):
    """
        Classe pour créer un notebook permettant la création
        et la gestion des compétences
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.evaluation = self.master.evaluation
        
        liste_categories = CompetencesManager.lister_categories()
        self.liste_frames = []
        for categorie in liste_categories:
            frame = CompetencesFrame(self, categorie)
            self.liste_frames.append(frame)
            self.add(frame, text=categorie)
        
        self.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def on_tab_changed(self, event):
        selected_tab = event.widget.select()
        selected_frame = event.widget.nametowidget(selected_tab)
        if hasattr(selected_frame, "canvas") and hasattr(selected_frame, "frame_competences"):
            selected_frame.canvas.configure(scrollregion=selected_frame.canvas.bbox("all"))
            selected_frame.update_idletasks()
    
    def update(self):
        for frame in self.liste_frames:
            frame.update()