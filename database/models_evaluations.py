from .connection import get_connection

def get_par_titre(classe_id, titre):
    """
        Renvoie l'évaluation.
        Arguments :
            - classe_id : identifiant de la classe ;
            - titre : titre de l'évaluation.
    """
    with get_connection() as conn:
        result = conn.execute("SELECT * FROM evaluation WHERE classe_id = ? AND titre = ?", (classe_id, titre)).fetchone()
        return result if result else None

def creer(classe_id, titre):
    """
        Crée une nouvelle évaluation.
        Arguments :
            - classe_id : identifiant de la classe ;
            - titre : titre de l'évaluation.
    """
    with get_connection() as conn:
        conn.execute("INSERT INTO evaluation (titre, classe_id) VALUES (?, ?)", (titre, classe_id))
        conn.commit()

def supprimer(evaluation_id):
    """
        Supprime une évaluation.
        Argument :
            - evaluation_id : identifiant de l'évaluation.
    """
    with get_connection() as conn:
        conn.execute("DELETE FROM evaluation WHERE id = ?", (evaluation_id,))
        conn.commit()

def ajouter_exercice(exercice_id, evaluation_id):
    """
        Ajouter un exercice à l'évaluation.
        Arguments :
            - exercice_id : identifiant de l'exercice ;
            - evaluation_id : identifiant de l'évaluation.
    """
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO exercice_evaluation (exercice_id, evaluation_id) VALUES (?, ?)",
            (exercice_id, evaluation_id)
        )

def get_exercices(evaluation_id):
    """
        Renvoie la liste des exercices de l'évaluation.
        Argument :
            - evaluation_id : identifiant de l'évaluation.
    """
    with get_connection() as conn:    
        return conn.execute(
            """
                SELECT *
                FROM exercice
                JOIN exercice_evaluation ON exercice.id = exercice_evaluation.exercice_id
                WHERE exercice_evaluation.evaluation_id = ?
            """,
            (evaluation_id,)
        ).fetchall()

def set_bareme_redaction(evaluation_id, valeur):
    """
        Fixe le barème pour la rédaction.
        Arguments :
            - evaluation_id : identifiant de l'évaluation ;
            - valeur : nombre de points pour la rédaction.
    """
    with get_connection() as conn:
        conn.execute(
            "UPDATE evaluation SET bareme_redaction = ? WHERE id = ?",
            (valeur, evaluation_id)
        )
        conn.commit()

def lister_competences_id(evaluation_id):
    """
        Renvoie la liste des identifiants des compétences de
        l'évaluation.
        Argument :
            - evaluation_id : identifiant de l'évaluation.
    """
    with get_connection() as conn:
        competences = conn.execute(
            "SELECT competence_id FROM competence_evaluation WHERE evaluation_id = ?",
            (evaluation_id,)
        ).fetchall()
        return [competence[0] for competence in competences]

def lier(evaluation_id, competence_id):
    """
        Associe une compétence à l'évaluation.
        Arguments :
            - evaluation_id : identifiant de l'évaluation ;
            - competence_id : identifiant de la compétence.
    """
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO competence_evaluation (evaluation_id, competence_id) VALUES (?, ?)",
            (evaluation_id, competence_id)
        )
        conn.commit()

def delier(evaluation_id, competence_id):
    """
        Supprime une compétence de l'évaluation.
        Arguments :
            - evaluation_id : identifiant de l'évaluation ;
            - competence_id : identifiant de la compétence.
    """
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM competence_evaluation WHERE evaluation_id = ? AND competence_id = ?",
            (evaluation_id, competence_id)
        )
        conn.commit()