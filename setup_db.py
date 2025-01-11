import sqlite3

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect("quiz_game.db")
cursor = conn.cursor()

# Création de la table Users
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
""")

# Création de la table Questions
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        theme TEXT NOT NULL,
        type TEXT NOT NULL,
        question TEXT NOT NULL,
        reponse_correcte TEXT NOT NULL,
        proposition1 TEXT,
        proposition2 TEXT,
        proposition3 TEXT,
        proposition4 TEXT,
        points INTEGER NOT NULL
    )
""")

# Création de la table Scores
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        theme TEXT NOT NULL,
        score INTEGER NOT NULL,
        temps_total REAL NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users (id)
    )
""")

# Fermeture de la connexion
conn.commit()
conn.close()
print("Base de données mise à jour avec succès.")
