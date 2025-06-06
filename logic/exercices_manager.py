from database import models_exercices, models_questions
from sqlite3 import IntegrityError

class ExercicesManager:
    """
        Classe permettant de gérer les exercices.
    """
    @staticmethod
    def creer(titre, niveau):
        """
            Crée un nouvelle exercice.
            Arguments :
                - titre : titre de l'exercice ;
                - niveau : niveau de l'exercice.
        """
        if not titre:
            raise ValueError("Le titre de l'exercice ne peut pas être vide.")
        try:
            models_exercices.creer(titre, niveau)
            exercice_id = models_exercices.get_id(titre)
            models_questions.creer_question(exercice_id, 1, "", "", 1.00)
        except IntegrityError:
            raise ValueError(f"L'exercice '{titre}' existe déjà.")
    
    @staticmethod
    def lister_exercices(niveau):
        """
            Retourne la liste des titres des exercices du niveau indiqué.
            Argument :
                - niveau : niveau des exercices.
        """
        exercices = models_exercices.lister_par_niveau(niveau)
        return [exercice[1] for exercice in exercices]