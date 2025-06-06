from .connection import get_connection

def creer(exercice_id, numero, reponseA, reponseB, bareme):
    """
        Crée une question.
        Arguments :
            - exercice_id : identifiant de l'exercice ;
            - numero : numéro de la question ;
            - reponseA : réponse pour le sujet A ;
            - reponseB : réponse pour le sujet B ;
            - bareme : nombre de points de la question.
    """
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO question (numero, reponseA, reponseB, bareme, exercice_id) VALUES (?, ?, ?, ?, ?)",
            (numero, reponseA, reponseB, bareme, exercice_id)
        )
        conn.commit()

def modifier(exercice_id, numero, reponseA, reponseB, bareme):
    """
        Modifie une question.
        Arguments :
            - exercice_id : identifiant de l'exercice ;
            - numero : numéro de la question ;
            - reponseA : réponse pour le sujet A ;
            - reponseB : réponse pour le sujet B ;
            - bareme : nombre de points de la question.
    """
    with get_connection() as conn:
        conn.execute(
            "UPDATE question SET numero = ?, reponseA = ?, reponseB = ?, bareme = ? WHERE exercice_id = ? AND numero = ?",
            (numero, reponseA, reponseB, bareme, exercice_id, numero)
        )
        conn.commit()

def supprimer(exercice_id, numero):
    """
        Supprime une question.
        Arguments :
            - exercice_id : identifiant de l'exercice ;
            - numero : numéro de la question.
    """
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM question WHERE exercice_id = ? AND numero = ?",
            (exercice_id, numero)
        )

def get(exercice_id, numero):
    """
        Renvoie la question demandée.
        Arguments :
            - exercice_id : identifiant de l'exercice ;
            - numero : numéro de la question.
    """
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM question WHERE exercice_id = ? AND numero = ?",
            (exercice_id, numero)
        ).fetchone()

def get_id(exercice_id, numero):
    """
        Renvoie l'identifiant de la question demandée.
        Arguments :
            - exercice_id : identifiant de l'exercice ;
            - numero : numéro de la question.
    """
    with get_connection() as conn:
        result = conn.execute(
            "SELECT id FROM question WHERE exercice_id = ? AND numero = ?",
            (exercice_id, numero)
        ).fetchone()
        return result[0] if result else None

def get_bareme(question_id):
    """
        Renvoie le barème de la question.
        Arguments :
            - question_id : identifiant de la question.
    """
    with get_connection() as conn:
        result = conn.execute("SELECT bareme FROM question WHERE id = ?", (question_id,)).fetchone()
        return result[0]

def get_erreurs(question_id):
    """
        Renvoie la liste des erreurs de la question.
        Arguments :
            - question_id : identifiant de la question.
    """
    with get_connection() as conn:
        result = conn.execute("SELECT erreur FROM erreur WHERE question_id = ?", (question_id,)).fetchall()
        return [erreur[0] for erreur in result]