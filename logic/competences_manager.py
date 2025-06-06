from database import models_competences

class CompetencesManager:
    """
        Classe permettant de gérer les compétences.
    """
    @staticmethod
    def lister_categories():
        """
            Renvoie la liste des catégories.
        """
        liste_db = models_competences.lister_categories()
        categories = []
        for categorie in liste_db:
            if not categorie in categories:
                categories.append(categorie)
        return categories
    
    @staticmethod
    def lister_competences(categorie):
        """
            Renvoie la liste des compétences pour une catégorie donnée.
            Argument :
                - categorie : catégorie de compétences.
        """
        return models_competences.lister(categorie)