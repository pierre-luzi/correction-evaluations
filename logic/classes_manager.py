from database import models_classes
import csv
from sqlite3 import IntegrityError

class ClassesManager:
    """
        Classe permettant de gérer les classes d'élèves.
    """
    @staticmethod
    def creer(nom):
        """
            Crée une nouvelle classe.
            Argument :
                - nom : nom de la classe.
        """
        if not nom:
            raise ValueError("Le nom de la classe ne peut pas être vide.")
        try:
            models_classes.ajouter(nom)
        except IntegrityError:
            raise ValueError(f"La classe '{nom}' existe déjà.")
    
    @staticmethod
    def lister():
        """
            Renvoie la liste des noms des classes.
        """
        classes = models_classes.lister_classes()
        return [row[1] for row in classes]