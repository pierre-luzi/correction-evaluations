from .connection import get_connection

def get(competence_id):
    """
        Renvoie la compétence demandée.
        Argument :
            - competence_id : identifiant de la compétence.
    """
    with get_connection() as conn:
        result = conn.execute("SELECT titre FROM competence WHERE id = ?", (competence_id,)).fetchone()
        return result[0]

def lister_categories():
    """
        Renvoie la liste des catégories de compétences.
    """
    with get_connection() as conn:
        result = conn.execute("SELECT categorie FROM competence").fetchall()
        return [categorie[0] for categorie in result]

def lister(categorie):
    """
        Renvoie la liste des compétences d'une catégorie.
        Argument :
            - categorie : catégorie des compétences.
    """
    with get_connection() as conn:
        result = conn.execute("SELECT titre FROM competence WHERE categorie = ?", (categorie,)).fetchall()
        return [competence[0] for competence in result]

def get_id(titre):
    """
        Renvoie l'identifiant d'une compétence.
        Argument :
            - titre : titre de la compétence.
    """
    with get_connection() as conn:
        result = conn.execute("SELECT id FROM competence WHERE titre = ?", (titre,)).fetchone()
        return result[0]