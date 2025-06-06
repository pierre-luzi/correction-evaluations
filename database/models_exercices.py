from .connection import get_connection

def creer(titre, niveau):
    """
        Crée un nouvel exercice.
        Arguments :
            - titre : titre de l'exercice ;
            - niveau : niveau scolaire de l'exercice.
    """
    with get_connection() as conn:
        conn.execute("INSERT INTO exercice (titre, niveau) VALUES (?, ?)", (titre, niveau))
        conn.commit()

def supprimer(id):
    """
        Supprimer l'exercice.
        Argument :
            - id : identifiant de l'exercice.
    """
    with get_connection() as conn:
        conn.execute("DELETE FROM exercice WHERE id = ?", (id,))
        conn.commit()

def lister_par_niveau(niveau):
    """
        Retourne la liste des titres des exercices d'un niveau donné.
        Argument :
            - niveau : niveau de l'exercice.
    """
    with get_connection() as conn:
        return conn.execute("SELECT * FROM exercice WHERE niveau = ? ORDER BY titre ASC", (niveau,)).fetchall()

def get_id(titre):
    """
        Retourne l'identifiant d'un exercice à partir de son nom.
        Argument :
            - nom : nom de l'exercice.
    """
    with get_connection() as conn:
        result = conn.execute("SELECT id FROM exercice WHERE titre = ?", (titre,)).fetchone()
        return result[0] if result else None

def get_questions(exercice_id):
    """
        Renvoie les questions de l'exercice.
        Argument :
            - exercice_id : identifiant de l'exercice.
    """
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM question WHERE exercice_id = ? ORDER BY numero ASC",
            (exercice_id,)
        ).fetchall()