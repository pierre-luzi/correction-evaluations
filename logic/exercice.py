from database import models_exercices, models_questions
from sqlite3 import IntegrityError

class Exercice:
    """
        Classe permettant de gérer un exercice.
    """
    def __init__(self):
        self.titre = None
        self.id = None
        self.niveau = None
    
    def set_niveau(self, niveau):
        """
            Change le niveau des exercices affichés.
            Argument :
                - niveau : niveau de l'exercice.
        """
        self.niveau = niveau
    
    def set_exercice(self, titre):
        """
            Change l'exercice sélectionné.
            Argument :
                - titre : titre de l'exercice.
        """
        self.titre = titre
        self.id = models_exercices.get_id(titre)
        
    def supprimer(self):
        """
            Supprime l'exercice.
        """
        models_exercices.supprimer(self.id)
        self.titre = None
        self.id = None
    
    def get_questions(self):
        """
            Renvoie la liste des questions de l'exercice.
            Chaque question est sous la forme d'un tuple :
            (numero, réponseA, réponseB, barême)
        """
        questions = []
        request = models_exercices.get_questions(self.id)
        for result in request:
            questions.append((result[1], result[2], result[3], result[4]))
        return questions
    
    def get_question_id(self, numero):
        """
            Renvoie l'identifiant de la question.
            Argument :
                - numero : numéro de la question.
        """
        return models_questions.get_id(self.id, numero)
    
    def enregistrer_exercice(self, questions):
        """
            Enregistre l'exercice.
            Argument :
                - questions : liste de tuples (reponseA, reponseB, bareme).
        """
        nombre_questions_db = len(self.get_questions())
        nombre_questions = len(questions)
        
        if nombre_questions_db > nombre_questions:
            numero = nombre_questions_db
            while numero > nombre_questions:
                models_questions.supprimer(self.id, numero)
                numero -= 1
                
        numero = 1
        for question in questions:
            reponseA = question[0]
            reponseB = question[1]
            bareme = question[2]
            if numero > nombre_questions_db:
                models_questions.creer(self.id, numero, reponseA, reponseB, bareme)
            else:
                models_questions.modifier(self.id, numero, reponseA, reponseB, bareme)
            numero += 1

exercice = Exercice()