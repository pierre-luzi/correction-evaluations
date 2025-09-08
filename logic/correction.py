from database import models_erreurs, models_corrections

class Correction:
    """
        Classe permettant de gérer la correction d'une question
        d'une évaluation pour un élève donné.
    """
    def __init__(self):
        self.commentaire = ""
        self.note = 0
        self.eleve_id = None
        self.evaluation_id = None
        self.question_id = None
        self.erreurs_id = []
    
    def set(self, eleve_id, evaluation_id, question_id):
        """
            Changer les informations de la correction sélectionnée.
            Arguments :
                - eleve_id : identifiant de l'élève ;
                - evaluation_id : identifiant de l'évaluation ;
                - question_id : identifiant de la question.
        """
        self.eleve_id = eleve_id
        self.evaluation_id = evaluation_id
        self.question_id = question_id
        correction = models_corrections.get(eleve_id, evaluation_id, question_id)
        if not correction == None:
            self.commentaire = correction[0]
            self.note = correction[1]
        self.erreurs_id = models_corrections.lister_erreurs_id(eleve_id, evaluation_id, question_id)
    
    def enregistrer(self):
        """
            Enregistrer le commentaire et la note et lie les erreurs à la correction.
        """
        models_corrections.enregistrer(self.eleve_id, self.evaluation_id, self.question_id, self.commentaire, self.note)
        
        erreurs_id = models_corrections.lister_erreurs_id(self.eleve_id, self.evaluation_id, self.question_id)
        for erreur_id in erreurs_id:
            if not erreur_id in self.erreurs_id:
                models_corrections.delier_erreur(self.eleve_id, self.evaluation_id, self.question_id, erreur_id)
        for erreur_id in self.erreurs_id:
            if not erreur_id in erreurs_id:
                models_corrections.lier_erreur(self.eleve_id, self.evaluation_id, self.question_id, erreur_id)
    
    # def lister_erreurs(self):
    #     return models_corrections.lister_erreurs(self.eleve_id, self.evaluation_id, self.question_id)
    
    def ajouter_erreur(self, erreur):
        """
            Ajoute une erreur à la correction.
            Argument :
                - erreur : description de l'erreur.
        """
        erreur_id = models_erreurs.get_id(self.question_id, erreur)
        self.erreurs_id.append(erreur_id)
    
    def supprimer_erreur(self, erreur):
        """
            Supprime une erreur de la correction.
            Argument :
                - erreur : description de l'erreur.
        """
        erreur_id = models_erreurs.get_id(self.question_id, erreur)
        self.erreurs_id.remove(erreur_id)
    
    def chercher_erreur(self, erreur):
        """
            Cherche si une erreur donnée est dans la correction.
            Argument :
                - erreur : description de l'erreur.
        """
        erreur_id = models_erreurs.get_id(self.question_id, erreur)
        if erreur_id in self.erreurs_id:
            return 1
        else:
            return 0