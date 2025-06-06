from database import models_eleves

class Eleve:
    """
        Classe permettant de gérer un élève.
    """
    def __init__(self):
        self.classe_id = None
        self.nom = None
        self.id = None
    
    def set(self, classe_id, nom):
        """
            Change l'élève sélectionné.
            Arguments :
                - classe_id : identifiant de la classe ;
                - nom : nom de l'élève.
        """
        self.classe_id = classe_id
        self.nom = nom
        self.id = models_eleves.get_id(self.classe_id, nom)

    def supprimer(self, classe_id):
        """
            Supprimer l'élève sélectionné.
            Argument :
                - classe_id : identifiant de la classe.
        """
        models_eleves.supprimer(self.nom, classe_id)
        self.__init__()        

eleve = Eleve()