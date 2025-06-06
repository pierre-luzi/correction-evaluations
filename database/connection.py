import sqlite3
import json
from config import DB_PATH, COMPETENCES_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Création de la table de classes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS classe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE NOT NULL
        )
        """)
        
        # Création de la table d'élèves
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS eleve (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            classe_id INTEGER,
            FOREIGN KEY (classe_id) REFERENCES classe(id) ON DELETE CASCADE
        )
        """)

        # Création de la table d'évaluations
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS evaluation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            bareme_redaction FLOAT DEFAULT '1.00',
            classe_id INTEGER,
            FOREIGN KEY (classe_id) REFERENCES classe(id) ON DELETE CASCADE
        )
        """)

        # Création de la table d'exercices
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT UNIQUE NOT NULL,
            niveau TEXT NOT NULL
        )
        """)
        
        # Création de la table de liaison exercices/évaluation
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercice_evaluation (
            exercice_id INTEGER NOT NULL,
            evaluation_id INTEGER NOT NULL,
            FOREIGN KEY (exercice_id) REFERENCES exercice(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (evaluation_id) REFERENCES evaluation(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            PRIMARY KEY (exercice_id, evaluation_id)
        )
        """)

        # Création de la table de questions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TINYINT UNSIGNED NOT NULL,
            reponseA TEXT NOT NULL,
            reponseB TEXT NOT NULL,
            bareme FLOAT NOT NULL,
            exercice_id INTEGER,
            FOREIGN KEY (exercice_id) REFERENCES exercice(id) ON DELETE CASCADE
        )
        """)
        
        # Création de la table de correction
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS correction (
            eleve_id INTEGER NOT NULL,
            evaluation_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            commentaire TEXT,
            note FLOAT NOT NULL,
            PRIMARY KEY (eleve_id, evaluation_id, question_id)
        )
        """)
        
        # Création de la table des erreurs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS erreur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            erreur TEXT NOT NULL,
            question_id INTEGER NOT NULL,
            FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE
        )
        """    
        )
        
        # Création de la table de liaison correction/erreur
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS correction_erreur (
            eleve_id INTEGER,
            evaluation_id INTEGER,
            question_id INTEGER,
            erreur_id INTEGER,
            PRIMARY KEY (eleve_id, evaluation_id, question_id, erreur_id),
            FOREIGN KEY (eleve_id, evaluation_id, question_id) REFERENCES correction(eleve_id, evaluation_id, question_id),
            FOREIGN KEY (erreur_id) REFERENCES erreur(id)  
        )      
        """)
        
        # Gestion de la table des compétences
        synchroniser_competences()
        
        # Création de la table de liaison compétences/évaluation
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS competence_evaluation (
            evaluation_id INTEGER NOT NULL,
            competence_id INTEGER NOT NULL,
            FOREIGN KEY (evaluation_id) REFERENCES evaluation(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (competence_id) REFERENCES competence(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            PRIMARY KEY (evaluation_id, competence_id)
        )
        """)
        
        # Création de la table de liaison compétences/évaluation/élève
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS competence_eleve_evaluation (
            competence_id INTEGER NOT NULL,
            eleve_id INTEGER NOT NULL,
            evaluation_id INTEGER NOT NULL,
            valeur INTEGER NOT NULL,
            FOREIGN KEY (competence_id) REFERENCES competence(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (eleve_id) REFERENCES eleve(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            FOREIGN KEY (evaluation_id) REFERENCES evaluation(id) ON DELETE RESTRICT ON UPDATE CASCADE,
            PRIMARY KEY (competence_id, eleve_id, evaluation_id)
        )
        """)
        
        conn.commit()

def charger_donnees_json(chemin_fichier):
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur : le fichier JSON '{chemin_fichier}' est introuvable.")
        return None
    except json.JSONDecodeError as e:
        print(f"Erreur de format dans le fichier JSON : {e}")
        return None
    except Exception as e:
        print(f"Erreur inattendue lors de la lecture du fichier : {e}")
        return None

def synchroniser_competences():
    """
        Synchronise la table des compétences avec la liste
        contenue dans le fichier JSON.
    """
    donnees_json = charger_donnees_json(COMPETENCES_PATH)
    if donnees_json is None:
        print("Aucune donnée JSON chargée. Synchronisation annulée.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categorie TEXT NOT NULL,
            titre TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("SELECT titre FROM competence")
    titres_existants = {titre for (titre,) in cursor.fetchall()}

    for categorie, titres in donnees_json.items():
        for titre in titres:
            if not titre in titres_existants:
                cursor.execute("INSERT INTO competence (categorie, titre) VALUES (?, ?)", (categorie, titre))

    conn.commit()
    conn.close()