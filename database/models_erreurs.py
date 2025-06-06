from .connection import get_connection

def ajouter(question_id, texte):
    """
        Ajoute une erreur à la base de données.
        Arguments :
            - question_id : identifiant de la question ;
            - texte : description de l'erreur.
    """
    with get_connection() as conn:
        conn.execute("INSERT INTO erreur (question_id, erreur) VALUES (?, ?)", (question_id, texte))
        conn.commit()

def get_id(question_id, erreur):
    """
        Renvoie l'identifiant de l'erreur.
        Arguments :
            - question_id : identifiant de l'erreur ;
            - erreur : description de l'erreur.
    """
    with get_connection() as conn:
        result = conn.execute("SELECT id from erreur WHERE question_id = ? AND erreur = ?", (question_id, erreur)).fetchone()
        return result[0]