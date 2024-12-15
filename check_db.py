import sqlite3

def afficher_questions():
    # Connexion à la base de données SQLite
    conn = sqlite3.connect("quiz_game.db")
    cursor = conn.cursor()

    # Vérifie si la table Questions existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Questions';")
    table = cursor.fetchone()
    
    if not table:
        print("La table 'Questions' n'existe pas dans la base de données.")
    else:
        # Affiche tout le contenu de la table Questions
        cursor.execute("SELECT * FROM Questions;")
        questions = cursor.fetchall()

        if not questions:
            print("La table 'Questions' est vide.")
        else:
            print("Contenu de la table 'Questions' :")
            for question in questions:
                print(question)
    
    # Ferme la connexion
    conn.close()

# Appelle la fonction pour vérifier
afficher_questions()
