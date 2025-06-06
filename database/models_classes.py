from .connection import get_connection

def ajouter(nom):
    """
        Crée une nouvelle classe.
        Argument :
            - nom : nom de la classe.
    """
    with get_connection() as conn:
        conn.execute("INSERT INTO classe (nom) VALUES (?)", (nom,))
        conn.commit()

def supprimer(classe_id):
    """
        Supprime une classe.
        Argument :
            - id : id de la classe.
    """
    with get_connection() as conn:
        conn.execute("DELETE FROM classe WHERE id = ?", (classe_id,))
        conn.commit()

def get_id(nom):
    """
        Retourne l'identifiant d'une classe à partir de son nom.
        Argument :
            - nom : nom de la classe.
    """
    with get_connection() as conn:
        result = conn.execute("SELECT id FROM classe WHERE nom = ?", (nom,)).fetchone()
        return result[0] if result else None

def lister_classes():
    """
        Retourne la liste des noms des classes.
    """
    with get_connection() as conn:
        return conn.execute("SELECT * FROM classe ORDER BY nom ASC").fetchall()

def get_eleves(classe_id):
    """
        Retourne la liste des élèves d'une classe.
        Argument :
            - classe_id : identifiant de la classe.
    """
    with get_connection() as conn:
        return conn.execute("SELECT * FROM eleve WHERE classe_id = ? ORDER BY nom ASC", (classe_id,)).fetchall()


def get_evaluations(classe_id):
    """
        Retourne l'ensemble des évaluations d'une classe.
        Argument :
            - classe_id : identifiant de la classe.
    """
    with get_connection() as conn:
        return conn.execute("SELECT * FROM evaluation WHERE classe_id = ?", (classe_id,)).fetchall()