from database import models_classes, models_evaluations, models_eleves
import csv
from sqlite3 import IntegrityError

class Classe:
    """
        Classe permettant de gérer une classe.
    """
    def __init__(self):
        self.nom = None
        self.id = None
    
    def set(self, nom):
        """
            Change la classe sélectionnée.
            Argument :
                - nom : nom de la classe.
        """
        self.nom = nom
        self.id = models_classes.get_id(nom)

    def supprimer(self):
        """
            Supprimer la classe sélectionnée.
        """
        models_classes.supprimer(self.id)
        self.__init__()
    
    def lister_eleves(self):
        """
            Renvoie la liste des noms des élèves de la classe.
        """
        eleves = models_classes.get_eleves(self.id)
        return [row[1] for row in eleves]
    
    def ajouter_eleve(self, nom):
        """
            Ajouter un élève à la classe.
            Argument :
                - nom : nom de l'élève.
        """
        if not nom:
            raise ValueError("Le nom de l'élève ne peut pas être vide.")
        eleves = models_classes.get_eleves(self.id)
        noms = [eleve[1] for eleve in eleves]
        if nom in noms:
            raise ValueError("L'élève est déjà enregistré dans cette classe.")
        models_eleves.ajouter(nom, self.id)
    
    def importer_liste(self, chemin):
        """
            Importe la liste des élèves de la classe.
            Argument :
                - chemin : chemin du fichier csv contenant la liste.
        """
        with open(chemin, newline='', encoding='utf-8') as fichier:
            lecteur = csv.reader(fichier)
            for i, ligne in enumerate(lecteur, start=1):
                if len(ligne) != 1:
                    raise ValueError("Le fichier ne doit avoir qu'une seule colonne.")
                if not isinstance(ligne[0], str):
                    raise ValueError("Le contenu doit être du texte.")

            fichier.seek(0)
            for i, ligne in enumerate(lecteur, start=1):
                nom = ligne[0]
                noms = self.lister_eleves()
                if not nom in noms:
                    models_eleves.ajouter(nom, self.id)
    
    def creer_evaluation(self, titre):
        """
            Créer une évaluation pour la classe sélectionnée.
            Argument :
                - titre : titre de l'évaluation.
        """
        if not titre:
            raise ValueError("Le titre de l'évaluation ne peut pas être vide.")
        if not models_evaluations.get_par_titre(self.id, titre) == None:
            raise ValueError("L'évaluation '{titre}' existe déjà pour cette classe.")
        models_evaluations.creer(self.id, titre)
    
    def lister_evaluations(self):
        """
            Retourne la liste des titres des évaluations de la classe.
        """
        evaluations = models_classes.get_evaluations(self.id)
        return [evaluation[1] for evaluation in evaluations]
        
classe = Classe()