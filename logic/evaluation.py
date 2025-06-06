from database import models_evaluations, models_exercices, models_questions, models_competences

class Evaluation:
    """
        Classe permettant de gérer une évaluation.
    """
    def __init__(self):
        self.classe_id = None
        self.titre = None
        self.id = None
        self.bareme_redaction = 1.0
        self.competences_id = []
    
    def set(self, classe_id, titre):
        """
            Change l'évaluation sélectionnée.
            Arguments :
                - classe_id : identifiant de la classe ;
                - titre : titre de l'évaluation.
        """
        evaluation = models_evaluations.get_par_titre(classe_id, titre)
        self.classe_id = None
        self.titre = titre
        self.id = evaluation[0]
        self.bareme_redaction = evaluation[2]
        self.competences_id = models_evaluations.lister_competences_id(self.id)
    
    def set_bareme_redaction(self, valeur):
        """
            Fixer le barème pour la rédaction.
            Arguments :
                - valeur : nombre de points pour la rédaction.
        """
        self.bareme_redaction = float(valeur)
    
    def creer(self, classe_id, titre):
        """
            Crée une nouvelle évaluation.
            Arguments :
                - classe_id : identifiant de la classe ;
                - titre : titre de l'évaluation.
        """
        if not titre:
            raise ValueError("Le titre de l'évaluation ne peut pas être vide.")
        if not models_evaluations.get_evaluation_id(classe_id, titre) == None:
            raise ValueError("L'évaluation '{titre}' existe déjà pour cette classe.")
        models_evaluations.creer_evaluation(classe_id, titre)
    
    def supprimer(self):
        """
            Supprimer l'évaluation.
        """
        models_evaluations.supprimer(self.id)
        self.__init__()
    
    def ajouter_exercice(self, exercice_id):
        """
            Ajoute une entrée à la table de liaison exercices/évaluations.
            Argument :
                - exercice_id : identifiant de l'exercice.
        """
        models_evaluations.ajouter_exercice(exercice_id, self.id)
    
    def lister_exercices(self):
        """
            Liste les titres des exercices contenus dans l'évaluation.
        """
        exercices = models_evaluations.get_exercices(self.id)        
        return [exercice[1] for exercice in exercices]
        
    def calculer_bareme(self):
        """
            Calcule le barème total de l'évaluation.
        """
        bareme = self.bareme_redaction
        exercices = models_evaluations.get_exercices(self.id)        
        for exercice in exercices:
            questions = models_exercices.get_questions(exercice[0])
            for question in questions:
                bareme += models_questions.get_bareme(question[0])
        return bareme
    
    def lister_competences(self):
        """
            Lister les compétences évaluées.
        """
        liste = []
        for competence_id in self.competences_id:
            liste.append(models_competences.get(competence_id))
        return liste
        
    
    def ajouter_competence(self, competence):
        """
            Ajoute une compétence à l'évaluation.
            Argument :
                - competence : intitulé de la compétence.
        """
        competence_id = models_competences.get_id(competence)
        self.competences_id.append(competence_id)
    
    def supprimer_competence(self, competence):
        """
            Supprime une compétence de l'évaluation.
            Argument :
                - competence : intitulé de la compétence.
        """
        competence_id = models_competences.get_id(competence)
        self.competences_id.remove(competence_id)
    
    def chercher_competence(self, competence):
        """
            Cherche si une compétence est incluse à l'évaluation.
            Argument :
                - competence : intitulé de la compétence.
        """
        competence_id = models_competences.get_id(competence)
        if competence_id in self.competences_id:
            return 1
        else:
            return 0
    
    def enregistrer(self):
        """
            Enregistrer l'évaluation.
        """
        # barème
        models_evaluations.set_bareme_redaction(self.id, self.bareme_redaction)
        
        # compétences
        competences_id = models_evaluations.lister_competences_id(self.id)
        for competence_id in competences_id:
            if not competence_id in self.competences_id:
                models_evaluations.delier(self.id, competence_id)      
        for competence_id in self.competences_id:
            if not competence_id in competences_id:
                models_evaluations.lier(self.id, competence_id)

evaluation = Evaluation()