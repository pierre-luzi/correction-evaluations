from .connection import get_connection

def get(eleve_id, evaluation_id, question_id):
    """
        Renvoie la correction d'une question d'une évaluation
        pour un élève donné.
        Arguments :
            - eleve_id : identifiant de l'élève ;
            - evaluation_id : identifiant de l'évaluation ;
            - question_id : identifiant de la question.
    """
    with get_connection() as conn:
        return conn.execute(
            "SELECT commentaire, note FROM correction WHERE eleve_id = ? AND evaluation_id = ? AND question_id = ?",
            (eleve_id, evaluation_id, question_id)
        ).fetchone()      

def enregistrer(eleve_id, evaluation_id, question_id, commentaire, note):
    """
        Enregistre la correction.
        Arguments :
            - eleve_id : identifiant de l'élève ;
            - evaluation_id : identifiant de l'évaluation ;
            - question_id : identifiant de la question ;
            - commentaire : commentaire sur la réponse de l'élève ;
            - note : pourcentage des points attribués à l'élève.
    """
    with get_connection() as conn:
        if get(eleve_id, evaluation_id, question_id) == None:
            conn.execute(
                """
                INSERT INTO correction (eleve_id, evaluation_id, question_id, commentaire, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                (eleve_id, evaluation_id, question_id, commentaire, note)
            )
        else:
            conn.execute(
                "UPDATE correction SET commentaire = ?, note = ? WHERE eleve_id = ? AND evaluation_id = ? AND question_id = ?",
                (commentaire, note, eleve_id, evaluation_id, question_id)
            )
        conn.commit()

def lier_erreur(eleve_id, evaluation_id, question_id, erreur_id):
    """
        Associe une erreur à la correction.
        Arguments :
            - eleve_id : identifiant de l'élève ;
            - evaluation_id : identifiant de l'évaluation ;
            - question_id : identifiant de la question ;
            - erreur_id : identifiant de l'erreur.
    """
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO correction_erreur (eleve_id, evaluation_id, question_id, erreur_id) VALUES (?, ?, ?, ?)",
            (eleve_id, evaluation_id, question_id, erreur_id)
        )
        conn.commit()

def delier_erreur(eleve_id, evaluation_id, question_id, erreur_id):
    """
        Enlève l'erreur pour l'élève.
        Arguments :
            - eleve_id : identifiant de l'élève ;
            - evaluation_id : identifiant de l'évaluation ;
            - question_id : identifiant de la question ;
            - erreur_id : identifiant de l'erreur.
    """
    with get_connection() as conn:
        conn.execute("""
            DELETE FROM correction_erreur
            WHERE eleve_id = ?
            AND evaluation_id = ?
            AND question_id = ?
            AND erreur_id = ?
            """,
            (eleve_id, evaluation_id, question_id, erreur_id)
        )
        conn.commit()

def lister_erreurs_id(eleve_id, evaluation_id, question_id):
    """
        Renvoie la liste des identifiants des erreurs faites par
        un élève pour une question donnée d'une évaluation.
        Arguments :
            - eleve_id : identifiant de l'élève ;
            - evaluation_id : identifiant de l'évaluation ;
            - question_id : identifiant de la question.
    """
    with get_connection() as conn:
        result = conn.execute("""
            SELECT erreur.id
            FROM erreur
            JOIN correction_erreur
            ON erreur.id = correction_erreur.erreur_id
            WHERE correction_erreur.eleve_id = ?
            AND correction_erreur.evaluation_id = ?
            AND correction_erreur.question_id = ?
            """,
            (eleve_id, evaluation_id, question_id)
        ).fetchall()
        return [erreur[0] for erreur in result]

def lister_erreurs(eleve_id, evaluation_id, question_id):
    """
        Renvoie la liste des erreurs faites par un élève pour
        une question donnée d'une évaluation.
        Arguments :
            - eleve_id : identifiant de l'élève ;
            - evaluation_id : identifiant de l'évaluation ;
            - question_id : identifiant de la question.
    """
    with get_connection() as conn:
        result = conn.execute("""
            SELECT erreur.erreur
            FROM erreur
            JOIN correction_erreur
            ON erreur.id = correction_erreur.erreur_id
            WHERE correction_erreur.eleve_id = ?
            AND correction_erreur.evaluation_id = ?
            AND correction_erreur.question_id = ?
            """,
            (eleve_id, evaluation_id, question_id)
        ).fetchall()
        return [erreur[0] for erreur in result]