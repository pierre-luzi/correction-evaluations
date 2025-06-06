from .connection import get_connection

def ajouter(nom, classe_id):
    """
        Ajoute un élève à une classe.
        Arguments :
            - nom : nom de l'élève ;
            - classe_id : identifiant de la classe.
    """
    with get_connection() as conn:
        conn.execute("INSERT INTO eleve (nom, classe_id) VALUES (?, ?)", (nom, classe_id))
        conn.commit()

def supprimer(nom, classe_id):
    """
        Supprime un élève de la classe.
        Arguments :
            - nom : nom de l'élève ;
            - classe_id : identifiant de la classe.
    """
    with get_connection() as conn:
        conn.execute("DELETE FROM eleve WHERE nom = ? AND classe_id = ?", (nom, classe_id))
        conn.commit()

def get_id(classe_id, nom):
    """
        Retourne l'identifiant d'un élève à partir de son nom.
        Argument :
            - nom : nom de l'élève.
    """
    with get_connection() as conn:
        result = conn.execute("SELECT id FROM eleve WHERE classe_id = ? AND nom = ?", (classe_id, nom)).fetchone()
        return result[0] if result else None