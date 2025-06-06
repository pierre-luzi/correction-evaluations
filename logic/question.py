from database import models_questions, models_erreurs

class Question:
    """
        Classe permettant de gérer une question.
    """
    def __init__(self):
        self.id = None
        self.exercice_id = None
        self.numero = None
        self.reponseA = None
        self.reponseB = None
        self.bareme = None
    
    def set(self, exercice_id, numero):
        """
            Change la question sélectionnée.
            Arguments :
                - exercice_id : identifiant de l'exercice ;
                - numero : numéro de la question.
        """
        question = models_questions.get(exercice_id, numero)
        self.id = question[0]
        self.numero = question[1]
        self.reponseA = question[2]
        self.reponseB = question[3]
        self.bareme = question[4]
    
    def lister_erreurs(self):
        """
            Renvoie la liste des erreurs de la question.
        """
        erreurs = models_questions.get_erreurs(self.id)
        return erreurs
    
    def ajouter_erreur(self, texte):
        """
            Ajoute une erreur à la question.
            Argument :
                - texte : description de l'erreur.
        """
        models_erreurs.ajouter(self.id, texte)

question = Question()